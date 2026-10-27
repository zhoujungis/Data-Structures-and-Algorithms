# 【LC 42】接雨水：四种解法，同一个问题

**来源**: https://zhoujungis.github.io/article/lc-42-trapping-rain-water/
**标签**: 算法、双指针、单调栈、LeetCode、面试
**难度**: Hard

## 题目

给定 `n` 个非负整数表示每个宽度为 `1` 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

```
输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出：6

输入：height = [4,2,0,3,2,5]
输出：9
```

## 思路

- **核心公式（木桶原理）**：位置 `i` 的水量 `water[i] = max(0, min(左最高, 右最高) - height[i])` —— 水会往两边流，能留住的高度是两侧的短板。整道题只在问一件事：每个位置的"左最高"和"右最高"分别是多少。
- **动态规划**：发现"往左扫"的结果可以复用 —— `leftMax[i]` 是 `[0..i]` 的最大值、`rightMax[i]` 是 `[i..n-1]` 的最大值，各扫一遍预处理，之后每个位置 `O(1)` 查表。时间降到 `O(n)`，代价是两个数组。
- **双指针**：把"预处理"变成"边走边算"，每轮只结算**较矮的那一端**。因为 `height[l] < height[r]` 时，`l` 的右侧最高至少是 `height[r] > height[l]`，外侧上界已由对面的柱子保证、对侧不可能是短板，所以敢用局部的 `left_max` 直接定水位（反证：若 `left_max` 真超过右侧最高，那根更高的柱子经过时判据不会选左端）。
- **易错点 1**：`left_max` 必须**先更新再结算**（`left_max = max(...)` 在前，`ans += left_max - height[l]` 在后），新高那格才会自动消零；反过来先结算会算出负数、把总量往回扣。
- **易错点 2**：判据 `height[l] < height[r]` 结算左端，写反会去结算较高的一端、答案偏大，而官方样例恰好测不出来（两端只差 1，两种判据都得 6）；要用 `[5,0,1]`、`[4,0,0,0,3]` 自测。
- **单调栈**：换视角"横着切"，不按列算而按凹槽一层层填。栈存**下标**且对应高度单调递减；弹出栈顶作槽底后若栈空说明只有右边界、围不出凹槽；`while` 弹栈让一根高柱一口气结算好几层。

## 答案

### 解法一：动态规划（前缀/后缀最大数组）（时间 O(n) / 空间 O(n)）

适用场景：思路最直白、面试时先用它把「左右最高」讲清楚，再引到双指针。

```python
def trap(height):
    n = len(height)
    leftMax = [0] * n     # leftMax[i] = max(height[0..i])
    rightMax = [0] * n    # rightMax[i] = max(height[i..n-1])

    leftMax[0] = height[0]
    for i in range(1, n):
        leftMax[i] = max(leftMax[i - 1], height[i])

    rightMax[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        rightMax[i] = max(rightMax[i + 1], height[i])

    return sum(min(leftMax[i], rightMax[i]) - height[i] for i in range(n))
```

### 解法二：双指针（时间 O(n) / 空间 O(1)）

适用场景：本题最推荐的手写解法 —— 空间 `O(1)`，两个指针合计最多走 `n` 步。

```python
def trap(height):
    l, r = 0, len(height) - 1
    left_max = right_max = 0
    ans = 0

    while l < r:
        if height[l] < height[r]:
            left_max = max(left_max, height[l])     # ① 先更新
            ans += left_max - height[l]             # ② 再结算
            l += 1
        else:
            right_max = max(right_max, height[r])
            ans += right_max - height[r]
            r -= 1

    return ans
```

### 解法三：单调栈（时间 O(n) / 空间 O(n)）

适用场景：需要讲「按层累加」这个横切视角时用；同一格的水会被分几次加上（凹槽逐层结算）。

```python
def trap(height):
    stack = []                      # 存的是下标（不是值），对应高度单调递减
    ans = 0

    for i in range(len(height)):
        while stack and height[i] > height[stack[-1]]:
            top = stack.pop()       # 槽底
            if not stack:
                break               # 只有右边界、没有左边界 → 围不出凹槽
            width = i - stack[-1] - 1
            bounded = min(height[i], height[stack[-1]]) - height[top]
            ans += width * bounded
        stack.append(i)

    return ans
```

### Java 版

```java
class Solution {
    public int trap(int[] height) {
        int l = 0, r = height.length - 1;
        int leftMax = 0, rightMax = 0, ans = 0;

        while (l < r) {
            if (height[l] < height[r]) {
                leftMax = Math.max(leftMax, height[l]);
                ans += leftMax - height[l];
                l++;
            } else {
                rightMax = Math.max(rightMax, height[r]);
                ans += rightMax - height[r];
                r--;
            }
        }
        return ans;
    }
}
```
