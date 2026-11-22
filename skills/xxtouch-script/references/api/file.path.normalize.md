# file.path.normalize

Purpose: Normalize a path. Available after 20250914.

## Signature
```lua
normalized, err = file.path.normalize(path)
```

## Example
```lua
local normalized = file.path.normalize('/usr/local/../bin/./script') -- '/usr/bin/script'
local clean = file.path.normalize('//tmp///file/') -- '/tmp/file'
```

## Parameters
- `path`: original path string.

## Returns
The normalized path string; invalid path: `nil, "Invalid path"`.

## Notes
Processes `.` and `..` components and redundant slashes without moving or renaming files/directories. For symbolic links, use [`file.path.resolve_symlinks`](file.path.resolve_symlinks.md).
