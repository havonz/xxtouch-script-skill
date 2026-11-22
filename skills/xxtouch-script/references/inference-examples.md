# Native Inference Examples

For `onnxruntime` / `coreml` development or debugging, check the [ONNX Runtime](api/onnxruntime.module.md) or [CoreML](api/coreml.module.md) API first, then read one relevant implementation. Function names below are source locators, not necessarily exported APIs.

| Topic | Source | Search terms |
| --- | --- | --- |
| ONNX sessions, metadata, image tensors, lifecycle | [yolo_onnx.lua](../assets/frameworks/yolo_onnx.lua) | `M.new`, `build_session_options`, `prepare_input_tensor`, `run_outputs`, `instance_mt:close` |
| CoreML compilation cache, image/multi-array inputs, prediction | [yolo_coreml.lua](../assets/frameworks/yolo_coreml.lua) | `compile_model_cached`, `new_instance`, `build_model_info`, `prepare_image_input`, `prepare_multi_array_input`, `run_outputs`, `instance_mt:close` |
| ONNX pipelines, quad crops, batching, CTC | [paddleocr_onnx.lua](../assets/frameworks/paddleocr_onnx.lua) | `make_det_session`, `make_rec_session`, `prepare_rec_tensor_from_quads`, `decode_rec_detections`, `decode_rec_output` |
| Detection decoding, coordinate restoration, masks | [captcha_recognizer.lua](../assets/frameworks/captcha_recognizer.lua) | `run_model`, `decode_predictions`, `build_proto_masks` |
| Input preprocessing, custom charsets, CTC results | [ddddocr.lua](../assets/frameworks/ddddocr.lua) | `prepare_ocr_tensor`, `run_single_output`, `decode_ocr_output` |

Follow shared helpers only when called by the selected code:

- [yolo_backend_common.lua](../assets/frameworks/yolo_backend_common.lua): `build_ort_session_options`, `build_ort_model_info`.
- [yolo_profile_runtime.lua](../assets/frameworks/yolo_profile_runtime.lua): `attach_segmentation_masks`, `attach_pose_keypoints`, `materialize_detect_detections`; inspect the caller's `ort` / `coreml` argument.

Search from the skill root, then open matching functions and necessary callers/callees:

```bash
rg -n 'prepare_input_tensor|run_outputs|instance_mt:close' assets/frameworks/yolo_onnx.lua
rg -n 'compile_model_cached|new_instance|prepare_multi_array_input' assets/frameworks/yolo_coreml.lua
```

Verify signatures, returns, input constraints, and cleanup before adapting model-specific layouts, normalization, class counts, or paths. Studying code requires no installation, weights, or large dictionaries. Ordinary OCR still prefers built-in Paddle Lite / Apple Vision; full PaddleOCR requires an explicit developer request.
