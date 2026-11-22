# Hardware mouse (XXTouch 20260805+)

```lua
local mouseObj = assert(mouse.connect({
  Product = 'My Mouse',
  Transport = 'USB'
}))

assert(mouseObj:is_connected())
assert(mouseObj:move(100, -50))
assert(mouseObj:down('left'))
assert(mouseObj:move(100, 0))
assert(mouseObj:up('left'))
assert(mouseObj:down(13))
assert(mouseObj:up(13))
assert(mouseObj:click('right'))
assert(mouseObj:click(13, 100))
assert(mouseObj:scroll(0, 10))

local properties = mouseObj:get_properties()
nLog(properties.Product, properties.Transport)
assert(mouseObj:disconnect())
```
