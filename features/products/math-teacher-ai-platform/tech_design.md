# 技术方案 — 数学教师 AI 工作台（Phase 1）

关联：`spec.md`

## 上下文与约束

### 当前现状

- 现有主仓库为 `repos/develop/FunctionCanvas`
- 已具备较完整的数学可视化前端能力（函数图、曲面、矢量场）
- 当前是单应用结构，无路由、无资产管理、无出题能力

### Phase 1 约束

- 优先利用现有 `React + Vite + Ant Design + TypeScript` 技术栈
- 单仓演进，不引入微前端
- 纯前端 + 本地/mock 数据，不要求后端服务
- AI 出题先通过统一服务层调用 LLM，不绑定单一模型厂商
- 只交付三个模块：Math Canvas、AI 出题、资源中心

### 设计原则

- **聚焦出题场景**：所有技术决策围绕"教师用 AI 出一套带可视化的题"这个核心流程
- **资产可复用**：可视化和题目都是资产，可保存、可引用、可检索
- **教师可控**：AI 产出是草稿，教师始终保留编辑权与最终决定权
- **数学原生**：对象模型能表达知识点、题型、可视化配置、题目结构

## 方案概览

### 总体结构

Phase 1 采用 **最小 App Shell + 3 Modules** 架构：

- `App Shell`：路由、导航、全局状态
- `MathCanvasModule`：可视化引擎 + 资产管理
- `QuestionGenModule`：AI 出题工作台
- `ResourceCenterModule`：统一资产浏览与检索
- `Shared Domain Layer`：跨模块的对象模型与资产服务
- `AI Service Layer`：统一 LLM 调用入口

### 核心数据流

```
教师选知识点+题型+难度
        │
        ▼
   AI Service 生成题目草稿
        │
        ▼
   题目中含函数图 → 自动调用 Math Canvas 渲染可视化
        │
        ▼
   教师编辑题目 / 调整可视化参数
        │
        ▼
   保存为"题目集"资产 → 资源中心
        │
        ▼
   可导出 PDF / 后续复用
```

## 信息架构

### 路由

| 路径 | 模块 | 说明 |
|---|---|---|
| `/` | 首页 | 简单入口，快捷跳转到三个模块 |
| `/canvas` | Math Canvas | 可视化工作台（现有能力 + 资产管理） |
| `/canvas/:id` | Math Canvas | 编辑已有可视化资产 |
| `/questions` | AI 出题 | 出题工作台 |
| `/questions/:id` | AI 出题 | 编辑已有题目集 |
| `/resources` | 资源中心 | 资产浏览、筛选、复用 |

### 导航

侧边栏三个一级入口 + 首页 logo 跳转，不设置其他占位入口。

## 核心领域对象

### 1. 可视化资产

```ts
/** 绘图类型，与现有 FunctionCanvas 的 PlotType 对齐 */
type CanvasPlotType = 'explicit' | 'polar' | 'surface' | 'vector' | 'volume' | 'implicit';

/** Canvas 配置——对应 FunctionCanvas 绘图器的核心参数 */
interface CanvasConfig {
  plotType: CanvasPlotType;
  /** 主表达式（mathjs 格式） */
  expression: string;
  /** 多函数叠加 */
  overlayExpressions?: Array<{ expr: string; color: string }>;
  /** 参数值映射 */
  scope?: Record<string, number>;
  /** 2D 坐标范围 */
  xRange?: [number, number];
  yRange?: [number, number];
  /** 极坐标 θ 范围 */
  thetaRange?: [number, number];
  /** 3D 空间范围 */
  spaceLimit?: number;
  /** 矢量场分量（仅 vector 类型） */
  vectorComponents?: { u: string; v: string; w: string };
  /** 矢量场网格密度与箭头长度 */
  vectorGridDensity?: number;
  vectorArrowLength?: number;
  /** 曲线颜色 */
  colors?: string[];
  /** 特殊点标注（极值、交点等） */
  specialPoints?: Array<{ x: number; y: number; type: string; label: string }>;
}

interface VisualizationAsset {
  id: string;
  /** 数据格式版本，用于后续迁移 */
  version: 1;
  title: string;
  canvasConfig: CanvasConfig;
  /** 预览图 base64 或 URL */
  preview?: string;
  knowledgePoints: string[];
  gradeBand?: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}
```

### 2. 题目

