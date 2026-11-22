# Remove A Single Line (LCC.web_file.remove_line)

## Signature
```lua
line, err = LCC.web_file.remove_line(path, line_number, timeout?)
```

## Parameters
- path  
    String. File path.  
- line_number  
    Number. Line index to delete; positive numbers start at `1`, negative values count from the end (`-1` is the last line), and `0` means after the last line.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- line  
    String. Content that was removed; `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Deletes the specified line and returns its original text.  
> See the parameter description above for line-number rules.  
> Returns `nil` when nothing is removed.  

## Example
```lua
local line, err = LCC.web_file.remove_line("/config/list.txt", 1)
if line then
    print("Removed:", line)
end
```
