# 【LC 322】零钱兑换：正序完全背包，逆序变 -1

**来源**: https://zhoujungis.github.io/article/lc-322-coin-change/
**标签**: 算法、动态规划、LeetCode、面试

## 题目

给你一个整数数组 `coins` 表示不同面额的硬币，以及一个整数 `amount` 表示总金额。计算并返回可以凑成总金额所需的**最少硬币个数**。如果没有任何一种硬币组合能组成总金额，返回 `-1`。每种硬币的数量是**无限的**。

```
输入: coins = [1, 2, 5], amount = 11
输出: 3   （11 = 5 + 5 + 1）

输入: coins = [2], amount = 3
输出: -1  （2 怎么翻倍都凑不出奇数）
```

说明与约束：

- 硬币面额为正整数，每枚硬币可以重复使用任意多次（完全背包）；
- `amount = 0` 时返回 `0`（一枚都不用）；
- 面额之间不保证整除，贪心先拿大面额会错（`[1,3,4]` 凑 `6` 贪心得 3 枚，正解 `3+3` 是 2 枚）；
- 凑不出时返回 `-1`，而不是某个大数或 `∞`。

## 思路

- **不问"用哪些硬币"，而问"凑出金额 `x` 最少要几枚"**：`dp[x]` = 凑出金额 `x` 的最少硬币枚数，`dp[0] = 0`，其余初始化成 `∞`（先假定凑不出，凑得出再往下降）。
- **转移一行写完**：`dp[x] = min over 每种硬币 c (dp[x-c] + 1)`，`x - c >= 0`。语义是把硬币 `c` 当作"最后一枚"去试，剩下 `x-c` 的最优解已知，补上这枚就是一条候选路径。
- **`∞` 不能写成 `0`**：用 0 初始化等于宣布"任何金额都凑得出、而且一枚就够"，`min` 会把答案大面积压成 1。Java 里不要用 `Integer.MAX_VALUE`，`MAX_VALUE + 1` 会溢出成负数，用 `amount + 1` 当哨兵。
- **内层金额的正序就是"硬币可无限复用"的开关**：正序时 `dp[x-c]`（下标更小）这一轮已更新过，可能本身就含硬币 `c`，于是允许"再叠一枚"；逆序读到的是上一轮旧值，等价于每枚只能用一次（退化成 0-1 背包），`[1,2,5]` 凑 `11` 会返回 `-1`。一句话记：**正序读"同一轮已经写好的自己"，逆序读"上一轮留下的自己"**。
- **易错点**：返回 `dp[amount]` 而不是 `-1`；忘记 `amount = 0` 短路；要用 322 的 min / 518 的 `+=` 与循环嵌套顺序时别混用（求方案数必须外层硬币、内层金额正序，求排列数是 LC 377 的外层金额、内层硬币）；要还原具体组合得另配 `chosen[x]` 前驱表。

## 答案

### 解法一：完全背包一维 DP（时间 O(amount × k) / 空间 O(amount)）

适用场景：本题标准解 —— 求「无限件物品装满容量、花费最少」的模板，`k` 为硬币种数。

```python
def coinChange(coins, amount):
    dp = [0] + [float('inf')] * amount
    for x in range(1, amount + 1):
        for c in coins:
            if x >= c:
                dp[x] = min(dp[x], dp[x - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

### Java 版

```java
class Solution {
    // LC 322：完全背包求最小 —— 与推演表逐帧一致
    public int coinChange(int[] coins, int amount) {
        int INF = amount + 1;              // 哨兵：比"全用 1 元"还大一，且 +1 不会溢出
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, INF);
        dp[0] = 0;
        for (int x = 1; x <= amount; x++) {
            for (int c : coins) {
                if (x >= c && dp[x - c] + 1 < dp[x]) {
                    dp[x] = dp[x - c] + 1; // 用更新前的 dp[x-c]；正序保证它可能已含 c
                }
            }
        }
        return dp[amount] == INF ? -1 : dp[amount];
    }
}
```
