# Read A Single Line (LCC.web_file.get_line)

## Signature
```lua
line, err = LCC.web_file.get_line(path, line_number, timeout?)
```

## Parameters
- path  
    String. File path.  
- line_number  
    Number. Line index to read; positive numbers start at `1`, negative values count from the end (`-1` is the last line), and `0` means after the last line.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- line  
    String or `nil`. Text of the requested line; returns an empty string when the line is not found, and `nil` only on failure.
- err  
    String or `nil`. Only set when the call fails.  

## Notes
> Reads the single line at the specified line index.  
> Positive numbers start at `1`; negative values count from the end (`-1` is the last line); `0` means after the last line.  
> Returns an empty string when the specified line is not found.

## Example
```lua
local line, err = LCC.web_file.get_line("/config/list.txt", 3)
if line then
    print("Line 3: " .. line)
end
```
