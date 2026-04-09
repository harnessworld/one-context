# 技术方案 — 数学教师 AI 平台（Phase 1）

关联：`spec.md`

## 上下文与约束

### 当前现状

- 现有主仓库为 `repos/develop/FunctionCanvas`
- 现有产品已经具备较完整的数学可视化前端能力
- 当前入口仍接近“单应用”，尚未形成平台化导航、模块边界和统一资产中心

### Phase 1 约束

- 优先利用现有 `React + Vite + Ant Design + TypeScript` 技术栈
- 优先单仓演进，避免一开始引入高复杂度微前端
- 先完成平台壳与模块边界，不追求一次性补完所有业务能力
- 所有 AI 能力先抽象为统一服务层，不在 Phase 1 绑定单一模型厂商

### 设计原则

- **平台优先**：先统一入口、导航、对象模型，再做垂直功能
- **教师工作流优先**：按备课、授课、班级、作业、讲评分工，而不是按技术组件分散
- **数学原生**：对象模型要能表达知识点、题型、可视化、解题过程、错因
- **资产可复用**：一次生成的可视化、教案、题目集都应可以被其他模块引用
- **教师可控**：AI 产出默认是草稿，教师始终保留编辑权与最终决定权

## 方案概览

### 总体结构

Phase 1 采用 **App Shell + Workbench Modules** 架构。

- `App Shell`：平台壳，负责导航、路由、权限上下文、全局搜索、资源入口
- `Workbench Modules`：各一级工作台
- `Shared Domain Layer`：统一对象模型、资源模型、状态模型
- `AI Service Layer`：统一的 AI 调用入口、提示模板、结果结构化协议
- `Data Adapters`：本地 mock / 后端 API / 第三方服务接入层

### 一级工作台

- `DashboardWorkbench`：首页、今日任务、最近资源、待处理事项
- `LessonPrepWorkbench`：AI 备课
- `MathCanvasWorkbench`：由 `FunctionCanvas` 演进而来
- `ClassroomWorkbench`：AI 班级与学情
- `AssessmentWorkbench`：出题、作业、组卷
- `GradingWorkbench`：阅卷、评分、讲评
- `ResearchWorkbench`：教研与教师成长
- `ResourceCenterWorkbench`：统一资源中心

### Phase 1 真实交付模块

- `DashboardWorkbench`
- `LessonPrepWorkbench`（骨架）
- `MathCanvasWorkbench`（实装）
- `ResourceCenterWorkbench`（骨架）
- 其余模块先保留导航入口和空状态页

## 信息架构

### 一级导航建议

1. `工作台`
2. `AI备课`
3. `Math Canvas`
4. `班级`
5. `出题与作业`
6. `阅卷与讲评`
7. `资源中心`
8. `教研`

### 核心页面建议

- `/`：平台首页
- `/prep`：AI 备课工作台
- `/apps/math-canvas`：数学可视化工作台
- `/classes`：班级列表
- `/assessments`：出题与作业
- `/grading`：阅卷与讲评
- `/resources`：资源中心
- `/research`：教研成长

### `Math Canvas` 在平台中的位置

`Math Canvas` 不是“工具菜单里的一个功能点”，而是平台一级工作台之一，同时也是多个模块可调用的能力引擎：

- 在 `AI备课` 中插入可视化资源
- 在 `资源中心` 中保存为“数学演示资产”
- 在 `讲评` 中复用为错因演示图
- 在后续 `学生练习` 中作为探索式学习对象

## 接口与数据

### 核心领域对象

建议在 Phase 1 先统一定义以下对象，不要求全部接后端。

#### 1. 教学主体

- `Teacher`
- `Classroom`
- `StudentGroup`
- `Course`
- `Lesson`

#### 2. 数学资产

- `MathAsset`
- `VisualizationAsset`
- `LessonPlanAsset`
- `QuestionSetAsset`
- `AssessmentPaperAsset`
- `CommentaryAsset`

#### 3. 教学过程对象

- `Assignment`
- `Submission`
- `GradingResult`
- `InsightReport`

#### 4. 数学语义对象

- `KnowledgePoint`
- `QuestionType`
- `MisconceptionTag`
- `VisualizationTemplate`

### 推荐最小类型结构

```ts
type MathAssetType =
  | 'visualization'
  | 'lesson-plan'
  | 'question-set'
  | 'assessment-paper'
  | 'commentary';

interface MathAsset {
  id: string;
  type: MathAssetType;
  title: string;
  subject: 'math';
  gradeBand?: string;
  knowledgePoints?: string[];
  tags?: string[];
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

interface VisualizationAsset extends MathAsset {
  type: 'visualization';
  engine: 'math-canvas';
  config: Record<string, unknown>;
  preview?: string;
}
```

