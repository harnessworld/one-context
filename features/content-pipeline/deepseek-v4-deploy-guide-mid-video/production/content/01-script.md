# 口播讲稿

<!-- format: script-v1 -->

---

## 00 开场（~45s）

上周我一个做运维的朋友跟我吐槽：他们团队为了跑 V4，上了八卡 A100 的 tensor 并行，结果 latency 比四卡还高。排查了一整天，发现是通信开销吃掉了所有收益。

这不是个例。V4 部署的资料太多了，但没有人告诉你：**哪些配置是锦上添花，哪些是火上浇油**。

今天我把从 API 到生产引擎的渐进路径、四个必改参数、三个调用陷阱，全部串成一张决策图。无论你是运维还是开发，听完都能少走一圈我那个朋友踩过的坑。

---

## 01 认识 V4（~2min）

在聊怎么部署之前，先回答一个问题：为什么偏偏是 V4？

跟 Kimi K2.6 和 GLM-5.1 比，三个模型在能力层面各有千秋。我们今天不评测谁更聪明，只聊一件事——从部署和调用的角度看，V4 有什么不一样。

**第一，MoE 架构的工程设计意图。**

V4 用的是混合专家架构。老观众应该听过这个词，但 V4 改了游戏规则：**它决定激活哪些专家的方式变了**。对运维来说最直观的感受是：同样参数规模下，V4 的激活参数量更小，这意味着推理时的显存峰值可以更低。但这个"可以"是有条件的，取决于你的 batch size 和并发策略。这一点我们后面在调优的部分会展开。

**第二，上下文长度。**

V4 支持的上下文窗口更长。对运维来说这决定了你的 max_model_len 能设多大；对开发来说，这决定了你一次能塞多少 token 进去。但这里有个坑：很多人觉得 128K 上下文就是 64K 的两倍显存，并不是。真实情况是，它确实会涨，但涨得比你想的更多一点——有个固定开销躲不掉。PagedAttention 能帮你缓解，但缓解不等于消除。

**第三，量化友好度。**

V4 在 FP8 精度下的表现比 V3 更稳定。这是一个很重要的工程事实，因为它直接决定了你手里如果是 H100、H20 这种支持 FP8 的显卡，是不是可以用更激进的量化策略去换取更高的吞吐。后面我会给你一个立刻就能用的选择逻辑。

对开发来说，这三件事对应三个你要调的参数：max_model_len、context window 的使用策略、以及量化方案的传参差异。后面调用篇都会覆盖到。

---

## 02 部署篇 — 运维视角（~5min）

### 02.1 渐进式部署路径

我不把量化单拎出来作为第四条路，因为在实际生产中，量化是一个**叠加在其他路径上的优化开关**。V4 的正确部署路径应该是三层递进，按需升级：

**L0：不部署——直接调官方 API。**

最简单，适合验证业务逻辑、快速原型，或者调用量还没大到需要自建集群。退出信号有三个：月费用逼近一张目标显卡的租赁成本、对延迟有确定性要求、需要锁定模型版本。当你的月 API 费用大约等于一张 A100 80G 的月度租赁费时，自建通常是一个经济拐点——当然还要加上你的人工运维成本，但这个数字足以让你启动评估了。

**L1：Docker 容器化自托管。**

这是一条性价比很高的快速验证路线。核心动作就是一条定性结构：`docker run -v /path/to/v4-weights:/models -p 8000:8000`，挂载权重目录、暴露端口。几小时就能从 0 到能响应请求。

但它的边界很清楚：容器内直接跑的是一个相对原始的推理进程，没有批处理优化、没有请求合并。单卡 A100 80G 裸跑 Docker，大概能撑 10 到 20 个并发——取决于你的平均序列长度。几百个并发？不可能。

正确用法是：内部工具、小团队共享、或者作为你验证"卡能不能跑"的第一步。

**L2：Docker + 推理引擎（vLLM）。**

注意，vLLM 不是取代 Docker，而是**在容器里跑 vLLM**。99% 的生产环境都是这个组合。vLLM 是目前社区最友好的选择，核心优势是 continuous batching 和 PagedAttention。TensorRT-LLM 吞吐更高，但构建复杂、生态绑死 NVIDIA。建议先用 vLLM 跑通，真的到瓶颈了再考虑换。

**叠加开关：量化优化。**

当你的显存装不下 FP16 的 V4，或者你想用更少的卡服务更多并发时，在 L1 或 L2 上叠加量化。V4 量化权重的 FP8 和 AWQ 版本在 HuggingFace 和 ModelScope 上都有现成 tag，不需要自己做转换，部署时 `--model` 指向下载好的目录即可。

