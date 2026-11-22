# file.path.remove_extension

Purpose: Remove the file extension. Available after 20250914.

## Signature
```lua
new_path, err = file.path.remove_extension(path)
```

## Example
```lua
local base = file.path.remove_extension('/path/archive.tar.gz') -- '/path/archive.tar'
local unchanged = file.path.remove_extension('/path/file') -- '/path/file'
```

## Parameters
- `path`: original path string.

## Returns
The new path string; invalid path: `nil, "Invalid path"`.

## Notes
Removes only the last extension and its preceding `.`; leaves paths without an extension unchanged. Does not rename files/directories.
