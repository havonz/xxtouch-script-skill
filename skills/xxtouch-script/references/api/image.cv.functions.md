# image.cv: Module Function Reference

Version requirement: **XXTouch later than 20260402 is required.** Load the built-in module with `local cv = require("image.cv")`. The signatures below describe the XXTouch Lua bindings, not the Python or C++ signatures.

Every supported `cv.*` function is indexed by name in `references/api-index.tsv`. Shared image/matrix functions have their full module signatures in the **Module call** column of the [cv.mat reference](cv.mat.md). This page documents functions without a matching matrix method and the higher-level ImageObject APIs.

- [Shared image and matrix functions](#shared-image-and-matrix-functions)
- [Types and conversion](#types-and-conversion)
- [Channel and image assembly](#channel-and-image-assembly)
- [Transform matrices and point transforms](#transform-matrices-and-point-transforms)
- [Kernels and windows](#kernels-and-windows)
- [Contour geometry](#contour-geometry)
- [Text measurement](#text-measurement)
- [High-level ImageObject functions](#high-level-imageobject-functions)
- [Built-in Paddle Lite bindings](#built-in-paddle-lite-bindings)

Examples assume `cv` is loaded. Image variables such as `img`, `other_img`, and `template_img` are existing ImageObjects. Coordinates are image-local pixels. Contours are one-based arrays of `{x, y}` points with integer pixel coordinates; transformation functions also accept floating-point points.

## Shared Image and Matrix Functions

For functions such as `cv.sobel`, `cv.in_range`, `cv.set_to`, `cv.find_contours`, or `cv.match_template`, look up the exact function name in [cv.mat](cv.mat.md). Each row includes an explicit `cv.function(src, ...)` signature, parameter purpose, result type, constraints, and examples in its section. Module-only geometry, creation, assembly, and high-level functions are documented below.

Important differences when using the module form:

- `src` normally accepts an ImageObject or `cv.mat`. Processing functions normally return a matrix; `opts.return_image = true` requests an ImageObject where supported.
- Drawing functions return an ImageObject by default for ImageObject inputs, and a matrix for matrix inputs. They copy their source unless supported matrix in-place processing is explicitly requested.
- `cv.resize(img, width, height)` modifies and returns the ImageObject when called with exactly those three arguments. `cv.resize(mat, width, height[, interpolation][, opts])` uses matrix processing. Convert with `cv.from_image` first for consistent matrix semantics, or use `cv.resize_copy` to resize an ImageObject without mutation.
- `cv.to_image(img)` returns the same ImageObject. `cv.to_image(mat[, opts])` creates an ImageObject from matrix data.
- `cv["repeat"](src, ny, nx[, opts])` requires bracket notation because `repeat` is a Lua keyword.
- A trailing options table does not replace preceding optional positional values on every function. Use the documented argument positions, especially `iterations` for morphology, `gamma` for blending, and the boolean angle unit for vector conversions.

```lua
local gray = cv.from_image(img, "gray")
local smooth = cv.gaussian_blur(gray, 3, 3)
local used, mask = cv.threshold(smooth, 0, 255, "binary|otsu", {
    return_threshold = true,
})
local contours = cv.find_contours(mask, "external", "simple")
local out = cv.draw_contours(img, contours, 0x00FF00, 2)
```

## Types and Conversion

| Call | Result and use |
| --- | --- |
| `cv.is(value)` | Boolean; true for either an ImageObject or `cv.mat`. |
| `cv.type(value)` | `"image_object"`, `"cv.mat"`, or `nil` for an unsupported value. This is different from the matrix storage type returned by `mat:type()`. |
| `cv.version()` | OpenCV version string, not the XXTouch release date. |
| `cv.from_image(src[, color_mode])` | Independent matrix copy. For an ImageObject, use `"bgra"`, `"bgr"`, `"gray"`/`"grey"`, `"rgb"`, or `"rgba"` as needed. |
| `cv.mat.is(value)` | Boolean; true only for a matrix userdata. |

For `cv.to_image(src[, opts])`, see the explicit signature and conversion rules in [inspection, copying, and conversion](cv.mat.md#inspection-copying-and-conversion). Keep analytical float matrices as matrices; converting them to images can normalize or truncate values.

```lua
local mat = cv.from_image(img, "gray")
assert(cv.is(img) and cv.is(mat))
assert(cv.type(img) == "image_object" and cv.mat.is(mat))
print(mat:type(), mat:depth(), mat:channels(), cv.version())
local out = cv.to_image(mat)
```

## Channel and Image Assembly

| Call | Result and use |
| --- | --- |
| `cv.merge(channels[, opts])` | Combine an array of channel matrices into one matrix; channel dimensions and depths must match. Channel order is the array order. |
| `cv.hconcat(sources[, opts])` | Concatenate images/matrices horizontally; heights and types must match. |
| `cv.vconcat(sources[, opts])` | Concatenate images/matrices vertically; widths and types must match. |

These functions return a matrix by default and support `opts.return_image = true`. They take a nonempty Lua array, not several positional images. `merge` normally receives single-channel results from `cv.split`; BGRA channel order is blue, green, red, alpha. Concatenation joins complete images without estimating overlaps; use `cv.stitch_long` for scrolling screenshots.

```lua
local a = cv.from_image(img, "bgr")
local width, height = a:size()
local b = cv.resize(cv.from_image(other_img, "bgr"), width, height)
local side_by_side = cv.hconcat({a, b}, {return_image = true})
local stacked = cv.vconcat({a, b})
local channels = cv.split(a)
local rebuilt = cv.merge(channels)
```

## Transform Matrices and Point Transforms

| Call | Result and use |
| --- | --- |
| `cv.get_affine_transform(src_points, dst_points)` | A 2-by-3 matrix from exactly three source and three destination points. Point order must correspond. |
| `cv.get_perspective_transform(src_points, dst_points)` | A 3-by-3 matrix from exactly four source and four destination points. Use consistently ordered, nondegenerate quadrilaterals. |
| `cv.get_rotation_matrix_2d(center, angle[, scale])` | A 2-by-3 rotation matrix; `center` is `{x, y}`, angle is in degrees, and scale defaults to `1`. |
| `cv.transform(points, matrix)` | Array of transformed `{x, y}` points using a 2-by-2 linear or 2-by-3 affine matrix. |
| `cv.perspective_transform(points, matrix)` | Array of transformed `{x, y}` points using a 3-by-3 projective matrix, including homogeneous-coordinate division. |

Matrices may be `cv.mat` values or numeric tables of the required shape, either nested rows or a flat row-major array. These functions transform points or create matrices; they do not warp image pixels. Apply the result with `cv.warp_affine` or `cv.warp_perspective`, whose full signatures are in [geometric transforms](cv.mat.md#resize-crop-and-geometric-transforms).

```lua
local src = {
    {x = 10, y = 20}, {x = 210, y = 20},
    {x = 210, y = 120}, {x = 10, y = 120},
}
local dst = {
    {x = 0, y = 0}, {x = 199, y = 0},
    {x = 199, y = 99}, {x = 0, y = 99},
}
local transform = cv.get_perspective_transform(src, dst)
local mapped = cv.perspective_transform({{x = 110, y = 70}}, transform)
local fixed = cv.warp_perspective(cv.from_image(img, "bgr"), transform, 200, 100)
local out = cv.to_image(fixed)
```

```lua
local src = {{x = 0, y = 0}, {x = 100, y = 0}, {x = 0, y = 100}}
local dst = {{x = 10, y = 20}, {x = 110, y = 20}, {x = 10, y = 120}}
local affine = cv.get_affine_transform(src, dst)
local shifted = cv.transform({{x = 25, y = 30}}, affine)
local rotation = cv.get_rotation_matrix_2d({x = 50, y = 50}, 15, 1)
```

## Kernels and Windows

| Call | Result and use |
| --- | --- |
| `cv.get_structuring_element(shape, width, height[, anchor_x][, anchor_y])` | Morphology kernel matrix. Shape is `"rect"`, `"ellipse"`, or `"cross"`; anchor defaults to `-1, -1` for the center. |
| `cv.create_hanning_window(width, height[, type_name])` | Single-channel Hanning window matrix for phase correlation. Use `"float32"` (default) or `"float64"`; dimensions should exceed `1`. |

The structuring-element anchor consists of two positional integers, not a point table. A Hanning window must match the frames' dimensions when passed to `cv.phase_correlate`.

```lua
local gray = cv.from_image(img, "gray")
local width, height = gray:size()
local kernel = cv.get_structuring_element("ellipse", 3, 3)
local binary = cv.threshold(gray, 127, 255, "binary")
local clean = cv.morphology_ex(binary, "open", kernel, 1)
local window = cv.create_hanning_window(width, height, "float32")
```

## Contour Geometry

These functions accept point arrays returned by `cv.find_contours`, `cv.to_shapes`, or explicit contour construction. They are module functions; there are no corresponding matrix methods. Use a contour, not a contour collection, unless the signature explicitly requests two contours.

| Call | Result and use |
| --- | --- |
| `cv.bounding_rect(contour)` | Axis-aligned `{x, y, width, height}` rectangle. |
| `cv.contour_area(contour[, oriented])` | Numeric enclosed area; `oriented = true` preserves orientation sign. |
| `cv.arc_length(contour[, closed])` | Numeric perimeter/path length; pass `true` to include the closing segment. |
| `cv.approx_poly_dp(contour, epsilon[, closed])` | Simplified contour; `epsilon` is an absolute distance in pixels, not a percentage. |
| `cv.convex_hull(contour[, return_points])` | Convex contour by default. With `false`, return one-based indices into the original contour. |
| `cv.point_polygon_test(contour, point[, measure_dist])` | With `false`, `1` inside, `0` on boundary, `-1` outside. With `true`, signed distance to the boundary. |
| `cv.match_shapes(contour1, contour2[, method][, parameter])` | Numeric shape difference; smaller is more similar. Method is integer `1`, `2`, or `3`, default `1`; parameter defaults to `0`. |
| `cv.min_area_rect(contour)` | Minimum-area rotated rectangle: `{center = {x, y}, size = {width, height}, angle}`. |
| `cv.box_points(rotated_rect)` | Four `{x, y}` corners of a rotated rectangle. Coordinates can be fractional. |
| `cv.min_enclosing_circle(contour)` | Table `{center = {x, y}, radius}`. |
| `cv.min_enclosing_triangle(contour)` | One table with an `area` field and `triangle = {point1, point2, point3}`, not two return values. |
| `cv.intersect_convex_convex(contour1, contour2[, handle_nested])` | One table with `area` and `contour` fields describing the intersection of two convex polygons; `handle_nested` defaults to `true`. |
| `cv.fit_line(contour[, dist_type][, param][, reps][, aeps])` | Table with `vx`, `vy`, `x`, `y`, plus the same four array entries; direction is `(vx, vy)` through `(x, y)`. Defaults: `"l2"`, `0`, `0.01`, `0.01`. |
| `cv.fit_ellipse(contour)` | Fitted rotated ellipse rectangle; at least five points required. |
| `cv.fit_ellipse_ams(contour)` | AMS ellipse fit, same return structure and minimum point count. |
| `cv.fit_ellipse_direct(contour)` | Direct ellipse fit, same return structure and minimum point count. |
| `cv.rotated_rectangle_intersection(rect1, rect2)` | One table `{code, type, contour}`. `type` is `"none"`, `"partial"`, or `"full"`; contour is the intersection polygon. |

Rotated rectangles use degrees and the `center`/`size` structure above; ellipse size values are full axis lengths, not radii. `fit_line` distance names include `l1`, `l2`, `l12`, `fair`, `welsch`, and `huber`. Pass `closed` explicitly for closed-shape perimeter and simplification. Image/mask moments are covered by `cv.moments(src[, binary_image])` and `cv.hu_moments(src[, binary_image])` in the [matrix reference](cv.mat.md#contours-components-and-moments).

```lua
local gray = cv.from_image(img, "gray")
local mask = cv.threshold(gray, 127, 255, "binary")
local contours = cv.find_contours(mask, "external", "none")
local marked = cv.from_image(img, "bgr")
for _, contour in ipairs(contours) do
    local area = cv.contour_area(contour)
    if area >= 50 then
        local perimeter = cv.arc_length(contour, true)
        local polygon = cv.approx_poly_dp(contour, perimeter * 0.02, true)
        local hull = cv.convex_hull(contour)
        local rect = cv.bounding_rect(contour)
        local signed_distance = cv.point_polygon_test(hull,
            {x = rect.x, y = rect.y}, true)
        marked = cv.polylines(marked, {polygon}, true, 0x00FF00, 2)
        if #contour >= 5 then
            local ellipse = cv.fit_ellipse(contour)
            local corners = cv.box_points(ellipse)
            print(area, ellipse.angle, #corners, signed_distance)
        end
    end
end
local out = cv.to_image(marked)
```

```lua
local a = {{x = 0, y = 0}, {x = 40, y = 0}, {x = 40, y = 30}, {x = 0, y = 30}}
local b = {{x = 20, y = 10}, {x = 60, y = 10}, {x = 60, y = 40}, {x = 20, y = 40}}
local difference = cv.match_shapes(a, b, 1, 0)
local intersection = cv.intersect_convex_convex(a, b)
local rotated = cv.rotated_rectangle_intersection(cv.min_area_rect(a), cv.min_area_rect(b))
local circle = cv.min_enclosing_circle(a)
local triangle = cv.min_enclosing_triangle(a)
local line = cv.fit_line(a, "l2", 0, 0.01, 0.01)
print(intersection.area, rotated.type, circle.radius, triangle.area, line.vx)
```

## Text Measurement

| Call | Result and use |
| --- | --- |
| `cv.get_text_size(text, font_face, font_scale[, thickness])` | One table `{width, height, baseline}` for Hershey text; thickness defaults to `1`. |

Use the same font, scale, and thickness when drawing with `cv.put_text`. Font names include `simplex`, `plain`, `duplex`, `complex`, `complex_small`, `triplex`, `script_simplex`, and `script_complex`. The drawing origin is the text's baseline anchor, not its upper-left corner. Use an image large enough for the placement below.

```lua
local text = "READY"
local size = cv.get_text_size(text, "simplex", 0.7, 1)
local mat = cv.from_image(img, "bgr")
local marked = cv.rectangle(mat, 8, 8, 12 + size.width,
    12 + size.height + size.baseline, 0x000000, -1)
local out = cv.put_text(marked, text, {x = 10, y = 10 + size.height},
    "simplex", 0.7, 0xFFFFFF, 1):to_image()
```

## High-Level ImageObject Functions

These functions require ImageObjects, not `cv.mat`, except that `stitch_long` takes an array of ImageObjects. They do not use generic `opts.inplace`/`opts.return_image` conventions.

| Call | Result and use |
| --- | --- |
| `cv.find_image(big, templ[, opts])` | Normally `x, y, confidence`; with `find_all = true`, an array of matches. See the return variants below. |
| `cv.binarize(img[, threshold])` | Modify and return `img` as a grayscale binary image. Omitted threshold selects Otsu; numeric threshold is an intensity value. |
| `cv.binarize_copy(img[, threshold])` | Same thresholding, returning a new ImageObject and preserving `img`. |
| `cv.resize_copy(img, width, height)` | New resized ImageObject; positive output dimensions required. |
| `cv.stitch_long(images[, opts])` | New long ImageObject assembled from ordered, overlapping scrolling screenshots; at least one input required. |
| `cv.find_polygon(img, opts)` | Array of polygon contours; optional visualization is the second return value. The options table and four filter fields are required. |
| `cv.compare_image(img1, img2[, opts])` | Array of difference contours, optionally followed by a visualization. Images must have identical dimensions. |
| `cv.to_shapes(img[, opts])` | Array of extracted contours, optionally followed by a visualization. |
| `cv.find_shapes(img, shape_image_or_contours[, opts])` | Array of result groups, one per template shape. Each matching contour has a `diff_score` field; optional visualization follows. |
| `cv.detect_templates(img, templates_and_options)` | Array of detected quadrilaterals with `index`, `angle`, and `confidence` fields; optional visualization follows. |

### Finding an Image

`find_image` options: `confidence_threshold` (default `95`, range `1..100`), `find_all` (default `false`), `downscale` (default `1`, range `0.1..1`), `should_visualize` (default `false`), and `mask` (an ImageObject with the original template dimensions). The template must fit inside `big`. White mask pixels participate; black mask pixels are ignored. Returned coordinates are relative to the original image even when downscaling.

- Single match: `x, y, confidence`; an unmatched result uses `x = -1, y = -1`. When visualization is requested, it is the fourth result.
- All matches: an array of `{x, y, confidence}`, empty when unmatched. When visualization is requested, it is the second result.

```lua
local matches, visual = cv.find_image(img, template_img, {
    confidence_threshold = 92,
    find_all = true,
    should_visualize = true,
    downscale = 0.5,
})
for _, match in ipairs(matches) do
    print(match.x, match.y, match.confidence)
end
```

A single-result search has a different return shape from `find_all = true`:

```lua
local x, y, confidence = cv.find_image(img, template_img, {
    confidence_threshold = 92,
})
if x ~= -1 then
    print(x, y, confidence)
end
```

### Binary and Resized Copies

```lua
local binary = cv.binarize_copy(img, 128)
local auto_binary = cv.binarize_copy(img)
local width, height = img:size()
local small = cv.resize_copy(img, math.max(1, math.floor(width / 2)),
    math.max(1, math.floor(height / 2)))
```

For the modifying variant, use a separate call when changing the source image is intentional. The returned ImageObject is the same `img`:

```lua
local binary = cv.binarize(img, 128)
```

The ImageObject forms have the same copy/mutation distinction:

```lua
local copied = img:cv_binarize_copy(128)
img:cv_binarize(128)
```

These APIs threshold brightness, not alpha. For transparency classification, extract alpha and use `cv.threshold`, as shown in the [color and transparency examples](image.cv.md#practical-examples-color-replacement-inverse-matching-and-transparency).

### Stitching Scrolling Screenshots

`stitch_long` options include `auto_crop` (default `true`), `top_crop`/`bottom_crop` (default `-1` for automatic), `keep_first_top`/`keep_last_bottom` (default `true`), `seam_blend_rows` (default `8`, `0` disables blending), `min_overlap_ratio`/`max_overlap_ratio` (defaults `0.02`/`0.95`), `template_height` (default `0` for automatic), and `score_threshold` (default `0.7`, a `0..1` match score).

Overlay options are `overlay_mode` (`none`, `remove_all`, `keep_first`), `overlay_fill_mode` (`temporal_only`, `temporal_then_inpaint`), and optional `overlay_regions` containing `{x, y, width, height}` rectangles. Supply images in scroll order with overlapping content. This function estimates alignment; `hconcat`/`vconcat` simply join complete images.

```lua
local out = cv.stitch_long({img, next_img, last_img}, {
    auto_crop = true,
    keep_first_top = true,
    keep_last_bottom = true,
    seam_blend_rows = 4,
})
```

### Polygon Filtering

`find_polygon` requires numeric `min_side_length`, `max_side_length`, `min_area`, and `max_area`. A negative limit disables that bound. Optional fields include `min_sides` (default `3`), `max_sides` (default `-1`), `blur_size` (default `3`, choose a positive odd value), `canny_threshold1`/`canny_threshold2` (defaults `100`/`200`), `approx_epsilon` (default `2`, a perimeter percentage), `closed` (default `true`), and `should_visualize` (default `false`). This percentage differs from `cv.approx_poly_dp`'s pixel-distance argument.

```lua
local polygons, visual = cv.find_polygon(img, {
    min_sides = 4, max_sides = 4,
    min_side_length = 10, max_side_length = -1,
    min_area = 100, max_area = -1,
    approx_epsilon = 2,
    closed = true,
    should_visualize = true,
})
```

### Image Differences and Shape Search

`compare_image` accepts `approx_epsilon` (default `2`, perimeter percentage in `0..100`) and `should_visualize`. It returns difference contours, not a numeric similarity score.

`to_shapes` accepts `blur_size`, `canny_threshold1`, `canny_threshold2`, `closed`, `approx_epsilon`, and `should_visualize`. Set `approx_epsilon` explicitly for consistent simplification. `find_shapes` accepts the same processing fields plus `min_area`, `max_area`, `diff_threshold` (default `0.001`, smaller is stricter), and integer `shape_match_mode` (`1..3`). Templates can be an ImageObject or an array of contours.

```lua
local shapes = cv.to_shapes(template_img, {
    closed = true, approx_epsilon = 2, blur_size = 3,
})
local groups, visual = cv.find_shapes(img, shapes, {
    closed = true, approx_epsilon = 2,
    min_area = 50, max_area = -1,
    diff_threshold = 0.01, shape_match_mode = 1,
    should_visualize = true,
})
for template_index, group in ipairs(groups) do
    for _, contour in ipairs(group) do
        print(template_index, contour.diff_score, #contour)
    end
end
```

```lua
local differences, visual = cv.compare_image(img, other_img, {
    approx_epsilon = 2, should_visualize = true,
})
```

### Feature-Based Template Detection

`templates_and_options` contains template ImageObjects in its array part and named options in the same table. `detector` is `0` (ORB, default), `1` (SIFT), or `2` (SURF). `score_thresh` (default `90`, range `0..100`) filters feature matches; it is not the same value as each result's combined `confidence`. Set `should_visualize = true` for a second visualization result. `index` identifies the original template by its one-based array position.

```lua
local detections, visual = cv.detect_templates(img, {
    template_img, second_template_img,
    detector = 0,
    score_thresh = 90,
    should_visualize = true,
})
for _, detection in ipairs(detections) do
    print(detection.index, detection.angle, detection.confidence)
end
```

## Built-in Paddle Lite Bindings

These are optional native bindings attached to `image.cv`, not NCNN/ONNX PaddleOCR wrappers. For ordinary OCR, prefer `screen.ocr_text` / `ImageObject:ocr_text` with explicit `engine = "paddle"` or `"apple"`. Read this section only when using these lower-level functions. Examples assume compatible local Paddle Lite models already exist; module discovery does not require installing models or wrappers.

| Call | Result and use |
| --- | --- |
| `cv.paddle_ocr(img)` | On success, `text, details`; on failure, `nil, error_message`. Uses shared OCR context, initialized with default local models when needed. No per-call options parameter. |
| `cv.paddle_ocr_init(opts)` | Initialize/configure shared OCR context; returns the context, or `nil, error_message` if model loading fails. |
| `cv.new_paddle_ocr(opts)` | Independent OCR context; returns the context, or `false, error_message` on model-loading failure. |
| `cv.new_paddle_yolov3(opts)` | New native Paddle Lite YOLOv3 detector context. Requires `model_path` and `label_list_path`. |
| `cv.new_paddle_yolov3_object_detector(opts)` | Alias of `cv.new_paddle_yolov3`, with identical options and context methods. |

For `paddle_ocr_init` and `new_paddle_ocr`, `det_path`, `cls_path`, `rec_path`, `config_path`, and `dict_path` are required strings. Optional `threads`, `power_mode` (default `"LITE_POWER_HIGH"`), and `downscale` configure inference; downscale is clamped to `0.1..1` and defaults to the inverse screen scale. The context supports `ctx:predict(img[, opts])` and `ctx:destroy()`. Prediction options are `downscale` and `should_visualize`; prediction returns an item array and optional visualization, or `nil, error_message` on failure. Items contain `text`, `confidence`, `x`, `y`, `w`, and `h`.

Shared `cv.paddle_ocr(img)` returns a text string first, then a details table whose array items have the same fields and whose `text` field contains the combined text. Do not interpret this pair as the independent context's `items, visualization` pair.

```lua
local root = XXT_HOME_PATH.."/models/ppocr_ch"
local ctx, err = cv.new_paddle_ocr({
    det_path = root.."/det_opt.nb",
    cls_path = root.."/cls_opt.nb",
    rec_path = root.."/rec_opt.nb",
    config_path = root.."/config.txt",
    dict_path = root.."/dict.txt",
    downscale = 1,
})
assert(ctx, err)
local items, visual_or_error = ctx:predict(img, {should_visualize = true})
ctx:destroy()
assert(items, visual_or_error)
```

For YOLOv3, optional fields are `threads`, `mean` (default `{0.485, 0.456, 0.406}`), `std` (default `{0.229, 0.224, 0.225}`), `downscale`, and `confidence_threshold` (default `50`, range `0..100`). Its context supports `detector:predict(img[, opts])` and `detector:destroy()`. Prediction options are `confidence_threshold`, `downscale`, and `should_visualize`; results contain `name`, `confidence` (percent), `x`, `y`, `w`, and `h`, followed by a visualization if requested. Unlike OCR prediction, inference failure can raise a Lua error.

```lua
local detector = cv.new_paddle_yolov3({
    model_path = model_path,
    label_list_path = label_list_path,
    confidence_threshold = 60,
    downscale = 1,
})
local ok, detections, visual = pcall(function()
    return detector:predict(img, {should_visualize = true})
end)
detector:destroy()
assert(ok, detections)
```
