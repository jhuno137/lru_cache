class CacheNode(object):
    """
    Cache node contains the key and value of the cached item.
    By default pointers to neighbour nodes, if any, are unlinked
    """
    def __init__(self, key: str, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class LRUCache(object):
    """"
    Implementation of a Least Recent Use cache using a Doubly Linked List (DLL)
    and a dictionary (hash map) which allows O(1) the retrieval of cache elements
    The main (private) operations on cache elements are:
    * _push: to add an element on the top of the cache (head of the DLL)
    * _pop: to remove the least used element (tail of the DLL by construction) when the cache
            reaches it's maximum capacity

    There is also a (private) helper method _get_size() to retrieve the current cache size

    The public API consists of three methods:

    * get(key) : to retrieve an elemnt from the cache
    * put(key, value): to add a new element or update an existing one from the cache
    * reset(): clears the cache
    """
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError(f"Capacity must be at least one, {capacity} given.")
        self._capacity = capacity
        self._cache = {}
        self._head = None
        self._tail = None

    # Public API
    def get(self, key: str):
        """
        Get an element from the cache by it's key.
        On cache miss return None
        """
        if key in self._cache:
            node = self._cache[key]
            self._push(node)
            return node.value

        return None

    def put(self, key: str, value) -> None:
        """
        Add or update an element to the cache.
        If the cache reaches maximum capacity then
        the last element of the list is deleted
        :param key:
        :param value:
        :return:
        """
        if key in self._cache:
            node = self._cache[key]
        else:
            node = CacheNode(key, value)
            self._cache[key] = node

        self._push(node)

        if self._get_size() > self._capacity:
            del self._cache[self._tail.key]
            self._pop()

    def delete(self, key) -> None:
        if key in self._cache.keys():
            node = self._cache[key]
            self._unlink(node)
            del self._cache[key]

    def reset(self) -> None:
        """
        Clear the cache
        :return:
        """
        self._cache.clear()
        self._head = None
        self._tail = None

    # Private methods to manage push and pop operations to/from the DLL

    def _get_size(self) -> int:
        """
        Get cache size
        """
        return len(self._cache)

    def _push(self, node):
        """
        Set node as head
        Two edge cases are considered;
        1. When the list is empty and we are adding a new element to the cache, this element is automatically the head
           of the DLL
        2. When the DLL only contains the head (there is only one element in the cache) then the second element is set
           as the tail of the DLL
        """
        size = self._get_size()
        if size == 1:
            # This is the first node -> set it as head
            self._head = node
            return

        node.next = self._head
        self._head.prev = node
        self._head = node

        if size == 2:
            # this was the second node -> set it as tail
            self._tail = self._head.next
            self._tail.next = None

    def _pop(self) -> None:
        """
        Remove the last node (tail) from the DLL
        :return: None
        """
        if self._tail is not None:
            new_tail = self._tail.prev
            new_tail.next = None
            self._tail = new_tail

    def _unlink(self, node):
        if node is self._head:
            if self._head.next is not None:
                new_head = self._head.next
                new_head.prev = None
                self._head = new_head
        elif node is self._tail:
            self._pop()
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            node.next = None
            node.prev = None

