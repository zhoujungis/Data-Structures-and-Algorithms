# 【LC 300】最长递增子序列：加锚，再压到 O(n log n)

**来源**: https://zhoujungis.github.io/article/lc-300-longest-increasing-subsequence/
**标签**: 算法、动态规划、LeetCode、面试

## 题目

给你一个整数数组 `nums`，找到其中**最长严格递增子序列**的长度。

```
输入: nums = [10,9,2,5,3,7,101,18]
输出: 4
解释: 最长递增子序列是 [2,3,7,101]（或 [2,3,7,18]），长度 4。
```

**进阶**：你能把时间复杂度降到 `O(n log n)` 吗？

说明与约束：

- 子序列可以跳着挑，只要保持原来的先后顺序：例如先挑 `2`，跳过 `5` 再拿 `3`，是合法的；
- 递增是**严格**递增，相等元素不能相接（如 `[7,7,7]` 的答案是 1）；
- 元素可以为负数；空数组返回 0；单元素返回 1；
- 最长的那条链不要求以最后一个元素结尾。

## 思路

- **状态要加锚**：`dp[i]` 定义为「**以 `nums[i]` 结尾**的最长严格递增子序列长度」。一条以 `nums[i]` 结尾的递增序列，砍掉末尾仍是一条以某个 `nums[j]`（`j < i`）结尾的递增序列 —— 子问题形状不变，转移写得出来。
- **为什么不能定义成「前 `i` 个数里的最长」**：那样定义出的"最长"未必以 `nums[i]` 结尾，接 `nums[i+1]` 时不知道末尾是谁，转移无法写出。递增性只在相邻两个元素之间起作用，所以锚必须落在"以谁结尾"。
- **转移**：`dp[i] = 1 + max(dp[j])`（`j < i` 且 `nums[j] < nums[i]`），找不到可接的前驱就取 1（自己单独成串）。内层必须把 `j` 从 0 到 `i-1` 全部回看一遍，不能一找到能接的就停。
- **答案取 `max(dp)`，不是 `dp[n-1]`**：最长链未必以最后一个元素结尾。反例 `[1,2,3,0]` 答案是 3 而 `dp[3] = 1`；官方样例恰好让 `dp[n-1]` 等于答案，用它自测永远发现不了这个 bug。
- **进阶换锚**：`tails[len]` = 所有长度为 `len+1` 的递增子序列中末尾元素的最小值。`tails` 严格递增（否则砍掉尾巴可得矛盾），因此可二分：每来一个 `x` 用 `bisect_left` 找第一个 `>= x` 的位置，存在则替换（同长度末尾更小，对后续更有利），越界则追加（长度加一，唯一能让答案变大的动作）。
- **易错点**：`dp` 初值必须是 1；严格递增用 `bisect_left`，最长**非减**要换 `bisect_right`；`tails` 不是 LIS 本身（内容会被覆盖，只有长度可信），要具体序列得回 dp 版用 `parent` 回溯；手写二分需 `hi = len(tails)`（开区间）+ 向下取整 `mid`，否则漏掉"追加到表尾"或死循环。

## 答案

### 解法一：动态规划（时间 O(n²) / 空间 O(n)）

适用场景：面试先讲透状态定义；需要回溯出具体的那条子序列时必须用这一版。

```python
def lengthOfLIS(nums):
    n = len(nums)
    if n == 0:
        return 0
    dp = [1] * n          # dp[i]: 以 nums[i] 结尾的最长严格递增子序列长度
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
    return max(dp)
```

### 解法二：贪心 + 二分（tails 登记表）（时间 O(n log n) / 空间 O(n)）

适用场景：只问长度、要求 `O(n log n)` 时的正解；面试可先用 `bisect_left`，再按需手写 `lower_bound` 验证理解。

```python
from bisect import bisect_left

def lengthOfLIS(nums):
    tails = []                      # tails[len]: 长度为 len+1 的子序列的最小末尾
    for x in nums:
        pos = bisect_left(tails, x) # 第一个 >= x 的位置
        if pos == len(tails):
            tails.append(x)         # 比所有末尾都大：长度加一
        else:
            tails[pos] = x          # 同长度下末尾更小
    return len(tails)
```

不依赖库函数时的手写二分版本（同一算法）：

```python
def lengthOfLIS(nums):
    tails = []
    for x in nums:
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < x:      # 往右收：mid 不可能是答案
                lo = mid + 1
            else:                   # 往左收：mid 可能是答案，hi 停在 mid
                hi = mid
        if lo == len(tails):
            tails.append(x)
        else:
            tails[lo] = x
    return len(tails)
```

### Java 版

```java
public int lengthOfLIS(int[] nums) {
    int n = nums.length;
    int[] dp = new int[n];
    int best = 0;
    for (int i = 0; i < n; i++) {
        dp[i] = 1;
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i] && dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
            }
        }
        best = Math.max(best, dp[i]);
    }
    return best;
}
```

```java
public int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
    int size = 0;                       // 当前长度
    for (int x : nums) {
        int lo = 0, hi = size;          // 在 [0, size) 里找第一个 >= x 的位置
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (tails[mid] < x) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        tails[lo] = x;
        if (lo == size) {
            size++;                     // 追加：长度加一
        }
    }
    return size;
}
```