```ts
type QuestionType = 'choice' | 'fill-blank' | 'short-answer' | 'graph';

/**
 * answer 格式约定：
 * - choice：选项索引字母，如 "A"、"C"
 * - fill-blank：多空用 "|||" 分隔，如 "3|||x+1"
 * - short-answer / graph：自由文本（LaTeX 格式）
 */
type QuestionAnswer = string;

interface Question {
  id: string;
  type: QuestionType;
  /** 题干，支持 LaTeX（KaTeX 渲染） */
  stem: string;
  /** 选择题选项，支持 LaTeX */
  options?: string[];
  answer: QuestionAnswer;
  /** 解析，支持 LaTeX */
  explanation?: string;
  /** 引用的可视化资产 id 列表 */
  visualizationIds: string[];
  knowledgePoints: string[];
  difficulty: 1 | 2 | 3 | 4 | 5;
}
```

### 3. 题目集

```ts
interface QuestionSet {
  id: string;
  /** 数据格式版本 */
  version: 1;
  title: string;
  questions: Question[];
  /** 总分、题型分布等元数据 */
  meta: {
    totalScore?: number;
    gradeBand?: string;
    knowledgePoints: string[];
  };
  createdAt: string;
  updatedAt: string;
}
```

### 4. 知识点

```ts
interface KnowledgePoint {
  id: string;
  name: string;
  /** 所属章节路径，如 "初中 > 二次函数 > 图像与性质" */
  path: string[];
  gradeBand: string;
}
```

Phase 1 知识点列表手动维护为 JSON 文件，不做动态管理。

## 公式渲染

复用现有 KaTeX（`katex@^0.16.40`）渲染能力及 `latexMathJsBridge` 工具。

- 题干、选项、解析中的数学公式统一使用 LaTeX 格式，前端用 KaTeX 渲染
- mathjs 表达式与 LaTeX 之间通过 `latexToMathJs` / `mathJsToLatex` 互转
- AI 返回的题目内容要求使用 LaTeX 格式，前端直接渲染无需额外转换

## 状态管理与模块通信

### 状态管理方案

现有 FunctionCanvas 使用 React `useState` 组件级状态。升级为多模块架构后，引入 **Zustand** 管理跨模块共享状态：

| Store | 职责 | 消费者 |
|---|---|---|
| `assetStore` | 可视化资产 CRUD、列表缓存 | Math Canvas、资源中心、出题模块 |
| `questionStore` | 题目集 CRUD、当前编辑态 | 出题模块、资源中心 |
| `aiStore` | 出题请求状态（loading / streaming / error） | 出题模块 |

各模块内部的 UI 状态（面板展开、表单输入等）仍用组件级 `useState`，不放入全局 store。

### 模块间通信

| 场景 | 机制 |
|---|---|
| 出题模块选取可视化资产 | 弹出资产选择抽屉（Drawer），选中后写入 `questionStore` 当前题目的 `visualizationIds` |
| 出题模块编辑可视化 | 路由跳转 `/canvas/:id?from=questions/:qsId`，编辑完成后返回（`from` 参数控制返回路径） |
| 出题模块新建可视化 | 路由跳转 `/canvas?from=questions/:qsId`，保存后自动关联到当前题目 |
| 资源中心进入编辑 | 路由跳转到对应模块页面 |

不使用全局事件总线，所有通信通过 **store + 路由参数** 完成。

## 模块设计

### Math Canvas 模块

#### 现有能力保留

- 函数图绘制、曲面图、矢量场、参数动画
- 表达式输入、坐标系控制、样式调整

#### Phase 1 新增

- **资产保存**：当前画布状态可保存为 `VisualizationAsset`，含元数据编辑（标题、知识点、标签）
- **资产列表**：查看和管理已保存的可视化资产
- **资产引用接口**：供 AI 出题模块调用，在题目中嵌入可视化预览
- **导出**：单个可视化导出为 PNG/SVG

#### 关键接口

```ts
// 供出题模块调用
interface CanvasEmbedProps {
  assetId: string;
  /** 只读预览模式 */
  readonly?: boolean;
  width?: number;
  height?: number;
}
```

### AI 出题模块

#### 出题工作台页面结构

- **左侧面板**：知识点选择（树形）、题型勾选、难度滑块、题目数量
- **中间主区域**：AI 生成的题目列表，每道题可展开编辑
- **右侧面板**：可视化资产选择器（从资源中心选取或新建）

#### 出题流程

1. 教师填写出题参数（知识点、题型分布、难度、数量）
2. 调用 AI Service 生成题目草稿
3. 前端解析 AI 返回的结构化题目数据
4. 对含函数图描述的题目，自动生成 Math Canvas 配置并渲染预览
5. 教师逐题编辑：改题干、换数据、调整可视化、删题、手动加题
6. 保存为 `QuestionSet`

