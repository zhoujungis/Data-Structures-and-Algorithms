# 【LC 704/69】二分查找 & 平方根：命中返回 vs 还向右

**来源**: https://zhoujungis.github.io/article/lc-704-69-binary-search-and-sqrt/
**标签**: 算法、二分查找、LeetCode、面试

## 题目

### LC 704 二分查找

给定一个 `n` 个元素**有序（升序）**的整型数组 `nums` 和一个目标值 `target`，在数组中查找 target，若存在返回其下标，否则返回 `-1`。要求时间复杂度 `O(log n)`。

```
输入: nums = [-1,0,3,5,9,12], target = 9
输出: 4

输入: nums = [-1,0,3,5,9,12], target = 2
输出: -1
```

说明与约束：

- 数组升序且**元素互不相同**（有重复时本模板不保证最左/最右，那是 LC 34 的事）；
- 未找到返回 `-1`；空数组直接返回 `-1`；
- 要求 `O(log n)`，线性扫描不合格。

### LC 69 x 的平方根

给定一个非负整数 `x`，计算并返回 `x` 的**算术平方根**，结果**只保留整数部分**（即向下取整，`⌊√x⌋`）。可用二分或牛顿法。

```
输入: x = 8
输出: 2   （√8 ≈ 2.828，小数部分舍去）

输入: x = 16
输出: 4
```

说明与约束：

- `x` 为非负整数，最大取到 `2³¹-1`（`mid * mid` 会撞 int 上限）；
- `x = 0` 返回 0，`x = 1` 返回 1；
- 结果为向下取整：`⌊√x⌋` 是满足 `k² ≤ x` 的**最大** `k`。

## 思路

- **二分的本质是不变量，不是「取中间比一下」**：若 `target` 在数组里，它的下标永远落在闭区间 `[left, right]` 内。每轮探 `mid`，把不可能是答案的那一半整段排除，不变量一次都不被违反。
- **三条铁律都源自「闭区间」这一个约定**：`while (left <= right)`（闭区间为空恰是 `left > right`）、`mid = left + ((right - left) >> 1)`（`left + right` 会爆 int）、收缩必带 ±1（`mid` 已检查过）。左闭右开是另一套（`while (left < right)` + `right = mid`），**两派混用正是二分出错的根源**。
- **69 的数组是自己造的**：构造单调谓词 `P(k) := (k * k <= x)`，在 `[0, x]` 上「前真后假」，`⌊√x⌋` 就是**最后一个 `true` 的下标**。这就是「答案二分」—— 只要谓词单调，答案空间就是你的数组（LC 875 / 1011 / 278 同一句话）。
- **与 704 的唯一动作之差**：`P(mid)` 成立时**不返回**，记候选 `ans = mid` 再向右（`lo = mid + 1`）；区间空了才结束，此时 `ans == hi == lo - 1`，`hi` 恰好停在最后一个真上。
- **69 的溢出陷阱**：`x = 2147395599` 时 `mid = 46340`，`mid² = 2147395600` 越过 int 上限变负数 → 谓词误判为真。升 `long` 或改写成 `mid <= x / mid`（注意 `mid == 0` 时除零，需先 `if (x < 2) return x;`）。
- **牛顿法**：`k ← (k + x/k) / 2` 二次收敛 `O(log log x)`，每步有效位数翻倍；停下必须用平方判停（`while k * k > x`），不能数步数 —— 整数除法会先停在 `⌊√x⌋ + 1` 再降下来。

## 答案

### LC 704

#### 解法一：闭区间二分（时间 O(log n) / 空间 O(1)）

适用场景：有序数组查找特定值的标准模板，命中即收工。

```python
def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:                      # 闭区间非空
        mid = left + ((right - left) >> 1)    # 防爆 int
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1                    # mid 检查过，跳过
        else:
            right = mid - 1
    return -1
```

#### Java 版

```java
class Solution {
    // LC 704
    public int search(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int mid = left + ((right - left) >> 1);   // 防 (left+right) 爆 int
            if (nums[mid] == target) return mid;
            if (nums[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
}
```

### LC 69

#### 解法一：答案二分（时间 O(log x) / 空间 O(1)）

适用场景：本题考察的正解 —— 谓词 `k² ≤ x` 找最后一个真，模板与 704 一步不差，写不错。

```python
def mySqrt(x):
    lo, hi, ans = 0, x, 0
    while lo <= hi:
        mid = lo + ((hi - lo) >> 1)
        if mid * mid <= x:      # 谓词成立
            ans = mid           # 记下候选
            lo = mid + 1        # 但不停手，继续向右找更大的真
        else:
            hi = mid - 1
    return ans
```

#### 解法二：牛顿法（时间 O(log log x) / 空间 O(1)）

适用场景：理论更快的加分项；需额外论证整除版为什么收敛到 `⌊√x⌋` 而非 `⌈√x⌉`。

```python
def mySqrt_newton(x):
    if x < 2:
        return x
    k = x
    while k * k > x:
        k = (k + x // k) // 2   # 向 √x 二次收敛
    return k
```

#### Java 版

```java
class Solution {
    // LC 69：long 版 —— 与推演表逐帧一致
    public int mySqrt(int x) {
        int lo = 0, hi = x, ans = 0;
        while (lo <= hi) {
            int mid = lo + ((hi - lo) >> 1);
            if ((long) mid * mid <= x) {   // 关键：mid*mid 先升 long 再比
                ans = mid;
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return ans;
    }
}
```
