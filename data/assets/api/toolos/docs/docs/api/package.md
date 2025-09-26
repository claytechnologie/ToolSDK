# Package API

The Package API provides package and mod management with simple authentication and file operations.

## Class Reference

::: toolos.api.PackageAPI

## Basic Usage

```python
from toolos.api import PackageAPI

# Initialize with package directory
package = PackageAPI("data/packages")

# Login (simple authentication)
if package.Login("admin", "password"):
    print(f"Logged in as: {package.USERNAME}")
    
    # Write package file
    package.WritePackageFile("mod_list.json", json.dumps(mod_data))
    
    # Read package file
    content = package.ReadPackageFile("mod_list.json")
    
    # Logout when done
    package.Logout()
```

## Authentication

The Package API includes basic authentication:

- Default credentials: `admin` / `password`
- Session management with `isLoggedIn` status
- Username tracking for logged-in users

## Methods

### `Login(username, password)`
Authenticates user with username and password.

### `Logout()`
Logs out current user and clears session.

### `WritePackageFile(filename, content)`
Writes content to a package file (requires login).

### `ReadPackageFile(filename)`
Reads content from a package file.

### `AddContent(filename, content)`
Appends content to a package file.

### `RemovePackageFile(filename)`
Removes a package file from the package directory.