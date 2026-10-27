# 【LC 53】最大子数组和：带上前面，是赚还是亏

**来源**: https://zhoujungis.github.io/article/lc-53-maximum-subarray/
**标签**: 算法、动态规划、LeetCode、面试
**难度**: Medium

## 题目

给你一个整数数组 `nums`，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

```
输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6。

输入：nums = [1]
输出：1

输入：nums = [5,4,-1,7,8]
输出：23
```

## 思路

- **DP 的定义是关键**：`cur` = 以当前位置**结尾**的最大子数组和。这个"结尾"让候选从 `O(n²)` 种子数组坍缩到每个位置 2 种 —— 接上前面的，或从自己重新开始。
- **转移**：`cur = max(x, cur + x)`，整句只在问"带上前面那段，是赚了还是亏了"。拆开看：`cur >= 0` 就带上，`cur < 0` 就是负资产、扔掉重起 —— 判据在 `cur` 身上，不在 `x` 身上。
- **为什么敢扔**：前面那段为负时，任何包含它的候选都比"只从 `i` 开始"的少一段负数，所以"以 `i` 结尾"的最优一定不含负段；而更早的最优已经记在 `best` 里（任何子数组都必然以某个位置结尾），两头都照顾到，不会漏解。
- **易错点 1**：`cur`、`best` 必须从 `nums[0]` 起步而不是 0 —— 子数组至少含一个元素，全负数组（`[-3,-1,-2]` 答 `-1`）从 0 起步会错答成 0。
- **易错点 2**：重置判据严格写 `cur < 0`，写 `cur <= 0` 虽然和一样、但会把起点白白提前，返回子数组时带上无用的零前缀。
- **分治的四个量**：`i_sum`（区间和）、`l_sum`（最大前缀）、`r_sum`（最大后缀）、`m_sum`（区间内最大子数组和）；合并 `O(1)`、递归树 `2n-1` 个节点 → 也是 `O(n)`（不是常说的 `O(n log n)`）。它的价值不在速度，而在这套合并规则正是线段树维护的东西。

## 答案

### 解法一：Kadane / DP（时间 O(n) / 空间 O(1)）

适用场景：本题正解，`O(n)` 已是理论下界；下面这版顺带返回子数组本身（位置信息只存在于 `if cur < 0` 的写法里）。

```python
def maxSubArray(nums):
    cur = best = nums[0]          # 子数组至少含一个元素，从 nums[0] 起步
    start = bestStart = bestEnd = 0

    for i in range(1, len(nums)):
        if cur < 0:               # 前面那段是负资产 → 扔掉，从 i 重新开始
            cur = nums[i]
            start = i
        else:                     # 前面那段是正的 → 带上
            cur = cur + nums[i]
        if cur > best:            # 刷新全局最优时，把当前区间记下来
            best = cur
            bestStart, bestEnd = start, i

    return best, nums[bestStart:bestEnd + 1]
```

### 解法二：分治（四元组信息合并）（时间 O(n) / 空间 O(log n)）

适用场景：题目改成"支持单点修改、随时询问区间最大子数组和"时的起点 —— 这套四元组正是线段树的维护量。

```python
def maxSubArrayDivide(nums):
    def get(l, r):
        if l == r:
            s = nums[l]
            return (s, s, s, s)          # (l_sum, r_sum, i_sum, m_sum)
        mid = (l + r) // 2
        L = get(l, mid)
        R = get(mid + 1, r)
        i_sum = L[2] + R[2]
        l_sum = max(L[0], L[2] + R[0])
        r_sum = max(R[1], R[2] + L[1])
        m_sum = max(L[3], R[3], L[1] + R[0])
        return (l_sum, r_sum, i_sum, m_sum)

    return get(0, len(nums) - 1)[3]
```

### Java 版

```java
class Solution {
    public int maxSubArray(int[] nums) {
        int cur = nums[0], best = nums[0];
        for (int i = 1; i < nums.length; i++) {
            cur = Math.max(nums[i], cur + nums[i]);
            best = Math.max(best, cur);
        }
        return best;
    }
}
```
