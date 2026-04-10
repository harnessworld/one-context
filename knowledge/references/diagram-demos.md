# Diagram Demos — 绘图引擎示例集

每种引擎、每种图表类型各一个精美示例，可直接复制到支持 PlantUML / Mermaid / Graphviz 的平台使用。

---

## 一、PlantUML

### 1. 序列图 (Sequence)

> 场景：电商下单支付全链路

```plantuml
@startuml
!theme cerulean-outline
skinparam backgroundColor #FEFEFE
skinparam roundcorner 12
skinparam sequenceArrowThickness 2
skinparam sequenceParticipantBorderColor #3B82F6
skinparam sequenceLifeLineBorderColor #94A3B8
skinparam noteBorderColor #F59E0B

title 电商下单支付全链路

actor 用户 as U #E0F2FE
participant "移动端 App" as App #DBEAFE
participant "API Gateway" as GW #EDE9FE
participant "订单服务" as Order #FEF3C7
participant "库存服务" as Stock #D1FAE5
participant "支付服务" as Pay #FCE7F3
database "MySQL" as DB #F1F5F9
queue "消息队列" as MQ #FFF7ED

U -> App : 点击「立即购买」
activate App
App -> GW : POST /api/v1/orders
activate GW

GW -> Order : createOrder()
activate Order
Order -> Stock : lockInventory(skuId, qty)
activate Stock
Stock -> DB : UPDATE inventory SET locked = locked + ?
Stock --> Order : 锁定成功
deactivate Stock

Order -> DB : INSERT INTO orders (status='PENDING')
Order --> GW : orderId + paymentToken
deactivate Order

GW --> App : 返回收银台参数
deactivate GW

App -> Pay : 调起支付 SDK
activate Pay
Pay -> Pay : 风控校验 + 渠道路由

alt 支付成功
    Pay --> App : paymentResult = SUCCESS
    Pay -> MQ : publish(OrderPaid)
    MQ -> Order : consume(OrderPaid)
    activate Order
    Order -> Stock : confirmDeduct(skuId, qty)
    Order -> DB : UPDATE orders SET status='PAID'
    deactivate Order
else 支付失败
    Pay --> App : paymentResult = FAILED
    Pay -> MQ : publish(PayFailed)
    MQ -> Order : consume(PayFailed)
    activate Order
    Order -> Stock : unlockInventory(skuId, qty)
    Order -> DB : UPDATE orders SET status='CANCELLED'
    deactivate Order
end

deactivate Pay
App --> U : 展示支付结果页
deactivate App

note over MQ : 所有跨服务调用\n均通过消息队列解耦
note right of Pay : 支持微信/银联\n双通道自动路由

@enduml
```

### 2. 时序图 (Timing)

> 场景：交通信号灯控制周期

```plantuml
@startuml
!theme cerulean-outline
skinparam backgroundColor #FEFEFE

title 交通信号灯控制周期（单路口）

robust "主干道" as Main
robust "支路" as Side
concise "行人信号" as Ped

@0
Main is Green
Side is Red
Ped is Stop

@+30
Main is Yellow
Ped is Stop

@+5
Main is Red
Side is Green
Ped is Walk

@+20
Side is Yellow
Ped is Blink

@+5
Side is Red
Main is Green
Ped is Stop

highlight 0 to 30 #D1FAE5 : 主干道通行
highlight 35 to 55 #DBEAFE : 支路通行
highlight 55 to 60 #FEF3C7 : 全红过渡

@enduml
```

### 3. 用例图 (Use Case)

> 场景：在线教育平台核心功能

