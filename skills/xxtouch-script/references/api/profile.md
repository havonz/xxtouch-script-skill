# profile

Manage iOS configuration profiles (`.mobileconfig`), not Lua performance profiling or XXTouch workspace settings.

```lua
local profile = require("profile")
```

This module is built into XXTouch; no third-party module download is needed.

## APIs

| Call | Parameters and defaults | Returns |
| --- | --- | --- |
| `profile.import(path, install)` | Device-local file path; optional boolean `install` defaults to `false`, queuing the file for system confirmation | `taskIdentifier, nil` on accepted submission; `nil, errMsg` on failure |
| `profile.install(path, install)` | Device-local file path; optional boolean `install` defaults to `true`, requesting direct installation | Same as `import` |
| `profile.list(filterFlags)` | Optional integer filter flags, default `1` | Array of installed profile information tables |
| `profile.filter(filterFlags)` | Same parameters and implementation as `list` | Same as `list` |
| `profile.fetch(identifier)` | Profile identifier (`PayloadIdentifier`), not a task identifier, UUID, display name, or file path | Profile information table, or `nil` when no information is available |
| `profile.remove(identifier)` | Profile identifier (`PayloadIdentifier`) | No return values |
| `profile.clear(filterFlags)` | Optional integer filter flags, default `1` | Number of removal requests issued for matching profiles with an identifier |

- `import(path, true)` uses the direct installation path; `install(path, false)` queues the file for system confirmation. Pass an actual boolean when overriding the default.
- A returned task identifier does not prove that installation has completed. Check installed state with the intended `PayloadIdentifier` after the system has processed the request or the user has completed confirmation. Do not pass the task identifier to `fetch` or `remove`.
- `filterFlags` is passed to the system unchanged. The meanings of other flag values are not documented here; use the default unless the target system's behavior has been established. Do not assume the default includes every system-managed profile.
- `remove` does not return a success boolean. `clear` counts requests, not confirmed removals. Re-query installed state before reporting completion; do not substitute `clear` for removal of one profile.
- Installation and removal depend on system policy and the target environment. Do not infer OS support, successful installation, or removal of a restricted profile solely from the presence of the module.

## Profile information

The system supplies these tables, preferring its summary dictionary and falling back to a serialized dictionary. Fields are optional and may vary by system version and profile type; `PayloadContent` is not guaranteed to contain the full original file.

| Field | Type |
| --- | --- |
| `PayloadIdentifier`, `PayloadUUID` | string |
| `PayloadDisplayName`, `PayloadDescription`, `PayloadOrganization` | string |
| `PayloadType` | string |
| `PayloadVersion` | integer |
| `PayloadRemovalDisallowed` | boolean |
| `PayloadContent` | table |

Other system-provided fields may also be present. A `nil` result from `fetch` means no information is available for that identifier, including when the profile is absent or the system cannot provide a nonempty dictionary.

## Examples

### Import for system confirmation

For an XXT project, package the file under `res/`:

```lua
local profile = require("profile")
local taskIdentifier, errMsg = profile.import(XXT_RES_PATH .. "/example.mobileconfig")
if not taskIdentifier then
  nLog("Profile import failed", errMsg)
  return
end
nLog("Profile submitted for system confirmation", taskIdentifier)
```

For XPP, resolve the packaged file with `xpp.resource_path("example.mobileconfig")`. Paths refer to files on the device, not Agent-local or control-center files. For a direct installation request, use `profile.install(path)` and handle its two return values in the same way.

### Inspect installed profiles

```lua
local profile = require("profile")
for _, info in ipairs(profile.list()) do
  nLog(info.PayloadIdentifier, info.PayloadDisplayName)
end

local info = profile.fetch("com.example.configuration")
if info then
  nLog(info)
else
  nLog("No installed profile information is available for this identifier")
end
```

### Remove a specific profile

```lua
local profile = require("profile")
profile.remove("com.example.configuration")
```

After the system has processed the request, re-query that identifier to inspect the resulting state. For a requested bulk removal of the matching set, use `local requestedCount = profile.clear()`; the count alone is not a completion check.
