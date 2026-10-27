# 【LC 224/772】基本计算器：一个来一个结，一个等优先级

**来源**: https://zhoujungis.github.io/article/lc-224-772-basic-calculator/
**标签**: 算法、栈、LeetCode、面试

## 题目

### LC 224 基本计算器

给你一个字符串表达式 `s`，请你实现一个基本计算器来计算并返回它的值。`s` 由数字、`'+'`、`'-'`、`'('`、`')'` 和空格组成，`s` 表示一个有效的表达式。

```
输入: "(1+(4+5+2)-3)+(6+8)"
输出: 23

输入: "1 + 2 - (3 + 4) - 5"
输出: -9
```

### LC 772 基本计算器 III

在 224 的基础上加上 `'*'`、`'/'`，处理运算优先级与括号。整数除法截断小数部分（**向零取整**）。

```
输入: "2*(5+5*2)/3+(6/2+8)"
输出: 21
```

两题共同的约定：表达式有效；空格可出现在任意位置；多位数字要正确切分（`"1-11"` 是 `1`、`-`、`11`）；不会出现除零。LC 224 官方数据不含一元负号，但变体（如 `"-2+5"`、`"2*(-3)"`）常有。

## 思路

- **LC 224：加减同级、左结合 ⇒ 根本没有优先级要处理**。任何数字读到，它前面的符号就已经定了，没有资格等待：立刻 `result += sign * num` 结算。所以不需要运算符栈，只需 `result` 和 `sign` 两个变量。
- **括号 = 外层欠账**：`(` 时把 `{外层 result, 括号 sign}` 压栈，然后重启一个干净的累加器（`result = 0, sign = +1`）；`)` 时把括号内的值当作整体，`result = 外层result + 外层sign * inner` 并回外层。**压栈的必须是清零之前的外层值**，顺序反了就存进 `{0, 1}`，外层账全丢。
- **LC 772：优先级打破「立刻结算」**——`2 + 3 * 4` 里的 `3` 有资格等待右边的 `*`，于是需要 Dijkstra 双栈调度场：`nums` 存操作数，`ops` 存运算符（`(` 也在里面，只当挡板不比优先级）。
- 唯一纪律：**新运算符来临时，弹出栈顶所有优先级 `>=` 自己的运算符结算，再入栈**。用 `>=` 而不是 `>` 是左结合的全部秘密（`10-2-3` 用 `>` 会算成 `10-(2-3)=11`）。
- `(` 挡住后面所有运算符，`)` 一路结算到挡板并把 `(` 弹掉；扫描结束后 `ops` 可能还沉着低优先级运算符，**必须 flush 收尾**，`nums[0]` 才是答案。
- **除法向零取整**：Python 的 `//` 是 floor（`-3 // 2 == -2`），题目要 `-1`，必须写成 `sign * (abs(a) // abs(b))`；Java/C++ 的 `/` 天然正确。Java 中间结果用 `long` 防结算中途溢出。
- 一元负号的判定：`+` `-` 出现在**开头、`(` 之后、或另一个运算符之后**时是符号不是二元运算符，要并进后面数字（或先压 `0`）。

## 答案

### LC 224

#### 解法一：累加器 + 括号欠账栈（时间 O(n) / 空间 O(n)）

适用：只有加减的版本，代码最短；栈深等于括号嵌套层数（最坏 O(n)）。

```python
def calculate(s: str) -> int:
    result, sign, stack = 0, 1, []
    i = 0
    while i < len(s):
        c = s[i]
        if c == ' ':
            i += 1
        elif c.isdigit():
            j = i
            while j < len(s) and s[j].isdigit():   # 连续数字合成一个数
                j += 1
            result += sign * int(s[i:j])
            i = j
        elif c == '+':
            sign = 1; i += 1
        elif c == '-':
            sign = -1; i += 1
        elif c == '(':
            stack.append((result, sign))           # 外层欠账进栈
            result, sign = 0, 1                    # 重启累加器
            i += 1
        else:                                      # ')'
            inner = result
            prev, psign = stack.pop()
            result = prev + psign * inner          # 括号塌缩成一个数并回外层
            i += 1
    return result
```

