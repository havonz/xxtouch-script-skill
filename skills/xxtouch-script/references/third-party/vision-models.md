# Model Downloads

Read only for model preparation or requested device download code. Query the catalog rather than loading it into context. Full PaddleOCR requires an explicit request; ordinary OCR uses built-in Paddle Lite / Apple Vision. Lite `.nb` models are documented in [screen.ocr_text](../api/screen.ocr_text.md) and cannot replace NCNN/ONNX files.

## Query and Download

From the skill root:

```bash
python3 scripts/manage_models.py list --module paddleocr_ncnn
python3 scripts/manage_models.py list --model ppocrv5-mobile-ncnn
python3 scripts/manage_models.py fetch <project-root> ppocrv5-mobile-ncnn
```

`list --module` lists IDs; `list --model` returns files, pinned source, checksums, constructor hints, and verification limits. Presets are download metadata, not bundled weights.

| Preset | Files / mode |
| --- | --- |
| `captcha-slider` | `slider.onnx`; preferred slider captcha model |
| `ddddocr-old` | `common_old.onnx` + `common_old.json`; default text captcha OCR |
| `ddddocr-beta` | `common.onnx` + `common.json`; `beta=true` |
| `ddddocr-det` | `common_det.onnx`; `det=true`, captcha detection |
| `ppocrv5-mobile-ncnn` | Converted DET/REC `.param/.bin`, dynamic inputs, bundled Lua dictionary |
| `ppocrv5-onnx-chinese`, `ppocrv5-onnx-english` | v5 `det.onnx`, language-specific `rec.onnx` + `dict.txt` |
| `paddleocr-onnx-custom`, `yolo-onnx-custom`, `yolo-coreml-custom`, `yolo-ncnn-custom` | `needs-model`: provide a [project catalog](#project-model-catalogs) |

- Destination: `res/models/<model-id>/`. `fetch` idempotently adds `/res/models` only to `.config.buildIgnores`, preserving other settings. Resolve any conflicting `ignores` entry first.
- Models transfer during development/debugging but stay out of release builds. Avoid `.tmp/`, normally excluded from development transfers too.
- Files download to temporary paths and replace targets after size/SHA256 verification. Failures clean temporary files; retries reuse verified files. A directory is returned only when the whole bundle succeeds.
- NCNN presets are converted artifacts. For unconverted Paddle/ONNX models targeting NCNN, read [conversion](paddleocr_ncnn_conversion.md). These helpers neither convert weights nor extract archives.

To set only the build exclusion:

```bash
python3 scripts/ensure_config_ignores.py <project-root> --entry res/models --build-only
```

Pass the project model directory explicitly:

```lua
local model_dir = XXT_RES_PATH .. '/models/ppocrv5-mobile-ncnn' -- XXT
-- For XPP: local model_dir = xpp.resource_path('res/models/ppocrv5-mobile-ncnn')
local ocr = require('paddleocr_ncnn').new({model_dir = model_dir})
```

Chinese and English ONNX presets place DET, REC, and `dict.txt` in one directory. Match the dictionary to the REC model. Use `list --model` for source URLs, tested versions, and known recognition limits.

## Device Download Code: Only When Requested

Build exclusion does not imply permission to add runtime networking. On developer request:

```bash
python3 scripts/manage_models.py emit-lua ppocrv5-mobile-ncnn --output <project-root>/lua/download_ppocr.lua
```

For XPP, output to package root. Without `--output`, print Lua to stdout. Existing differing files are refused; entry scripts are not modified.

```lua
local prepare_model = require('download_ppocr')
local model_dir, err = prepare_model()
assert(model_dir, err)
local ocr = require('paddleocr_ncnn').new({model_dir = model_dir})
```

The returned function runs only when called; default destination: `XXT_HOME_PATH..'/models/<model-id>'`, optionally another absolute directory. Returns the directory or `nil, err`. Uses `http.get{download_file=...}` and streaming OpenSSL SHA256 without loading full weights into Lua memory. Valid files skip networking; HTTP, timeout, write, or verification failures clean partial files and return errors. The helper does not retry automatically. Callers close inference instances. Releases without download code need separately deployed weights and explicit device paths.

## Project Model Catalogs

Append entries with `--catalog <catalog.json>`; IDs must not duplicate presets. Store the catalog under `res/models/` if it should share the build exclusion.

```json
{
  "schema_version": 1,
  "models": {
    "my-yolo-detect": {
      "module": "yolo_onnx",
      "status": "downloadable",
      "source": "Model release page",
      "revision": "Pinned release or commit",
      "description": "Detection model compatible with this wrapper",
      "constructor_options": {"task": "detect"},
      "files": [
        {"path": "model.onnx", "url": "https://example.com/releases/v1/model.onnx", "size": 12345, "sha256": "REPLACE_WITH_THE_FILE_64_CHARACTER_LOWERCASE_SHA256"}
      ]
    }
  }
}
```

Replace example values. Each file needs a safe relative path, HTTP(S) URL, positive byte size, and lowercase SHA256. List all labels, dictionaries, ONNX external data, or `.mlpackage` contents, preserving relative paths. No archive extraction or `.pt` conversion occurs.

```bash
python3 scripts/manage_models.py fetch <project-root> my-yolo-detect --catalog <catalog.json>
python3 scripts/manage_models.py emit-lua my-yolo-detect --catalog <catalog.json>
```

`constructor_options` are hints, not executed actions; resolve paths against the returned directory. Compile `.mlpackage` / `.mlmodel` on-device with `compile_model_cached`; training weights or another device's cache are not ready `.mlmodelc` files. Recheck model layout, dictionary/classes, and `profile` when replacing models.
