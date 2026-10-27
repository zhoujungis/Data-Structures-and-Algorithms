# 【LC 70】爬楼梯：递推人人会写，美团考的是 n=80

**来源**: https://zhoujungis.github.io/article/lc-70-climbing-stairs/
**标签**: 算法、动态规划、LeetCode、面试

## 题目

你正在爬楼梯。需要 `n` 阶你才能到达楼顶，每次可以爬 1 或 2 个台阶，问有多少种不同的方法可以爬到楼顶。

```
输入: n = 3
输出: 3
解释: 1+1+1、1+2、2+1，共三种。
```

说明与约束：

- `1 <= n <= 45`（官方约束）；`n = 0` 约定答案为 1（空方案）；
- `1+1` 与 `2` 视为不同的走法（顺序不同即不同）；
- 追问：`n = 80` 时怎么办 —— 此时 `int` 早已溢出。

## 思路

- **最后一步分类法**：到第 `i` 阶的最后一步只有两种来路 —— 从 `i-1` 迈 1 阶、从 `i-2` 迈 2 阶。这两种分类**互斥且完备**，所以才能直接相加：`dp[i] = dp[i-1] + dp[i-2]`。这是所有计数型 DP 的第一课。
- **初值是语义不是凑数**：`dp[0] = 1`（站在地面不动也是一种走法 —— 空方案），`dp[1] = 1`。把 `dp[0]` 填成 0，`dp[2]` 就错成 1（应为 2），整张表从第三格起全错。
- **无后效性**：第 `i` 阶之后的走法不改变「到第 `i` 阶有几种走法」这个数，所以可以从左往右一路填，填过的格子永不修改。
- **空间可以压到两个变量**：依赖只有两个紧邻前驱，没有 LC 72 那种「对角线被覆盖」的问题。Python 的 `a, b = b, a + b` 天然安全；Java 必须先存 `next = a + b` 再挪指针。
- **易错点：n = 80 先爆的是类型**。`ways(n) = Fib(n+1)` 是乘性增长（每阶约 ×1.618），`int` 撑到 `ways(45) = 1836311903`，第 46 阶就爆；`long` 也只到 `ways(91)`。`n = 80` 的答案是 `37889062373143906` —— 要么 `long`、要么 `BigInteger`、要么题目改成对 `1e9+7` 取模且**每步都取模**。
- **易错点：朴素递归没记忆化**。`T(n) = 2·Fib(n+1) - 1`，`n = 40` 就要 3.3 亿次调用；加一个 memo 就是 `O(n)`。

## 答案

### 解法一：一维 DP 递推（时间 O(n) / 空间 O(n)）

适用场景：面试先按标准形态写出状态与转移，讲清 `dp[0] = 1` 的语义。

```python
def climbStairs(n: int) -> int:
    if n <= 1:
        return 1
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1        # 空方案也是一种走法
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

### 解法二：两个变量滚动（时间 O(n) / 空间 O(1)）

适用场景：本题正解的空间最优写法 —— 只有两个紧邻前驱，直接压到 O(1) 无坑。

```python
def climbStairs(n: int) -> int:
    a, b = 1, 1                # dp[0], dp[1]
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b if n >= 1 else a
```

### Java 版

```java
// n <= 45：int 够用（ways(45) = 1836311903 是 int32 最后一个）
public int climbStairs(int n) {
    int a = 1, b = 1;                 // dp[0], dp[1]
    for (int i = 2; i <= n; i++) {
        int next = a + b;             // 先算 next，再挪 —— 顺序反了就丢 dp[i-1]
        a = b;
        b = next;
    }
    return n >= 1 ? b : a;
}
```

```java
// n <= 91：换 long（ways(91) = 7540113804746346429 是 int64 最后一个）
public long climbStairsLong(int n) {
    long a = 1, b = 1;
    for (int i = 2; i <= n; i++) {
        long next = a + b;
        a = b;
        b = next;
    }
    return n >= 1 ? b : a;
}
```

```java
// 题目若要求对 1e9+7 取模（或 n 特别大直接上 BigInteger）
import java.math.BigInteger;

public BigInteger climbStairsBig(int n) {
    BigInteger a = BigInteger.ONE, b = BigInteger.ONE;
    for (int i = 2; i <= n; i++) {
        BigInteger next = a.add(b);
        a = b;
        b = next;
    }
    return n >= 1 ? b : BigInteger.ONE;
}
```
