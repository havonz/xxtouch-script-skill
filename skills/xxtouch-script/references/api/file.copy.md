# file.copy

Purpose: Copy a file or directory. Available after 20250313.

## Signature
```lua
ok, err = file.copy(src, dst [, mode])
```

## Example
```lua
-- Assume /d/e exists; the final destination includes the source name.
local ok, err = file.copy('/a/b/c', '/d/e/c')
nLog(ok, err)
-- Alternative: replace /d/e/c itself (20250914+).
-- file.copy('/a/b/c', '/d/e/c', 'overwrite')
```

## Parameters
- `src`: string, absolute source file/directory path.
- `dst`: string, complete absolute destination, including the file/directory name.
- `mode`: optional string, supported after 20250914:
  - Omitted or `""`: fail if the destination exists.
  - `"overwrite"` / `"o"`: delete and replace the destination itself.
  - `"merge"` / `"m"`: merge directories, keeping existing destination files.
  - `"overwrite-merge"` / `"om"` / `"mo"`: merge directories, overwriting same-name files.

## Returns
`ok`: boolean success; `err`: error string on failure.

## Notes
`dst` is the final target, not a containing directory. An existing directory or trailing `/` never causes the source name to be appended: `/d/e/` targets `e` itself, not `/d/e/c`. Directory merge modes merge source contents into the destination.
To build a destination that keeps the source name, use [`file.path.last_component`](file.path.last_component.md) and [`file.path.add_component`](file.path.add_component.md).
