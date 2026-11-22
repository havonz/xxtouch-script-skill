# XXTLanControl.lua Integration

Read this guide when a device script needs control-center communication: reading script configuration, reporting logs or UI state, sharing files, using KVDB or TableDB, or requesting human assistance while running. Prefer the `LCC.*` APIs in `XXTLanControl.lua` over recreating the same business requests with raw HTTP. Ordinary touch or recognition scripts do not need this dependency.

Agent-side MCP operations and device-side `LCC.*` calls run in different environments. MCP business tool IDs are not device Lua functions, and a control-center workflow Lua node is not an XXTouch device runtime.

## Obtain the Module

Download the matching module from the target control center with `GET /api/down/XXTLanControl.lua`. Resolve the backend base URL from the user's address, the current MCP connection configuration, or a Skill result's `downloadUrl`. The `/api/skills/.../archive` part belongs to the Skill ZIP; append the module endpoint to the same backend base URL instead. Ask only if the address cannot be established. Do not guess a LAN IP or substitute a module from an unrelated source.

Reuse an existing project module when appropriate. To install or update it, run the bundled helper from the extracted Skill directory. Set `PROJECT_DIR` to the destination XXT or XPP project and use the address of its control center.

```bash
python3 scripts/install_lancontrol.py "$PROJECT_DIR" \
  --backend-url http://CONTROL_HOST:46990 --apply
```

- Without `--apply`, the helper only previews the target path; it neither downloads nor writes files.
- Project type comes from `.config`, or explicitly from `--type xxt` / `--type xpp`.
- XXT defaults to `lua/scripts/XXTLanControl.lua`, preserving an existing `lua/XXTLanControl.lua` location. XPP uses `XXTLanControl.lua` at package root.
- A differing existing file is not overwritten automatically. Compare it for project-specific changes before using `--force`. Resolve duplicate Lua or encrypted modules first so `require` cannot load an old copy.
- The helper does not change the entry script, devices, `.config`, or build ignores. The XXT template's SDK `buildIgnores` entries allow the control center to transfer the module separately while development transfers still include it. For independent distribution, ensure the device also receives the module; do not assume it is embedded in the built `.xxt`.

This guide also works when read through MCP without local helpers: download the module over HTTP and place it at the corresponding project path. Obtain the complete Skill ZIP through `downloadUrl` only when the installer is needed; `skill_read` returns document text.

## Initialize and Resolve the Device Address

`XXTLanControl` is a downloaded module loaded with `require`, not an XXTouch built-in global. Once it is available, use this in the entry script:

```lua
local LCC = require("XXTLanControl")

if not LCC.connect() then
    error("Unable to connect to the control center")
end

LCC.log(1, "Script connected to the control center")
```

When the control center launches the script, use its injected address and runtime configuration rather than hardcoding a different backend. For independent launches, call `LCC.set_api_url(backend_url)` before `LCC.connect()`. The URL must be an HTTP backend base address **reachable from the device**, without `/mcp`. An Agent-accessible loopback, container, or proxy address may not be reachable from the device.

Check the boolean result of `connect()` before business calls. It validates the module version and can download a matching version and reconnect. A successful `require` alone does not establish communication. Follow each API's retry policy, timeout, and return values; do not assume every function returns a boolean.

After a successful connection, normal script exit attempts to cancel unfinished assist requests from that script instance and report `is_running = false`. Abnormal termination or communication failure does not confirm that cleanup succeeded; check the remote task state before treating a pending human-assist request as cancelled.

## Read Only the Required APIs

Each API reference includes the function signature, parameters, return values, and examples. Open the page for the function you need. To find its path, look up the function in the Skill's `references/api-index.tsv`. Both the index and the individual pages are available through `skill_read`.

MCP read example:

```javascript
skill_read({skill:"xxtouch-script",path:"references/lancontrol-api/kvdb/dict/get.md"})
```

| Task | Reference |
| --- | --- |
| Connection, independent-launch address, retries | [connect](lancontrol-api/core/connect.md), [set_api_url](lancontrol-api/core/set_api_url.md), [set_retry_count](lancontrol-api/core/set_retry_count.md) |
| Read `main.json` script configuration | [get_ui_config](lancontrol-api/core/get_ui_config.md); XPP `.xui` configuration still uses `xui.*` |
| Text/image logs and channel aliases | [log](lancontrol-api/core/log.md), [set_log_aliases](lancontrol-api/core/set_log_aliases.md) |
| UI state containing a screenshot and element tree | [capture_ui_state](lancontrol-api/core/capture_ui_state.md); release objects as documented |
| Shared control-center resource files | [Shared files](lancontrol-api/web-file/README.md); these paths refer to Resource Directory, not device or Agent-local files |
| Queue consumption, batch pops, atomic transfers | [Queues](lancontrol-api/kvdb/queue/README.md); popping consumes data and is not a read-only query |
| Dictionary values, copying, atomic increments | [Dictionaries](lancontrol-api/kvdb/dict/README.md) |
| Structured data, queries, task claiming | [TableDB](lancontrol-api/tabledb/README.md), [fetch_one](lancontrol-api/tabledb/fetch_one.md); the Lua namespace is `LCC.db`, not `LCC.tabledb` |
| Runtime requests for text, coordinates, or human remote control | [Device-side human assistance](lancontrol-api/assist/README.md); `LCC.assist.*` differs from Agent-side `xxt_assist_*` operations |

Use the required slice's parameters and return conventions. Missing dictionary keys, empty queues, or unmatched table queries may return `nil, "not found"`. Task claiming with `fetch_one` needs suitable conditions and a state update. Do not consume, clear, overwrite, or claim real business data merely to test connectivity.

Pass KVDB names and keys as their original strings; do not URL-encode or hex-encode SDK arguments. Image-log calls wait for the upload response, so frequent large screenshots can delay the script and other device operations. Use cropped images and an appropriate sampling interval when visual evidence is needed.

## Verify

With MCP and an explicitly identified test device, use the existing project transfer and execution flow to verify module loading and a successful `connect()`, then inspect status and logs. Exercise only the requested business behavior. Distinguish network failures, initialization failures, and unmatched business data, preserving error details. Without a device or reachable backend, complete code and acquisition work where possible and state that device-side communication remains unverified.
