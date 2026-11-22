# file.path.resolve_symlinks

Purpose: Resolve symbolic links and normalize a path. Available after 20250914.

## Signature
```lua
resolved, err = file.path.resolve_symlinks(path)
```

## Example
```lua
-- Assume /var/mobile/link points to /var/mobile/Documents.
local resolved = file.path.resolve_symlinks('/var/mobile/link/script.lua')
-- '/var/mobile/Documents/script.lua'
```

## Parameters
- `path`: path string that may contain symbolic links.

## Returns
The resolved, normalized path string; invalid path string: `nil, "Invalid path"`.

## Notes
Results depend on actual device links. A returned path does not prove existence; missing paths or unresolved parts do not necessarily produce nil or an error. Check existence with [`file.exists`](file.exists.md).
