# 【LC 21】合并两个有序链表：哑结点到底替你扛了什么

**来源**: https://zhoujungis.github.io/article/lc-21-merge-two-sorted-lists/
**标签**: 算法、链表、LeetCode、面试
**难度**: 简单

## 题目

将两个**升序**链表合并为一个新的**升序**链表并返回。新链表是通过**拼接**给定的两个链表的所有节点组成的。

```
输入：l1 = [1,2,4]，l2 = [1,3,4]
输出：[1,1,2,3,4,4]
```

注意题目里「**拼接**」两个字：不是 new 出一串新节点把值抄过去，而是**把原来的节点重新串起来**——值一个都不改，改的只有 `next` 指针的指向。

链表节点的定义（后面所有代码都用它）：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

两个链表都可能为空（`l1 = []` 或 `l2 = []`），此时结果就是另一条链表本身；长度可以悬殊。

## 思路

- 数组归并要搬运元素，**链表归并只改 `next` 指针**：每「放进结果一个节点」只是 `tail.next = X`，不复制不搬移，所以额外空间能做到 O(1)。
- 两条链表都升序 ⇒ **全局最小只可能是两个头节点之一**：比较取小、接到结果尾部、该链表后移，直到某条走空。
- **哑结点（dummy）的真实价值**：第一个节点来自哪条链表并不确定，没有 dummy 就得为「头是谁」写一串特判；有了它，第一个接进来的节点和第二十个走**完全相同的代码路径**，答案就是 `dummy.next`。
- **顺序不能反，`tail` 不能忘前移**：先接（`tail.next = l1`）再走（`l1 = l1.next`）；接完必须 `tail = tail.next`，否则下一轮覆盖旧节点，不报错但结果少一截。
- **循环退出后剩余部分要整段接上**（`tail.next = l1 if l1 else l2`）——这是本题 WA 排行榜第一名。循环条件是 `and` 不是 `or`。
- 相等时取 `l1`（用 `<=`）不影响本题结果，但这个「稳定性」习惯在归并排序里是必需品。
- 递归写法三行核心，代价是 O(m+n) 调用栈：Python 默认递归上限约 1000 层，长链表会爆栈，工程上选迭代。

## 答案

### 解法一：哑结点 + tail 迭代（时间 O(m+n) / 空间 O(1)）

适用：工程实现首选，无递归栈风险，额外空间只有两个指针。

```python
def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
    dummy = ListNode(0)              # 占位符，值无所谓
    tail = dummy                     # tail 永远指向结果链表最后一个节点
    while l1 and l2:                 # 两条都还有货，才需要比较
        if l1.val <= l2.val:         # 相等时取 l1，保证稳定性
            tail.next = l1           # l1 的头接上结果
            l1 = l1.next             # l1 后移（先接，再走，顺序不能反）
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next             # tail 前移到新接的节点——忘了这行就是大事故
    tail.next = l1 if l1 else l2     # 一方走空，另一方整段接上
    return dummy.next                # dummy 是占位符，真正的头在它后面
```

### 解法二：递归（时间 O(m+n) / 空间 O(m+n) 栈帧）

适用：面试中展示合并的自相似结构；也是 LC 23 分治解法的零件，但长链表有爆栈风险。

```python
def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
    if not l1:                       # 一方空了，返回另一方
        return l2
    if not l2:
        return l1
    if l1.val <= l2.val:             # 小的当头，它的 next 指向「剩下的合并结果」
        l1.next = mergeTwoLists(l1.next, l2)
        return l1
    else:
        l2.next = mergeTwoLists(l1, l2.next)
        return l2
```

### Java 版

```java
public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0);
    ListNode tail = dummy;
    while (l1 != null && l2 != null) {
        if (l1.val <= l2.val) {
            tail.next = l1;
            l1 = l1.next;
        } else {
            tail.next = l2;
            l2 = l2.next;
        }
        tail = tail.next;
    }
    tail.next = (l1 != null) ? l1 : l2;
    return dummy.next;
}
```

```java
public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    if (l1 == null) return l2;
    if (l2 == null) return l1;
    if (l1.val <= l2.val) {
        l1.next = mergeTwoLists(l1.next, l2);
        return l1;
    } else {
        l2.next = mergeTwoLists(l1, l2.next);
        return l2;
    }
}
```
