# Temp API

The Temp API manages temporary files with automatic cleanup capabilities.

## Class Reference

::: toolos.api.TempAPI

## Basic Usage

```python
from toolos.api import TempAPI

# Initialize with temp directory
temp = TempAPI("data/temp")

# Write temporary file
temp.WriteTempFile("session.json", json.dumps(session_data))

# Read temporary file
if temp.TempExists("session.json"):
    data = temp.ReadTempFile("session.json")

# Clean up all temp files
temp.RemoveTempFile()  # Removes all files

# Remove specific temp file
temp.RemoveTempFile("old_session.json")
```

## Methods

### `WriteTempFile(filename, content)`
Writes content to a temporary file.

### `ReadTempFile(filename)`
Reads content from a temporary file.

### `AddContent(filename, content)`
Appends content to a temporary file.

### `RemoveTempFile(filename=None)`
Removes temp file(s). If no filename provided, removes all temp files.

### `TempExists(filename=None)`
Checks if temp file or directory exists.