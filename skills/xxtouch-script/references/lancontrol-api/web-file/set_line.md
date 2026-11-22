# Replace A Single Line (LCC.web_file.set_line)

## Signature
```lua
ok, old_line_or_err = LCC.web_file.set_line(path, line_number, line, timeout?)
```

## Parameters
- path  
    String. File path.  
- line_number  
    Number. Line index to write; positive numbers start at `1`, negative values count from the end (`-1` is the last line), and `0` means after the last line.  
- line  
    String. New content.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `false` on failure.  
- old_line_or_err  
    String or `nil`. Previous text when successful; `nil` when no existing line was replaced; error description when the call fails.  

## Notes
> Replaces the content at the specified line index.  
> If `line` is an empty string, the target line becomes a blank line; the line is not deleted.  
> See the parameter description above for line-number rules.  
> Returns the previous text so you can compare or roll back.  
> Writing beyond the current content still creates a new line, with `nil` as the old value.  

## Example
```lua
local ok, old_line = LCC.web_file.set_line("/config/list.txt", 1, "Alpha")
if ok then
    print("Old text: " .. (old_line or ""))
end
```
