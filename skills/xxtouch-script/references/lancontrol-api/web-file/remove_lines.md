# Remove A Range Of Lines (LCC.web_file.remove_lines)

## Signature
```lua
removed, err = LCC.web_file.remove_lines(path, start_line, count?, timeout?)
```

## Parameters
- path  
    String. File path.  
- start_line  
    Number. Starting line index; positive numbers start at `1`, negative values count from the end (`-1` is the last line), and `0` means after the last line.  
- count  
    Number, optional. Number of lines to remove, default `1`.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- removed  
    Table. Array of removed lines; returns `{}` when the request succeeds but nothing is removed, and `nil` on failure.  
- err  
    String or `nil`. Error description when the operation fails.  

## Notes
> Removes several lines at once from the file.  
> See the parameter description above for line-number rules.  
> Missing files, out-of-range selections, or `count = 0` all return `{}`.  
> The returned lines can be logged or used to build an undo stack.  

## Example
```lua
local removed, err = LCC.web_file.remove_lines("/config/list.txt", 2, 3)
if removed then
    LCC.log(2, "Removed lines", table.concat(removed, ","))
end
```
