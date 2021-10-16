# LRUCache Documentation (Linux/OS X)

## Using the LRU cache

From the root of the project (see main.py as a concrete example) import LRUCache:

```python
from cache.lru import LRUCache

cache = LRUCache(5)                 # instantiate a cache instance of capacity 5
cache.put("foo", "bar")             # add an element to the cache
cache.put("secret", 1234)
cache.put("user_id", 789)
cache.get("secret")                 # read and element from the cache
cache.put("cookie", "prov=uc670a3f-79ec-44e6-f1fc-fc5c65c3d48c;")
cache.put("token", "AK3G5676TANGF098ZQ")
cache.put("form_color", "#fcaad1")  # exeding cache capacity
cache.get("foo")                    # None as item was at the end of the cache
cache.delete("cookie")              # delete an element from the cache
cache.reset()                       # clear cache
```

### The public API:<br/>
- `put(key, value)`: adds a new element to the cache<br/>
- `get(key)`: get a key vale from the cache, or `None` on miss
- `delete(key)`: delete an element from the cache if exists, otherwise nothing happens (method is idempotent)<br>
- `reset()`: clears the cache by removing all elements from it


## Run the tests
Within the project root directory run:
```commandline
export PYTHONPATH=$(pwd) && python3 tests/lru_cache_tests.py
```