```plantuml
@startuml
!theme cerulean-outline
skinparam backgroundColor #FEFEFE
skinparam roundcorner 12
skinparam actorBorderColor #3B82F6
skinparam usecaseBorderColor #6366F1
skinparam packageBorderColor #94A3B8

title 在线教育平台 — 核心用例

left to right direction

actor "学生" as Student #E0F2FE
actor "讲师" as Teacher #EDE9FE
actor "管理员" as Admin #FEF3C7
actor "支付网关" as PayGW #FCE7F3

rectangle "在线教育平台" {
    package "学习中心" {
        usecase "浏览课程目录" as UC1
        usecase "观看视频课程" as UC2
        usecase "提交作业" as UC3
        usecase "参加在线考试" as UC4
        usecase "获取学习证书" as UC5
    }

    package "教学管理" {
        usecase "创建课程" as UC6
        usecase "上传教学资源" as UC7
        usecase "批改作业" as UC8
        usecase "查看学习数据" as UC9
    }

    package "平台运营" {
        usecase "用户管理" as UC10
        usecase "课程审核" as UC11
        usecase "数据报表" as UC12
        usecase "处理退款" as UC13
    }

    usecase "购买课程" as UC14
}

Student --> UC1
Student --> UC2
Student --> UC3
Student --> UC4
Student --> UC14
UC4 ..> UC5 : <<include>>
UC14 --> PayGW

Teacher --> UC6
Teacher --> UC7
Teacher --> UC8
Teacher --> UC9

Admin --> UC10
Admin --> UC11
Admin --> UC12
Admin --> UC13

UC2 ..> UC14 : <<precondition>>
UC6 ..> UC11 : <<include>>

@enduml
```

### 4. 类图 (Class)

> 场景：事件驱动架构的领域模型

```plantuml
@startuml
!theme cerulean-outline
skinparam backgroundColor #FEFEFE
skinparam roundcorner 10
skinparam classBorderColor #3B82F6
skinparam classBackgroundColor #F8FAFC
skinparam stereotypeCBackgroundColor #DBEAFE

title 事件驱动架构 — 领域模型

package "聚合根" <<Frame>> #F0F9FF {
    abstract class AggregateRoot<ID> {
        - id: ID
        - version: Long
        - domainEvents: List<DomainEvent>
        + getId(): ID
        + getVersion(): Long
        # registerEvent(event: DomainEvent): void
        + clearEvents(): List<DomainEvent>
    }
}

package "订单领域" <<Frame>> #FFFBEB {
    class Order extends AggregateRoot {
        - orderId: OrderId
        - customer: CustomerId
        - items: List<OrderItem>
        - status: OrderStatus
        - totalAmount: Money
        - createdAt: Instant
        --
        + {static} create(cmd: CreateOrderCmd): Order
        + addItem(product: ProductId, qty: int, price: Money): void
        + confirm(): void
        + cancel(reason: String): void
        + ship(trackingNo: String): void
    }

    class OrderItem <<Value Object>> {
        - product: ProductId
        - quantity: int
        - unitPrice: Money
        - subtotal: Money
        + calculateSubtotal(): Money
    }

    enum OrderStatus <<Enumeration>> {
        DRAFT
        CONFIRMED
        PAID
        SHIPPED
        DELIVERED
        CANCELLED
    }

    class Money <<Value Object>> {
        - amount: BigDecimal
        - currency: Currency
        + add(other: Money): Money
        + multiply(factor: int): Money
    }
}

package "领域事件" <<Frame>> #F0FDF4 {
    interface DomainEvent {
        + eventId(): String
        + occurredOn(): Instant
        + aggregateId(): String
    }

    class OrderCreated implements DomainEvent {
        - orderId: String
        - customerId: String
        - items: List<OrderItem>
    }

    class OrderConfirmed implements DomainEvent {
        - orderId: String
        - totalAmount: Money
    }

    class OrderShipped implements DomainEvent {
        - orderId: String
        - trackingNo: String
    }
}

Order *-- "1..*" OrderItem
Order --> OrderStatus
Order ..> OrderCreated : <<creates>>
Order ..> OrderConfirmed : <<creates>>
Order ..> OrderShipped : <<creates>>
OrderItem --> Money : unitPrice/subtotal

@enduml
```

### 5. 活动图 (Activity)

> 场景：CI/CD 流水线（含并行）

