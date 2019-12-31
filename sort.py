# 排序算法
# 冒泡排序
def bubble_sort(lst):
     l = len(lst)
     for i in range(l):
          for j in range(l-i-1):
               if lst[j] > lst[j+1]:
                    lst[j], lst[j+1] = lst[j+1], lst[j]
# 改进版1.0
def bubble_sort1(lst):
     l = len(lst)
     for i in range(l):
          isSorted = True
          for j in range(l-i-1):
               if lst[j] > lst[j+1]:
                    lst[j], lst[j+1] = lst[j+1], lst[j]
                    isSorted = False
          if isSorted:
               break
# 改进版2.0
def bubble_sort2(lst):
     l = len(lst)
     lastExchangeIndex = 0
     sortBorder = l - 1
     for i in range(l):
          isSorted = True
          for j in range(sortBorder):
               if lst[j] > lst[j+1]:
                    lst[j], lst[j+1] = lst[j+1], lst[j]
                    isSorted = False
                    lastExchangeIndex = j
          sortBorder = lastExchangeIndex
          if isSorted:
               break


# 插入排序
def insert_sort(lst):
     for i in range(1, len(lst)):
          x = lst[i]
          j = i
          while j > 0 and lst[j-1] > x:
               lst[j] = lst[j-1]
               j -= 1
          lst[j] = x


# 选择排序
def select_sort(lst):
     for i in range(len(lst)-1):
          k = i
          for j in range(i, len(lst)):
               if lst[j] < lst[k]:
                    k = j
          if i != k:
               lst[i], lst[k] = lst[k], lst[i]


# 快速排序
# 递归版
def quick_sort(lst):
     return qSort(lst, 0, len(lst)-1)

def qsort(lst, left, right):
     if left < right:
          tmp = partion(lst, left, right)
          qsort(lst, left, tmp-1)
          qsort(lst, tmp+1, right)

def partion(lst, left, right):
     key = lst[left]
     while left < right:
          while left < right and lst[right] >= key:
               right -= 1
          if left < right:
               lst[left],lst[right] = lst[right],lst[left]
          while left < right and lst[left] < key:
               left += 1
          if left < right:
               lst[right],lst[left] = lst[left],lst[right]
     return left

# 非递归版
def quick_sort_norec(lst):
     l, r = 0, len(lst)-1
     if l >= r:
          return
     stack = []
     stack.append(l)
     stack.append(r)
     while stack:
          low = stack.pop(0)
          high = stack.pop(0)
          if high - low <= 0:
               continue
          x = lst[high]
          i = low - 1
          for j in range(low, high):
               if lst[j] <= x:
                    i += 1
                    lst[i], lst[j] = lst[j], lst[i]
          lst[i + 1], lst[high] = lst[high], lst[i + 1]
          stack.extend([low, i, i + 2, high])


# 归并排序
def merge(lfrom, lto, low, mid, high):
     i, j, k = low, mid, low
     while i < mid and j < high:
          if lfrom[i] <= lfrom[j]:
               lto[k] = lfrom[i]
               i += 1
          else:
               lto[k] = lfrom[j]
               j += 1
          k += 1
     while i < mid:
          lto[k] = lfrom[i]
          i += 1
          k += 1
     while j < high:
          lto[k] = lfrom[j]
          j += 1
          k += 1

def merge_pass(lfrom, lto, llen, slen):
     i = 0
     while i + 2 * slen < llen:
          merge(lfrom, lto, i, i + slen, i + 2 * slen)
          i += 2 * slen
     if i + slen < llen:
          merge(lfrom, lto, i, i + slen, llen)
     else:
          for j in range(i, llen):
               lto[j] = lfrom[j]

def merge_sort(lst):
     slen, llen = 1, len(lst)
     tmp = [None] * llen
     while slen < llen:
          merge_pass(lst, tmp, llen, slen)
          slen *= 2
          merge_pass(tmp, lst, llen, slen)
          slen *= 2


# 堆排序
def heapify(lst, n, i):
     largest = i
     l, r = 2 * i + 1, 2 * i + 2
     if l < n and lst[i] < lst[l]:
          largest = l
     if r < n and lst[largest] < lst[r]:
          largest = r
     if largest != i:
          lst[i], lst[largest] = lst[largest], lst[i]
          heapify(lst, n, largest)
               
def heap_sort(lst):
     n = len(lst)
     # 初始建堆
     for i in range(n, -1, -1):
          heapify(lst, n, i)
     # 交换
     for i in range(n-1, 0, -1):
          lst[i], lst[0] = lst[0], lst[i]
          heapify(lst, i, 0)


# 拓扑排序
def topo_sort(graph):
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


# 希尔排序
def shell_sort(lst):
     n = len(lst)
     gap = int(n/2)
     while gap > 0:
          for i in range(gap, n):
               tmp = lst[i]
               j = i
               while j >= gap and lst[j-gap] > tmp:
                    lst[j] = lst[j-gap]
                    j -= gap
               lst[j] = tmp
          gap = int(gap/2)
