# Batch Update Rows (LCC.db.edit)

## Signature
```lua
rows, err = LCC.db.edit(name, rows, timeout?)
```

## Parameters
- name  
    String. Table name. Must be non-empty and no longer than 256 bytes.  
- rows  
    Table. Array of objects containing `id` plus the fields to update. Every item must include an integer-valued `id` greater than or equal to `1`.
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- rows  
    Table. Array of original rows before the update; `nil` on failure.  
- err  
    String or `nil`. Error message such as `unknown table` or `unknown column`.

## Notes
> Updates multiple rows by `id` and returns the pre-update data.  
> A missing `id`, or an `id` that is not an integer value greater than or equal to `1`, triggers a Lua parameter validation error.
> The `id` column itself cannot be updated.  

## Example
```lua
local before, err = LCC.db.edit("tasks", {
    { id = 5, Status = "Done" },
    { id = 6, Status = "Running", Remark = "Manual approval" }
})
if not before then
    error(err)
end
```