```plantuml
@startuml
!theme cerulean-outline
skinparam backgroundColor #FEFEFE
skinparam roundcorner 12
skinparam ActivityBorderColor #3B82F6
skinparam ActivityDiamondBorderColor #F59E0B

title CI/CD 流水线 — 从提交到生产部署

start

:开发者推送代码到 feature 分支;

:触发 CI Pipeline;

partition "构建阶段" #E0F2FE {
    :拉取代码 & 安装依赖;
    :编译构建;
    :生成 Docker 镜像;
}

fork
    partition "质量门禁（并行）" #EDE9FE {
        :单元测试;
        note right: 覆盖率 ≥ 80%
    }
fork again
    partition "质量门禁（并行）" #EDE9FE {
        :代码扫描 (SonarQube);
    }
fork again
    partition "质量门禁（并行）" #EDE9FE {
        :安全漏洞扫描 (Trivy);
    }
end fork

if (全部通过?) then (是)
    :合并到 main 分支;
else (否)
    :通知开发者修复;
    stop
endif

partition "部署阶段" #D1FAE5 {
    :部署到 Staging 环境;
    :运行集成测试 & E2E 测试;

    if (测试通过?) then (是)
        :人工审批;
        note right: 需 Tech Lead 确认
        if (审批通过?) then (是)
            :蓝绿部署到 Production;
            :切换流量 (金丝雀 10% → 50% → 100%);
            :健康检查 & 监控告警;
        else (否)
            :记录原因，退回开发;
            stop
        endif
    else (否)
        :自动回滚 Staging;
        :生成失败报告;
        stop
    endif
}

:部署完成，通知团队;

stop

@enduml
```

### 6. 组件图 (Component)

> 场景：数据分析平台架构（严格分层，自上而下）

```plantuml
@startuml
!theme cerulean-outline
skinparam backgroundColor #FEFEFE
skinparam roundcorner 15
skinparam padding 8
skinparam componentStyle rectangle
skinparam defaultFontSize 12

skinparam component {
    BorderColor #475569
    BackgroundColor #F8FAFC
    FontColor #1E293B
    BorderThickness 1.5
}

skinparam package {
    BorderColor #CBD5E1
    BackgroundColor transparent
    FontColor #334155
    FontStyle bold
    BorderThickness 2
    style rectangle
}

skinparam interface {
    BorderColor #3B82F6
    BackgroundColor #DBEAFE
}

skinparam database {
    BorderColor #7C3AED
    BackgroundColor #EDE9FE
}

skinparam arrow {
    Color #64748B
    Thickness 1.5
}

title 数据分析平台 — 组件架构
header 自上而下分层：接入 → 处理 → 存储 → 服务 → 展示

package "展示层" as L5 #F0F9FF {
    [BI Dashboard\n(Metabase)] as BI
    [报表中心\n(JasperReports)] as Report
    [数据 API\n(GraphQL)] as DataAPI
}

package "服务层" as L4 #F0FDF4 {
    [查询引擎\n(Presto)] as Query
    [指标服务\n(自研)] as Metric
    [预警服务\n(自研)] as Alert
}

package "存储层" as L3 #FFFBEB {
    database "数据仓库\n(ClickHouse)" as DW
    database "数据湖\n(Iceberg + S3)" as Lake
    database "元数据\n(Hive Metastore)" as Meta
}

package "处理层" as L2 #EDE9FE {
    [实时计算\n(Flink)] as Flink
    [离线计算\n(Spark)] as Spark
    [数据质量\n(Great Expectations)] as DQ
}

package "接入层" as L1 #FCE7F3 {
    [日志采集\n(Filebeat)] as Log
    [数据库 CDC\n(Debezium)] as CDC
    [API 采集\n(Airbyte)] as APICollect
    queue "消息总线\n(Kafka)" as Kafka
}

' === 接入层内部 ===
Log -down-> Kafka
CDC -down-> Kafka
APICollect -down-> Kafka

' === 接入 → 处理 ===
Kafka -down-> Flink : 实时流
Kafka -down-> Spark : 批量消费

' === 处理 → 存储 ===
Flink -down-> DW : 实时写入
Spark -down-> Lake : 批量写入
Spark -down-> DW : 聚合结果
DQ -left-> Spark : 质量校验
Flink .right.> DQ : 异常上报

' === 存储层内部 ===
DW .right.> Meta : 注册表
Lake .left.> Meta : 注册表

' === 存储 → 服务 ===
DW -down-> Query : SQL 查询
Lake -down-> Query : 联邦查询
DW -down-> Metric : 指标计算
Metric -right-> Alert : 阈值触发

' === 服务 → 展示 ===
Query -down-> BI : 数据可视化
Query -down-> Report : 定时报表
Metric -down-> DataAPI : 指标接口
Alert -down-> Report : 预警报告

@enduml
```

