# Replace A Range Of Lines (LCC.web_file.set_range_lines)

## Signature
```lua
ok, replaced_or_err = LCC.web_file.set_range_lines(path, start_line, lines, timeout?)
```

## Parameters
- path  
    String. File path.  
- start_line  
    Number. Starting line index; positive numbers start at `1`, negative values count from the end (`-1` is the last line), and `0` means after the end.  
- lines  
    Table. Array of new line strings.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `false` on failure.  
- replaced_or_err  
    Table or string. Replaced original lines on success, or the error description on failure.  

## Notes
> Overwrites multiple lines at once starting from the given position.  
> Each empty string in the array represents a blank line, including at the end; for example, `{"New content", ""}` replaces two lines.  
> An empty array `{}` contains no replacement lines and differs from an array containing one empty string, `{""}`.  
> See the parameter description above for line-number rules.  
> When the target position is beyond the current end, blank lines are padded automatically.  
> Returns `{}` when no existing lines were replaced.  
> The returned old content is useful for auditing or undo flows.  

## Pairing reads and writes

When a file ends with a newline, `get_lines` keeps the empty string produced by splitting at the end. For example, the two-line text `"A\nB\n"` returns `{"A", "B", ""}`; passing this array to `set_range_lines(path, 1, lines)` writes three lines, with a blank last line.

To read and replace content by line number, pair [`get_range_lines`](./get_range_lines.md) with `set_range_lines`. To read, modify, and overwrite the whole file, pair `get_lines` with [`set_lines`](./set_lines.md). `set_lines` overwrites the entire file and is not suitable for partial replacements.

In both pairs, reading and writing are separate requests, so the complete read-modify-write sequence is not atomic. Coordinate access when there are concurrent writes to avoid overwriting changes made after the read.

## Example
```lua
local ok, old_lines_or_err = LCC.web_file.set_range_lines("/config/list.txt", 2, {"Beta", "Gamma"})
if ok then
    print("Original:", table.concat(old_lines_or_err, ","))
end
```
