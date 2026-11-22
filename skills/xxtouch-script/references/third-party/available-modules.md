# Available Third-Party Require Names

This is a capability map, not a full API reference. Open the linked local note before using a module.

| Library | Require | Local note | Notes |
| --- | --- | --- |
| LuaSocket | `require "socket"` | `luasocket.md` | TCP/UDP sockets and DNS. Prefer `http` for normal HTTP requests. |
| LuaSocket HTTP | `require "socket.http"` | `luasocket-http-ftp.md` | Legacy HTTP client with LTN12 sinks/sources. No HTTPS by itself. |
| LuaSocket FTP | `require "socket.ftp"` | `luasocket-http-ftp.md` | Legacy FTP client. Prefer XXTouch `ftp` for normal transfers. |
| LuaSocket URL | `require "socket.url"` | `luasocket-dns-url.md` | URL parse/build/escape helpers. |
| LTN12 | `require "ltn12"` | `luasocket-http-ftp.md` | Source/sink/pump helpers used by LuaSocket protocols. |
| MIME | `require "mime"` | `luasocket-http-ftp.md` | Base64 and MIME helpers often used with LuaSocket. |
| LuaSSL | `require "ssl"` | `luassl.md` | TLS support for socket workflows. Prefer high-level HTTP clients. |
| lua-openssl | `require "openssl"` | `lua-openssl.md`, `lua-openssl-reference.md` | OpenSSL bindings; use only for explicit crypto/TLS tasks. |
| LPeg | `require "lpeg"` | `lpeg.md`, `lpeg-patterns.md`, `lpeg-captures.md` | Pattern grammar parsing. |
| SLAXML | `require "slaxml"` or `require "slaxdom"` | `slaxml.md` | XML streaming parse, DOM parse, and XML serialization. |
| lyaml | `require "lyaml"` | `lyaml.md` | YAML load/dump. Prefer JSON/plist unless YAML is required. |
| LuaFileSystem | `require "lfs"` | `luafilesystem.md`, `luafilesystem-*.md` | Directory iteration, file attributes, current directory. Prefer `file` for simple file operations. |
| XXTouch UI element API | `require "ui_element"` | `ui_element.md` | Element query and action automation. Prefer this for semantic UI operations; prefer `touch` for fixed-position taps. |
| LuaCJSON | `require "cjson"` or `require "cjson.safe"` | `luacjson.md`, `luacjson-options.md` | JSON codec. Prefer global `json` unless `cjson` behavior is specifically needed. |
| lua-iconv | `require "iconv"` | `luaiconv.md` | Encoding conversion. |
| LuaSQLite3 | `require "sqlite3"` | `luasqlite3.md`, `luasqlite3-statements.md` | SQLite database access. Prefer current handbook examples over old `lsqlite3` mentions. |
| lcurl | `require "lcurl"` or `require "curl.safe"` | `lcurl.md`, `lcurl-easy.md` | libcurl wrapper. Prefer global `http`/`ftp` for ordinary transfers. |
| lunix | `require "unix"` | `lunix.md` | Unix file ownership and permission helpers. |
| lua-posix | `require "posix"` | `lua-posix.md` | POSIX bindings. Use only when documented XXTouch APIs are insufficient. |
| cffi-lua | `require "ffi"` | `cffi-lua.md`, `cffi-lua-reference.md` | FFI access. High risk; avoid unless explicitly requested. |
| lobjc | `require "objc"` | `lobjc.md`, `lobjc-objc-bridge.md` | Objective-C bridge. Prefer `fork_dostring` for risky isolated calls. |
| lua-ev | `require "ev"` | `lua-ev.md` | Event loop library. |
| lua-archive | `require "archive"` | `lua-archive.md` | Archive handling. Prefer `file.zip` / `file.unzip` for ZIP. |
| lua-path | `require "path"` | `lua-path.md` | Path manipulation. |
| lua-zip | `require "zip"` | `lua-zip.md` | ZIP handling. XXTouch alias differs from upstream `brimworks.zip`; prefer `file.zip` / `file.unzip`. |
| lua-websockets | `require "websocket"` | `lua-websockets.md` | WebSocket client/server workflows. |
| Slider captcha recognition | `require "captcha_recognizer"` | `captcha_recognizer.md` | Preferred for slider gaps; uses ONNX Runtime and a matching slider model. |
| Text captcha recognition | `require "ddddocr"` | `ddddocr.md` | Text captcha OCR and detection within captcha images; template matching and image comparison only when specifically needed. |
| Full PaddleOCR ONNX wrapper | `require "paddleocr_onnx"` | `paddleocr_onnx.md` | Use only when full PaddleOCR is explicitly requested; prefer built-in Paddle Lite or Apple Vision for ordinary text. |
| YOLO ONNX wrapper | `require "yolo_onnx"` | `yolo_onnx.md` | YOLO detect/classify/OBB through ONNX Runtime; profile support for seg/pose/track. |
| YOLO CoreML wrapper | `require "yolo_coreml"` | `yolo_coreml.md` | YOLO detect/classify/OBB through CoreML; supports cached model compilation. |

## Recognition Modules Available for Project Installation

The skill includes source snapshots of these Lua wrappers. Having XXTouch installed on a device does not establish that the project includes a specific wrapper version. Use the [module installer](vision-modules.md) to copy dependencies; prepare native backends and models separately.

| Require name | Guide |
| --- | --- |
| `paddleocr_ncnn` | Use the [NCNN wrapper](paddleocr_ncnn.md) only for explicitly requested full PaddleOCR; source models usually need [conversion](paddleocr_ncnn_conversion.md) |
| `yolo_ncnn` | [NCNN YOLO](yolo_ncnn.md) |
| `yolo_tracker` | [Track detection results](yolo_tracker.md) |
| `yolo_profile_runtime` | [YOLO profiles](yolo_profile_runtime.md); business code passes options through its backend |
| `yolo_backend_common`, `paddleocr_ncnn_dict` | Automatically installed implementation dependencies; no separate reading required |

Together with `captcha_recognizer`, `ddddocr`, `paddleocr_onnx`, `yolo_onnx`, and `yolo_coreml` above, all 11 modules can be copied by the installer.
