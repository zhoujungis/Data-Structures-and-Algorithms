# 【LC 3】无重复字符的最长子串：窗口里才算重复

**来源**: https://zhoujungis.github.io/article/lc-3-longest-substring-without-repeating-characters/
**标签**: 算法、滑动窗口、字符串、LeetCode、面试
**难度**: 中等

## 题目

给定一个字符串 `s`，请你找出其中**不含有重复字符的最长子串**的长度。

```
输入：s = "abcabcbb"
输出：3
解释：最长无重复子串是 "abc"，长度为 3。

输入：s = "bbbbb"
输出：1
解释：最长无重复子串是 "b"，长度为 1。

输入：s = "pwwkew"
输出：3
解释：最长无重复子串是 "wke"，长度为 3。注意答案必须是子串（连续的一段），"pwke" 是子序列，不是子串。
```

**子串 vs 子序列**：

| | 定义 | 例子（`"pwwkew"`） |
|---|---|---|
| **子串** | 原串中**连续**的一段 | `"wke"` ✓ |
| 子序列 | 保持相对顺序、允许跳过字符 | `"pwke"` —— 它是子序列，**不是子串** |

## 思路

- 枚举所有子串是 `O(n³)`，且完全浪费：`s[i..j]` 有重复时，`s[i..j+1]…` 全都有重复。改成维护一个**始终合法**的窗口 `[left, right]` 一路右推。
- 两条规则：`right` 每轮右移一格把字符吃进窗口；吃进来的字符若**在窗口内**已存在，`left` 跳到「旧位置 + 1」把它挤出窗口。两指针都只右移，共走不超过 `2n` 步。
- 表里存**字符最后出现的下标**（不是布尔/集合）：这样 `left` 能一步跳到位，没有内层循环，常数比 `set` 版小。
- 本题唯一的真难点：判据是 `last[ch] >= left`（「上次出现的位置**还在窗口里**」），不是 `if ch in last`（「这个字符出现过」）。少了 `>= left`，`left` 会**倒退**，破掉「窗口内无重复」的不变量。
- 反例：`"abba"` 走到最后一个 `a` 时 `last['a'] = 0 < left = 2`，`left` 该原地不动；漏判据会算成 `left = 1`，窗口变 `"bba"`，答案从 2 虚高成 3。官方三个样例都抓不到这个错。
- 其它易错点：数组版初始值必须是 `-1`（`0` 是合法下标，"没出现过"会与"出现在 0"混淆）；`last[ch] = right` 必须每轮都更新；`ans` 要在收缩之后再算。

## 答案

### 解法一：哈希表存最后下标，左指针一步跳（时间 O(n) / 空间 O(min(n, 字符集))）

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}                       # 字符 -> 它最后出现的下标
        left = 0
        ans = 0
        for right, ch in enumerate(s):
            # 关键条件：出现过，并且那个位置还在窗口里
            if ch in last and last[ch] >= left:
                left = last[ch] + 1     # 把它挤出窗口
            last[ch] = right            # 记录/更新它的最后位置
            ans = max(ans, right - left + 1)
        return ans
```

### 解法二：`set` + `while` 逐步收缩（时间 O(n) / 空间 O(min(n, 字符集))）

更好理解，紧张时不易写错；`while` 只会让 `left` 增大，天然不倒退，代价是左指针要一格格挪、扫过更多中间状态，常数更大。

```python
def lengthOfLongestSubstring(s):
    win = set()
    left = 0
    ans = 0
    for right, ch in enumerate(s):
        while ch in win:            # 一步一步挪，边挪边删
            win.remove(s[left])
            left += 1
        win.add(ch)
        ans = max(ans, right - left + 1)
    return ans
```

### Java 版

```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        int[] last = new int[128];
        java.util.Arrays.fill(last, -1);        // ⚠️ -1 不是 0
        int left = 0, ans = 0;
        for (int right = 0; right < s.length(); right++) {
            char ch = s.charAt(right);
            if (last[ch] >= left) {
                left = last[ch] + 1;            // 一步跳到重复字符的下一位
            }
            last[ch] = right;
            ans = Math.max(ans, right - left + 1);
        }
        return ans;
    }
}
```
