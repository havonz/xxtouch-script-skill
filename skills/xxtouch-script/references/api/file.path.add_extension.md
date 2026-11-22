# file.path.add_extension

Purpose: Append a file extension. Available after 20250914.

## Signature
```lua
new_path, err = file.path.add_extension(path, extension)
```

## Example
```lua
local backup = file.path.add_extension('/path/file.txt', 'bak') -- '/path/file.txt.bak'
local dotted = file.path.add_extension('/path/file', '.txt') -- '/path/file..txt'
```

## Parameters
- `path`: base path string.
- `extension`: string to append, usually without a leading `.`.

## Returns
The new path string, or nil if appending fails. Invalid path/extension strings return `nil, "Invalid path"` / `nil, "Invalid extension"`; an extension containing `/` may return nil without an error message.

## Notes
Appends `.` plus the extension after any existing extension. A supplied leading `.` is not removed. Does not rename files/directories.