选择逻辑：先确认你的卡支不支持 FP8——H100、H20 原生支持，精度损失最小，首选。不支持 FP8？再评估业务能不能接受 4-bit 的精度损失。摘要、分类这类低精度敏感任务可以上 AWQ；数学推理或代码生成不能碰 4-bit，老老实实加卡或换更大的显存。

PPT 里我放了这张递进图，你可以截图保存。

### 02.2 核心概念解释

接下来讲四个你在配置推理引擎时一定会碰到的参数。我不讲命令，只讲逻辑——你理解了逻辑，参数怎么设你自己就能判断。

**第一个是 tensor_parallel_size。**

把模型每一层的权重矩阵按列切开，分到多张卡上。推理的时候每张卡算一部分，最后把结果拼起来。V4 FP16 权重大概率装不进一张 80G 的卡——社区实测 V4 的 FP16 权重加载显存需求约为 4 到 8 张 80G 卡的水平，所以必须切开。

但注意：tensor 并行的卡数不是越多越好。2 张或 4 张是甜点区；切到 8 张，通信开销可能吃掉你一半的收益。只在极端显存不足时考虑 8 张。另外，tensor 并行只在单节点内部有效，跨节点不能用这个参数，要用 pipeline 并行。

**第二个是 pipeline_parallel_size。**

如果说 tensor 并行是"横着切"，pipeline 并行就是"竖着切"。它把模型的不同层分到不同节点上，数据流水一样地从第一层流到最后层。V4 的层数很多，流水线并行的效果比小模型更显著。

但 pipeline 有个天生缺陷叫 bubble——当前面层在算、后面层空等。缓解方法是增加 micro-batch 数量，但这又会吃显存。所以这是个权衡，不是无脑开。

生产环境最常见的组合拳是：**单节点内横着切，跨节点竖着切**。为什么不用同一种？因为跨节点带宽太宝贵了，tensor 并行在那会哭。

**第三个是 KV Cache 管理，也就是 PagedAttention。**

这个点非常关键，因为 KV Cache 有时候比你加载模型权重本身还大。PagedAttention 做的就是把 KV Cache 从连续显存改成离散块管理，类似操作系统虚拟内存分页。一个请求结束了，它的块可以立刻回收给新请求用。

V4 的长上下文窗口放大了这个优化的价值——上下文越长，KV Cache 越大，没有 PagedAttention 的话你会浪费大量显存在已经提前结束的请求上。

你在 vLLM 里看到 max_num_seqs 这个参数，控制同时能有多少个序列在跑。设太小，GPU 算力没吃满；设太大，KV Cache 把显存撑爆。怎么定？两步走：

如果你有模型参数，可以按这个粗糙公式估算单条请求的 KV Cache 大小：`2 × 层数 × 隐藏维度 × 序列长度 × 精度字节 / 1024³`，单位 GB。

如果你懒得算，更实用的方法是压测：先设 `max_num_seqs=10`，观察 `nvidia-smi` 里的显存占用，再线性外推到 80% 显存的位置。最后乘个 0.8 的安全系数——给突发流量留口气。

**第四个是 max_model_len。**

这个参数决定了一个请求最多能处理多长的上下文。在 V4 上，这个值不是直接往大了写就好。设太大，vLLM 在 block table 调度和显存预算中会过度乐观地预留空间，相当于给每个请求都按 128K 排队占地，实际只用 4K，挤占了真实并发空间。

正确的做法是先统计业务 95 分位的输入长度，再预留一点余量。比如你的输入通常 4K，偶尔到 8K，那设 12K 就够了。不要直接设 128K。

### 02.3 调优思路 + 运维检查清单

部署完之后必然要调优。但调优之前请你记住一个三角形：**延迟、吞吐、显存，这三者你只能优化其中两个，第三个一定会牺牲。**

实时对话保延迟和显存，吞吐可以低一点；批量处理保吞吐和显存，延迟无所谓。拿这个框架去跟业务方对齐需求。

**场景一：高并发低延迟。**

最难的。策略是启用 continuous batching，把 max_num_seqs 压到刚刚不爆显存的值，吃满 GPU。怎么知道 GPU 吃满了？看 `nvidia-smi` 的 GPU 利用率，而不是显存占用。显存满了、利用率只有 60%，说明 batch size 不够大。

**场景二：长上下文。**

长上下文的敌人是 KV Cache 显存。除了 PagedAttention，V4 上还可以开 prefix caching——如果多个请求的前缀一样，前面的 KV Cache 不需要重复算。开启方式是在 vLLM 启动参数里加 `--enable-prefix-caching`。有固定 system prompt 或多轮问答模板的业务收益最大。

