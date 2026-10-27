# 【LC 82】删除重复元素 II：为什么必须有 dummy

**来源**: https://zhoujungis.github.io/article/lc-82-remove-duplicates-from-sorted-list-ii/
**标签**: 算法、链表、LeetCode、面试
**难度**: 中等

## 题目

给你一个已排序的链表的头 `head`，**删除原始链表中所有重复数字的节点，只留下不同的数字**。

```
输入：head = [1,2,3,3,4,4,5]
输出：[1,2,5]
解释：3 和 4 都出现过重复，所以它们一个都不留

输入：head = [1,1,1,2,3]
输出：[2,3]
解释：1 出现了三次，全删；2、3 各只出现一次，保留
```

说明与约束：

- 关键是「**出现过重复的值，一个都不留**」：与 LC 83（每个值留一个）不同，`[1,2,3,3,4,4,5]` 这里要得到 `[1,2,5]` 而不是 `[1,2,3,4,5]`；
- 链表已排序，重复的元素一定相邻；
- 头节点本身也可能是重复段的一员，`[1,1,2]` 的答案是 `[2]`。

链表节点定义：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

## 思路

- **排序白送 O(1) 空间的判重**：重复元素必然相邻，看到「当前节点与下一个节点同值」就知道碰上重复，不需要哈希表统计全局出现次数。
- **删除需要前驱，而 82 要连重复段的第一个节点也删**：这一段的第一节点可能是 `head` 自己，`head` 没有前驱，`head.next` 这个赋值无从执行 —— 这就是必须架 `dummy` 哨兵的准确理由：把「删头节点」变成一次普通删除。
- **返回 `dummy.next` 而不是 `head`**：`head` 可能已被摘掉，成为脱离链表的孤儿节点；`dummy.next` 才永远是正确表头。`dummy` 的值随便填，它不参与比较。
- **`prev` 只在确认 `curr` 不属于重复段时才前进**：发现重复时 `curr` 一路冲到段外，而 `prev` 必须**钉在原地**（它是这段的接回点），最后 `prev.next = curr` 一次把整段摘掉。`prev` 跟着一起推，被摘的节点就会卡在 `prev` 和 `curr` 之间。
- **内层 `while curr and curr.val == dup_val` 的 `curr and` 不能省**：重复段延伸到链表末尾（如 `1 → 2 → 2`）时 `curr` 会跑到 `None`，漏掉判断就是 `AttributeError` / `NullPointerException`。
- **判据跟着题目走**：这里比值（题目要删的就是「重复数字」），与 LC 160 相交链表必须比引用正好相反；内层外层推的是**同一个 `curr`**，所以不是嵌套循环，总时间仍是 `O(n)`。

## 答案

### 解法一：dummy 哨兵 + 双指针（时间 O(n) / 空间 O(1)）

适用场景：本题标准解 —— 无需特判头节点，`prev` 冻结 + 整段摘链一次完成。

```python
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)       # 给头节点造一个前驱
        prev, curr = dummy, head

        while curr:
            # 发现重复：curr 和下一个值相同
            if curr.next and curr.val == curr.next.val:
                dup_val = curr.val
                while curr and curr.val == dup_val:
                    curr = curr.next     # 整段跳过
                prev.next = curr         # 一次摘掉整段；prev 不动
            else:
                prev = curr              # 确认安全，prev 才前进
                curr = curr.next

        return dummy.next                # 不是 head —— head 可能已被摘
```

### Java 版

```java
class Solution {
    public ListNode deleteDuplicates(ListNode head) {
        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy, curr = head;

        while (curr != null) {
            if (curr.next != null && curr.val == curr.next.val) {
                int dupVal = curr.val;
                while (curr != null && curr.val == dupVal) {
                    curr = curr.next;          // 整段跳过
                }
                prev.next = curr;              // 一次摘掉；prev 不动
            } else {
                prev = curr;                   // 确认安全，prev 才前进
                curr = curr.next;
            }
        }
        return dummy.next;
    }
}
```
