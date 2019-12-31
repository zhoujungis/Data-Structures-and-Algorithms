from error import GraphError
from stack import SStack
from queue import SQueue
from prioqueue import PrioQueue

inf = float("inf")

# 基于邻接矩阵实现图
class Graph:
    def __init__(self, mat, unconn=0):
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise GraphError("Argument for 'Graph'.")
            self._mat = [mat[i][:] for i in range(vnum)]
            self._unconn = unconn
            self._vnum = vnum

    def vertex_num(self):
        return self._vnum

    def _invalid(self, v):
        return 0 > v or v >= self._vnum

    def add_vertex(self):
        raise GraphError("Adj-Matrix does not support 'add_vertex'.")

    def add_edge(self, vi, vj, val=1):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + " or " + str(vj) + " is not a valid vertex.")
        self._mat[vi][vj] = val

    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + " or " + str(vj) + " is not a valid vertex.")    
        return self._mat[vi][vj]

    def out_edges(self, vi):
        if self._invalid(vi):
            raise GraphError(str(vi) + " is not a valid vertex.")
        return self._out_edges(self._mat[vi], self._unconn)

    @staticmethod
    def _out_edges(row, unconn):
        edges = []
        for i in range(len(row)):
            if row[i] != unconn:
                edges.append((i, row[i]))
        return edges

    def __str__(self):
        return "[\n" + ",\n".join(map(str, self._mat)) + "\n]"
                + "\nUnconnected: " + str(self._unconn)


# 基于邻接表实现
class GraphAL(Graph):
    def __init__(self, mat=[], unconn=0):
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise GraphError("Argument for 'Graph'.")
        self._mat = [Graph._out_edges(mat[i], unconn) for i in range(vnum)]
        self._vnum = vum
        self._unconn = unconn

    def add_vertex(self):
        self._mat.append([])
        self._vnum += 1
        return self._vnum - 1

    def add_edge(self, vi, vj, val=1):
        if self._vnum == 0:
            raise GraphError("Cannot add edge tp empty graph.")
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + " or " + str(vj) + " is not a valid vertex.")

        row = self._mat[vi]
        i = 0
        while i < len(row):
            if row[i][0] == vj:
                self._mat[vi][i] = (vj, val)
                return
            if row[i][0] > vj:
                break
            i += 1
        self._mat[vi].insert((i, val))

    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + " or " + str(vj) + " is not a valid vertex.")

        for i, val in self._mat[vi]:
            if i == vj:
                return val
        return self._unconn

    def out_edges(self, vi):
        if self._invalid(vi):
            raise GraphError(str(vi) + " is not a valid vertex.")
        return self._mat[vi]


# 图的遍历——深度优先和广度优先遍历
# 深度优先遍历
def DFS_graph(graph, v0):
    vnum = graph.vertex_num()
    visited = [0] * vnum
    visited[v0] = 1
    DFS_seq = [v0]
    st = SStack()
    st.push((0, graph.out_edges(v0)))
    while not st.is_empty():
        i, edges = st.pop()
        if i < len(edges):
            v, e = edges[i]
            st.push((i+1, edges))
            if not visited[v]:
                DFS_seq.append(v)
                visited[v] = 1
                st.push((0, graph.out_edges(v)))
    return DFS_seq

# 广度优先遍历
def BFS_graph(graph, v0):
    vnum = graph.vertex_num()
    visited = [0] * vnum
    visited[v0] = 1
    BFS_seq = [v0]
    qu = SQueue()
    qu.enqueue(graph.out_edges(v0))
    while not qu.is_empty():
        edges = qu.dequeue()
        for i in range(len(edges)):
            v, e = edges[i]
            if not visited[v]:
                BFS_seq.append[v]
                visited[v] = 1
                qu.enqueue(graph.out_edges(v))
    return BFS_seq

# 生成树
def DFS_span_forest(graph):
    vnum = graph.vertex_num()
    spam_forest = [None] * vnum

    def dfs(graph, v):
        nonlocal span_forest
        for u, w in graph.out_edges(v):
            if span_forest[u] is None:
                span_forest[u] = (v, w)
                dfs(graph, u)

    for v in range(vnum):
        if span_forest[v] is None:
            span_forest[v] = (v, 0)
            dfs(graph, v)

    return span_forest


