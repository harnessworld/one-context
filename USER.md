# USER.md - About Your Human

_Learn about the person you're helping. Update this as you go._

- **Name / 品牌:** 大厂吾师兄
- **What to call them:** 吾师兄 / 师兄
- **Timezone:** Asia/Shanghai (GMT+8)
- **Notes:** 技术视频创作者，专注 AI 工具、Claude Code、Cursor、生产力方向

## Context

### 创作偏好
- **视频风格**：古风/文言文/山顶洞人视觉元素（案例：穴居人模式主题）
- **字体要求**：手机横屏观看，字号尽量大，留白少
- **字幕**：黄色，烧录到视频里
- **品牌**：封面和视频 PPT 均不加额外品牌元素（与其他已有 presentation 保持一致）
- **发布平台**：抖音/B站竖屏+横屏封面

### 技术栈
- one-context 项目管理（features/ 开发目录）
- Cursor / Claude Code
- Whisper (small 模型，CPU + int8，hf-mirror 加速）
- ffmpeg 字幕烧录
- VideoFactory 封面生成模板
- Git（分支：superno，不要随便提交到 main）

### 工作流
1. 下载音频 → Whisper 转写生成 SRT
2. **必须先 review 校对 SRT** → 确认后才烧录（不能先烧后改）
3. 创建/更新 presentation.html（古风视觉）
4. wav-auto 出片（幻灯片截图 + 音频切片 + 合并 + 烧字幕）

### 忌讳
- 不喜欢 AI 敷衍的封面（要有设计感）
- 不随意加品牌元素，必须参考已有 presentation 的做法
- 分支管理严格：skill 改动应在 superno，不应动 main