### 7. 状态图 (State)

> 场景：订单全生命周期

```plantuml
@startuml
!theme cerulean-outline
skinparam backgroundColor #FEFEFE
skinparam roundcorner 12
skinparam stateBorderColor #3B82F6
skinparam stateBackgroundColor #F8FAFC

title 订单全生命周期状态机

[*] --> 待支付 : 用户下单

state 待支付 #FFFBEB {
    待支付 : entry / 锁定库存
    待支付 : exit / 记录支付时间
    待支付 : 超时30分钟自动取消
}

待支付 --> 已支付 : 支付成功
待支付 --> 已取消 : 用户取消 / 支付超时

state 已支付 #DBEAFE {
    已支付 : entry / 扣减库存
    已支付 : entry / 通知卖家
}

已支付 --> 待发货 : 卖家确认
已支付 --> 退款中 : 用户申请退款

state 待发货 #EDE9FE {
    [*] --> 拣货中
    拣货中 --> 打包中 : 拣货完成
    打包中 --> 已交付快递 : 打包完成
    已交付快递 --> [*]
}

待发货 --> 已发货 : 快递揽收

state 已发货 #D1FAE5 {
    已发货 : 运单号 = trackingNo
    已发货 : 可查看物流轨迹
}

已发货 --> 已签收 : 物流签收
已发货 --> 退货中 : 用户拒收

已签收 --> 已完成 : 确认收货 / 7天自动确认
已签收 --> 退货中 : 7天内申请退货

state "售后处理" as AfterSale #FCE7F3 {
    state 退款中
    state 退货中
    退货中 --> 退款中 : 卖家收到退货
}

退款中 --> 已退款 : 退款到账

state 已完成 #F0FDF4 {
    已完成 : entry / 发放积分
    已完成 : entry / 邀请评价
}

已取消 --> [*]
已退款 --> [*]
已完成 --> [*]

@enduml
```

### 8. 对象图 (Object)

> 场景：运行时订单实例关系

```plantuml
@startuml
!theme cerulean-outline
skinparam backgroundColor #FEFEFE
skinparam roundcorner 10
skinparam objectBorderColor #3B82F6
skinparam objectBackgroundColor #F8FAFC

title 运行时订单实例 — 2026-04-07 快照

object "order2024001 : Order" as o1 #FFFBEB {
    orderId = "ORD-2024001"
    status = PAID
    totalAmount = ¥2,847.00
    createdAt = "2026-04-07T10:30:00"
}

object "customer_zhangsan : Customer" as c1 #E0F2FE {
    customerId = "CUS-88001"
    name = "张三"
    level = VIP_GOLD
    balance = ¥15,200.00
}

object "item1 : OrderItem" as i1 #F0FDF4 {
    product = "iPhone 16 手机壳"
    quantity = 2
    unitPrice = ¥49.00
    subtotal = ¥98.00
}

object "item2 : OrderItem" as i2 #F0FDF4 {
    product = "AirPods Pro 3"
    quantity = 1
    unitPrice = ¥1,899.00
    subtotal = ¥1,899.00
}

object "item3 : OrderItem" as i3 #F0FDF4 {
    product = "MagSafe 充电器"
    quantity = 1
    unitPrice = ¥399.00
    subtotal = ¥399.00
}

object "addr : ShippingAddress" as a1 #EDE9FE {
    province = "浙江省"
    city = "杭州市"
    district = "西湖区"
    street = "文三路 478 号"
    zipCode = "310012"
    phone = "138****5678"
}

object "coupon_spring : Coupon" as cp #FCE7F3 {
    couponId = "CPN-SPRING2026"
    type = AMOUNT_OFF
    discount = ¥200.00
    minOrder = ¥500.00
    expireAt = "2026-04-30"
}

object "payment_wx : Payment" as p1 #D1FAE5 {
    paymentId = "PAY-WX-78923"
    channel = WECHAT
    amount = ¥2,196.00
    paidAt = "2026-04-07T10:32:15"
}

o1 --> c1 : customer
o1 *-- i1 : items[0]
o1 *-- i2 : items[1]
o1 *-- i3 : items[2]
o1 --> a1 : shippingAddress
o1 --> cp : appliedCoupon
o1 --> p1 : payment

note bottom of o1
    totalAmount = 98 + 1899 + 399 = ¥2,396
    优惠券减免 = -¥200
    实付金额 = ¥2,196
end note

@enduml
```

