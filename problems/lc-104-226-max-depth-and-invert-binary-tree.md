# 【LC 104/226】最大深度 & 翻转二叉树：各藏一颗钉子

**来源**: https://zhoujungis.github.io/article/lc-104-226-max-depth-and-invert-binary-tree/
**标签**: 算法、二叉树、LeetCode、面试
**难度**: 简单

## 题目

### LC 104 二叉树的最大深度

给定一个二叉树 `root`，返回其**最大深度**。最大深度是指从根节点到最远叶子节点的最长路径上的节点数。

```
输入：root = [3,9,20,null,null,15,7]
输出：3

输入：root = [1,null,2]
输出：2
```

```
       3                ← 第 1 层
      / \
     9   20             ← 第 2 层
        /  \
       15   7           ← 第 3 层
```

### LC 226 翻转二叉树

给你一棵二叉树的根节点 `root`，翻转这棵二叉树，并返回其根节点。

```
输入：root = [4,2,7,1,3,6,9]
输出：[4,7,2,9,6,3,1]
```

```
        4                        4
       / \                      / \
      2   7        →           7   2
     / \ / \                  / \ / \
    1  3 6  9                9  6  3  1
```

## 思路

- **LC 104**：答案是 `1 + max(左高, 右高)`，那个 `1` 是把自己这一层算上；漏掉它整棵树都返回 0。
- **LC 104 必须后序**：子树高度是从下往上冒的信息，父节点手里没有，只能先下去要。先序也能写（把 `depth` 当参数自顶向下累加），但那样就拿不到「子树高度」这个中间量，110 平衡二叉树这类题就做不了。
- **LC 104 的钉子长在 111 上**：最小深度不能把 `max` 直接换成 `min` —— `null` 不是叶子，「空子树记 0」这个约定位在 `max` 下恰好把 0 淘汰（无害），在 `min` 下却会伪造一条长度 0 的假路径，`[1,2]` 会错答 1（正确是 2）。必须先把单侧空的分支单独摘出来。
- **LC 226**：本质就是「遍历每个节点，把它的两个孩子交换一次」，五行代码。
- **LC 226 顺序自由，但有一个雷**：每个节点换自己两个孩子，不依赖子树状态，所以前序（先换再递归）和后序（先递归再换）都对；**但交换绝不能夹在两个递归中间** —— 交换改变了 `root.left` / `root.right` 的指向，会让已翻好的子树白翻、真正的另一侧一次没翻。
- 易错点：104 返回的是节点数（543 直径返的是边数，差 1）；226 忘了 `return root` 会返回 `None`；深偏斜树会爆 Python 默认递归上限 1000，104 可改 BFS，226 可改显式栈迭代。

## 答案

### LC 104

#### 解法一：后序递归（时间 O(n) / 空间 O(h)）

```python
class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

#### 解法二：BFS 层序数层数（时间 O(n) / 空间 O(n)）

树很深、递归会爆栈时用这个（没有递归深度限制）。

```python
from collections import deque

class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        q = deque([root])
        depth = 0
        while q:
            depth += 1
            for _ in range(len(q)):        # ← 关键：先锁住这一层的节点数（LC 102 的坑）
                node = q.popleft()
                if node.left:  q.append(node.left)
                if node.right: q.append(node.right)
        return depth
```

#### Java 版

```java
// LC 104
class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }
}
```

### LC 226

#### 解法一：前序递归，先交换再递归（时间 O(n) / 空间 O(h)）

```python
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:
        if not root:
            return None
        root.left, root.right = root.right, root.left   # 换掉自己的两个孩子
        self.invertTree(root.left)                     # 递归左边
        self.invertTree(root.right)                    # 递归右边
        return root
```

#### Java 版

```java
// LC 226
class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) return null;
        TreeNode tmp = root.left;          // Java 不能像 Python 那样一行交换，得借临时变量
        root.left  = root.right;
        root.right = tmp;
        invertTree(root.left);
        invertTree(root.right);
        return root;
    }
}
```
