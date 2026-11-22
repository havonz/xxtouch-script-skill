# Count Rows (LCC.db.count)

## Signature
```lua
count, err = LCC.db.count(name, conditions?, timeout?)
```

## Parameters
- name  
    String. Table name. Must be non-empty and no longer than 256 bytes.  
- conditions  
    Table, optional. Equality conditions combined with AND; counts all rows when omitted.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- count  
    Number. Number of matching rows; `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Returns the number of matching rows; `conditions` has the same semantics as in `list`.  
> Unknown tables or columns produce errors that are returned to the caller.  

## Example
```lua
local total, err = LCC.db.count("tasks", { Status = "Idle" })
if total then
    LCC.log(1, "Idle tasks", total)
end
```
