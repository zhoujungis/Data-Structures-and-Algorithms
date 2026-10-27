# 【LC 236】二叉树的最近公共祖先：命中即返回

**来源**: https://zhoujungis.github.io/article/lc-236-lowest-common-ancestor-of-a-binary-tree/
**标签**: 算法、二叉树、LeetCode、面试
**难度**: 中等

## 题目

给定一个二叉树，找到该树中两个指定节点的**最近公共祖先**（Lowest Common Ancestor，LCA）。

> 最近公共祖先的定义：对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 **x 的深度尽可能大**（一个节点也可以是它自己的祖先）。

```
输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
输出：3
解释：节点 5 和节点 1 的最近公共祖先是节点 3。

输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
输出：5
解释：节点 5 和节点 4 的最近公共祖先是节点 5，因为根据定义最近公共祖先节点可以为节点本身。
```

输入采用 LeetCode 的**层序数组编码**：下标 `i` 的节点，左孩子在 `2i+1`、右孩子在 `2i+2`，空缺位置用 `null` 占位。节点值可以重复，判断「是不是同一个节点」必须比对象身份而非 `val`。

节点的定义（下面所有代码都用它）：

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

## 思路

- 换个问法：不问「p、q 的祖先链」，而问「站在你这个节点往下看，你的子树里能找到 p 和 q 吗」—— 问题被下沉到每个节点，一遍遍历就能解决。
- 递归返回值有**三种含义**：`None` = 子树里一个都没找到；返回 p 或 q 本身 = 只找到一个（这只是**标记**，不是答案）；返回自己 = 我就是分叉点。把「返回值是答案」和「返回值是标记」混为一谈就一定会绕晕。
- 判据：`left` 与 `right` **都非空** ⇒ p、q 分居两侧 ⇒ 当前节点是 LCA。因为递归自底向上，第一个满足该条件的节点深度最大，这就是「最近」；更上面的祖先只有一个非空，不会覆盖已经确定的答案。
- 「一个节点也可以是它自己的祖先」不需要特判：`if not root or root is p or root is q: return root` 命中即返回、不再下探。若 q 在 p 的子树里，dfs(p) 返回 p 并一路冒到根（上面的祖先右侧必为空，不会覆盖），答案自然就是 p。
- 必须是**后序**：要判断「我是不是分叉点」得先拿到左右子树的结果，而且**没有剪枝空间** —— 只找到一侧时也必须把另一侧跑完，所以时间 `O(n)` 是下界。
- 易错点：用 `root is p`（Java 用 `root == p`）而不是 `root.val == p.val`，树里允许重复值；另外不能写成「左边没找到就直接返回右边」，两棵子树都必须跑完。

## 答案

### 解法一：后序 DFS「命中即返回」（时间 O(n) / 空间 O(h)）

```python
class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        # base case 1：空节点
        # base case 2：命中 p 或 q —— 立刻返回，不再下探子树
        #             （"一个节点也可以是它自己的祖先"就靠这一行）
        if not root or root is p or root is q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)    # 左子树找到了啥
        right = self.lowestCommonAncestor(root.right, p, q)  # 右子树找到了啥

        if left and right:
            return root      # ★ 左右都非空 = 两个目标分居两侧 = root 就是 LCA
        return left or right # ★ 只有一个非空就如实上报（可能两个都空 → 返回 None）
```

### 解法二：两次 DFS 求路径后比对（时间 O(n) / 空间 O(h)）

先求根到 p、根到 q 的两条路径，再从根开始找最后一个相同的节点；直观但有内层数组、要遍历两遍，常数不如解法一。

```python
def lowestCommonAncestor(self, root, p, q):
    path_p, path_q = [], []

    def dfs(node, target, path):        # 求从根到 target 的路径
        if not node:
            return False
        path.append(node)
        if node is target:
            return True
        if dfs(node.left, target, path) or dfs(node.right, target, path):
            return True
        path.pop()                      # 回溯：这条分支里没有
        return False

    dfs(root, p, path_p)
    dfs(root, q, path_q)
    # 两条路径从根开始逐位比较，最后一个相同的节点就是 LCA
    i = 0
    while i < len(path_p) and i < len(path_q) and path_p[i] is path_q[i]:
        i += 1
    return path_p[i - 1]
```

### Java 版

```java
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        // 空节点 或 命中目标 → 返回自己（命中即返回，不再下探）
        if (root == null || root == p || root == q) return root;

        TreeNode left  = lowestCommonAncestor(root.left,  p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);

        if (left != null && right != null) return root;  // 分叉点
        return left != null ? left : right;              // 如实上报
    }
}
```
