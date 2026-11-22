# Fetch Entire Dictionary (LCC.kvdb.dict.get_all)

## Signature
```lua
values, err = LCC.kvdb.dict.get_all(name, timeout?)
```

## Parameters
- name  
    String. Dictionary name (non-empty, max `256` bytes).  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- values  
    Table. Mapping `{ key = value }`; returns an empty table when the dictionary is empty, or `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Returns a full snapshot of the dictionary as a key/value table.  
> An empty dictionary returns an empty table, not `nil`.  

## Example
```lua
local dict, err = LCC.kvdb.dict.get_all("settings")
if dict then
    for k, v in pairs(dict) do
        print(k, v)
    end
end
```