**场景三：资源受限，单卡或者低端 GPU。**

就一条：量化。先用 FP8，不行再 AWQ。同时把 max_model_len 压到最低可接受值，max_num_seqs 打满。再不行，就只能降并发上限了。

**一个常见误区：**

很多人觉得 "batch size 越大吞吐越高"，然后无脑把 max_num_seqs 调很高。这是错的。vLLM 里有一个 preemption 机制——当显存不够的时候，它会把正在跑的请求 swap 出去，等有空位了再换回来。这个动作极其昂贵。吞吐反而会断崖式下跌。

**怎么识别 preemption 已经发生了？** 看三个信号：

1. vLLM 日志里频繁出现 `preemption`、`swap blocks` 或 `recompute` 字样；
2. `nvidia-smi` 里 GPU 利用率开始下降，但平均延迟猛涨；
3. 请求的成功率没变，但 P99 响应时间飙升。

出现以上任何一个信号，就立刻降低 max_num_seqs，而不是继续扩容。

**部署后第一小时检查清单**（截图这段）：

- GPU 利用率是否稳定在 80% 以上（`nvidia-smi`）
- 显存 allocated vs reserved 是否差距过大（差距大说明 PagedAttention 没生效或 block size 设错）
- P99 延迟是否在业务方可接受的 SLA 范围内

---

## 03 调用篇 — 开发视角（~3min）

不管你现在手里拿的是运维键盘还是代码编辑器，这部分都建议听完——因为**调接口时传错一个参数，前面的部署全白费**。

### 03.1 API 调用方式

V4 的 API 基本兼容 OpenAI 格式，无论你调官方 API 还是自托管的 vLLM 服务，接口结构都差不多。这本身是好事，你可以复用现有的 SDK。

但注意两个地方。

**第一，model 名称。**

调官方 API 时 model 字段通常是 `deepseek-chat` 或 `deepseek-reasoner`。调自托管 vLLM 时，要填你在启动参数 `--served-model-name` 里指定的名字。很多人这里踩坑：SDK 里写的是 `deepseek-chat`，但自托管不认识，返回 model not found。

**第二，reasoning 模式开关。**

V4 存在推理模式的显式开关，默认关闭。需要推理过程时必须手动打开。目前这个参数叫 `enable_thinking`，但即便以后改名了，逻辑不会变——reasoning 不是白送的。你不开的话，调用的是 V4 的 non-reasoning 版本，速度快、价格低，但复杂任务的表现会差一些。

### 03.2 最小可运行示例

在讲传参细节之前，先给一个能直接跑的 Python 模板。这段代码覆盖了 model 字段、reasoning 开关、流式输出和 usage 解析：

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.deepseek.com/v1",  # 或自托管地址
    api_key="sk-xxx"
)

response = client.chat.completions.create(
    model="deepseek-chat",  # 自托管时改 --served-model-name
    messages=[{"role": "user", "content": "9.11 和 9.9 哪个更大"}],
    temperature=0.6,
    max_tokens=2048,
    stream=True,
    # enable_thinking=True,  # 需要推理时取消注释
)

for chunk in response:
    print(chunk.choices[0].delta.content, end="")

