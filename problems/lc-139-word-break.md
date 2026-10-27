# 【LC 139】单词拆分：布尔 dp 与切分回溯

**来源**: https://zhoujungis.github.io/article/lc-139-word-break/
**标签**: 算法、动态规划、LeetCode、面试

## 题目

给你一个字符串 `s` 和一个字符串列表 `wordDict` 作为字典。请你判断是否可以利用字典中出现的单词拼接出 `s`。

```
输入: s = "leetcode", wordDict = ["leet", "code"]
输出: true   （"leetcode" = "leet" + "code"）

输入: s = "applepenapple", wordDict = ["apple", "pen"]
输出: true   （"apple" + "pen" + "apple"，"apple" 用了两次）

输入: s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
输出: false
```

约束与前提：

- 字典中的**单词可以重复使用**（完全背包语义），不限制每个词的使用次数；
- 拼接必须覆盖 `s` 的全部字符、连续且不重叠；
- 匹配是精确匹配，区分大小写；字典中可能出现重复词或比 `s` 更长的词。

## 思路

- 不问「切成哪些词」，而问「`s` 的前 `i` 个字符能不能拼出来」：`dp[i]` = 前 `i` 个字符能否由字典拼出，转移为 `dp[i] = OR over j<i ( dp[j] && s[j:i] ∈ dict )`，把 `s[j:i]` 当作「最后一个词」去试。
- `dp[0] = true` 是唯一的底座：空串天然拼得出。写成 `false` 会让「整串就是一个词」（`j = 0`）直接判死；全部初始化成 `true` 则函数永远返回 `true`。
- `i` 必须**正序**推进，这样 `dp[i]` 依赖的、下标更小的 `dp[j]` 已经算好；正序也正好对应「同一个词可以重复使用」。
- 两项不改语义的剪枝：字典转 `set` 做哈希查找（取代线性扫描）；切分点 `j` 只枚举 `maxLen` 窗口内（`j >= i - maxLen`，最后一个词最长就是 `maxLen`），把 `O(n²)` 压到 `O(n × maxLen)`。
- 命中即 `break`；易错点是切片左闭右开（`s[j:i]` 正是「从 `j` 起、长度 `i-j` 的一段」），以及「前缀可达 ≠ 整体可达」（如 `"catsandog"`）。

## 答案

### 解法一：前缀布尔 dp（时间 O(n²)，加 maxLen 窗口可降到 O(n × maxLen) / 空间 O(n)）

```python
def wordBreak(s, wordDict):
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]
```

### Java 版

带 `maxLen` 窗口剪枝的标准 DP（时间 O(n × maxLen) / 空间 O(n)）：

```java
class Solution {
    // LC 139：标准 DP —— 与推演表逐帧一致
    public boolean wordBreak(String s, List<String> wordDict) {
        Set<String> dict = new HashSet<>(wordDict);   // 哈希查找，别在 list 里逐个比
        int n = s.length();
        int maxLen = 0;
        for (String w : wordDict) maxLen = Math.max(maxLen, w.length());
        boolean[] dp = new boolean[n + 1];
        dp[0] = true;                                 // 唯一的底座：空串拼得出
        for (int i = 1; i <= n; i++) {
            int lo = Math.max(0, i - maxLen);         // 最后一词最长 maxLen
            for (int j = i - 1; j >= lo; j--) {
                if (dp[j] && dict.contains(s.substring(j, i))) {
                    dp[i] = true;
                    break;                            // 命中即短路
                }
            }
        }
        return dp[n];
    }
}
```
