# XXTLanControl Module

`XXTLanControl.lua` provides a unified interface for device-side scripts to talk to the control center. It is organized into five main areas:

- **Core control**: initialize the connection, configure retry behavior, capture UI state, set log aliases, and send logs back to the control center.
- **Human assist**: request a text reply, picked coordinate, or remote-control handling from the control center.
- **Shared files**: read and write files in the `Resource Directory`.
- **KVDB operations**: work with queues and dictionaries stored on the control center.
- **TableDB operations**: create, query, and edit structured table data on the control center.

## Obtain the Module

See [module acquisition and script integration](../lancontrol.md).

## Import the Module

```lua
local LCC = require("XXTLanControl")
```

## Before You Start

- Make sure the XXTouch version on the device is new enough.
- `LCC.capture_ui_state()` requires device-side `ui_element` version 0.6.0 or later. If the module is unavailable or outdated, update XXTouch before using **capture_ui_state**.
- If the script is not started directly by the control center, call `LCC.set_api_url("http://control-center-address:46990")` first.
- Always call `LCC.connect()` before using other helpers.

If the module version on the device does not match the one from the control center, `LCC.connect()` will try to download the newer `XXTLanControl.lua` automatically and reconnect.

## Common Usage Patterns

- Use `LCC.get_ui_config()` to read values submitted from a flat script or XPP package `main.json` configuration UI.
- Use `LCC.log()` to write messages back into log channels 1 to 6 in the control center.
- Use [`LCC.capture_ui_state()`](./core/capture_ui_state.md) to capture a screenshot and text-element tree, then save it as `.xxtuie` or attach it to a log.
- Use `LCC.kvdb` and `LCC.db` when you want scripts and the UI to share state or business data.
