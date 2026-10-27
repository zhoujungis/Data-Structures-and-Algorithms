# 【LC 5】最长回文子串：枚举中心 —— 2n-1 个中心，别漏了间隙

**来源**: https://zhoujungis.github.io/article/lc-5-longest-palindromic-substring/
**标签**: 算法、双指针、LeetCode、面试

## 题目

给你一个字符串 `s`，找到 `s` 中最长的回文子串。

```
输入: s = "babad"
输出: "bab"    （"aba" 同样符合题意）

输入: s = "cbbd"
输出: "bb"
```

回文串是正着读和反着读都一样的字符串。题面保证 `s` 至少含一个字符（最短答案就是单字符）。

## 思路

- **别枚举子串**：子串有 `O(n²)` 个、每个验证回文 `O(n)`，暴力共 `O(n³)`。回文关于中心对称、完全由"中心 + 半径"决定，所以应该**枚举中心**。
- **中心是 `2n - 1` 个，不是 `n` 个**：回文有两种长度奇偶 —— `n` 个字符中心（`expand(i, i)`，管奇数回文）+ `n - 1` 个间隙中心（`expand(i, i + 1)`，管偶数回文）。只写 `expand(i, i)` 会漏掉所有偶数回文（`"abba"`、`"cbbd"` 的中心在两个字符之间），这是本题最经典的 bug。
- **扩展是"往外长一格"**：循环里比较 `s[l-1] == s[r+1]`、守卫 `l > 0 && r < n - 1`；写成 `s[l] == s[r]`（收缩式）会让 `[i, i]` 时恒真、指针走出字符串。
- **两个细节**：间隙中心先判 `s[i] == s[i+1]`（不相等连最小的偶数回文都构不成，否则把非回文区间 `[i, i+1]` 当候选更新就错了）；同长度用 `>` 而非 `>=`，先到先得，行为可预测。
- **复杂度**：时间 `O(n²)`、空间 `O(1)`。区间 DP 同样 `O(n²)` 时间但 `O(n²)` 空间；Manacher `O(n)` 但状态多、易错，面试口头提一句即可。

## 答案

### 解法一：中心扩展（时间 O(n²) / 空间 O(1)）

适用场景：面试首选 —— 代码短、空间 `O(1)`，同族的 LC 647 直接复用同一套 2n-1 中心。

```python
def expand(s, l, r):
    # 从 [l, r] 向两边扩到不能再扩，返回边界
    while l > 0 and r < len(s) - 1 and s[l - 1] == s[r + 1]:
        l -= 1
        r += 1
    return l, r


def longestPalindrome(s: str) -> str:
    n = len(s)
    best_l, best_r = 0, 0

    for i in range(n):
        # 字符中心：奇数回文
        l, r = expand(s, i, i)
        if r - l > best_r - best_l:
            best_l, best_r = l, r
        # 间隙中心：偶数回文（i 与 i+1 之间；s[i] != s[i+1] 时天然构不成）
        if i + 1 < n and s[i] == s[i + 1]:
            l, r = expand(s, i, i + 1)
            if r - l > best_r - best_l:
                best_l, best_r = l, r

    return s[best_l:best_r + 1]
```

### 解法二：区间 DP（时间 O(n²) / 空间 O(n²)）

适用场景：只作口头对照 —— 视角是"大回文由小回文长出来"，但空间比中心扩展多一个量级。

```python
def longestPalindrome(s: str) -> str:
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    best_l, best_r = 0, 0
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            dp[i][j] = s[i] == s[j] and (j - i < 2 or dp[i + 1][j - 1])
            if dp[i][j] and j - i > best_r - best_l:
                best_l, best_r = i, j
    return s[best_l:best_r + 1]
```

### Java 版

```java
public String longestPalindrome(String s) {
    int n = s.length(), bestL = 0, bestR = 0;
    for (int i = 0; i < n; i++) {
        int[] odd = expand(s, i, i);            // 字符中心
        if (odd[1] - odd[0] > bestR - bestL) { bestL = odd[0]; bestR = odd[1]; }
        if (i + 1 < n && s.charAt(i) == s.charAt(i + 1)) {
            int[] even = expand(s, i, i + 1);   // 间隙中心
            if (even[1] - even[0] > bestR - bestL) { bestL = even[0]; bestR = even[1]; }
        }
    }
    return s.substring(bestL, bestR + 1);
}

private int[] expand(String s, int l, int r) {
    while (l > 0 && r < s.length() - 1 && s.charAt(l - 1) == s.charAt(r + 1)) {
        l--; r++;
    }
    return new int[]{l, r};
}
```
