# file.path.remove_last_component

Purpose: Remove the last path component. Available after 20250914.

## Signature
```lua
parent, err = file.path.remove_last_component(path)
```

## Example
```lua
local parent = file.path.remove_last_component('/usr/local/bin') -- '/usr/local'
local root = file.path.remove_last_component('/usr') -- '/'
local unchanged = file.path.remove_last_component('/') -- '/'
```

## Parameters
- `path`: original path string.

## Returns
The new path string; invalid path: `nil, "Invalid path"`.

## Notes
Only changes the string, without deleting files/directories. `/usr` and `/` both produce `/`.