# 注意：如果开了 reasoning，usage 里有 completion_tokens_details.reasoning_tokens
print(response.usage)
```

核心记住三点：base_url 指向你实际的服务端、model 名称要对上、stream 模式下的 delta 解析跟 OpenAI 一样。

### 03.3 传参注意事项

**temperature**

V4 的采样策略优化过，temperature 敏感度比以前低——0.7 和 0.9 的差异可能比你预期的小。迁移时不要直接复用 GPT 上的经验值。

按场景来：
- 代码生成 / 数学推理：temperature 0.0–0.3
- 通用对话 / RAG：temperature 0.5–0.7
- 创意写作 / 头脑风暴：temperature 0.8–1.2

挑一个场景对号入座，不要两个参数一起开。

**max_tokens 与 context_window**

`max_tokens` 控制模型最多输出多少 token，不是输入上限。输入上限由服务端的 `max_model_len` 控制，你在客户端改不了。长上下文任务记得分段处理，不要把整本书直接丢进去——虽然 V4 支持 128K，但长上下文的使用技巧跟其它模型一样，核心信息放首尾。

**常见 HTTP 错误码**

429 Too Many Requests——官方 API 去平台后台查 rate limit；自托管说明并发或队列满了。

503 Service Unavailable——自托管先看 `docker logs` 或 vLLM 的日志输出，常见原因是模型权重路径错误或 GPU OOM。先看日志，不要直接重启。

Context length exceeded——你输入的 token 数超过了服务端 max_model_len。解法：缩短输入，或让运维同学评估后调大。

### 03.4 与 V3 调用的差异

如果你之前用过 V3，迁移到 V4 时主要检查两个地方。

**计费逻辑——reasoning tokens：**

V4 的 usage 字段会额外暴露 reasoning tokens。这个值会计入 `total_tokens`，但**不计入 `completion_tokens`**。如果你的计费逻辑写的是 `prompt_tokens + completion_tokens`，会漏掉 reasoning 这部分。正确做法：计费基数用 `total_tokens`，或者显式把 `completion_tokens_details.reasoning_tokens` 加进去。

代码层面可以这样兜底：

```python
# 兼容 V3 和 V4 的计费
billable = usage.total_tokens  # 包含 reasoning，不会漏
# 或者如果你需要拆分展示：
# billable = usage.prompt_tokens + usage.completion_tokens + getattr(
#     usage.completion_tokens_details, "reasoning_tokens", 0
# )
```

**stop_reason：**

V3 的 stop_reason 通常是 `stop` 或 `length`。V4 在 reasoning 模式下可能会返回 `stop`（生成结束）、`eos`（遇到结束符）或 `completed`（思考链路完成）。不要写死 `== "stop"`，建议用 `in ["stop", "eos", "completed"]` 做兜底。

---

## 04 总结与行动建议（~1min）

好，快速总结。

**如果你是运维工程师：** 先拿 Docker 跑通确认卡能加载 V4，再上 vLLM 引擎。上线第一周做三件事：按 95 分位设 max_model_len、压测找 max_num_seqs 的上限、看日志有没有 preemption。如果显存不够，确认卡支持 FP8 就上 FP8，不支持则评估 AWQ。

**如果你是开发者：** 先跑通上面的 Python 示例，重点核对 model 字段、reasoning 开关和 temperature 场景值。计费时记得用 total_tokens，不要漏 reasoning。

这期视频里的决策图、参数对照表和代码示例，我都整理在置顶评论的链接里了。**截图容易糊，直接去拿高清版**。

但如果你正在部署 V4，现在就可以做一件事：打开你的 vLLM 配置，对照我今天的三条检查清单——max_model_len 是否按实际业务长度设了、max_num_seqs 有没有无脑开太大、GPU 利用率是不是被打满了却延迟飙升。如果中了任何一条，你今晚就能少改一轮配置。

下期我们讲量化部署里的一个隐形陷阱——为什么 INT8 有时候比 FP8 还慢。到时候见。

---

## 拍摄 / 制作备注

- 提到"PPT 里的决策图"时，需配合 `production/slides/presentation.html` 翻页。
- 02.1 递进图需展示为三层阶梯（L0→L1→L2）+ 量化叠加开关
- 口播中涉及的量化路径对比、HTTP 错误码速查、运维检查清单，建议 slides 中以表格形式呈现
- Python 代码示例建议 slides 中以高亮代码块呈现，配合关键行（如 `enable_thinking`、usage 解析）做标注
- 语气节奏：开场故事偏轻快；运维篇偏沉稳、信息密集；调用篇偏轻快、点到为止；结尾 CTA 要有紧迫感

## 事实核查清单

| # | 事实点 | 来源 | 状态 |
|---|-------|------|------|
| 1 | V4 采用 MoE 架构，激活参数量更小 | DeepSeek 官方技术报告 | ⚠️ 待验证 |
| 2 | V4 FP16 权重加载显存需求约为 4~8×80GB | 社区实测数据 | ⚠️ 待验证 |
| 3 | FP8 在 H100/H20 上为硬件原生支持 | NVIDIA HOPPER 架构白皮书 | ⚠️ 待验证 |
| 4 | vLLM 支持 prefix caching（`--enable-prefix-caching`） | vLLM 官方文档 | ⚠️ 待验证 |
| 5 | V4 API 存在 reasoning 显式开关 | DeepSeek API 文档 | ⚠️ 待验证 |
| 6 | V4 usage 字段中 reasoning tokens 不计入 completion_tokens | DeepSeek API 文档 | ⚠️ 待验证 |
| 7 | Tensor 并行通信开销在 8 卡时显著增大 | NVIDIA / vLLM 社区实测数据 | ⚠️ 待验证 |
| 8 | Docker 单卡 A100 80G 裸跑约 10~20 并发 | 社区实测数据 | ⚠️ 待验证 |
| 9 | 月 API 费用 ≈ A100 月租时为自建经济拐点 | 经验公式，需验证 | ⚠️ 待验证 |
