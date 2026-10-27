# 【LC 124】二叉树最大路径和：返回值只选一条

**来源**: https://zhoujungis.github.io/article/lc-124-binary-tree-maximum-path-sum/
**标签**: 算法、二叉树、LeetCode、面试
**难度**: 困难

## 题目

**路径**被定义为一条节点序列，序列中每对相邻节点之间都存在一条边。同一个节点在一条路径序列中**至多出现一次**。该路径**至少包含一个节点**，且**不一定经过根节点**。

**路径和**是路径中各节点值的总和。给你一个二叉树的根节点 `root`，返回其**最大路径和**。

```
输入：root = [-10,9,20,null,null,15,7]
输出：42
解释：最优路径是 15 → 20 → 7，路径和为 15 + 20 + 7 = 42

输入：root = [1,2,3]
输出：6
解释：最优路径是 2 → 1 → 3

输入：root = [-3]
输出：-3
```

约束：`-1000 <= Node.val <= 1000`；节点数不超过 `3×10^4`。输入用 LeetCode 的层序数组编码，空缺位置用 `null` 占位。

## 思路

- 因为同一节点至多出现一次，树上任意一条路径必有一个唯一的「最高点」（拐弯处）：要么是直链（只有一条向下的胳膊），要么是拱形（左右各一条胳膊）。
- 于是对每个节点算「以它为最高点的最优路径」，再取全局最大，整体 O(n)。
- 关键难点是同一节点要同时算**两个不同的量**：向上汇报的贡献值 `gain = val + max(左, 右)`（只能带一条胳膊），和以自己为拱顶的答案 `through = val + 左 + 右`（两条胳膊都用，到此为止）。
- 返回值不能写成 `val + left + right`：父节点拿到后还会再拐一次，两次拐弯就成树杈，不是路径了。
- `max(gain, 0)` 是算法的核心剪枝而不是判空 —— 负的胳膊接进来只会让和更小，返回 0 表示「别走这边」。
- `best` 必须初始化成 `-inf` 而不是 0，因为「路径至少包含一个节点」，全负树（如 `[-3]`）会暴露初值错误。

## 答案

### 解法一：后序树形 DP（时间 O(n) / 空间 O(h)）

```python
class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        self.best = -float('inf')          # ← 不能是 0：路径至少含一个节点

        def gain(node: TreeNode) -> int:
            """返回 node 向上汇报的贡献值（一条胳膊的直链最大和）。"""
            if not node:
                return 0
            left  = max(gain(node.left),  0)    # ← 负贡献直接剪掉
            right = max(gain(node.right), 0)

            # ① 以 node 为拱顶的完整路径（两条胳膊），用它更新全局最优
            self.best = max(self.best, node.val + left + right)

            # ② 向上汇报的贡献值（只能选一条胳膊）
            return node.val + max(left, right)

        gain(root)
        return self.best
```

### Java 版

```java
class Solution {
    private int best = Integer.MIN_VALUE;

    public int maxPathSum(TreeNode root) {
        gain(root);
        return best;
    }

    private int gain(TreeNode node) {
        if (node == null) return 0;
        int left  = Math.max(gain(node.left),  0);
        int right = Math.max(gain(node.right), 0);

        // ① 拱顶路径：两条胳膊都用
        best = Math.max(best, node.val + left + right);

        // ② 向上贡献：只选一条胳膊
        return node.val + Math.max(left, right);
    }
}
```
