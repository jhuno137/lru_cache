from cache.lru import LRUCache
from string import ascii_lowercase

# LRUCache usage example
# We will read files from the file system
# or the cache when available
cache = LRUCache(10)


def get_file_content(file_name):
	content = cache.get(file_name)
	if content is None:
		# cache miss
		print(f"Reading {file_name} content from file system")
		with open(file_name, 'rb') as f:
			content = f.read()
			cache.put(file_name, content)  # warming up the cache
	else:
		print(f"Reading {file_name} content from cache")

	return content


if __name__ == "__main__":
	a = get_file_content("files/a.txt") 		# Reading from file system
	a_cache = get_file_content("files/a.txt") 	# reading from cache
	assert a == a_cache 						# same content either from file system or cache

	cache.reset()
	assert cache.get("files/a.txt") is None		# After clearing the cache all elements are removed

	for c in ascii_lowercase[0:11]:
		get_file_content(f"files/{c}.txt")

	print(cache.get("files/a.txt"))		# None as capacity was 10
	print(cache.get("files/k.txt")) 	# Content of k.txt (last cache element)
	print(cache.get("files/b.txt")) 	# content of b.txt (now first cache element)


