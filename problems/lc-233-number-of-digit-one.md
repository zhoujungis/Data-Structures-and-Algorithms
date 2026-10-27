# 【数学】1~n 中数字 1 的个数：逐位拆解

**来源**: https://zhoujungis.github.io/article/lc-233-number-of-digit-one/
**标签**: 算法、数学、LeetCode、面试

## 题目

给定 `n`，统计 `1 ~ n` 所有整数中数字 `1` 出现的次数。要求找规律，不要暴力。

```
输入: n = 13
输出: 6
解释: 1, 10, 11, 12, 13 里共有 6 个 1 ——
      11 贡献两个，其余各一个。
```

约束：`0 ≤ n ≤ 2^31 - 1`（`n = 2147483647` 时答案为 `2971027783`，超出 32 位有符号整数范围）；`n < 0` 语义上无定义。

## 思路

- 换个问法：不问「哪些数含有 1」，而问「每个数位上分别出现了多少个 1」。两者总和相同，但后者可以把每个数位**独立**计算。
- 对权值为 `weight` 的数位（个位 1、十位 10、百位 100……），一位的答案只由三个值决定：`higher = n // (weight * 10)`（完整循环数）、`cur = (n // weight) % 10`、`lower = n % weight`。
- 每位贡献 = 完整循环数 × 每循环贡献（`weight`） + 零头里那一截：`cur = 0` 不多给；`cur = 1` 加 `lower + 1`；`cur > 1` 满额加 `weight`。
- 易错点：循环条件必须是 `weight <= n`。写成 `weight < n` 时 `n` 恰好是 10 的幂会漏掉最高位那一份，最小反例是 `n = 10`（得 1，正确是 2）。
- 易错点：`cur = 0` 分支在官方样例 `n = 13` 里一次都不执行，所以三种错法都能过样例；必须用 `n = 10, 20, 100, 101` 这类「数位中间有 0」的用例自测。
- 复杂度：`weight` 每轮 ×10，只走 `O(log10 n)` 轮、每轮 `O(1)`，`n` 从 1304 到 21 亿轮数只从 4 变到 10。

## 答案

### 解法一：逐位统计（迭代）（时间 O(log n) / 空间 O(1)）

```python
def count_digit_one(n: int) -> int:
    if n < 0:
        raise ValueError("n 必须是非负整数")
    total = 0
    weight = 1              # 当前数位的权值：1、10、100……
    # 注意是 <=：n 恰好是 10 的幂时，最高位那个数位也必须扫
    while weight <= n:
        higher = n // (weight * 10)
        cur = (n // weight) % 10
        lower = n % weight
        if cur == 0:
            total += higher * weight
        elif cur == 1:
            total += higher * weight + lower + 1
        else:
            total += (higher + 1) * weight
        weight *= 10
    return total
```

### 解法二：按最高位切分的递归（时间 O(log² n) / 空间 O(log n) 递归栈）

适用于想从最高位往下拆的写法；结果与迭代版在 `n ≤ 3000` 及 `2147483647` 上全量一致，但迭代版空间 `O(1)`、无递归深度问题，面试推荐迭代版。

```python
def count_digit_one_rec(n: int) -> int:
    if n <= 0:
        return 0
    if n < 10:
        return 1
    s = str(n)
    high = int(s[0])
    power = pow(10, len(s) - 1)
    rest = n - high * power
    if high == 1:
        # 最高位贡献 rest + 1 个；低位模式完整出现 1 次 + 尾巴上再出现一次
        return rest + 1 + count_digit_one_rec(power - 1) + count_digit_one_rec(rest)
    # 最高位贡献 power 个；低位模式完整出现 high 次 + 尾巴上再出现一次
    return power + high * count_digit_one_rec(power - 1) + count_digit_one_rec(rest)
```

### Java 版

```java
public class CountDigitOne {
    // 统计 1 ~ n 中数字 1 出现的次数
    public static long countDigitOne(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("n 必须是非负整数，收到 " + n);
        }
        long total = 0;
        // weight 必须用 long：n 接近 int 上限时循环会走到 10^9，
        // 下一步 weight *= 10 就是 10^10，int 装不下会回绕成负数，循环直接失控
        long weight = 1;
        while (weight <= n) {
            long higher = n / (weight * 10);
            int cur = (int) ((n / weight) % 10);
            long lower = n % weight;
            if (cur == 0) {
                total += higher * weight;
            } else if (cur == 1) {
                total += higher * weight + lower + 1;
            } else {
                total += (higher + 1) * weight;
            }
            weight *= 10;
        }
        return total;
    }
}
```
