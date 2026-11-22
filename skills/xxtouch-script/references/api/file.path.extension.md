# file.path.extension

Purpose: Get the file extension. Available after 20250914.

## Signature
```lua
extension, err = file.path.extension(path)
```

## Example
```lua
local ext = file.path.extension('/path/archive.tar.gz') -- 'gz'
local absent = file.path.extension('/path/file') -- ''
```

## Parameters
- `path`: path string.

## Returns
Extension string without the leading `.`, or `""` if absent; invalid path: `nil, "Invalid path"`.

## Notes
Uses only the final extension segment of the last path component.
