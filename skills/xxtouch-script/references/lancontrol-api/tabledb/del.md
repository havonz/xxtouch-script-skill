# Batch Delete Rows (LCC.db.del)

## Signature
```lua
rows, err = LCC.db.del(name, id_rows, timeout?)
```

## Parameters
- name  
    String. Table name. Must be non-empty and no longer than 256 bytes.  
- id_rows  
    Table. Array of objects containing `id`, or a plain array of `id` values. Every `id` must be an integer value greater than or equal to `1`.
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- rows  
    Table. Rows deleted from the table; `nil` on failure.  
- err  
    String or `nil`. Error message such as `'unknown table'`.

## Notes
> Removes rows by `id` and returns the original data for auditing.  
> Each array element can be a plain numeric `id` or an object containing `id`; for objects only the `id` field is used.  
> An item whose `id` is not an integer value greater than or equal to `1` triggers a Lua parameter validation error.

## Example
```lua
local removed, err = LCC.db.del("tasks", { {id = 10}, 11, 12 })
if removed then
    LCC.log(1, "Deleted rows", #removed)
end
```
