# 【LC 121/122】买卖股票 I & II：等低点与吃上坡

**来源**: https://zhoujungis.github.io/article/lc-121-122-best-time-to-buy-and-sell-stock/
**标签**: 算法、动态规划、LeetCode、面试

## 题目

### LC 121 买卖股票的最佳时机

给定数组 `prices`，`prices[i]` 是第 `i` 天的股价。选择一个低点**买入**、一个更高的点**卖出**（只能买卖**一次**，且必须先买后卖），计算最大利润。无法获利则返回 `0`（干脆不买）。

```
输入: prices = [7,1,5,3,6,4]
输出: 5   （第 1 天以 1 买入、第 4 天以 6 卖出，6 - 1 = 5）

输入: prices = [7,6,4,3,1]
输出: 0   （全程下跌，不买）
```

### LC 122 买卖股票的最佳时机 II

同一组价格，可以**无限次**交易（多次买卖），但仍须先买后卖、**手里最多持一股**（买了才能再买下一次）。求最大利润。

```
输入: prices = [7,1,5,3,6,4]
输出: 7   （1→5 赚 4，3→6 赚 3，共 7）

输入: prices = [1,2,3,4,5]
输出: 4   （连续持有 1→5 即可，频繁买卖不加分）
```

## 思路

- **LC 121**：不枚举「哪天买」，而是逐天问「今天卖，最赚能多少」—— 卖出日是今天时，买入日必然是 `0..d-1` 里的最低价，于是 O(n²) 的对枚举压成 `minPrice`（截至昨天的最低价）和 `best` 两个单调变量。
- **121 是「顺序最大差」，不是「极差」**：`[2,4,1]` 的极差 `4-1=3` 非法（低点在 4 之后），真实答案是 2，`minPrice` 必须边走边记。
- **121 的 `best` 初始化为 0**（不是 `-∞`）：全程下跌时 `candidate` 恒为负，`best` 停在 0，语义就是「干脆不买」，这是合法答案，也是「最大利润」与「最大差值」的分界。
- **LC 122 贪心**：每一段上坡都吃下、下坡空仓路过，利润 = 所有正差之和。相邻正差可以无缝拼接（把连续上坡拆成逐日小额交易总和不变），所以「天天吃正差」不违反「手里最多一股」。
- **LC 122 状态机**：每天收盘后只有 `cash`（空仓）与 `hold`（持股）两态，`cash = max(不动, hold + p)`、`hold = max(不动, cash - p)`；开局 `hold = -prices[0]`（建仓必须付钱，否则等于允许做空），终态必须取 `cash`（持股未变现不算利润）。
- 两条路**逐帧等价**：把 DP 展开，`cash` 每次的增量恰是当天的正差 —— 贪心是状态机「每天必做决定」的特例。后续 714（卖支减 fee）、309（加 `rest` 冷冻态）、123（按笔数复制成四变量）、188（k 层、`k ≥ n/2` 退化回 122）改的都只是转移方程。
- 易错点：贪心忘了 `max(0, diff)`（跌也吃会算成负数）；123 四变量必须按 `buy1 → sell1 → buy2 → sell2` 的依赖顺序更新。

## 答案

### LC 121

#### 解法一：双变量一次扫描（时间 O(n) / 空间 O(1)）

```python
def maxProfit(prices):
    min_price, best = prices[0], 0
    for p in prices[1:]:
        best = max(best, p - min_price)   # 先按今天的价格卖一把
        min_price = min(min_price, p)     # 再把今天并入历史最低价
    return best
```

#### Java 版

```java
class Solution {
    // LC 121：一次买卖 —— 与推演表逐帧一致
    public int maxProfit(int[] prices) {
        int minPrice = prices[0], best = 0;
        for (int i = 1; i < prices.length; i++) {
            best = Math.max(best, prices[i] - minPrice); // 先卖一把
            minPrice = Math.min(minPrice, prices[i]);    // 再记最低价
        }
        return best;
    }
}
```

### LC 122

#### 解法一：贪心吃正差（时间 O(n) / 空间 O(1)）

```python
def maxProfit(prices):
    return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))
```

#### 解法二：cash / hold 状态机 DP（时间 O(n) / 空间 O(1)）

```python
def maxProfit(prices):
    cash, hold = 0, -prices[0]
    for p in prices[1:]:
        cash = max(cash, hold + p)
        hold = max(hold, cash - p)   # 先卖后买同日允许，等价于继续持有
    return cash
```

#### Java 版

```java
class Solution {
    // LC 122：无限次 —— cash/hold 状态机（贪心一行也满分，但要会讲等价）
    public int maxProfit(int[] prices) {
        int cash = 0, hold = -prices[0];
        for (int i = 1; i < prices.length; i++) {
            cash = Math.max(cash, hold + prices[i]);
            hold = Math.max(hold, cash - prices[i]); // 用更新后的 cash 亦可：同日先卖后买 = 继续持有
        }
        return cash; // 终态必须空仓
    }
}
```
