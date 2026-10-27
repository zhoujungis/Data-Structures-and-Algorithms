# 【LC 72】编辑距离：前缀对前缀，与滚动数组

**来源**: https://zhoujungis.github.io/article/lc-72-edit-distance/
**标签**: 算法、动态规划、LeetCode、面试

## 题目

给你两个单词 `word1` 和 `word2`，返回将 `word1` 转换成 `word2` 所使用的**最少操作数**，可以对一个单词进行如下三种操作：插入一个字符、删除一个字符、替换一个字符。

```
输入: word1 = "horse", word2 = "ros"
输出: 3
解释: horse -> rorse (替换 h 为 r)
      rorse -> rose  (删除 r)
      rose  -> ros   (删除 e)
```

说明与约束：

- 三种操作（插入 / 删除 / 替换）代价都是 1；
- 任一串为空时，答案是另一个串的长度；
- 编辑距离对称：`dist(a, b) = dist(b, a)`；
- 求的是**最少步数**，不要求输出具体操作序列。

## 思路

- **一次下两个锚**：`dp[i][j]` = 把 `word1` 的前 `i` 个字符变成 `word2` 的前 `j` 个字符的最少操作数。必须是「前缀对前缀」而不是「以 `i` 结尾」—— 编辑操作会在任意位置增删，只有「两个串各自还剩多长」能完整描述现场（这是子序列型与双串型的分岔点）。
- **三种操作恰对应三个邻居**：替换 → 对角 `dp[i-1][j-1] + 1`；删除 `a[i-1]` → 上方 `dp[i-1][j] + 1`；插入 `b[j-1]` → 左方 `dp[i][j-1] + 1`。取三者最小；`a[i-1] == b[j-1]` 时免费收尾，直接抄对角。
- **边界是语义不是占位符**：`dp[0][j] = j`（空串长成 `b` 的前 `j` 个字符只能一个个插）、`dp[i][0] = i`（缩成空串只能一个个删）。填 0 的代码在官方样例上输出 2。
- **滚动数组只丢一格**：`buf[j]`（写前）是上方、`buf[j-1]`（刚写完）是左方，**只有对角 `dp[i-1][j-1]` 被上一轮覆盖了**，用一个标量 `prev` 接住即可。每行开头先 `prev = buf[0]` 再 `buf[0] = i`，每格先 `tmp = buf[j]` 再写 —— 覆盖之前的那一刻是拿到旧值的唯一机会。
- **易错点：内层不能倒着扫**。`buf[j-1]` 要的是本行刚写的值（0/1 背包的肌肉记忆在这里害人）。官方样例 `horse -> ros` 倒扫仍得 3（最小值恰好落在唯一没错位的「上方」），但 `kitten -> sitting` 会得 6、`abc -> abc` 会得 2。
- **对称性**：插入与删除的标注互换不影响数值（`min` 覆盖同一个集合 `{对角, 上方, 左方}`），但会毁掉操作序列的重建；也正因对称，可让短串当列，空间 `O(min(m, n))`。

## 答案

### 解法一：二维 DP（时间 O(m·n) / 空间 O(m·n)）

适用场景：面试先写这一版讲清两个锚与三条转移；需要输出操作序列、回溯时只能用它。

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    a, b = list(word1), list(word2)
    # dp[i][j]：a 的前 i 个字符 变成 b 的前 j 个字符 的最少操作数
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for j in range(n + 1):
        dp[0][j] = j          # 空串长成 b 的前 j 个字符：插入 j 次
    for i in range(1, m + 1):
        dp[i][0] = i          # a 的前 i 个字符缩成空串：删除 i 次
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]      # 相同：这一对免费
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],   # 替换：把 a[i-1] 改成 b[j-1]
                    dp[i - 1][j],       # 删除：删掉 a[i-1]
                    dp[i][j - 1],       # 插入：补一个 b[j-1]
                )
    return dp[m][n]
```

### 解法二：滚动数组（时间 O(m·n) / 空间 O(n)，短串当列则 O(min(m, n))）

适用场景：被追问「空间能压到 O(n) 吗」时的正解 —— 只回答最少步数，不负责重建方案。

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    a, b = list(word1), list(word2)
    buf = list(range(n + 1))              # 第 0 行直接当初值
    for i in range(1, m + 1):
        prev = buf[0]                     # dp[i-1][0]：先备份，再覆盖
        buf[0] = i
        for j in range(1, n + 1):
            tmp = buf[j]                  # dp[i-1][j]：写完就没了，先存下来
            if a[i - 1] == b[j - 1]:
                buf[j] = prev             # 对角，免费收尾
            else:
                buf[j] = 1 + min(prev, buf[j], buf[j - 1])
            prev = tmp                    # 下一格的对角
    return buf[n]
```

### Java 版

```java
public int minDistance(String word1, String word2) {
    char[] a = word1.toCharArray();
    char[] b = word2.toCharArray();
    int m = a.length, n = b.length;
    int[] buf = new int[n + 1];
    for (int j = 0; j <= n; j++) buf[j] = j;      // 第 0 行
    for (int i = 1; i <= m; i++) {
        int prev = buf[0];        // dp[i-1][0]，先备份再覆盖
        buf[0] = i;
        for (int j = 1; j <= n; j++) {
            int tmp = buf[j];     // dp[i-1][j]
            if (a[i - 1] == b[j - 1]) {
                buf[j] = prev;    // 相同：免费收尾
            } else {
                buf[j] = 1 + Math.min(prev, Math.min(buf[j], buf[j - 1]));
            }
            prev = tmp;
        }
    }
    return buf[n];
}
```