# 最小生成树
# Kruskal算法
def Kruskal(graph):
    vnum = graph.vertex_num()
    reps = [i for i in range(vnum)]
    mst, edges = [], []
    for vi in range(vnum):
        for v, w in graph.out_edges(vi):
            edges.append((w, vi, v))
    edges.sort()
    for w, vi, vj in edges:
        if reps[vi] != reps[vj]: # 位于不同的连通分量
            mst.append(((vi, vj), w))
            if len(mst) == vnum-1: # 若已存在vnum-1条边
                break
            # 合并连通分量
            rep, orep = reps[vi], reps[vj]
            for i in range(vnum):
                if reps[i] == orep:
                    reps[i] = rep
    return mst

# Prim算法
def Prim(graph):
    vnum = graph.vertex_num()
    mst = [None] * vnum
    cands = PrioQueue([(0, 0, 0)]) # 记录侯选边(w, vi, vj)
    count = 0
    while count < vnum and not cands.is_empty():
        w, u, v = cands.dequeue()  # 取当前最短边
        if mst[v]:
            continue
        mst[v] = ((u, v), w) # 记录新的边
        count += 1
        for vi, w in graph.out_edges(v):
            if not mst[vi]: # 如果vi不在mst中则作为侯选边
                cands.enqueue((w, v, vi))
    return mst


# 最短路径算法
# 单源点最短路径Dijkstra算法
def dijkstra(graph, v0):
    vnum = graph.vertex_num()
    assert 0 <= v0 < vnum
    paths = [None] * vnum
    count = 0
    cands = PrioQueue([(0, v0, v0)])
    while count < vnum and not cands.is_empty():
        plen, u, vmin = cands.dequeue()
        if paths[vmin]:
            continue
        paths[vmin] = (u, plen)
        for v, w in graph.out_edges(vmin):
            if not graph[v]:
                cands.enqueue((plen+w, vmin, v))
        count += 1
    return paths

# 任意点最短路径Floyd算法
def floyd(graph):
    vnum = graph.vertex_num()
    a = [[graph.get_edge(i, j) for j in range(vnum)] for i in range(vnum)]
    nvertex = [[-1 if a[i][j] == inf else j for j in range(vnum)] for i in range(vnum)]
    for k in range(vnum):
        for i in range(vnum):
            for j in range(vnum):
                if a[i][j] > a[i][k] + a[k][j]:
                    a[i][j] = a[i][k] + a[k][j]
                    nvertex[i][j] = nvertex[i][k]
    return (a, nvertex)


# AOV网与topo排序
def toposort(graph):
     vnum = graph.vertex_num()
     indegree, toposeq = [0]*vnum, []
     zerov = -1
     for vi in range(vnum):
          for v, w in graph.out_edges(vi):
               indegree[v] += 1
     for vi in range(vnum):
          if indegree[vi] == 0:
               indegree[vi] = zerov
               zerov = vi
     for n in range(vnum):
          if zerov == -1:
               return False
          vi = zerov
          zerov = indegree[zerov]
          toposeq.append(vi)
          for v, w in graph.out_edges(vi):
               indegree[v] -= 1
               if indegree[v] == 0:
                    indegree[v] = zerov
                    zerov = v
     return toposeq


# AOE网与关键路径
def critical_paths(graph):
    def events_earliest_time(vnum, graph, toposeq):
        ee = [0] * vnum
        for i in toposeq:
            for j, w in graph.out_edges(i):
                if ee[i] + w > ee[j]:
                    ee[j] = ee[i] + w
        return ee

    def events_latest_time(vnum, graph, toposeq, eelast):
        le = [eelast] * vnum
        for k in range(vnum-2, -1, -1):
            i = toposeq[k]
            for j, w in graph.out_edges(i):
                if le[j] - w < le[i]:
                    le[i] = le[j] - w
        return le

    def crt_paths(vnum, graph, ee, le):
        crt_actions = []
        for i in range(vnum):
            for j, w in graph.out_edges(i):
                if ee[i] == le[j] - w:
                    crt_actions.append((i, j, ee[i]))
        return crt_actions

    toposeq = toposort(graph)
    if not toposeq:
        return False
    vnum = graph.vertex_num()
    ee = events_earliest_time(vnum, graph, toposeq)
    le = events_latest_time(vnum, graph, toposeq, ee[vnum-1])
    return crt_paths(vnum, graph, ee, le)