#### AI 出题 Prompt 结构

```ts
interface QuestionGenRequest {
  knowledgePoints: string[];
  questionTypes: QuestionType[];
  difficulty: { min: number; max: number };
  count: number;
  /** 额外要求，如"需要包含函数图像题" */
  instructions?: string;
}

interface QuestionGenResponse {
  questions: Array<{
    type: QuestionType;
    stem: string;
    options?: string[];
    answer: string;
    explanation?: string;
    /** AI 判断此题需要可视化时，给出表达式和坐标范围 */
    visualization?: {
      expressions: string[];
      xRange: [number, number];
      yRange: [number, number];
      annotations?: string[];
    };
    knowledgePoints: string[];
    difficulty: number;
  }>;
}
```

#### 可视化自动生成

当 AI 返回的题目包含 `visualization` 字段时：
1. 用 `visualization.expressions` 等参数生成 Math Canvas 配置
2. 自动渲染预览嵌入题目卡片
3. 教师可点击预览进入 Math Canvas 编辑模式调整

### 资源中心模块

#### 功能

- 统一展示所有已保存的资产：可视化资产、题目集
- 按类型、知识点、年级、标签筛选
- 资产卡片预览（可视化缩略图 / 题目集摘要）
- 点击进入对应模块编辑
- 复制、归档、删除

#### 数据源

Phase 1 使用 localStorage 或 IndexedDB 持久化，不依赖后端。

## AI Service 层

### 统一接口

```ts
interface AiService {
  generateQuestions(req: QuestionGenRequest): Promise<QuestionGenResponse>;
}
```

### Phase 1 实现

- 调用通用 LLM API（如 Claude / GPT），使用数学出题专用 prompt
- Prompt 模板独立存放于 `src/services/ai/prompts/` 目录，按题型/场景拆分文件，便于迭代
- 返回结构化 JSON，前端解析渲染

### 错误处理与 UX

- **Partial Parse**：LLM 返回的 JSON 可能局部损坏。前端按题目粒度逐条解析，成功的题目正常展示，解析失败的题目标记为"生成异常"并允许教师手动编辑原始文本
- **全量失败**：网络错误或 JSON 完全不可解析时，提示"生成失败，请重试或调整参数"
- **响应延迟 UX**：生成 10-15 道题预计耗时 10-30 秒。采用 **streaming 逐题渲染**——LLM 返回流式响应，前端逐条解析并渲染题目卡片，教师无需等待全部生成完毕即可开始浏览
- **重试策略**：保留上次的出题参数，教师可一键重试或微调参数后重新生成

### Prompt 设计要点

- 要求 AI 返回严格 JSON 格式，每道题为独立 JSON 对象（便于 streaming 逐条解析）
- 对每道题标注是否需要可视化，以及可视化的表达式和坐标范围
- 数学公式统一使用 LaTeX 格式（与 KaTeX 渲染对齐）
- 按中国教材的知识点体系组织题目
- Prompt 模板支持 few-shot 示例，逐步积累高质量样本

## 存储层设计

### 技术选型

