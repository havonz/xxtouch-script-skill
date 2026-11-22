# file.path.last_component

Purpose: Get the last path component. Available after 20250914.

## Signature
```lua
name, err = file.path.last_component(path)
```

## Example
```lua
local name = file.path.last_component('/usr/local/bin') -- 'bin'
local root = file.path.last_component('/') -- '/'
```

## Parameters
- `path`: path string.

## Returns
The last component as a string; invalid path: `nil, "Invalid path"`.

## Notes
The root directory `/` returns `/`.
