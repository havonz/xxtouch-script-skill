# Shared Files

`LCC.web_file` corresponds to the `Resource Directory` in the file manager.

It is useful for shared resources, text file reading and writing, file moves, and checksum-related operations. If you need to work with the `Script Directory` or `Reports Directory`, the file management UI is usually the better choice.

## Import the Module

```lua
local LCC = require("XXTLanControl")
```

## Before You Start

Before using any helper, make sure you either call `LCC.set_api_url()` or start the script from the control center, and always complete initialization with `LCC.connect()`.