Phase 1 使用 **IndexedDB**（通过 [idb](https://github.com/jakearchibald/idb) 封装）。localStorage 容量有限（5-10MB），不适合存储含预览图的资产。

### Schema

```ts
// DB: math-teacher-db, version: 1
// ObjectStore 定义：

// 可视化资产
store: 'visualizations'
  keyPath: 'id'
  indexes:
    - 'knowledgePoints'  (multiEntry: true)  // 按知识点查询
    - 'gradeBand'                             // 按年级段筛选
    - 'updatedAt'                             // 按时间排序

// 题目集
store: 'questionSets'
  keyPath: 'id'
  indexes:
    - 'meta.knowledgePoints'  (multiEntry: true)
    - 'meta.gradeBand'
    - 'updatedAt'
```

### 查询模式

- 资源中心列表：按 `updatedAt` 降序分页
- 按知识点筛选：使用 multiEntry index 查询
- 出题模块引用资产：按 id 直接获取
- 全文搜索（标题/标签）：Phase 1 前端内存过滤，资产量 < 500 条时性能可接受

### 多标签页安全

IndexedDB 事务天然支持多标签页并发读写。写入时使用 `readwrite` 事务保证原子性。Zustand store 监听 `storage` 事件或使用 `BroadcastChannel` 同步标签页间的状态变更。

## PDF 导出

Phase 1 将 PDF 导出作为**可选交付**，不阻塞核心流程。

### 技术方案

使用 **html2canvas + jsPDF** 纯前端方案：

1. 将题目集渲染为打印专用 HTML 布局（A4 尺寸、分页标记）
2. KaTeX 公式在 HTML 中已渲染为 DOM，无需额外处理
3. 可视化预览使用 Canvas 截图（`toDataURL`）嵌入
4. 通过 html2canvas 转为图片，jsPDF 生成 PDF

### 已知限制

- 纯前端方案在复杂排版下可能有精度损失
- Phase 2 可升级为后端 Puppeteer 方案以获得更好的排版质量

## 前端目录结构

```text
src/
  app/
    router.tsx          # 路由配置
    layout/             # App Shell（导航、布局）
    providers/          # 全局 Context
  modules/
    math-canvas/        # Math Canvas 模块
      pages/
      components/
      hooks/
      services/
    questions/          # AI 出题模块
      pages/
      components/
      hooks/
      services/
    resources/          # 资源中心模块
      pages/
      components/
  domain/
    assets/             # VisualizationAsset, QuestionSet 类型与存储
    math/               # KnowledgePoint, QuestionType 等
  services/
    ai/                 # AI Service 层
      prompts/          # Prompt 模板文件（按题型/场景拆分）
    storage/            # IndexedDB 封装（idb）
  stores/
    assetStore.ts       # Zustand — 可视化资产状态
    questionStore.ts    # Zustand — 题目集状态
    aiStore.ts          # Zustand — AI 请求状态
  shared/
    ui/                 # 通用 UI 组件
    hooks/
    utils/
```

### 当前仓库演进方式

1. 保留现有绘图组件与数学工具函数
2. 新增 `app/router.tsx` 与 `app/layout/`
3. 将当前 `App.tsx` 中的可视化主体迁移至 `modules/math-canvas/`
4. 新增 `modules/questions/` 和 `modules/resources/`
5. 将跨模块共享类型抽离到 `domain/`

## 迁移与回滚

### 迁移策略

渐进迁移，不破坏现有能力：

1. 新增路由框架，将原主页面挂载到 `/canvas`
2. 保留当前可视化能力不变
3. 新增出题模块和资源中心模块
4. 新增简单首页（快捷入口）
5. 最后调整默认路由指向首页

### 回滚策略

- 路由层回滚：将 `/` 直接指向 Math Canvas，等同回退到单应用模式
- 不直接修改现有数学可视化核心组件，保证可回滚

## Spec 开放问题回应

| # | 问题 | Phase 1 结论 |
|---|---|---|
| 1 | AI 出题的模型选择 | Phase 1 直接调用通用 LLM + 数学专用 prompt，不做微调。通过 few-shot 示例和结构化 prompt 保障质量。AI Service 层已做抽象，后续可替换为微调模型或 RAG |
| 2 | 知识点体系 | Phase 1 手动维护 JSON 文件，先覆盖初中函数 + 高中函数两个高频章节（约 80-120 个知识点）。Phase 2 可对接人教版教材目录 |
| 3 | 题目格式 | Phase 1 支持 4 种题型：选择题、填空题、解答题、作图题。作图题通过 Math Canvas 可视化承载 |
| 4 | PDF 导出 | Phase 1 可选交付（不阻塞 MVP）。技术方案为 html2canvas + jsPDF 纯前端方案，详见"PDF 导出"章节 |

## 依赖与风险

### 依赖

- 现有 FunctionCanvas 前端代码可支持模块迁移
- 现有 KaTeX + latexMathJsBridge 可直接复用
- AI 出题需要 LLM API 访问（Phase 1 可先用 mock 数据开发 UI）
- 知识点列表需手动整理（初中/高中数学函数章节，约 80-120 个知识点）

### 风险

| 风险 | 影响 | 规避 |
|---|---|---|
| AI 生成的题目质量不稳定 | 教师体验差 | AI 产出定位为草稿；提供便捷编辑能力；积累 few-shot 示例 |
| AI 返回的可视化参数不准确 | 图形与题目不匹配 | 教师可在 Math Canvas 中手动调整；前端做基础校验（表达式合法性、坐标范围合理性） |
| AI 响应延迟（10-30s） | 教师等待体验差 | 采用 streaming 逐题渲染，教师可在生成过程中浏览已完成题目 |
| 知识点体系维护成本 | 初始内容不全 | Phase 1 先覆盖初中函数 + 高中函数两个高频章节 |
| IndexedDB 兼容性 | 极少数旧浏览器不支持 | 目标用户为教师（桌面 Chrome/Edge 为主），兼容性风险极低 |
