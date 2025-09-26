# Log API

The Log API provides structured logging with automatic timestamps and log file management.

## Class Reference

::: toolos.api.LogAPI

## Basic Usage

```python
from toolos.api import LogAPI

# Initialize with log directory
log = LogAPI("data/logs")

# Write log entries
log.WriteLog("app.log", "Application started")
log.WriteLog("error.log", f"Error occurred: {error_message}")
log.WriteLog("debug.log", f"Processing item {item_id}")

# Read log file
if log.LogExists("app.log"):
    log_content = log.ReadLog("app.log")
    print(log_content)

# Clear log file
log.ClearLog("old_errors.log")

# Delete log file
log.DeleteLog("temporary.log")
```

## Log Format

All log entries are automatically timestamped in ISO format:

```
[2024-09-26T10:30:45.123456] Application started
[2024-09-26T10:30:46.234567] User logged in: john_doe
[2024-09-26T10:30:47.345678] Processing request #12345
```

## Methods

### `WriteLog(filename, message)`
Appends a timestamped message to the specified log file.

### `ReadLog(filename)`
Reads the entire content of a log file.

### `DeleteLog(filename)`
Deletes a log file completely.

### `ClearLog(filename)`
Clears the content of a log file (makes it empty).

### `LogExists(filename=None)`
Checks if log file or directory exists.