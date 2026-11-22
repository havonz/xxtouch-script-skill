# Hardware keyboard (XXTouch 20260805+)

```lua
local keyboard = assert(key.connect_keyboard({
  Product = 'My Keyboard',
  Transport = 'USB'
}))

assert(keyboard:is_connected())
assert(keyboard:down('LEFTSHIFT'))
assert(keyboard:down(0x07, 4))
assert(keyboard:up(0x07, 4))
assert(keyboard:up('LEFTSHIFT'))
assert(keyboard:press('A'))
assert(keyboard:press(0x07, 4, 30))
assert(keyboard:send_text('Hello', 30, 10))

local properties = keyboard:get_properties()
nLog(properties.Product, properties.Transport)
assert(keyboard:disconnect())

local globalKeyboard = assert(key.connect_global_keyboard())
assert(key.get_global_keyboard() == globalKeyboard)
key.press('A')
key.send_text('Hello')
assert(key.disconnect_global_keyboard())
```
