# 【LC 1262】可被三整除的最大和：贪心与滚动 dp

**来源**: https://zhoujungis.github.io/article/lc-1262-greatest-sum-divisible-by-three/
**标签**: 算法、贪心、动态规划、LeetCode、面试

## 题目

给你一个整数数组 `nums`，请你找出并返回能被 `3` 整除的**元素最大和**。如果不存在可行解，返回 `0`。

```
输入: nums = [3,6,5,1,8]
输出: 18   （3 + 6 + 1 + 8 = 18）

输入: nums = [4]
输出: 0    （4 不能被 3 整除，只能选空集，空集和是 0）

输入: nums = [1,2,3,4,4]
输出: 12   （1 + 3 + 4 + 4 = 12）
```

约束：`1 <= nums.length <= 4×10^4`，`1 <= nums[i] <= 10^4`。选的是**任意个**元素（一个子集），不是「恰好三个」；真正的约束只有一条：所选元素之和 ≡ 0 (mod 3)。

## 思路

- 元素全是正数，所以全选的和 `S` 是所有子集和的上界；要让结果被 3 整除，只需从全选里「削掉最小的一撮」。
- 记 `r = S % 3`：`r == 0` 直接返回 `S`；否则按余数把元素分成 `m0 / m1 / m2` 三桶并升序排列，余 0 的元素永远不用扔。
- `r == 1` 时只需在「扔一个 `m1`」和「扔两个 `m2`」中取代价更小者（1≡1，2+2≡1）；`r == 2` 时对称地取「一个 `m2`」或「两个 `m1`」。三种及以上的组合必然被这两种支配：三个同类抵消为 0，混合 1+2 也白扔，而多扔只会让和更小。
- 易错点：候选凑不齐时必须给 `∞` 而不是 `0`（否则 `min` 会选中一条不存在的路）；桶必须先排序，否则取到的不是最小的两个。
- 贪心依赖「元素全为正」。一旦允许负数，「全选再削」的框架失效，改用三格滚动 dp：`dp[j]` = 和 ≡ `j (mod 3)` 的最大和，初值 `[0, -∞, -∞]`，同样 O(n) / O(1)。
- dp 的坑：每个数必须先快照 `old` 再写 `dp`（0-1 背包「每件只用一次」），且不可达状态要用 `-∞` 而不是 `0`。

## 答案

### 解法一：按余数分组的贪心（时间 O(n log n) / 空间 O(n)）

适用于元素全为正（本题约束）的场景，答案即 `S - min(一个 m_r, 两个 m_{3-r})`。

```python
def maxSumDivThree(nums):
    total = sum(nums)
    r = total % 3
    if r == 0:
        return total
    m1 = sorted(x for x in nums if x % 3 == 1)
    m2 = sorted(x for x in nums if x % 3 == 2)

    def two(bucket):
        return bucket[0] + bucket[1] if len(bucket) >= 2 else float('inf')

    if r == 1:                      # 削掉一个 1，或两个 2
        drop = min(m1[0] if m1 else float('inf'), two(m2))
    else:                           # r == 2：削掉一个 2，或两个 1
        drop = min(m2[0] if m2 else float('inf'), two(m1))

    return 0 if drop == float('inf') else total - drop
```

### 解法二：三格滚动的取模 dp（时间 O(n) / 空间 O(1)）

通用解，不依赖「元素全为正」，允许负数同样成立。

```python
def maxSumDivThree(nums):
    NEG = float('-inf')
    dp = [0, NEG, NEG]                 # dp[j] = 和 ≡ j (mod 3) 的最大和
    for x in nums:
        old = dp[:]                    # 先快照，避免同一个 x 被用两次
        rem = x % 3
        for j in range(3):
            if old[j] == NEG:
                continue
            k = (j + rem) % 3
            dp[k] = max(dp[k], old[j] + x)
    return dp[0]
```

### Java 版

贪心（余数分组，一趟扫描维护最小/次小，时间 O(n) / 空间 O(1)）：

```java
class Solution {
    // LC 1262：余数分组的贪心 —— 与推演表逐帧一致
    public int maxSumDivThree(int[] nums) {
        int total = 0;
        final int INF = Integer.MAX_VALUE / 2;   // 别用 MAX_VALUE，相加会溢出
        int one1 = INF, one2 = INF;              // 最小的两个余 1
        int two1 = INF, two2 = INF;              // 最小的两个余 2
        for (int x : nums) {
            total += x;
            if (x % 3 == 1) {
                if (x < one1) { one2 = one1; one1 = x; }
                else if (x < one2) { one2 = x; }
            } else if (x % 3 == 2) {
                if (x < two1) { two2 = two1; two1 = x; }
                else if (x < two2) { two2 = x; }
            }
        }
        int r = total % 3;
        if (r == 0) return total;
        long drop;
        if (r == 1) drop = Math.min(one1, (long) two1 + two2);   // 削一个 1，或两个 2
        else        drop = Math.min(two1, (long) one1 + one2);   // 削一个 2，或两个 1
        return drop >= INF ? 0 : total - (int) drop;
    }
}
```

取模 dp（三格滚动，允许负数，时间 O(n) / 空间 O(1)）：

```java
class Solution {
    // LC 1262：三格滚动的取模 dp —— 允许负数，同样 O(n)
    public int maxSumDivThree(int[] nums) {
        final int NEG = Integer.MIN_VALUE / 2;
        int[] dp = {0, NEG, NEG};                 // dp[j] = 和 ≡ j (mod 3) 的最大和
        for (int x : nums) {
            int[] old = dp.clone();               // 每件只用一次：先快照
            for (int j = 0; j < 3; j++) {
                if (old[j] == NEG) continue;
                int k = (j + Math.floorMod(x, 3)) % 3;
                dp[k] = Math.max(dp[k], old[j] + x);
            }
        }
        return dp[0];
    }
}
```
