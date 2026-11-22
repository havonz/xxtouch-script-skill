# PaddleOCR to NCNN

Use for explicitly requested full PaddleOCR when conversion or compatibility work is needed. The `ppocrv5-mobile-ncnn` preset is already converted; use its [module guide](paddleocr_ncnn.md) directly.

| Input | Preparation |
| --- | --- |
| Paddle inference model | Typically Paddle2ONNX export, then pnnx to NCNN |
| ONNX | pnnx to NCNN; verify names and dynamic dimensions |
| NCNN `.param/.bin` pair | Verify compatibility; extensions alone are insufficient |

Convert DET and REC separately, retaining REC's training/export dictionary. Renaming files does not convert models.

## PP-OCRv5 Example

Follow the [pinned upstream guide](https://github.com/nihui/ncnn-android-ppocrv5/blob/671ac4a72299a86ddee160131ba88fed748df425/README.md#guidelines-for-converting-ppocrv5-models). Other versions may need different tools/operators.

1. Use matching PaddleOCR, PaddlePaddle, Paddle2ONNX, and pnnx versions. Export DET/REC with `paddlex --paddle2onnx`, setting `--paddle_model_dir` and `--onnx_model_dir`.
2. Convert the exported files; adapt paths and shapes to the model:

```bash
pnnx PP-OCRv5_mobile_det.onnx 'inputshape=[1,3,320,320]' 'inputshape2=[1,3,256,256]'
pnnx PP-OCRv5_mobile_rec.onnx 'inputshape=[1,3,48,160]' 'inputshape2=[1,3,48,256]'
```

3. Verify dynamic input support. Upstream models include manual adaptations; a successful converter run need not reproduce them.

`manage_models.py fetch` / `emit-lua` only download artifacts; they neither install conversion tools nor run them.

## Wrapper Compatibility

- Input/output defaults: `in0` / `out0`. Override `det_input_name`, `det_output_names`, `rec_input_name`, `rec_output_names` as needed.
- Test different DET image sizes and REC widths. REC defaults to height 48 and width bucketing; fixed-size models need matching preprocessing.
- Check channels, normalization, output layout, probabilities/logits, and REC dictionary ordering. Pass custom REC's matching `dict_path`.
- Compare known-text results before/after conversion, then test device loading, full-image/single-line recognition, and cleanup. Record conversion and inference validation separately.

Store artifacts in `res/models/<model-id>/`, excluded only via `buildIgnores`. Use local files directly or a [project catalog](vision-models.md#project-model-catalogs) with pinned sources, sizes, and SHA256 for distribution.
