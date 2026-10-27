# 【LC 1】两数之和：先查再存，反了就匹配自己

**来源**: https://zhoujungis.github.io/article/lc-1-two-sum/
**标签**: 算法、哈希表、LeetCode、面试
**难度**: 简单

## 题目

给定一个整数数组 `nums` 和一个整数目标值 `target`，请你在该数组中找出**和为目标值的那两个整数**，并返回它们的数组下标。

你可以假设**每种输入只会对应一个答案**，但是，数组中**同一个元素在答案里不能重复出现**。

```
输入：nums = [2, 7, 11, 15], target = 9
输出：[0, 1]
解释：因为 nums[0] + nums[1] == 9，返回 [0, 1]。

输入：nums = [3, 2, 4], target = 6
输出：[1, 2]

输入：nums = [3, 3], target = 6
输出：[0, 1]
```

## 思路

- 暴力两重循环 O(n²) 在枚举组合；换个问法：站在 `i` 的位置问「我缺的那个数 `target - nums[i]` 之前来过吗」，问题就从「两两组合」变成「查一个值在不在」，而查表是 O(1)。
- 表里必须存 `值 → 下标`（题目要返回下标），所以不能用 `set`；`set` 只能回答「在不在」，回答不了「在哪」。
- **顺序不能颠倒：先查表、再登记自己**。查表那一刻表里只有 `nums[0..i-1]`，所以任何命中下标必然 `< i`，「同一元素不能重复使用」这条约束自动成立，无需额外判断。
- 若反过来「先存再查」，当 `target == 2 * x` 时会查到自己，返回 `[i, i]`，违反题意。触发条件是「当前元素恰好是目标值的一半」。
- 易错点：官方第一组样例 `[2,7,11,15]` 配 `9` 恰好不触发该 bug（9 的一半不是整数），必须自己构造 `target = 2 * x` 的用例（如 `[3,3]`、`[0,0]`）验证。
- 其他坑：别用 `if seen.get(need)` 判存在（值为 0 时是假值）；`seen[need]` 一定在 `i` 左边，返回 `[seen[need], i]` 才是升序；题目保证唯一解，所以可以命中即 `return`。

## 答案

### 解法一：一次遍历 + 哈希表，先查再存（时间 O(n) / 空间 O(n)）

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}                          # 值 -> 它的下标
        for i, x in enumerate(nums):
            need = target - x
            if need in seen:               # ① 先在我左边找
                return [seen[need], i]
            seen[x] = i                    # ② 再把自己记进去
        return []
```

### 解法二：先建完整张表，再查（时间 O(n) / 空间 O(n)）

同样正确但常数更大：要多扫一遍，且必须显式写 `seen[need] != i` 排除自己；重复值会互相覆盖（只保留最后一个下标），不适合「求所有答案对」的场景。

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, x in enumerate(nums):       # 第一遍：把整张表建好
            seen[x] = i
        for i, x in enumerate(nums):       # 第二遍：再查
            need = target - x
            if need in seen and seen[need] != i:    # ← 必须排除自己
                return [i, seen[need]]
        return []
```

### Java 版

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();       // 值 -> 下标
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            if (seen.containsKey(need)) {                    // ① 先查
                return new int[] { seen.get(need), i };
            }
            seen.put(nums[i], i);                            // ② 再存
        }
        return new int[] {};
    }
}
```