### 模块间数据流

#### 备课到可视化

`AI备课` 生成教案草稿 -> 老师点击“插入可视化” -> 打开 `Math Canvas` 选择或创建演示 -> 保存为 `VisualizationAsset` -> 回填到教案中

#### 可视化到资源中心

`Math Canvas` 中创建的函数图、曲面图、矢量场配置 -> 保存到 `Resource Center` -> 后续被备课、讲评、作业模块复用

#### 阅卷到讲评

后续 `GradingResult` 中的知识点与错因标签 -> 推荐相关 `VisualizationAsset` -> 自动生成讲评草稿

### AI 服务抽象

Phase 1 先统一服务接口，不在业务组件中直接写模型调用。

```ts
interface AiTaskRequest {
  task: 'lesson-plan' | 'question-gen' | 'grading-summary' | 'resource-tagging';
  input: Record<string, unknown>;
  context?: Record<string, unknown>;
}

interface AiTaskResponse<T = unknown> {
  ok: boolean;
  data?: T;
  warnings?: string[];
  traceId?: string;
}
```

## 推荐前端分层

### 目录建议

```text
src/
  app/
    router/
    layout/
    providers/
  modules/
    dashboard/
    prep/
    math-canvas/
    classes/
    assessments/
    grading/
    resources/
    research/
  domain/
    assets/
    teaching/
    grading/
    math/
  services/
    ai/
    assets/
    classes/
  shared/
    ui/
    hooks/
    utils/
```

### 当前仓库的演进方式

- 保留现有绘图组件与数学工具函数
- 新增 `router` 与 `layout`
- 将当前 `App.tsx` 中的可视化主体迁移至 `modules/math-canvas/`
- 将平台首页、备课页、资源页作为新模块加入
- 把跨模块共享类型从组件文件中逐步抽离到 `domain/`

### 为什么 Phase 1 不建议上微前端

- 当前还没有多个成熟子应用团队
- 模块边界尚未稳定，过早拆分会让路由、共享状态、主题、资产复用成本飙升
- 单仓壳 + 模块化目录已经足够支撑第一阶段验证

建议顺序是：

1. 先在单仓内把边界理顺
2. 待 `Math Canvas`、`AI备课`、`阅卷` 各自稳定后，再评估是否拆成多仓或微前端

## Phase 1 页面骨架建议

### 首页

- 今日待办
- 最近使用的教案 / 可视化 / 题目集
- 班级学情摘要
- 快捷入口

### AI备课页

- 左侧：教材章节 / 课程目标 / 班级选择
- 中间：教案生成与编辑区
- 右侧：可插入资源推荐
- 底部：一键调用 `Math Canvas`

### Math Canvas 页

- 继承当前主要能力
- 新增“保存到资源中心”“插入到教案”“用于讲评”入口
- 新增资产元数据编辑：标题、知识点、适用年级、标签

### 资源中心页

- 资源筛选：教案 / 可视化 / 题目集 / 试卷 / 讲评
- 资源卡片预览
- 收藏、复用、复制、归档

## 依赖与风险

### 依赖

- 现有 `FunctionCanvas` 前端代码质量足以支持模块迁移
- 后续若要落地 AI 备课与阅卷，需要独立后端或 BFF
- 若要进入学校场景，后续必须补齐权限、审计、隐私、校本资源隔离

### 风险

- **风险 1：继续把平台做成“大号单页面工具”**
  - 规避：先做路由、模块边界、对象模型，再做新能力

- **风险 2：`Math Canvas` 与平台其他模块割裂**
  - 规避：统一资产模型，要求其产出可保存、可引用、可检索

- **风险 3：AI 功能先天不稳定**
  - 规避：先把 AI 设计成“草稿生成器”，不是“自动决策器”

- **风险 4：业务范围过大，首期失焦**
  - 规避：Phase 1 只追求“平台看起来成立”，不追求全链路都成熟

## 迁移与回滚

### 迁移策略

Phase 1 采用渐进迁移：

1. 新增平台壳与路由
2. 保留当前可视化页面能力不变
3. 将原主页面挂载到 `/apps/math-canvas`
4. 新增首页和骨架模块
5. 最后再调整默认首页与品牌表达

### 回滚策略

- 若平台壳改造影响过大，可临时保留“旧版直达数学画板入口”
- 若导航改造影响使用体验，可让首页继续直达 `Math Canvas`
- 在路由层回滚，不直接破坏现有数学可视化核心组件
