# 【LC 33/153】旋转排序数组：同一断崖，比法相反

**来源**: https://zhoujungis.github.io/article/lc-33-153-rotated-binary-search/
**标签**: 算法、二分查找、LeetCode、面试

## 题目

### LC 33 搜索旋转排序数组

整数数组 `nums` 原本按**升序**排列且元素**互不相同**，在某个未知下标处被旋转一次（例如 `[0,1,2,4,5,6,7]` → `[4,5,6,7,0,1,2]`）。给定目标值 `target`，在数组中搜索 `target`：存在则返回其下标，不存在返回 `-1`。要求时间复杂度 `O(log n)`。

```
输入: nums = [4,5,6,7,0,1,2], target = 0
输出: 4

输入: nums = [4,5,6,7,0,1,2], target = 3
输出: -1

输入: nums = [4,5,6,7,0,1,2], target = 4     # 第一段左端点
输出: 0

输入: nums = [4,5,6,7,0,1,2], target = 2     # 第二段右端点
输出: 6
```

### LC 153 寻找旋转排序数组中的最小值

已知长度为 `n` 的数组预先按升序排列，经旋转后得到输入数组，元素**互不相同**。请找出并返回其中的**最小值**。要求时间复杂度 `O(log n)`。

```
输入: nums = [4,5,6,7,0,1,2]
输出: 0
```

说明与约束（两题共同）：数组非空、元素互不相同（因此可以做到 `O(log n)`）；旋转数组可看作两段各自上升的折线，中间一道断崖，最小值站在断崖右侧那段的起点上。

## 思路

- **先立画面**：旋转数组 = 两段上升折线 + 一道断崖（`[4,5,6,7 | 0,1,2]`）。二分每步只回答一个问题 —— **mid 站在断崖的哪一边**，或**哪一半完全有序**。
- **153 和 `nums[r]` 比，收缩用 `r = mid`**：`nums[mid] > nums[r]` 说明 mid 在第一段、断崖在右边，最小值在 `[mid+1, r]`；否则 mid 在第二段，最小值在 `[l, mid]` 且 **mid 自己可能就是答案**，所以是 `r = mid` 不是 `r = mid - 1`。循环条件必须是 `l < r`（缩到一点即答案），配 `l <= r` 会死循环。
- **153 为什么不和 `nums[l]` 比**：`nums[mid] > nums[l]` 时 mid 可能在第一段，也可能整个数组没旋转，两种情况这一个比较区分不了，方向无从谈起；和 `nums[r]` 比没有这种歧义（两段内部严格递增，`nums[mid] == nums[r]` 只在区间缩到一两个元素时出现）。
- **33 和 `nums[l]` 比，找"有序的那半"**：mid 把 `[l, r]` 切成两半，断崖只在其中一半，另一半点名有序 —— `nums[l] <= nums[mid]` 则左半 `[l, mid]` 有序，否则右半 `[mid, r]` 有序。**等号不能漏**：`l == mid` 时区间只剩一两个元素，必须判"有序"，否则方向错乱。
- **有序半里的值域判断一开一闭**：左半 `nums[l] <= target < nums[mid]`，右端开（相等已在开头命中返回）；右半 `nums[mid] < target <= nums[r]`，右端闭（`nums[r]` 本身可以是 target）。写错任何一端的开闭都会在 target 恰为端点值时丢解。
- **两题比较对象相反不是巧合**：153 要的是"mid 在断崖哪边"（和 right 比一步实锤），33 要的是"哪半有序"（和 left 比一步得到）。允许重复元素时（LC 81/154）无法判断方向，只能 `l += 1` / `r -= 1` 退一格，最坏退化 `O(n)`。

## 答案

### LC 153

#### 解法一：二分收缩到断崖右段起点（时间 O(log n) / 空间 O(1)）

适用场景：无重复元素的旋转数组找最小值 —— 记住 `r = mid` 与 `l < r` 必须配套。

```python
def findMin(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        mid = (l + r) // 2
        if nums[mid] > nums[r]:
            l = mid + 1     # mid 在第一段，断崖在右边
        else:
            r = mid         # mid 在第二段，mid 可能就是最小值
    return nums[l]
```

### LC 33

#### 解法一：二分 + 有序半值域判断（时间 O(log n) / 空间 O(1)）

适用场景：无重复元素的旋转数组搜索指定值 —— 每步先用 `nums[l] <= nums[mid]` 定出有序半，再在有序半里做普通二分的值域判断。

```python
def search(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target:
            return mid
        if nums[l] <= nums[mid]:                       # 左半有序
            if nums[l] <= target < nums[mid]:          # target 在左半值域内
                r = mid - 1
            else:
                l = mid + 1                            # 只可能在右半
        else:                                          # 右半有序
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
    return -1
```

### Java 版

```java
// LC 153
class Solution {
    public int findMin(int[] nums) {
        int l = 0, r = nums.length - 1;
        while (l < r) {
            int mid = (l + r) >>> 1;
            if (nums[mid] > nums[r]) l = mid + 1;   // mid 在第一段
            else r = mid;                            // mid 在第二段，不能丢
        }
        return nums[l];
    }
}

// LC 33
class Solution {
    public int search(int[] nums, int target) {
        int l = 0, r = nums.length - 1;
        while (l <= r) {
            int mid = (l + r) >>> 1;
            if (nums[mid] == target) return mid;
            if (nums[l] <= nums[mid]) {                        // 左半有序
                if (nums[l] <= target && target < nums[mid]) r = mid - 1;
                else l = mid + 1;
            } else {                                           // 右半有序
                if (nums[mid] < target && target <= nums[r]) l = mid + 1;
                else r = mid - 1;
            }
        }
        return -1;
    }
}
```