---

## 二、Mermaid

### 1. Flow Chart

> 场景：用户注册风控决策

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
    'primaryColor': '#EFF6FF',
    'primaryBorderColor': '#3B82F6',
    'primaryTextColor': '#1E293B',
    'lineColor': '#94A3B8',
    'secondaryColor': '#F0FDF4',
    'tertiaryColor': '#FFFBEB',
    'fontSize': '14px',
    'fontFamily': 'Inter, system-ui, sans-serif'
}}}%%
flowchart TD
    A([fa:fa-user-plus 用户提交注册]):::start --> B{fa:fa-mobile-alt 手机号\n格式校验}
    B -->|不合法| C[fa:fa-times-circle 返回错误提示]:::danger
    B -->|合法| D{fa:fa-shield-alt IP\n风险评估}

    D -->|高风险| E[fa:fa-puzzle-piece 触发滑块验证码]:::action
    D -->|正常| F{fa:fa-ban 黑名单\n检查}

    E --> E1{验证通过?}
    E1 -->|失败 3 次| C
    E1 -->|成功| F

    F -->|命中| G[fa:fa-exclamation-triangle 拒绝注册\n上报风控中心]:::danger
    F -->|未命中| H[fa:fa-sms 发送短信验证码]:::action

    H --> I{fa:fa-clock 60s 内\n输入验证码}
    I -->|超时| J[fa:fa-hourglass-end 验证码失效\n可重新获取]:::warning
    I -->|验证正确| K{fa:fa-fingerprint 设备指纹\n检查}

    K -->|同设备 24h > 3 次| L[fa:fa-hand-paper 限流拦截]:::danger
    K -->|正常| M[fa:fa-check-circle 创建账户]:::success

    M --> N[fa:fa-database 写入用户表]:::action
    M --> O[fa:fa-chart-pie 初始化用户画像]:::action
    M --> P[fa:fa-bell 发送欢迎通知]:::action
    N & O & P --> Q([fa:fa-flag-checkered 注册完成]):::success

    classDef start fill:#DBEAFE,stroke:#2563EB,stroke-width:2px,color:#1E40AF,font-weight:bold
    classDef action fill:#F8FAFC,stroke:#94A3B8,stroke-width:1.5px,color:#334155
    classDef danger fill:#FEE2E2,stroke:#EF4444,stroke-width:2px,color:#991B1B,font-weight:bold
    classDef warning fill:#FEF3C7,stroke:#F59E0B,stroke-width:2px,color:#92400E
    classDef success fill:#D1FAE5,stroke:#10B981,stroke-width:2px,color:#065F46,font-weight:bold

    linkStyle default stroke:#94A3B8,stroke-width:1.5px
```

### 2. Sequence Diagram

> 场景：OAuth 2.0 授权码流程

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
    'actorBkg': '#EFF6FF',
    'actorBorder': '#3B82F6',
    'actorTextColor': '#1E3A5F',
    'signalColor': '#475569',
    'signalTextColor': '#1E293B',
    'labelBoxBkgColor': '#F8FAFC',
    'labelBoxBorderColor': '#CBD5E1',
    'noteBkgColor': '#FFFBEB',
    'noteBorderColor': '#F59E0B',
    'activationBkgColor': '#DBEAFE',
    'activationBorderColor': '#3B82F6',
    'loopTextColor': '#6366F1',
    'fontSize': '14px'
}}}%%
sequenceDiagram
    autonumber

    actor U as 👤 用户
    participant App as 📱 客户端应用
    participant Auth as 🔐 授权服务器
    participant API as 🖥️ 资源服务器

    U->>App: 点击「第三方登录」
    activate App

    App->>Auth: 302 重定向到授权端点<br/>GET /authorize?response_type=code<br/>&client_id=xxx&redirect_uri=xxx&scope=profile
    activate Auth

    Auth->>U: 展示授权确认页面
    U->>Auth: 用户同意授权

    Auth-->>App: 302 回调 redirect_uri?code=AUTH_CODE
    deactivate Auth

    rect rgb(240, 253, 244)
        Note over App,Auth: 🔒 后端安全通道（服务端到服务端）
        App->>Auth: POST /token<br/>grant_type=authorization_code<br/>&code=AUTH_CODE&client_secret=xxx
        activate Auth
        Auth->>Auth: 验证 code + client_secret
        Auth-->>App: { access_token, refresh_token, expires_in }
        deactivate Auth
    end

    App->>API: GET /api/userinfo<br/>Authorization: Bearer {access_token}
    activate API
    API->>Auth: 验证 Token 有效性
    Auth-->>API: Token 有效 ✓
    API-->>App: { id, name, email, avatar }
    deactivate API

    App-->>U: 登录成功，展示用户信息
    deactivate App

    Note over U,API: ⏰ access_token 过期后使用 refresh_token 刷新
```

