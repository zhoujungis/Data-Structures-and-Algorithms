# 【LC 234】回文链表：翻后半段，比是否相同

**来源**: https://zhoujungis.github.io/article/lc-234-palindrome-linked-list/
**标签**: 算法、链表、LeetCode、面试
**难度**: 简单

## 题目

给你一个单链表的头节点 `head`，请判断该链表是否为回文链表。

```
输入：head = [1,2,2,1]
输出：true

输入：head = [1,2]
输出：false
```

**进阶**：你能否用 `O(n)` 时间复杂度和 `O(1)` 空间复杂度解决此题？

链表节点的定义（下面所有代码都用它）：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

## 思路

- 链表没有下标，`j` 从尾部往回走要重走一遍（`O(n²)`）；把「后半段反转过来」就变成了「从前往后逐位比」—— 判断回文 = 判断前半段与「后半段反转后」是否逐位相等。
- 三步都是做过的题：快慢指针找中点（LC 876）+ 原地反转链表（LC 206）+ 双指针逐对比较，所以全程 `O(1)` 空间。
- 中点用 `slow = fast = head` 出发，`slow` 停在后半段的第一个节点，中间节点归后半段 —— 它跟自己比必然相等，不影响结论，反而反转后自动落到末尾。
- 不用写 `slow.next = None` 断开：反转时中点的 `next` 已被置成 `None`，前半段链走到中点就自然终止；也正因为全程没断开，再反转一次后半段就能恢复原链表。
- 易错点：比较循环必须是 `while p2`。偶数长度时前半段链比反转后的后半段多一个节点，写成 `while p1` 会让 `p2` 先走到 `None` 并访问 `None.val` 报错。
- 易错点：别和 LC 143 的中点取法串了 —— 143 用 `slow=head, fast=head.next`（中点归前半段），234 用 `slow=fast=head`（中点归后半段）。

## 答案

### 解法一：找中点 + 反转后半段 + 逐对比较（时间 O(n) / 空间 O(1)）

```python
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        if head is None or head.next is None:
            return True

        # ① 找中点：fast 一次两格、slow 一次一格
        #    fast 走完时，slow 正好停在后半段的开头（奇数长度时是正中间）
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # ② 反转后半段（LC 206 原样搬过来，起点换成 slow）
        prev, curr = None, slow
        while curr:
            nxt = curr.next      # 先记住
            curr.next = prev     # 再掉头
            prev = curr          # 后前移
            curr = nxt

        # ③ 逐对比较：以后半段为准，它更短
        p1, p2 = head, prev
        while p2:
            if p1.val != p2.val:
                return False
            p1, p2 = p1.next, p2.next
        return True
```

### Java 版

```java
class Solution {
    public boolean isPalindrome(ListNode head) {
        if (head == null || head.next == null) return true;

        // ① 找中点：slow 停在后半段的开头
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        // ② 反转后半段
        ListNode prev = null, curr = slow;
        while (curr != null) {
            ListNode nxt = curr.next;   // 先记住
            curr.next = prev;           // 再掉头
            prev = curr;                // 后前移
            curr = nxt;
        }

        // ③ 逐对比较：以后半段为准
        ListNode p1 = head, p2 = prev;
        while (p2 != null) {
            if (p1.val != p2.val) return false;
            p1 = p1.next;
            p2 = p2.next;
        }
        return true;
    }
}
```
