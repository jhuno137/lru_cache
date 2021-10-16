import random
import unittest
from cache.lru import LRUCache, CacheNode


class TestLRUCache(unittest.TestCase):
	def test_it_raises_exception_for_invalid_capacity(self):
		for capacity in [-1, 0]:
			self.assertRaises(ValueError, LRUCache, capacity)

	def test_cache_does_not_go_over_capacity(self):
		for m in range(10):
			capacity = random.randint(1, 100)
			cache = LRUCache(capacity)
			number_cache_elements = random.randint(100, 200)
			for n in range(number_cache_elements):
				cache.put(str(n), n)
				self.assertLessEqual(cache._get_size(), capacity)

	def test_it_gets_the_values(self):
		for m in range(10):
			capacity = random.randint(10, 1000)
			cache = LRUCache(capacity)
			for n in range(capacity):
				cache.put(str(n), n)

			for n in range(capacity):
				self.assertEqual(cache.get(str(n)), n)

	def test_it_pops_least_recently_used_cache(self):
		for m in range(10):
			capacity = random.randint(1, 1000)
			cache = LRUCache(capacity)
			for n in range(capacity):
				# fill cache up to capacity
				cache.put(str(n), n)

			# Adding one more element to the cache should result in a cache
			# miss for the first element inserted
			cache.put("foo", "bar")
			self.assertEqual(cache.get("0"), None)

	def test_it_resets_the_cache(self):
		for m in range(10):
			capacity = random.randint(1, 1000)
			cache = LRUCache(capacity)
			for n in range(capacity):
				# fill cache up to capacity
				cache.put(str(n), n)

			cache.reset()
			self.assertEqual(cache._head, None, f"Using capacity of {capacity}")
			self.assertEqual(cache._tail, None)
			self.assertEqual(cache._get_size(), 0)

	def test_it_deletes(self):
		cache = LRUCache(10)
		for n in range(5):
			cache.put(str(n), n)

		self.assertEqual(cache.get("3"), 3)
		cache.delete("3")
		self.assertEqual(cache.get("3"), None)
		self.assertEqual(cache._get_size(), 4)

	def test_dll_head_and_tail_are_set_at_get_and_put(self):
		cache = LRUCache(10)
		for n in range(5):
			cache.put(str(n), n)
			self.assertEqual(cache._head.value, n)
			if n == 0:
				# the first time around there is no tail, just head
				self.assertEqual(cache._tail, None)
			else:
				# tail should be set and have the proper value
				self.assertEqual(cache._tail.value, 0)

		self.assertEqual(cache.get("0"), 0)
		self.assertEqual(cache._tail.value, 1)

		for n in range(5, 10):
			# fil the cache up to capacity
			cache.put(str(n), n)
			self.assertEqual(cache._head.value, n)
			self.assertEqual(cache._tail.value, 1)

		cache.put("foo", "bar") 	# when adding a new item, cache needs to evict current current tail
		self.assertEqual(cache._tail.value, 2)

	def test_dll_has_the_same_size_as_the_cache(self):
		for m in range(10):
			capacity = random.randint(1, 1000)
			cache = LRUCache(capacity)
			for n in range(capacity):
				cache.put(str(n), n)

			cache.put("foo", "bar")

			size = self._get_dll_size(cache._head)
			self.assertEqual(cache._get_size(), size)

			cache.delete("foo")
			size = self._get_dll_size(cache._head)
			self.assertEqual(cache._get_size(), size)

			cache.reset()
			size = self._get_dll_size(cache._head)
			self.assertEqual(size, 0)

	@staticmethod
	def _get_dll_size(head: CacheNode) -> int:
		"""
		Get the doubly linked list size
		:param head:
		:return:
		"""
		if head is None:
			return 0
		node = head
		size = 1
		while node.next is not None:
			size += 1
			node = node.next

		return size


if __name__ == "__main__":
	unittest.main()
