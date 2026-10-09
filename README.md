# 麦门省钱助手 🍔

基于**麦当劳官方 MCP** 的真实点餐省钱助手。输入人数/预算/口味，查真实菜单、领真实优惠券、算最优组合——每一分钱都有 MCP 实时数据支撑，不编价格。

> 参赛项目：2026 麦当劳程序员创意开发大赛

## 你能用它干什么

| 场景 | 输入 | 输出 |
|---|---|---|
| 穷鬼单点 | 预算25元+口味 | 预算内满足感最高的2-3套方案 |
| 双人拼单 | 2人+偏好 | 拼单 vs 单点的价差+分账明细 |
| 团建团餐 | 10人+人均预算 | 满减凑单团餐方案 |
| 领券 | "帮我领券" | 一键领取所有可用优惠券 |

## 快速开始

1. 申请麦当劳 MCP Token：https://open.mcd.cn/mcp （手机号登录 → 控制台激活）
2. 配置 MCP：
```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": { "Authorization": "Bearer YOUR_MCP_TOKEN" }
    }
  }
}
```
3. 把 `SKILL.md` 导入你的 AI 客户端（支持 Skill 的均可），然后说："2个人，预算60，到店吃，帮我算最划算的"

## 工作原理

```
定门店 → 拉菜单 → 查券领券 → 组合试算 → MCP算价验证 → 输出省钱方案
```

核心 MCP 工具链：`query-meals`（菜单）→ `query-store-coupons`/`available-coupons`（券）→ `auto-bind-coupons`（领券）→ `calculate-price`（含券总价验证）。

详细说明见 [MCP_INTEGRATION.md](./MCP_INTEGRATION.md)。

## 文件结构

```
├── SKILL.md              # Skill 定义（核心）
├── agents/openai.yaml    # Agent 配置
├── MCP_INTEGRATION.md    # MCP 接入说明
├── CONTEST_DECLARATION.md # 参赛声明（官方文件，未改动）
├── scripts/              # 辅助脚本（MCP 连通性探针）
├── examples/             # 使用示例
└── icon.png              # 项目图标
```

## 目标用户

- 麦当劳爱好者（麦门信徒）
- 预算有限的学生党、打工人
- 需要团餐方案的行政/HR
- 想薅券但懒得研究的懒人

## 注意事项

- 所有价格、券、活动以 MCP 实时查询为准；本项目不硬编码任何价格
- 下单前必须经用户确认，不会自动下单
- Token 请用环境变量 `MCD_MCP_TOKEN`，不要写进代码
- 本项目为大赛参赛作品，非麦当劳官方产品

## License

MIT
