# 【LC 1928】规定时间内到达终点的最小花费：分层图上的 dp

**来源**: https://zhoujungis.github.io/article/lc-1928-min-cost/
**标签**: 算法、动态规划、LeetCode、面试

## 题目

**LC 1928 规定时间内到达终点的最小花费**：有 `n` 个城市（编号 `0 .. n-1`）。`edges[i] = [x, y, time]` 是一条**无向边**，边上只有**时间**、**没有花费**。另有 `passingFees[v]`：**每经过一座城市付一次**该城市的通行费 —— **起点与终点也要付**。求从 `0` 走到 `n-1`，在总时间 **≤ maxTime** 的前提下**最少**要付多少通行费；走不到返回 `-1`。

```
输入: edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]]
      passingFees = [5,1,2,20,20,3]

maxTime = 30 → 11   （0 → 1 → 2 → 5：耗时 10+10+10 = 30，费 5+1+2+3 = 11）
maxTime = 29 → 48   （0 → 3 → 4 → 5：耗时 1+10+15 = 26，费 5+20+20+3 = 48）
maxTime = 25 → -1   （最快的一条路也要 26 分钟，25 分钟内根本到不了）
```

## 思路

- 一维 `dp[v]`（到城市 `v` 的最少花费）是错的：它丢掉了「第几时刻到达」，会把一条**超时的便宜路**当成答案（示例里 `dp[5] = 11` 那条要 30 分钟，`maxTime = 29` 时根本不允许）。
- 修法只有一句：**把时间并进状态**——不问「到某城最少花多少」，而问「在某个确定的时刻到达某城，最少花多少」。
- 定义 `dp[t][v]` = 恰好在时刻 `t` 到达城市 `v` 的最小通行费；底座 `dp[0][0] = passingFees[0]`（起点也要付自己的费），其余为 `∞`；按 `t` 正序松弛每条无向边的两个方向：`dp[t+et][u] = min(dp[t+et][u], dp[t][v] + passingFees[u])`。
- 三处剪枝/检查决定正确性：只从「已到达」（`dp[t][v] < INF`）的格子出发；`arr = t + et > maxTime` 直接丢弃（时间不回头）；无向边两个方向都要松弛。
- 答案不是 `dp[maxTime][n-1]`，而是 `min over t ≤ maxTime of dp[t][n-1]`——到达终点不必用满时间，且「晚到」可能更贵（示例中 `dp[5][5] = 71 > dp[3][5] = 48`）。
- 本质是分层图最短路：点 = `(t, v)`，边 = `(x, y, time)`，`maxTime` 是层数上限；同一台机器换成 `(花费, 已用时间, 城市)` 上跑小顶堆 Dijkstra 也等价（第一次弹出终点即答案）。

## 答案

### 解法一：分层图 DP（时间进状态，按时刻正序松弛）（时间 O(maxTime × E) / 空间 O(maxTime × n)）

```python
def minCost(maxTime, edges, passingFees):
    n = len(passingFees)
    INF = float("inf")
    dp = [[INF] * n for _ in range(maxTime + 1)]
    dp[0][0] = passingFees[0]                  # 起点也要付自己的费
    for t in range(maxTime + 1):
        for x, y, et in edges:                 # 无向边，两个方向都要试
            arr = t + et
            if arr > maxTime:                  # 迟到就是迟到，剪掉
                continue
            if dp[t][x] < INF:
                dp[arr][y] = min(dp[arr][y], dp[t][x] + passingFees[y])
            if dp[t][y] < INF:
                dp[arr][x] = min(dp[arr][x], dp[t][y] + passingFees[x])
    ans = min(dp[t][n - 1] for t in range(maxTime + 1))
    return -1 if ans == INF else ans
```

### Java 版

```java
class Solution {
    // LC 1928 标准解：分层图 DP —— 与推演表逐帧一致
    public int minCost(int maxTime, int[][] edges, int[] passingFees) {
        int n = passingFees.length;
        final int INF = Integer.MAX_VALUE / 2;       // 别用 MAX_VALUE，免得加法溢出
        int[][] dp = new int[maxTime + 1][n];
        for (int[] row : dp) Arrays.fill(row, INF);
        dp[0][0] = passingFees[0];                   // 底座：起点也要付自己的费
        for (int t = 0; t <= maxTime; t++) {
            for (int[] e : edges) {
                int x = e[0], y = e[1], et = e[2];
                int arr = t + et;
                if (arr > maxTime) continue;         // 迟到就是迟到，剪掉
                if (dp[t][x] < INF) dp[arr][y] = Math.min(dp[arr][y], dp[t][x] + passingFees[y]);
                if (dp[t][y] < INF) dp[arr][x] = Math.min(dp[arr][x], dp[t][y] + passingFees[x]);
            }
        }
        int ans = INF;
        for (int t = 0; t <= maxTime; t++) ans = Math.min(ans, dp[t][n - 1]);
        return ans >= INF ? -1 : ans;                 // 时间窗内到不了 → -1
    }
}
```
