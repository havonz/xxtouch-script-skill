# file.path.components

Purpose: Split a path into ordered components. Available after 20250914.

## Signature
```lua
components, err = file.path.components(path)
```

## Example
```lua
local parts = file.path.components('/usr/local/bin') -- {'/', 'usr', 'local', 'bin'}
```

## Parameters
- `path`: string to split.

## Returns
A string array (table); invalid path: `nil, "Invalid path"`.

## Notes
Absolute paths include `/` as a separate root component.
