# 【LC 146】LRU 缓存：手写哈希表与双向链表

**来源**: https://zhoujungis.github.io/article/lc-146-lru-cache/
**标签**: 算法、设计题、哈希表、链表、LeetCode、面试

## 题目

**LC 146 LRU 缓存**：请你设计并实现一个满足 **LRU（最近最少使用）** 缓存约束的数据结构。

- `LRUCache(int capacity)`：以正整数 `capacity` 初始化；
- `int get(int key)`：如果 key 存在，返回其值，否则返回 `-1`；
- `void put(int key, int value)`：key 存在则改值；不存在则插入；**容量满时淘汰最久未使用的那一个**；
- **`get` 和 `put` 必须都是 O(1)**。

要求**手写双向链表 + 哈希表**（禁用 `LinkedHashMap` / `OrderedDict` 这类现成结构）。

标准用例：

```
LRUCache(2)
put(1,1); put(2,2)        → 链表: [1] → [2,1]
get(1)                    → 返回 1,  链表重排: [1,2]
put(3,3)                  → 淘汰 2,  链表: [3,1]
get(2)                    → -1
put(4,4)                  → 淘汰 1,  链表: [4,3]
get(1) → -1; get(3) → 3; get(4) → 4
```

## 思路

- **O(1) 的两条腿**：哈希表 `key → 节点` 负责「一步找到」，双向链表按使用顺序排队（队首 = 最近使用，队尾 = 最久未使用 / 淘汰对象），缺一不可 —— 只用哈希表淘汰要扫全表，只用链表查找是 O(n)。
- **必须是双向链表**：`get` 命中后要把节点从链表**中间**摘下来移到队首，单向链表找不到前驱只能从头扫（O(n)），双向链表有 `prev`，摘除本身 O(1)。
- **两个哨兵**：`head` / `tail` 让任何节点的 `prev` / `next` 都非空，插入和摘除**永远不需要判空**，容量为 1 时也不用特判。
- **三个固定动作**：`addToFront`（头插）、`unlink`（摘除）、`moveToFront` = `unlink` + `addToFront`；把这些指针顺序背下来就不会写错。
- **`put` 的三种情形**：key 已存在（改值 + 移到队首，**改值也算一次使用**）、容量未满（直接头插）、容量已满（先摘队尾**双删**再头插）。
- **易错点**：淘汰时必须链表摘尾的**同时** `del cache[key]`，只摘链表会留下幽灵节点（下次 `get` 摸到已脱链的节点），只删表则链表泄漏。

## 答案

### 解法一：哈希表 + 手写双向链表（时间 O(1) / 空间 O(capacity)）

```python
class Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}                    # key -> Node
        self.head = Node()                 # 哨兵：head.next 才是第一个真节点
        self.tail = Node()                 # 哨兵：tail.prev 才是最后一个真节点
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_front(self, node):
        self._unlink(node)
        self._add_to_front(node)

    def get(self, key: int) -> int:
        node = self.cache.get(key)
        if node is None:
            return -1
        self._move_to_front(node)          # 命中 = 使用
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.cache.get(key)
        if node is not None:
            node.value = value
            self._move_to_front(node)      # 改值也算使用！
            return
        if len(self.cache) == self.cap:    # 容量满：先淘汰队尾
            victim = self.tail.prev
            self._unlink(victim)
            del self.cache[victim.key]     # 两处都要删，漏一个就是幽灵节点
        node = Node(key, value)
        self.cache[key] = node
        self._add_to_front(node)
```

### Java 版

```java
class LRUCache {
    private static final class Node {
        int key, value;
        Node prev, next;
        Node(int k, int v) { key = k; value = v; }
    }

    private final int capacity;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0);   // 哨兵
    private final Node tail = new Node(0, 0);   // 哨兵

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) return -1;
        moveToFront(node);
        return node.value;
    }

    public void put(int key, int value) {
        Node node = map.get(key);
        if (node != null) {
            node.value = value;
            moveToFront(node);
            return;
        }
        if (map.size() == capacity) {
            Node victim = tail.prev;            // 队尾 = 最久未使用
            remove(victim);
            map.remove(victim.key);             // 双删
        }
        Node fresh = new Node(key, value);
        map.put(key, fresh);
        addToFront(fresh);
    }

    private void addToFront(Node node) {
        node.prev = head;
        node.next = head.next;
        head.next.prev = node;
        head.next = node;
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void moveToFront(Node node) {
        remove(node);
        addToFront(node);
    }
}
```
