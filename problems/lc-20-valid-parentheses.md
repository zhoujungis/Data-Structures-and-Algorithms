# 【LC 20】有效的括号：栈是被结构逼出来的

**来源**: https://zhoujungis.github.io/article/lc-20-valid-parentheses/
**标签**: 算法、栈、LeetCode、面试

## 题目

给定一个只包括 `'('`、`')'`、`'{'`、`'}'`、`'['`、`']'` 的字符串 `s`，判断字符串是否有效。

有效需满足：左括号必须用**相同类型**的右括号闭合，且以**正确的顺序**闭合（嵌套不乱）。每个右括号都有一个对应的同类型左括号。

```
输入: s = "{[()]}"   输出: true
输入: s = "()[]{}"   输出: true
输入: s = "(]"       输出: false   （类型不匹配）
输入: s = "([)]"     输出: false   （嵌套交错）
输入: s = "(()"      输出: false   （左括号没闭合）
```

## 思路

- 结构直接逼出数据结构：每个右括号匹配的是**离它最近、尚未闭合**的同类型左括号，即「最内层未闭合的最先闭合」——后开先闭就是 LIFO，正是栈。
- 解法即白话：遇左括号入栈（记下「我在等什么」）；遇右括号先判空、再对比栈顶类型；扫完栈必须为空。
- 「有效」是三个独立否定条件的合取，对应三处检查，漏一处就错一类输入：① 类型不匹配（`"(]"`、`"([)]"`）→ `pairs[stack.pop()] != ch`；② 右括号没人接（`"())"` 的第二个 `)`、`"]"`）→ `if not stack`；③ 左括号没闭合（`"(()"`）→ 循环外的 `return not stack`。第三处最容易漏，因为它在循环外。
- 空栈检查必须在 `pop()` **之前**，否则空栈时会直接运行时崩溃（Python `IndexError` / Java 异常）。
- 计数器代替栈不成立：计数器只能查「余额」，查不了「顺序」，`"([)]"` 数量与类型全对但嵌套交错，只有栈顶比较能查出来。
- 实现取舍：栈里可存左括号（弹出时查映射表），也可直接存期待的右括号（`push(pairs[ch])`，遇右括号只需 `pop() == ch`），后者少一次查表。
- 复杂度：时间 O(n)（每个字符至多入栈/出栈一次），空间 O(n)（最坏全是左括号）。

## 答案

### 解法一：栈（存左括号，弹出时查映射）（时间 O(n) / 空间 O(n)）

```python
def isValid(s: str) -> bool:
    pairs = {'(': ')', '[': ']', '{': '}'}
    stack = []
    for ch in s:
        if ch in pairs:                 # 左括号：入栈
            stack.append(ch)
        else:                           # 右括号：问栈顶
            if not stack:               # 失败模式二：没人接
                return False
            if pairs[stack.pop()] != ch:  # 失败模式一：类型不匹配
                return False
    return not stack                    # 失败模式三：栈里还留着
```

### Java 版

```java
public boolean isValid(String s) {
    Map<Character, Character> pairs = Map.of('(', ')', '[', ']', '{', '}');
    Deque<Character> stack = new ArrayDeque<>();
    for (char ch : s.toCharArray()) {
        if (pairs.containsKey(ch)) {
            stack.push(ch);
        } else {
            if (stack.isEmpty() || pairs.get(stack.pop()) != ch) {
                return false;      // 模式二（空栈）与模式一（不匹配）合并成一行
            }
        }
    }
    return stack.isEmpty();        // 模式三
}
```
