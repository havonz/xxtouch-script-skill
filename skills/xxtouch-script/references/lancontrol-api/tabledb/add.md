# Batch Insert Rows (LCC.db.add)

## Signature
```lua
ok, err = LCC.db.add(name, rows, timeout?)
```

## Parameters
- name  
    String. Table name. Must be non-empty and no longer than 256 bytes.  
- rows  
    Table. Array of row objects. Field names must already exist, and `id` must not be included.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` when insert succeeds, otherwise `false`.  
- err  
    String or `nil`. Error details (invalid columns, empty payload, etc.).  

## Notes
> Inserts rows in bulk; all user columns are stored as strings.  
> Including an `id` field causes an error.  
> Unknown tables or columns produce error messages.  

## Example
```lua
local ok, err = LCC.db.add("tasks", {
    { Name = "Deploy script", Status = "Running" },
    { Name = "Clean data", Status = "Idle", Remark = "Night batch" }
})
if not ok then
    error(err)
end
```