### 3. Class Diagram

> 场景：策略模式 — 多渠道消息推送

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
    'primaryColor': '#F8FAFC',
    'primaryBorderColor': '#3B82F6',
    'lineColor': '#64748B',
    'fontSize': '13px'
}}}%%
classDiagram
    direction TB

    class MessageService {
        -strategyMap: Map~String, PushStrategy~
        -templateEngine: TemplateEngine
        -messageRepo: MessageRepository
        +send(req: SendRequest): SendResult
        +batchSend(reqs: List~SendRequest~): BatchResult
        -selectStrategy(channel: String): PushStrategy
        -renderContent(templateId: String, vars: Map): String
    }

    class SendRequest {
        +userId: String
        +channel: String
        +templateId: String
        +variables: Map~String, Object~
        +priority: Priority
        +scheduleAt: LocalDateTime?
    }

    class SendResult {
        +messageId: String
        +status: DeliveryStatus
        +channel: String
        +sentAt: Instant
        +errorMsg: String?
    }

    class PushStrategy {
        <<interface>>
        +send(target: String, content: String, opts: Map): SendResult
        +supports(channel: String): boolean
        +getQuota(): RateLimit
    }

    class SmsPushStrategy {
        -smsClient: AliyunSmsClient
        -signName: String
        +send(phone, content, opts): SendResult
        +supports(channel): boolean
        +getQuota(): RateLimit
    }

    class EmailPushStrategy {
        -mailSender: JavaMailSender
        -fromAddress: String
        +send(email, content, opts): SendResult
        +supports(channel): boolean
        +getQuota(): RateLimit
    }

    class WechatPushStrategy {
        -wxClient: WxMpService
        -templateMap: Map~String, String~
        +send(openId, content, opts): SendResult
        +supports(channel): boolean
        +getQuota(): RateLimit
    }

    class DingTalkPushStrategy {
        -robotClient: DingTalkClient
        -webhook: String
        +send(userId, content, opts): SendResult
        +supports(channel): boolean
        +getQuota(): RateLimit
    }

    class RateLimit {
        +maxPerSecond: int
        +maxPerDay: int
        +currentUsed: AtomicLong
        +tryAcquire(): boolean
    }

    PushStrategy <|.. SmsPushStrategy
    PushStrategy <|.. EmailPushStrategy
    PushStrategy <|.. WechatPushStrategy
    PushStrategy <|.. DingTalkPushStrategy

    MessageService --> PushStrategy : 持有多个策略
    MessageService --> SendRequest : 接收
    MessageService --> SendResult : 返回

    SmsPushStrategy --> RateLimit
    EmailPushStrategy --> RateLimit
    WechatPushStrategy --> RateLimit
    DingTalkPushStrategy --> RateLimit
