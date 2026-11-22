# Insert Multiple Lines (LCC.web_file.insert_lines)

## Signature
```lua
ok, err = LCC.web_file.insert_lines(path, start_line, lines, timeout?)
```

## Parameters
- path  
    String. File path.  
- start_line  
    Number. Reference line index for insertion. Positive numbers start at `1` and insert before that line; negative values count from the end, `0` appends after the last line, and `-1` inserts before the last line.  
- lines  
    Table. Array of line strings to insert in order.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `false` on failure.  
- err  
    String or `nil`. Error description when the operation fails.  

## Notes
> Inserts multiple lines before the specified line index.  
> See the parameter description above for the line-number rules.  
> When the target position is beyond the current end, blank lines are padded automatically.  
> The function appends a newline to the inserted content automatically so the file structure remains valid.  

## Example
```lua
local ok, err = LCC.web_file.insert_lines("/config/list.txt", 2, {"New 1", "New 2"})
if not ok then
    error(err)
end
```
