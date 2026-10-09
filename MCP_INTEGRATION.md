# MCP_INTEGRATION.md

## 使用的 MCP Server

- **名称**：麦当劳中国 MCP 服务（mcd-mcp）
- **地址**：`https://mcp.mcd.cn`
- **协议**：Streamable HTTP（MCP 2025-03-26）
- **认证**：请求头 `Authorization: Bearer <MCP_TOKEN>`
- **申请**：https://open.mcd.cn/mcp（手机号登录 → 控制台激活）
- **覆盖场景**：麦乐送点餐、到店取餐、团餐、积分兑换券、活动日历查询

## 实际使用的 Tool（共 17 个）

| Tool | 用途 | 调用时机 |
|---|---|---|
| `query-nearby-stores` | 查附近可点餐门店 | 到店/得来速场景定门店 |
| `delivery-query-addresses` | 查配送地址列表 | 外送场景第一步 |
| `delivery-query-stores` | 查地址可配送门店 | 外送/团餐定门店 |
| `query-meals` | 拉取门店在售菜单 | 拿真实餐品+价格 |
| `query-meal-detail` | 餐品详情/套餐组成 | 看套餐里有什么 |
| `query-store-coupons` | 门店可用优惠券 | 下单前查能用的券 |
| `query-my-coupons` | 我的卡包 | 看已有券 |
| `available-coupons` | 可领取的券列表 | 领券前看有什么 |
| `auto-bind-coupons` | 一键领取所有券 | 用户说"领券"时执行 |
| `calculate-price` | 计算含券总价 | **每个方案必须用它验证** |
| `campaign-calendar` | 营销活动日历 | 查限时活动 |
| `query-promotions` | 团餐满减满折规则 | 团餐凑单 |
| `query-meal-assistance` | 团餐助餐服务 | 团餐下单前 |
| `list-nutrition-foods` | 营养成分 | 按需辅助 |
| `query-my-account` | 积分账户 | 按需查询 |
| `create-order` | 创建订单 | **必须用户确认后才调** |
| `cancel-order` / `query-order` | 取消/查询订单 | 售后 |

## 典型调用流程（穷鬼模式）

```
1. query-nearby-stores(beType=1, city="深圳市")
   → 得到 storeCode

2. query-meals(storeCode, orderType=1)
   → 得到在售菜单与价格

3. available-coupons() + query-my-coupons()
   → 看到可领券和已有券

4. auto-bind-coupons()
   → 一键领券

5. query-store-coupons(storeCode, orderType=1)
   → 确认当前门店订单可用券

6. [本地组合] 按预算拼出 2-3 套候选方案

7. calculate-price(storeCode, orderType=1, items=[...])
   → 逐套验证含券实付价

8. 输出方案：原价 / 券后价 / 省了多少
```

## 业务价值

1. **真实省钱**：所有价格来自 MCP 实时数据，不是写死的假菜单——券后价经 `calculate-price` 服务端验证，可信。
2. **券不浪费**：自动发现可领券+一键领取，解决"有券不知道"的痛点。
3. **决策透明**：每个方案标注"比单点省 X 元"，用户看得懂为什么划算。
4. **场景覆盖**：单人穷鬼餐 → 多人拼单 → 企业团餐，一套工具链全覆盖。

## 连通性验证

`scripts/mcp_probe.py` 可验证 Token 有效性并列出可用工具：
```bash
MCD_MCP_TOKEN=你的token python3 scripts/mcp_probe.py
```
（脚本内无硬编码 Token，必须通过环境变量传入。）
