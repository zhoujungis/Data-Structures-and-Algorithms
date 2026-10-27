# 【LC 15】三数之和：难点是两处去重，不是双指针

**来源**: https://zhoujungis.github.io/article/lc-15-3sum/
**标签**: 算法、双指针、LeetCode、面试
**难度**: 中等

## 题目

给你一个整数数组 `nums`，判断是否存在三元组 `[nums[i], nums[j], nums[k]]` 满足 `i != j`、`i != k` 且 `j != k`，同时还满足 `nums[i] + nums[j] + nums[k] == 0`。请你返回所有和为 `0` 且不重复的三元组。

注意：答案中不可以包含重复的三元组。

```
输入：nums = [-1, 0, 1, 2, -1, -4]
输出：[[-1, -1, 2], [-1, 0, 1]]
解释：
  nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0
  nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0
  nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0
  不同的三元组是 [-1, 0, 1] 和 [-1, -1, 2]。
  注意输出的顺序和三元组的顺序并不重要。

输入：nums = [0, 1, 1]
输出：[]

输入：nums = [0, 0, 0]
输出：[[0, 0, 0]]
```

## 思路

- 先排序，再固定一个数 `i`（三元组里最小的那个），内层退化成「两数之和」：在 `i` 右边找和为 `-nums[i]` 的两个数，用双指针 `l = i + 1`、`r = n - 1` 夹逼，整体 O(n²)。
- 双指针正确性（单调性论证）：`r` 在最右端时 `nums[l] + nums[r]` 是以当前 `l` 为左端能取到的**最大和**，若它都小于目标，则 `l` 为左端的任何一对都不行，`l` 可放心右移且永不回头；对称地 `l` 在最左端时是最小和，太大就让 `r` 左移。由此也证明两指针合计最多走 `n` 步，内层是严格 O(n)。
- 排序的真正作用不是「查找更快」，而是**让相同的数挨在一起**，从而使去重退化成「跟前一个值比一比」。
- 去重只有两处且形态不同：外层 `i` 是**事前跳过**（`continue`，挡「起点重复」，整轮无需进内层）；命中后双指针是**事后跳过**（`while` 跳重复再各走一步，挡「配对数重复」，因为只有拿到一组解才知道该从哪里跳）。
- 边界不能省：`i > 0` 必须写，否则 `nums[-1]` 在 Python 里会绕到数组末尾造成随机跳过；`while` 里的 `l < r` 既防越界也防跳过头；两个 `while` 结束后必须再 `l += 1`、`r -= 1`，否则死循环。
- 剪枝：`nums[i] > 0` 直接 `break`；进阶可提前算本轮最小三数和（`> 0` 则 `break`）与最大三数和（`< 0` 则 `continue`）。
- 官方样例恰好两处去重都不触发，必须自测 `[0,0,0,0]`、`[-2,0,0,2,2]`、`[-1,-1,0,1]` 这类输入。

## 答案

### 解法一：排序 + 固定一个数 + 双指针（时间 O(n²) / 空间 O(1)，不计结果与排序开销）

```python
def threeSum(nums):
    nums.sort()                                     # ① 排序：让相同的数挨在一起
    res = []
    n = len(nums)

    for i in range(n - 2):                          # 留两个位置给 l 和 r
        if nums[i] > 0:                             # ② 剪枝：最小的都 > 0，后面没戏
            break
        if i > 0 and nums[i] == nums[i - 1]:        # ③ 第一处去重：起点重复，整轮跳过
            continue

        l, r = i + 1, n - 1
        while l < r:
            total = nums[i] + nums[l] + nums[r]
            if total < 0:
                l += 1                              # 和太小 → 换个更大的
            elif total > 0:
                r -= 1                              # 和太大 → 换个更小的
            else:
                res.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l + 1]:   # ④ 第二处去重：跳
                    l += 1
                while l < r and nums[r] == nums[r - 1]:
                    r -= 1
                l += 1
                r -= 1

    return res
```

### Java 版

```java
class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();

        for (int i = 0; i < nums.length - 2; i++) {
            if (nums[i] > 0) break;                          // 剪枝
            if (i > 0 && nums[i] == nums[i - 1]) continue;   // 第一处去重

            int l = i + 1, r = nums.length - 1;
            while (l < r) {
                int total = nums[i] + nums[l] + nums[r];
                if (total < 0) {
                    l++;
                } else if (total > 0) {
                    r--;
                } else {
                    res.add(Arrays.asList(nums[i], nums[l], nums[r]));
                    while (l < r && nums[l] == nums[l + 1]) l++;   // 第二处去重
                    while (l < r && nums[r] == nums[r - 1]) r--;
                    l++;
                    r--;
                }
            }
        }
        return res;
    }
}
```
