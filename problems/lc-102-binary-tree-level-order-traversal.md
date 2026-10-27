# 【LC 102】二叉树的层序遍历：为什么先存队列长度

**来源**: https://zhoujungis.github.io/article/lc-102-binary-tree-level-order-traversal/
**标签**: 算法、二叉树、LeetCode、面试
**难度**: 中等偏易

## 题目

给你二叉树的根节点 `root`，返回其节点值的 **层序遍历**（即逐层地，从左到右访问所有节点）。

```
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[9,20],[15,7]]

输入：root = [1]
输出：[[1]]

输入：root = []
输出：[]
```

注意输出的**嵌套结构**：不是 `[3,9,20,15,7]`，而是 `[[3],[9,20],[15,7]]`。

## 思路

- 裸 BFS 只能吐出 `[3,9,20,15,7]`，丢掉了「层边界」；而分层信息本来就在队列里：同一层节点在队列中连续排列，且一定比下一层先出队（FIFO 保证）。
- 关键在于进 `while` 的第一件事取快照 `size = len(q)`：内层是一边出队一边把下一层入队，若用实时的 `len(q)` 当循环条件，层就会串在一起。
- `size` 一行同时给三样东西：这一层的节点数（分层）、`for _ in range(size)` 的精确次数、以及所有变体的抓手（103 的锯齿、199 的右视图都挂在它上面）。
- 易错点：忘了 `if not root` 守卫（`deque([None])` 会 `AttributeError`）；空树要返回 `[]` 而不是 `[[]]`；`list.pop(0)` 是 O(n)，必须用 `deque.popleft()` / `ArrayDeque.poll()`。
- 变体只换皮不改骨架：锯齿（103）改「值放哪一头」，右视图（199）封层取 `level[-1]` 或 `i == size - 1`，自底向上（107）`res[::-1]`，N 叉树（429）换入队来源。注意锯齿下入队顺序永远是 `left → right`，只反输出不反遍历。

## 答案

### 解法一：BFS + 队列长度快照分层（时间 O(n) / 空间 O(n)）

```python
from collections import deque
from typing import List, Optional

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        res = []
        q = deque([root])

        while q:
            size = len(q)              # ★ 这一层的节点数，快照
            level = []
            for _ in range(size):      # 只处理这一层
                node = q.popleft()
                level.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(level)          # 封层

        return res
```

### Java 版

```java
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> res = new ArrayList<>();
        if (root == null) return res;

        Deque<TreeNode> q = new ArrayDeque<>();
        q.offer(root);

        while (!q.isEmpty()) {
            int size = q.size();                    // ★ 快照
            List<Integer> level = new ArrayList<>(size);
            for (int i = 0; i < size; i++) {
                TreeNode node = q.poll();
                level.add(node.val);
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
            res.add(level);
        }
        return res;
    }
}
```
