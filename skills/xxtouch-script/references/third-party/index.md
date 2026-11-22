# Third-Party Modules and Installable Lua Wrappers

Use this directory only when a script truly needs a bundled third-party Lua module. Prefer XXTouch globals first: `json`, `http`, `file`, `plist`, `screen`, `image`, `sys`, and related APIs are usually simpler and safer.

Recognition wrapper sources can be installed into projects. Open the module guide directly when its name is known; see [vision-modules.md](vision-modules.md) for selection and dependency installation, and [vision-models.md](vision-models.md) only when preparing weights.

For ordinary text recognition, prefer built-in Paddle Lite or Apple Vision through [screen.ocr_text](../api/screen.ocr_text.md) / [ImageObject:ocr_text](../api/ImageObject.ocr_text.md). Read and install NCNN/ONNX PaddleOCR wrappers only when the developer explicitly requests full PaddleOCR.

## Read Order

1. Run `rg -n "<module|require|api|task keyword>" references/third-party`.
2. Open the module overview first only if the result set is unclear.
3. Open only the matching topic slice, such as `luasocket-tcp.md` or `luafilesystem-attributes.md`.
4. Start from the first short example in that slice, then adapt parameters and cleanup logic.

## Task Map

| Task | Prefer | Open |
| --- | --- | --- |
| JSON compatibility with old Lua code | `cjson.safe` | `luacjson.md`, `luacjson-options.md` |
| Raw TCP/UDP protocol | `socket` | `luasocket-tcp.md`, `luasocket-udp.md` |
| HTTPS or complex HTTP options | XXTouch `http`, then `lcurl` | `lcurl.md`, `lcurl-easy.md` |
| WebSocket client | `websocket` | `lua-websockets.md` |
| SQLite read/write | `sqlite3` | `luasqlite3.md`, `luasqlite3-statements.md` |
| Directory walk or file metadata | `lfs` | `luafilesystem-dir-cwd.md`, `luafilesystem-attributes.md` |
| UI element query/action automation | `ui_element` | `ui_element.md` |
| Regex-like parsing | LPeg | `lpeg.md`, `lpeg-patterns.md`, `lpeg-captures.md` |
| XML parse/edit/write | `slaxml` / `slaxdom` | `slaxml.md` |
| YAML read/write | `lyaml` | `lyaml.md` |
| HMAC/certificate/OpenSSL interop | `openssl` | `lua-openssl.md`, `lua-openssl-reference.md` |
| POSIX-only operation | `posix` or `unix` | `lua-posix.md`, `lunix.md` |
| C library binding | `ffi` | `cffi-lua.md`, `cffi-lua-reference.md` |
| Objective-C bridge or private UIKit/Foundation task | `objc` | `lobjc.md`, `lobjc-objc-bridge.md` |
| Slider captcha recognition and gap location | Prefer `captcha_recognizer` | `captcha_recognizer.md` |
| Text captchas and detection within captcha images | `ddddocr` | `ddddocr.md` |
| Explicitly requested captcha template matching or image comparison | `ddddocr.slide_match` / `slide_comparison` | `ddddocr.md` |
| Explicitly requested full PaddleOCR, ONNX backend | `paddleocr_onnx` | `paddleocr_onnx.md` |
| Explicitly requested full PaddleOCR, NCNN backend | `paddleocr_ncnn` | `paddleocr_ncnn.md` |
| Convert original PaddleOCR / ONNX models to NCNN | Model conversion and compatibility checks | `paddleocr_ncnn_conversion.md` |
| YOLO NCNN detection, classification, and advanced tasks | `yolo_ncnn` | `yolo_ncnn.md` |
| Object tracking across frames | `yolo_tracker` | `yolo_tracker.md` |
| Custom YOLO outputs, segmentation, and pose | YOLO `profile` | `yolo_profile_runtime.md` |
| YOLO ONNX detection/classification/OBB | `yolo_onnx` | `yolo_onnx.md` |
| YOLO CoreML detection/classification/OBB | `yolo_coreml` | `yolo_coreml.md` |

## Module Notes

- `cjson` / `json`: see `luacjson.md` and `luacjson-options.md`.
- `socket`: see `luasocket.md`, `luasocket-tcp.md`, `luasocket-udp.md`, `luasocket-dns-url.md`, `luasocket-http-ftp.md`.
- `ssl`: see `luassl.md`.
- `openssl`: see `lua-openssl.md` and `lua-openssl-reference.md`.
- `lpeg`: see `lpeg.md`, `lpeg-patterns.md`, `lpeg-captures.md`.
- `slaxml` / `slaxdom`: see `slaxml.md`.
- `lyaml`: see `lyaml.md`.
- `lfs`: see `luafilesystem.md`, `luafilesystem-attributes.md`, `luafilesystem-dir-cwd.md`, `luafilesystem-mutate-lock.md`.
- `ui_element`: see `ui_element.md`.
- `iconv`: see `luaiconv.md`.
- `sqlite3`: see `luasqlite3.md` and `luasqlite3-statements.md`.
- `lcurl` / `curl.safe`: see `lcurl.md` and `lcurl-easy.md`.
- `unix`: see `lunix.md`.
- `posix`: see `lua-posix.md`.
- `ffi`: see `cffi-lua.md` and `cffi-lua-reference.md`.
- `objc`: see `lobjc.md` and `lobjc-objc-bridge.md`.
- `ev`: see `lua-ev.md`.
- `archive`: see `lua-archive.md`.
- `path`: see `lua-path.md`.
- `zip`: see `lua-zip.md`.
- `websocket`: see `lua-websockets.md`.
- `captcha_recognizer`: see `captcha_recognizer.md`.
- `ddddocr`: see `ddddocr.md`.
- `paddleocr_onnx`: see `paddleocr_onnx.md`.
- `yolo_onnx`: see `yolo_onnx.md`.
- `yolo_coreml`: see `yolo_coreml.md`.
- `paddleocr_ncnn`: see `paddleocr_ncnn.md`.
- `yolo_ncnn`: see `yolo_ncnn.md`.
- `yolo_tracker`: see `yolo_tracker.md`.
- The installer includes `yolo_profile_runtime`, `yolo_backend_common`, and `paddleocr_ncnn_dict` automatically. Ordinary tasks do not need to read their source.
- Full require-name map: see `available-modules.md`.

## General Rules

- Prefer example code in the topic slice over prose summaries.
- Do not require third-party modules defensively just to check whether they exist; documented built-ins are assumed present.
- Keep third-party usage isolated in small helper functions.
- Close sockets, database handles, and files explicitly.
- Avoid shell execution modules unless the user explicitly asks for system command execution.
- Treat callbacks and long-running loops as script lifecycle code: add timeouts, stop conditions, and cleanup.
- Prefer explicit `return nil, err` helpers instead of throwing from deep utility functions unless the caller already uses `assert`.
