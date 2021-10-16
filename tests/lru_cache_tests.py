import random
import unittest
from cache.lru import LRUCache


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


if __name__ == "__main__":
	unittest.main()
