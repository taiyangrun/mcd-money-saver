---
name: maimen-money-saver
slug: maimen-money-saver
displayName: 麦门省钱助手
version: 1.0.0
description: "基于麦当劳官方 MCP 的真实点餐省钱助手。输入人数/预算/口味，查真实门店菜单、一键领取优惠券、用 MCP 算价验证，输出穷鬼单点/多人拼单/企业团餐三种省钱方案，每一分钱都有实时数据支撑。2026 麦当劳程序员创意开发大赛参赛作品。"
summary: "基于麦当劳官方 MCP 的真实点餐省钱助手：输入人数/预算/口味，查真实菜单、领优惠券、算最优组合，输出穷鬼套餐/优惠叠加/拼单三种省钱方案，每一分钱都有 MCP 真实数据支撑。"
license: MIT
category: food-lifestyle
---

# 麦门省钱助手

吃麦当劳，别再瞎点了。这个 Skill 接麦当劳官方 MCP（`https://mcp.mcd.cn`），用**真实**的门店、菜单、优惠券、活动数据，给你算出最省钱的点餐方案。

## 什么时候用

当用户说以下任何一种时触发：
- "麦当劳怎么点最划算" / "穷鬼套餐" / "预算XX吃麦当劳"
- "有什么券可以用" / "帮我领券"
- "X个人吃麦当劳点什么" / "团建点餐"
- "第二份半价怎么拼最值"

## 三种省钱模式

### 1. 穷鬼模式（单人，预算有限）
输入：预算（如 25 元）、口味偏好、到店/外送。
流程：
1. `query-nearby-stores`（到店）或 `delivery-query-addresses`+`delivery-query-stores`（外送）定门店
2. `query-meals` 拉菜单 → `query-meal-detail` 看套餐组成
3. `query-store-coupons` 查门店可用券 + `available-coupons` 看可领券 → `auto-bind-coupons` 一键领
4. 按"汉堡+小食+饮料"组合试算，用 `calculate-price` 验证含券总价
5. 输出：在预算内热量/满足感最高的 2-3 套方案，标注每套原价、券后价、省了多少

### 2. 拼单模式（2-4 人）
输入：人数、各自偏好、预算上限。
流程：
1. 同上定门店、拉菜单、领券
2. 重点找：第二份半价、双人餐、分享桶等人均更低的组合
3. `calculate-price` 对比"各点各的"vs"拼单"的总价差
4. 输出：拼单方案 + 人均价格 + 比单点省多少，附分账明细

### 3. 团餐模式（5 人以上/企业）
输入：人数、预算/人、日期。
流程：
1. `delivery-query-stores`（beType=6 团餐）定门店
2. `query-promotions` 查满减满折规则 + `query-meal-assistance` 查助餐服务
3. 按官方搭配规则组套餐（20元以下小食 / 20-30 汉堡+小食 / 30-40 汉堡+薯条+饮料 / 40-50 全套）
4. `calculate-price` 验证，输出：人均预算内的团餐方案 + 满减凑单建议

## 麦门黑话（输出时可玩梗，但价格必须真实）
- "麦门" = 麦当劳爱好者自称
- "穷鬼套餐" = 高性价比组合（官方叫法：超值组合）
- 梗归梗，**所有价格、券、活动必须来自 MCP 实时查询，不许编**

## 重要规则
1. 价格、优惠券、活动一律以 MCP 实时返回为准，不许凭记忆编价格
2. 下单（`create-order`）前必须让用户确认，不许自动下单
3. 领券（`auto-bind-coupons`）是安全的，可直接执行
4. 积分相关（`query-my-account`、`mall-points-products`）按需查询，不主动推销
5. 营养需求可用 `list-nutrition-foods` 辅助，但本 Skill 主打省钱不主打健康

## MCP 配置
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
Token 申请：https://open.mcd.cn/mcp （手机号登录后控制台激活）

## 输出示例
```
🍔 麦门省钱方案（2人·到店·预算60元）

方案A：双人拼单（推荐）
- 麦香鸡双人餐 ×1 = 59元
- 用券：麦麦省"满50减10" → 实付 49元
- 人均 24.5元，比各点各的省 18元

方案B：穷鬼单点
- 麦香鸡(11) + 中薯(13.5) + 可乐(9) = 33.5/人
...
```