```

### 4. State Diagram

> 场景：Kubernetes Pod 生命周期

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
    'primaryColor': '#EFF6FF',
    'primaryBorderColor': '#3B82F6',
    'lineColor': '#64748B',
    'fontSize': '13px'
}}}%%
stateDiagram-v2
    direction LR

    [*] --> Pending : kubectl apply

    state Pending {
        [*] --> Scheduling
        Scheduling --> ImagePulling : 节点已分配
        ImagePulling --> Scheduled : 镜像拉取完成
        --
        note right of Scheduling : kube-scheduler\n根据资源请求选择节点
    }

    Pending --> Running : 所有容器启动成功

    state Running {
        [*] --> Healthy
        Healthy --> Unhealthy : 健康检查失败
        Unhealthy --> Healthy : 健康检查恢复
        Unhealthy --> CrashLoop : 连续失败 > 3次
        CrashLoop --> Healthy : backoff 后重启成功
        --
        note right of CrashLoop : 指数退避重启\n10s → 20s → 40s → ... → 5min
    }

    Running --> Succeeded : 所有容器正常退出 (exit 0)
    Running --> Failed : 容器异常退出 (exit ≠ 0)
    Running --> Terminating : 收到删除信号

    state Terminating {
        [*] --> PreStop
        PreStop --> SIGTERM : 执行 preStop Hook
        SIGTERM --> GracePeriod : 等待优雅关闭
        GracePeriod --> SIGKILL : 超过 terminationGracePeriodSeconds
    }

    Terminating --> [*] : Pod 已清理

    Succeeded --> [*]
    Failed --> [*]

    Pending --> Failed : ImagePullBackOff\nInsufficientCPU\nInsufficientMemory
```

### 5. ER Diagram

