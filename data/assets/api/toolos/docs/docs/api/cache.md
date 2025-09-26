# Cache API

The Cache API provides file-based caching for temporary data storage with automatic directory management.

## Class Reference

::: toolos.api.CacheAPI

## Basic Usage

```python
from toolos.api import CacheAPI

# Initialize with cache directory
cache = CacheAPI("data/cache")

# Write cache file
cache.WriteCacheFile("user_data.json", json.dumps(data))

# Read cache file
if cache.CacheExists("user_data.json"):
    data = cache.ReadCacheFile("user_data.json")
    user_data = json.loads(data)

# Append to cache file
cache.AddContent("log.txt", "New log entry")

# Remove cache file
cache.RemoveCacheFile("old_data.json")
```

## Methods

### `WriteCacheFile(filename, content)`
Writes content to a cache file with UTF-8 encoding.

### `ReadCacheFile(filename)`
Reads content from a cache file with UTF-8 encoding.

### `AddContent(filename, content)`
Appends content to an existing cache file with newline.

### `RemoveCacheFile(filename)`
Removes a cache file from the cache directory.

### `CacheExists(filename=None)`
Checks if cache file or directory exists.

## Best Practices

- Use JSON format for structured data
- Check existence before reading files
- Clean up unused cache files regularly
- Handle file I/O exceptions properly