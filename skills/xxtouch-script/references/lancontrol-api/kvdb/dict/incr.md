# Atomic Increment/Decrement (LCC.kvdb.dict.incr)

## Signature
```lua
value, meta_or_err = LCC.kvdb.dict.incr(name, key, by?, init?, min?, max?, coerce?, timeout?)
```

## Parameters
- name  
    String. Dictionary name (non-empty, max `256` bytes).  
- key  
    String. Key to modify (must be valid UTF-8 and non-empty).  
- by  
    Integer, optional. Step size; defaults to `1` and can be negative.  
- init  
    Integer, optional. Initial value when the key is missing; defaults to `0`.  
- min  
    Integer, optional. Lower bound; results are clamped when below it.  
- max  
    Integer, optional. Upper bound; results are clamped when above it.  
- coerce  
    Boolean, optional. When `true`, non-integer existing values are reset to `init`; defaults to `false`.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- value  
    Number. Result after incrementing; `nil` on failure.  
- meta_or_err  
    Table or string. On success returns metadata:
    - `created`: whether the key was created this time
    - `coerced`: whether coercion happened
    - `clamped`: whether the value was clamped
    - `clamp_reason`: `'min'` or `'max'` when clamped
    - `original_value`: previous numeric value (when one existed)
    - `computed_value`: result before clamping
    - `result_value`: final stored value
    On failure contains the error message.  

## Notes
> Provides a thread-safe atomic counter operation.  
> Use `min`/`max` to constrain the range and `coerce` to reset invalid values back to `init`.  
> Returns `nil` with an error string when the call fails.  

## Example
```lua
local value, meta = LCC.kvdb.dict.incr("counter", "retry", 1, 0, 0, 5, true)
if value then
    LCC.log(1, "Retry count", value, meta.clamped and "Reached limit" or "")
end
```