> 场景：SaaS 多租户权限系统

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
    'primaryColor': '#F8FAFC',
    'primaryBorderColor': '#3B82F6',
    'lineColor': '#64748B',
    'fontSize': '13px'
}}}%%
erDiagram
    TENANT ||--o{ USER : "拥有"
    TENANT ||--o{ ROLE : "定义"
    TENANT ||--o{ RESOURCE : "管理"
    TENANT {
        uuid tenant_id PK
        varchar name
        varchar plan "FREE|PRO|ENTERPRISE"
        int max_users
        jsonb settings
        timestamp created_at
        timestamp expired_at
    }

    USER ||--o{ USER_ROLE : "关联"
    USER {
        uuid user_id PK
        uuid tenant_id FK
        varchar email UK
        varchar phone UK
        varchar password_hash
        varchar display_name
        varchar avatar_url
        enum status "ACTIVE|LOCKED|DEACTIVATED"
        timestamp last_login_at
        timestamp created_at
    }

    ROLE ||--o{ USER_ROLE : "分配给"
    ROLE ||--o{ ROLE_PERMISSION : "包含"
    ROLE {
        uuid role_id PK
        uuid tenant_id FK
        varchar role_name
        varchar description
        boolean is_system "系统内置角色不可删除"
        timestamp created_at
    }

    USER_ROLE {
        uuid user_id FK
        uuid role_id FK
        timestamp granted_at
        uuid granted_by FK "授权人"
    }

    PERMISSION ||--o{ ROLE_PERMISSION : "被引用"
    PERMISSION {
        uuid permission_id PK
        varchar resource_type "menu|api|data|button"
        varchar action "read|write|delete|export"
        varchar resource_code "如 order:export"
        varchar description
    }

    ROLE_PERMISSION {
        uuid role_id FK
        uuid permission_id FK
        jsonb conditions "数据范围条件"
    }

    RESOURCE ||--o{ PERMISSION : "对应"
    RESOURCE {
        uuid resource_id PK
        uuid tenant_id FK
        varchar resource_type
        varchar resource_name
        varchar path "菜单路径或API路径"
        int sort_order
        uuid parent_id FK "树形结构"
    }

    USER ||--o{ AUDIT_LOG : "产生"
    AUDIT_LOG {
        bigint log_id PK
        uuid user_id FK
        uuid tenant_id FK
        varchar action "login|access|modify|delete"
        varchar resource
        varchar ip_address
        jsonb detail
        timestamp created_at
    }
```

### 6. Gantt

> 场景：产品 v2.0 迭代排期

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
    'fontSize': '13px',
    'gridColor': '#E2E8F0',
    'todayLineColor': '#EF4444',
    'taskBkgColor': '#DBEAFE',
    'activeTaskBkgColor': '#3B82F6',
    'doneTaskBkgColor': '#D1FAE5',
    'critBkgColor': '#FEE2E2',
    'critBorderColor': '#EF4444',
    'taskTextColor': '#1E293B',
    'sectionBkgColor': '#F8FAFC'
}}}%%
gantt
    title 产品 v2.0 迭代排期（2026 Q2）
    dateFormat YYYY-MM-DD
    axisFormat %m/%d
    todayMarker stroke-width:3px,stroke:#EF4444

    section 📋 需求 & 设计
        需求评审 & PRD 定稿          :done,    req1, 2026-04-01, 5d
        交互设计 & UI 设计稿          :done,    des1, after req1, 7d
        技术方案评审                  :done,    tec1, after req1, 3d

    section 🔧 后端开发
        用户中心重构                  :crit,    be1, 2026-04-14, 10d
        权限系统 RBAC                 :crit,    be2, after be1, 8d
        消息推送服务                  :         be3, 2026-04-20, 7d
        数据导出模块                  :         be4, after be3, 5d
        OpenAPI 文档                 :         be5, after be2, 3d

    section 🎨 前端开发
        新版 Dashboard               :         fe1, 2026-04-16, 8d
        权限管理页面                  :         fe2, after fe1, 6d
        消息中心 UI                   :         fe3, after fe1, 5d
        数据可视化组件                :         fe4, after fe2, 7d

    section 🧪 测试 & 发布
        集成测试                      :crit,    qa1, 2026-05-12, 5d
        性能压测                      :         qa2, after qa1, 3d
        UAT 验收                     :         qa3, after qa2, 3d
        生产发布                      :milestone, rel, 2026-05-25, 0d
```

### 7. Pie Chart

> 场景：系统故障根因分布

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
    'pieSectionTextSize': '14px',
    'pieLegendTextSize': '14px',
    'pieOuterStrokeWidth': '2px'
}}}%%
pie showData
    title 2026 Q1 生产故障根因分布（共 47 起）
    "代码缺陷" : 15
    "配置变更" : 11
    "基础设施故障" : 8
    "第三方依赖" : 6
    "容量不足" : 4
    "人为误操作" : 3
```

---

## 三、Graphviz

### Finite State Machine

> 场景：正则表达式 `(a|b)*abb` 的 DFA 识别器

```dot
digraph finite_state_machine {
    // 全局样式
    bgcolor="#FEFEFE"
    fontname="Inter, Helvetica, Arial"
    fontsize=14
    rankdir=LR
    size="10,6"
    pad=0.4
    nodesep=0.6
    ranksep=1.0
    label="DFA: 正则表达式 (a|b)*abb 的识别器"
    labelloc=t
    labeljust=c
    fontcolor="#1E293B"

    // 节点默认样式
    node [
        fontname="SF Mono, Menlo, Consolas, monospace"
        fontsize=12
        style="filled,bold"
        fillcolor="#EFF6FF"
        color="#3B82F6"
        penwidth=2
        width=0.7
    ]

    // 边默认样式
    edge [
        fontname="SF Mono, Menlo, Consolas, monospace"
        fontsize=11
        color="#64748B"
        fontcolor="#334155"
        penwidth=1.5
        arrowsize=0.8
    ]

    // 接受状态（双圆圈）
    node [shape=doublecircle fillcolor="#D1FAE5" color="#10B981"];
    S4;

    // 普通状态
    node [shape=circle fillcolor="#EFF6FF" color="#3B82F6"];

    // 起始标记
    start [label="" shape=point width=0.15 color="#1E293B"];

    // 状态标签
    S0 [label="S₀" fillcolor="#DBEAFE"];
    S1 [label="S₁" fillcolor="#EDE9FE" color="#6366F1"];
    S2 [label="S₂" fillcolor="#FFFBEB" color="#F59E0B"];
    S3 [label="S₃" fillcolor="#FFF7ED" color="#EA580C"];
    S4 [label="S₄" fillcolor="#D1FAE5" color="#10B981"];

    // 转换
    start -> S0;
    S0 -> S1 [label="a"];
    S0 -> S0 [label="b"];
    S1 -> S1 [label="a"];
    S1 -> S2 [label="b"];
    S2 -> S1 [label="a"];
    S2 -> S3 [label="b"];
    S3 -> S1 [label="a"];
    S3 -> S4 [label="b" color="#10B981" fontcolor="#065F46" penwidth=2.5];
    S4 -> S1 [label="a" style=dashed];
    S4 -> S0 [label="b" style=dashed];
}
```
