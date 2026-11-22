# Request a Picked Point (LCC.assist.pick_point)

## Declaration

```lua
result, err, task = LCC.assist.pick_point(options)
```

## Parameters

- options  
    Table. Assist request configuration. See [Common Options and Return Objects](./common-options.md). This function sets `type = "point"` automatically.

## Return Values

- result  
    Table or `nil`. On success, includes physical device coordinates `x` and `y`.
- err  
    String or `nil`. Failure reason.
- task  
    Table or `nil`. The latest task state.

## Notes

> Use this when the operator can decide where to tap from the screenshot and the script can directly tap the returned coordinate.  
> `result.x` and `result.y` are physical device coordinates and can be used directly with `touch.tap(result.x, result.y)`.  
> If you pass a cropped screenshot, also pass `imageRect`; the control center maps the picked image coordinate back to physical device coordinates.  

## Example

```lua
local result, err = LCC.assist.pick_point({
    title = "Pick confirm button",
    text = "Pick the center of the confirm button",
    screenshotLocalPath = XXT_SCRIPTS_PATH .. "/screen.png",
    timeout = 180,
})

if result then
    touch.tap(result.x, result.y)
end
```

Cropped-image example:

```lua
local result, err = LCC.assist.pick_point({
    title = "Pick button",
    text = "Pick the confirm button in this cropped image",
    screenshotLocalPath = XXT_SCRIPTS_PATH .. "/button-crop.png",
    imageRect = { left = 120, top = 360, width = 300, height = 160 },
})
```
