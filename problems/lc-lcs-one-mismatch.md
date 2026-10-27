# 【动态规划】允许一个错的最长公共连续子串：额度只能从干净的 f 接

**来源**: https://zhoujungis.github.io/article/lc-lcs-one-mismatch/
**标签**: 算法、动态规划、面试

## 题目

给定两个字符串，求**最长公共连续子序列**的长度，允许其中出现**最多一处"错误"**——也就是两个子串按位对齐时，至多有一个位置的字符不相等，这一整段仍然算「公共的、连续的」。

```
s = "abcdef", t = "abcdxf"
只有 e / x 这一处不同，所以 6 个字符整体就算一段带 1 处错的公共连续子串
输出: 6
```

约束与说明：

- 「连续」是**子串**（substring），不能跳格，两个串只能沿对角线对齐；允许跳格的「子序列（subsequence）」是另一道题，转移里会出现左、上两格。
- 答应「至多」一处错误，包含 0 处：完全相同的串也合法，`abc` / `abc` 应返回 3。
- 两个毫无关系的字符（如 `a` / `b`）答案是 1，不是 0。
- 答案取全表最大值，子串可以结束在任何一格；空串返回 0。

## 思路

- 拆成两个状态才够用：`f[i][j]` = 以 `s[i-1]`、`t[j-1]` 结尾且**全程字符相等**的最长公共子串长度；`g[i][j]` = 同一结尾但**至多一处不等**的长度。
- 字符相等时两个状态都沿左上角 +1（不消耗额度）：`f[i][j] = f[i-1][j-1] + 1`、`g[i][j] = g[i-1][j-1] + 1`。
- 字符不等时是整题分水岭：`f[i][j] = 0`，而 `g[i][j] = max(f[i-1][j-1] + 1, 1)` —— **额度只能从干净的 `f` 接**。若写成 `g[i-1][j-1] + 1`，同一个字符会被反复消耗配额，答案一路虚涨（`ab` / `ba` 正解 1，错法 2）。
- `max(..., 1)` 保证「光这一格不相等」也算长度 1 的合法答案，同时不能把「至多」误读成「恰好用掉一次」，否则 `abc` / `abc` 会返回 0。
- 答案取全表最大的 `g`（不是 `g[n][m]`）；`g` 只依赖左上角，可把空间压到 `O(min(n, m))`。
- 滚动数组的唯一陷阱：`f_diag = f_prev[j-1]` 必须在被覆盖之前取出，否则静默偏小、不崩不越界。

## 答案

### 解法一：二维双状态 DP（时间 O(n × m) / 空间 O(n × m)）

最直白的写法，适合需要回溯出具体子串、或长度规模在 1000 左右的场景。

```python
def lcs1(s: str, t: str) -> int:
    n, m = len(s), len(t)
    f = [[0] * (m + 1) for _ in range(n + 1)]
    g = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                f[i][j] = f[i - 1][j - 1] + 1
                g[i][j] = g[i - 1][j - 1] + 1
            else:
                f[i][j] = 0
                g[i][j] = max(f[i - 1][j - 1] + 1, 1)
    return max(max(row) for row in g) if n and m else 0
```

### 解法二：滚动数组（时间 O(n × m) / 空间 O(min(n, m))）

只保留上一行，滚动维度取短边；适合长串、内存受限或只需要长度不需要回溯的场景。

```python
def lcs1_rolling(s: str, t: str) -> int:
    if len(s) < len(t):
        s, t = t, s                      # 让滚动维度取短边
    f_prev = [0] * (len(t) + 1)
    g_prev = [0] * (len(t) + 1)
    best = 0
    for i in range(1, len(s) + 1):
        f_cur = [0] * (len(t) + 1)
        g_cur = [0] * (len(t) + 1)
        for j in range(1, len(t) + 1):
            f_diag = f_prev[j - 1]       # 左上角：必须在覆盖 prev 之前存下
            g_diag = g_prev[j - 1]
            if s[i - 1] == t[j - 1]:
                f_cur[j] = f_diag + 1
                g_cur[j] = g_diag + 1
            else:
                f_cur[j] = 0
                g_cur[j] = max(f_diag + 1, 1)
            best = max(best, g_cur[j])
        f_prev, g_prev = f_cur, g_cur
    return best
```
