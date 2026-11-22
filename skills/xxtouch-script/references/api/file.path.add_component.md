# file.path.add_component

Purpose: Append a path component. Available after 20250914.

## Signature
```lua
new_path, err = file.path.add_component(path, component)
```

## Example
```lua
local full = file.path.add_component('/usr/local', 'bin') -- '/usr/local/bin'
local tmp = file.path.add_component('/', 'tmp') -- '/tmp'
```

## Parameters
- `path`: base path string.
- `component`: string to append.

## Returns
The new path string; invalid path or component: `nil, "Invalid path"`.

## Notes
Handles `/` at the join automatically; does not create files/directories.