#### Java 版

```java
class Solution {
    public int calculate(String s) {
        Deque<int[]> stack = new ArrayDeque<>();   // {外层result, 括号sign}
        int result = 0, sign = 1;
        for (int i = 0; i < s.length(); ) {
            char c = s.charAt(i);
            if (c == ' ') { i++; }
            else if (Character.isDigit(c)) {
                int j = i;
                while (j < s.length() && Character.isDigit(s.charAt(j))) j++;
                result += sign * Integer.parseInt(s.substring(i, j));
                i = j;
            } else if (c == '+') { sign = 1; i++; }
            else if (c == '-') { sign = -1; i++; }
            else if (c == '(') {
                stack.push(new int[]{result, sign});
                result = 0; sign = 1; i++;
            } else {                                // ')'
                int inner = result;
                int[] ctx = stack.pop();
                result = ctx[0] + ctx[1] * inner;
                i++;
            }
        }
        return result;
    }
}
```

### LC 772

#### 解法一：双栈调度场（shunting-yard）（时间 O(n) / 空间 O(n)）

适用：含 `*` `/` 与括号的满血版；每个运算符至多入栈、出栈各一次，结算总量的摊还成本是 O(n)，也天然可扩展到函数、变量、幂运算。

```python
def calculate(s: str) -> int:
    prec = {'+': 1, '-': 1, '*': 2, '/': 2}
    nums, ops = [], []

    def apply():
        op, b, a = ops.pop(), nums.pop(), nums.pop()
        if op == '+': nums.append(a + b)
        elif op == '-': nums.append(a - b)
        elif op == '*': nums.append(a * b)
        else:                                   # 向零截断：// 是 floor，负数会错
            q = abs(a) // abs(b)
            nums.append(q if (a >= 0) == (b >= 0) else -q)

    i = 0
    while i < len(s):
        c = s[i]
        if c == ' ':
            i += 1
        elif c.isdigit():
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            nums.append(int(s[i:j]))
            i = j
        elif c == '(':
            ops.append(c); i += 1
        elif c == ')':
            while ops[-1] != '(':               # 结算到挡板
                apply()
            ops.pop()                           # 弹掉 '(' 本身
            i += 1
        else:                                   # + - * /
            while ops and ops[-1] != '(' and prec[ops[-1]] >= prec[c]:
                apply()                         # 优先级 >= 我的，先结账
            ops.append(c)
            i += 1
    while ops:                                  # 收尾：从顶到底全结算
        apply()
    return nums[0]
```

#### Java 版

```java
class Solution {
    public int calculate(String s) {
        Deque<Long> nums = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        for (int i = 0; i < s.length(); ) {
            char c = s.charAt(i);
            if (c == ' ') { i++; }
            else if (Character.isDigit(c)) {
                long v = 0;
                while (i < s.length() && Character.isDigit(s.charAt(i)))
                    v = v * 10 + (s.charAt(i++) - '0');
                nums.push(v);
            } else if (c == '(') { ops.push(c); i++; }
            else if (c == ')') {
                while (ops.peek() != '(') apply(nums, ops);
                ops.pop(); i++;
            } else {
                while (!ops.isEmpty() && ops.peek() != '('
                        && rank(ops.peek()) >= rank(c)) apply(nums, ops);
                ops.push(c); i++;
            }
        }
        while (!ops.isEmpty()) apply(nums, ops);
        return nums.pop().intValue();
    }

    private int rank(char op) { return op == '+' || op == '-' ? 1 : 2; }

    private void apply(Deque<Long> nums, Deque<Character> ops) {
        char op = ops.pop();
        long b = nums.pop(), a = nums.pop();
        long r = switch (op) {
            case '+' -> a + b;
            case '-' -> a - b;
            case '*' -> a * b;
            default -> a / b;      // 向零截断
        };
        nums.push(r);
    }
}
```
