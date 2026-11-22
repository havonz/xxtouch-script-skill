# Hardware gamepad (XXTouch 20260805+)

```lua
local pad = assert(gamepad.connect({
  Product = 'My Gamepad',
  Transport = 'USB'
}))

assert(pad:is_connected())
assert(pad:down('left_shoulder'))
assert(pad:up('left_shoulder'))
assert(pad:down(13))
assert(pad:up(13))
assert(pad:press('a'))
assert(pad:press('menu'))
assert(pad:press(32, 100))
assert(pad:set_stick('left', 0.5, 1))
assert(pad:set_stick('left', 0, 0))
assert(pad:set_dpad(1, 0))
assert(pad:set_dpad(-1, 1))
assert(pad:set_dpad(0, 0))
assert(pad:reset())

local properties = pad:get_properties()
nLog(properties.Product, properties.Transport)
assert(pad:disconnect())
```
