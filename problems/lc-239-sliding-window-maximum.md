# 【LC 239】滑动窗口最大值：单调队列只留候选

**来源**: https://zhoujungis.github.io/article/lc-239-sliding-window-maximum/
**标签**: 算法、栈、LeetCode、面试

## 题目

给你一个整数数组 `nums` 和滑动窗口大小 `k`。窗口从数组最左侧移动到最右侧，每次向右移动一位，返回每个窗口中的最大值。要求**线性时间**。

```
输入: nums = [1,3,-1,-3,5,3,6,7], k = 3
输出: [3,3,5,5,6,7]

窗口位置                  最大值
[1  3  -1] -3  5  3  6  7   → 3
 1 [3  -1  -3] 5  3  6  7   → 3
 1  3 [-1  -3  5] 3  6  7   → 5
 1  3  -1 [-3  5  3] 6  7   → 5
 1  3  -1  -3 [5  3  6] 7   → 6
 1  3  -1  -3  5 [3  6  7]  → 7
```

约束：`1 ≤ k ≤ nums.length`，返回数组长度为 `nums.length - k + 1`；`k > nums.length` 或空数组时无有效窗口，返回空。

## 思路

- 暴力每窗扫一遍是 `O(n·k)`，`k = n/2` 时退化为平方；要线性，就得避免重复比较。
- 核心是**支配**关系：若窗口里右边来了一个不小于旧元素 `x` 的新元素，旧元素既更小又更早离开窗口（新元素出窗时它早出窗了），永远轮不到它当最大值 → 可以**永久淘汰**。
- 于是队列里只留「还有机会当最大值」的候选，按值**严格递减**排列，队首恒为当前窗口最大值；淘汰判据用 `<=` 而非 `<`，相等的旧元素留着不增加信息还占位（全相等输入会堆出 `k` 个）。
- 两个**互相独立**的维护动作：队首看**下标**（`dq[0] < i - k + 1` 就出窗，用 `if` 够），队尾看**值**（`while nums[dq[-1]] <= x` 就弹出，必须 `while`）。
- 易错点：队列必须**存下标不存值**，动作一判断「还在不在窗里」只有下标能回答（`nums[dq[0]]` 随时取值）；顺序也要对：先维护（出窗 + 支配）、再 push、最后读答案。
- 均摊 `O(n)`：每个元素最多入队一次、出队一次，队尾 `while` 不是嵌套循环；空间 `O(k)`（下标都在窗内且严格递增）。

## 答案

### 解法一：单调队列（时间 O(n) / 空间 O(k)）

```python
from collections import deque

def maxSlidingWindow(nums, k):
    dq = deque()          # 存下标！对应值严格递减
    ans = []
    for i, x in enumerate(nums):
        # 动作一：队首淘汰（出窗）—— 看下标
        if dq and dq[0] < i - k + 1:
            dq.popleft()
        # 动作二：队尾淘汰（被支配）—— 看值
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            ans.append(nums[dq[0]])
    return ans
```

### 解法二：大顶堆 + 惰性删除（时间 O(n log n) / 空间 O(n)）

写起来快、不易错，且天然支持「任意时刻查询前 m 大」这类扩展；比单调队列慢一档，只回答「窗口最大」时不如解法一。

```python
import heapq

def maxSlidingWindow(nums, k):
    h, ans = [], []
    for i, x in enumerate(nums):
        heapq.heappush(h, (-x, i))          # Python 堆是小顶，取负变最大
        if i >= k - 1:
            while h[0][1] < i - k + 1:      # 堆顶已出窗 → 惰性弹出
                heapq.heappop(h)
            ans.append(-h[0][0])
    return ans
```

### Java 版

```java
public int[] maxSlidingWindow(int[] nums, int k) {
    int n = nums.length;
    int[] ans = new int[n - k + 1];
    Deque<Integer> dq = new ArrayDeque();     // 存下标，值严格递减
    for (int i = 0; i < n; i++) {
        if (!dq.isEmpty() && dq.peekFirst() < i - k + 1) {
            dq.pollFirst();                   // 动作一：队首出窗
        }
        while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[i]) {
            dq.pollLast();                    // 动作二：队尾被支配
        }
        dq.offerLast(i);
        if (i >= k - 1) {
            ans[i - k + 1] = nums[dq.peekFirst()];
        }
    }
    return ans;
}
```
