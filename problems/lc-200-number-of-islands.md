# 【LC 200】岛屿数量：一次染色与防爆栈替代

**来源**: https://zhoujungis.github.io/article/lc-200-number-of-islands/
**标签**: 算法、图、LeetCode、面试、并查集

## 题目

**LC 200 岛屿数量**：给你一个由 `'1'`（陆地）和 `'0'`（水）组成的二维网格 `grid`，请你计算网格中**岛屿的数量**。岛屿总是被水包围，并且每座岛屿只能由**水平方向**和/或**竖直方向**上相邻的陆地连接而成。你可以假设网格的四条边均被水包围。

```
输入: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
输出: 1

输入: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
输出: 3
```

一个 `3 × 3` 全是陆地的网格 → 输出 `1`，因为九块陆地水平竖直全连通，是**一座**岛。注意 `'1'`/`'0'` 是**字符**，也**只有上下左右**四个方向算连通，对角线不算。

## 思路

- 骨架一句话：扫描整个网格，每遇到一块「还没被访问过的」陆地，答案 `+1`，然后把与它连通的整座岛一次性「淹掉」（标记为已访问）。
- 本质是数连通块：把每块陆地看成图上的点、上下左右相邻连边，岛屿数量 = 这张图的连通块数量。两条互为镜像的路子——染色法（flood fill，DFS/BFS）与并查集（相邻即合并，剩余集合数即答案）。
- 三个细节决定成败：① 只对「未被访问的陆地」计数；② **入队/入栈即标记**（否则同一格会被多个邻居重复塞入，队列爆炸甚至超时）；③ `visited` 可独立开数组，也可原地把 `'1'` 改 `'0'`（省空间但破坏输入）。
- 递归 DFS 的隐藏代价：递归深度 = 从入口到最远的那条最长无重复连通路径，最坏 `O(m·n)`。一条蛇形长岛在 `m, n ≤ 300` 下可达 `90000` 层，Python 默认递归上限 1000 直接 `RecursionError`，Java 也会 `StackOverflowError`——「递归 DFS 能过」只是赌测试数据里没有长条连通块。
- 防爆栈两条出路：把调用栈搬到堆上（显式栈 DFS / BFS 队列，逻辑只差 LIFO 换 FIFO），或换成并查集（数连通块，全程无递归、也不依赖「一入就标」）。
- 并查集额外好处：合并成功才 `count--`，用 `union` 的返回值驱动最稳；且支持**动态加陆地**（LC 305）时增量维护答案，这是它被追问的原因。
- 易错点：`'1'` 是字符不是整数；方向只有四个；边界检查少一个就数组越界；原地改数组后原网格不可复用。

## 答案

### 解法一：BFS 染色（入队即标记，最稳）（时间 O(m·n) / 空间 O(m·n)）

```python
from collections import deque

def numIslands_bfs(grid):
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    count = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] != "1":
                continue
            count += 1
            grid[r][c] = "0"                 # 入队即标记，防止重复入队
            q = deque([(r, c)])
            while q:
                x, y = q.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == "1":
                        grid[nx][ny] = "0"   # 关键：入队时就标记
                        q.append((nx, ny))
    return count
```

### 解法二：并查集（数连通块，全程无递归）（时间 O(m·n·α) / 空间 O(m·n)）

适用于需要动态加陆地（LC 305）或想彻底避开 BFS/DFS 的场景。

```python
def numIslands_uf(grid):
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    parent = {}

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:          # 路径压缩
            parent[x], x = root, parent[x]
        return root

    count = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] != "1":
                continue
            parent[(r, c)] = (r, c)
            count += 1                    # 先各自成一个集合
            for pr, pc in ((r - 1, c), (r, c - 1)):
                if 0 <= pr < m and 0 <= pc < n and grid[pr][pc] == "1":
                    a, b = find((r, c)), find((pr, pc))
                    if a != b:
                        parent[a] = b         # 合并
                        count -= 1            # 合并成功，连通块少一个
    return count
```

### Java 版

```java
class Solution {
    // 显式栈 DFS：把"递归深度"搬到堆上的 Stack，避免 StackOverflowError
    private static final int[][] DIRS = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

    public int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0) return 0;
        int m = grid.length, n = grid[0].length, count = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] != '1') continue;
                count++;
                grid[r][c] = '0';                        // 入栈即标记
                Deque<int[]> stack = new ArrayDeque<>();
                stack.push(new int[]{r, c});
                while (!stack.isEmpty()) {
                    int[] cur = stack.pop();
                    for (int[] d : DIRS) {
                        int nx = cur[0] + d[0], ny = cur[1] + d[1];
                        if (nx >= 0 && nx < m && ny >= 0 && ny < n && grid[nx][ny] == '1') {
                            grid[nx][ny] = '0';
                            stack.push(new int[]{nx, ny});
                        }
                    }
                }
            }
        }
        return count;
    }
}
```
