# 【LC 415】字符串相加：把竖式翻译成代码

**来源**: https://zhoujungis.github.io/article/lc-415-add-strings/
**标签**: 算法、双指针、LeetCode、面试

## 题目

给定两个字符串形式的非负整数 `num1` 和 `num2`，计算它们的和并同样以字符串形式返回。

你不能使用任何内建的用于处理大整数的库（比如 BigInteger），也不能直接将输入的字符串转换为整数形式。

```
输入: num1 = "456", num2 = "77"
输出: "533"
```

说明与约束：

- 输入为非负整数的字符串形式，不含前导零（`"0"` 本身除外）；长度可以很长，因此禁止整串转 int；
- 输出同样是不含前导零的字符串，`"0" + "0"` 必须返回 `"0"`（不是空串，也不是 `"00"`）；
- 逐字符把 `'0'`..`'9'` 转成数值（如 `ord(c) - 48`）不算"整串转整数"，是竖式的本意；
- 注意最高位溢出：`"999" + "1"` 应得 `"1000"`，长度比两个输入都长一位。

## 思路

- **"不能转整数"不是刁难，而是排除法**：它把「先转数字再算」的捷径全部排除，剩下的唯一解法就是列竖式。这题考的不是想出算法，而是**把一个人人都会的过程无遗漏地翻译成代码**。
- **三个关键词**：从个位开始（末尾对齐）、写下个位带走进位、缺位补零 —— 对应双指针从两串末尾出发 + 一个 `carry` 变量。
- **对齐用下标判断，不动原串**：`i >= 0 ? num1[i] : 0`，`i < 0` 表示这一位用完、**这一列它贡献 0**（不是跳过这一列：列还在，只是这一侧加数为 0）。比先 `padStart` 补零少一次拷贝，也不会踩前导零。
- **每列只有三步**：`s = a + b + carry`；本位写 `s % 10`；`carry = 1 if s >= 10 else 0`。两个非负一位数相加（低位最多再进 1）最大是 `9+9+1=19`，所以进位是 0/1 变量，不必用 `s // 10` 的一般化写法。
- **循环条件必须三连 or**：`while i >= 0 or j >= 0 or carry > 0`。前两个管"还有数位没加"，`carry > 0` 管"最后还有进位要长出一位" —— 漏掉它是这题最经典的丢分点（`"999" + "1"` 会输出 `"000"`）。
- **结果低位在前收集再反转**：竖式天然从低位往高位生成，用数组 `append`/`StringBuilder.append` 尾插、最后 reverse 一次 join。用 `unshift`/头插会让整体退化成 `O(n²)`。

## 答案

### 解法一：竖式模拟（双指针 + 进位）（时间 O(max(m, n)) / 空间 O(1)）

适用场景：本题唯一正解；骨架可直接复用到 LC 67（换基数）、LC 2（链表存数）、LC 43（每列多层累加）。

```python
def addStrings(num1: str, num2: str) -> str:
    i, j = len(num1) - 1, len(num2) - 1
    carry = 0
    res_low_to_high = []          # 低位在前，push 顺序天然从个位往高位

    while i >= 0 or j >= 0 or carry > 0:
        a = ord(num1[i]) - 48 if i >= 0 else 0
        b = ord(num2[j]) - 48 if j >= 0 else 0
        s = a + b + carry
        res_low_to_high.append(s % 10)
        carry = 1 if s >= 10 else 0
        i -= 1
        j -= 1

    return ''.join(map(str, reversed(res_low_to_high)))
```

### Java 版

```java
public String addStrings(String num1, String num2) {
    int i = num1.length() - 1, j = num2.length() - 1, carry = 0;
    StringBuilder sb = new StringBuilder();   // append 尾插 = 低位在前

    while (i >= 0 || j >= 0 || carry > 0) {
        int a = i >= 0 ? num1.charAt(i) - '0' : 0;
        int b = j >= 0 ? num2.charAt(j) - '0' : 0;
        int s = a + b + carry;
        sb.append(s % 10);
        carry = s >= 10 ? 1 : 0;
        i--; j--;
    }
    return sb.reverse().toString();
}
```
