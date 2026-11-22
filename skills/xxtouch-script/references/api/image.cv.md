# image.cv / cv.mat

`image.cv` is XXTouch's OpenCV-style image processing module. It must be loaded explicitly:

```lua
local cv = require("image.cv")
```

Version requirement: **XXTouch later than 20260402 is required.** This requirement applies to all practical examples below.

After loading, it returns the `cv` module table and adds a set of `cv_*` methods to `image_object`.

For lookup by function name, use the [cv.* module function reference](image.cv.functions.md). Shared functions also have explicit module signatures in the [cv.mat method tables](cv.mat.md).

## Use Cases

- Color space conversion, thresholding, filtering, morphology, contours, template matching, and geometric transforms.
- Use `cv.mat` when an `image_object` needs to be converted into an intermediate matrix for processing.
- For simple screenshots, color search, and basic ImageObject operations, prefer existing `screen` / `image_object` APIs.

## image_object and cv.mat

```lua
local img = assert(image.load_file(XXT_HOME_PATH.."/res/input.png"))

local mat = cv.from_image(img, "gray")
local out = mat:canny(80, 160):to_image()
out:save_to_png_file(XXT_HOME_PATH.."/res/edges.png")
```

Common conversions:

```lua
local mat1 = cv.from_image(img)
local mat2 = cv.from_image(img, "bgr")
local mat3 = img:cv_to_mat("gray")

local img2 = cv.to_image(mat1)
local img3 = mat1:to_image({normalize = true})
```

`cv.from_image(src[, color_mode])` supports common `color_mode` values:

- `"bgra"`
- `"bgr"`
- `"gray"` / `"grey"`
- `"rgb"`
- `"rgba"`

`cv.to_image(src[, opts])` converts `cv.mat` back to `image_object`. `opts.normalize = true` is commonly used to normalize floating-point matrices to `0` to `255`.

## Type Checks

```lua
print(cv.is(img))          -- true
print(cv.type(img))        -- image_object

local mat = cv.from_image(img)
print(cv.mat.is(mat))      -- true
print(cv.type(mat))        -- cv.mat
print(cv.version())        -- OpenCV version
```

Note: `image.type(img)` returns `"image"`, and `cv.type(img)` returns `"image_object"`.

## Return Rules

- Most processing functions return `cv.mat` by default, such as `cv.cvt_color`, `cv.blur`, `cv.threshold`, and `cv.canny`. For consistent matrix resize behavior, first use `cv.from_image(img)`; the three-argument `cv.resize(img, width, height)` call follows ImageObject resize behavior.
- Many functions support `opts.return_image = true` to return `image_object` directly.
- Drawing functions usually return `image_object` by default when an `image_object` is passed in, such as `cv.rectangle`, `cv.circle`, `cv.line`, `cv.draw_contours`, and `cv.put_text`.
- `opts.inplace = true` mainly makes sense for `cv.mat`, and not all functions support in-place writeback.

## cv.mat Methods

Read the [cv.mat working guide and complete method reference](cv.mat.md) for signatures, return values, mutation rules, channel requirements, and worked examples covering all public matrix methods.

Start with an image, keep intermediate results as matrices, then export the final image:

```lua
local mat = cv.from_image(img, "gray")
local width, height = mat:size()
local smoothed = mat:gaussian_blur(3, 3)
local binary = smoothed:threshold(127, 255, "binary")
local out = binary:to_image()
```

- `mat:operation(args)` usually matches `cv.operation(mat, args)`; matrix methods omit the first source argument.
- Capture returned matrices unless that specific method supports `inplace = true` and you explicitly request it.
- `mat:size()` returns `width, height`; `mat:shape()` returns `{rows, cols, channels}` with named fields.
- Select a section in the detailed guide for masks, geometry, arithmetic, statistics, filters, morphology, contours, matching, features, motion, or drawing.

## Color Spaces and Channels

```lua
local gray = cv.cvt_color(img, "bgra2gray")
local hsv = cv.cvt_color(img, "bgr2hsv")
local rgba = cv.cvt_color(hsv, "hsv2rgba")
```

Common conversion codes:

- `bgra2gray`
- `bgr2gray`
- `gray2bgr`
- `gray2bgra`
- `bgr2rgb`
- `bgra2rgba`
- `bgr2hsv` / `hsv2bgr`
- `bgr2lab` / `lab2bgr`
- `bgr2ycrcb` / `ycrcb2bgr`

Channel operations:

```lua
local bgr = cv.from_image(img, "bgr")
local channels = cv.split(bgr)
local merged = cv.merge(channels)
local alpha = cv.extract_channel(cv.from_image(img), 3)
```

## Size and Geometry

```lua
local mat = cv.from_image(img, "bgr")
local small = mat:resize(540, 960)
local half = mat:resize(0, 0, {fx = 0.5, fy = 0.5})
local rotated = cv.rotate(small, "90clockwise")
local flipped = cv.flip(rotated, "horizontal")
```

Common interpolation modes: `nearest`, `linear` / `bilinear`, `cubic`, `area`, `lanczos4`.

Perspective and affine:

```lua
local M = cv.get_perspective_transform(src_points, dst_points)
local fixed = cv.warp_perspective(img, M, 300, 200)
```

Common border types: `constant`, `replicate`, `reflect`, `wrap`, `reflect101`, `transparent`.

## Thresholding, Filtering, and Morphology

```lua
local gray = cv.from_image(img, "gray")
local used, binary = cv.threshold(gray, 0, 255, "binary|otsu", {
    return_threshold = true,
})

local kernel = cv.get_structuring_element("rect", 3, 3)
local opened = cv.morphology_ex(binary, "open", kernel)
```

`cv.threshold` types support `binary`, `binary_inv`, `trunc`, `tozero`, and `tozero_inv`. Combinations such as `binary|otsu` and `binary|triangle` are also supported.

Common functions:

- `cv.blur(src, ksize[, opts])`
- `cv.gaussian_blur(src, kx, ky[, sigma_x][, sigma_y][, opts])`
- `cv.median_blur(src, ksize[, opts])`
- `cv.bilateral_filter(src, d, sigma_color, sigma_space)`
- `cv.normalize(src[, opts])`
- `cv.in_range(src, lower, upper)`
- `cv.canny(src, threshold1, threshold2)`
- `cv.erode(src, kernel[, iterations][, opts])`
- `cv.dilate(src, kernel[, iterations][, opts])`
- `cv.morphology_ex(src, op, kernel[, iterations][, opts])`

Morphology `op` supports `open`, `close`, `gradient`, `tophat`, and `blackhat`.

## Contours and Template Matching

```lua
local contours, hierarchy = cv.find_contours(binary, "external", "simple", {
    return_hierarchy = true,
})

local marked = cv.draw_contours(img, contours, 0x00FF00, 2)
```

Common `find_contours` `mode` values: `external`, `list`, `ccomp`, `tree`. Common `method` values: `none`, `simple`, `tc89l1`, `tc89kcos`.

Template matching:

```lua
local response = cv.match_template(big, small, "ccoeff_normed")
local stat = cv.min_max_loc(response)
print(stat.max_val, stat.max_loc.x, stat.max_loc.y)
```

`cv.min_max_loc` returns `min_val`, `max_val`, `min_loc = {x, y}`, and `max_loc = {x, y}`.

## Drawing

```lua
local out = cv.rectangle(img, 100, 100, 300, 260, 0x00FF00, 2)
out = cv.put_text(out, "OK", {x = 20, y = 40}, "simplex", 1.0, 0x00FF00, 2)
```

The `org` parameter of `put_text` is the baseline position of the lower-left corner of the text, not the upper-left corner.

## Practical Examples: Color Replacement, Inverse Matching, and Transparency

These snippets assume that `img` is an existing `image_object` and `local cv = require("image.cv")` has already run. Each example is independent and produces a new image named `out` without modifying the original `img`.

Shared conventions:

- `cv.from_image(img, "bgra")` preserves the alpha channel. Channel indices start at `0`; alpha is channel `3`.
- Determine transparency from alpha. A pixel with RGB `0x000000` can still be fully opaque black.
- `cv.in_range` checks each channel against inclusive lower and upper bounds and returns a single-channel `0/255` mask. Its range checks differ from the similarity algorithms used by `replace_color`.
- `cv.bitwise_not` inverts a `0/255` mask; `cv.bitwise_or` combines color conditions; `cv.set_to` replaces only pixels selected by nonzero mask values.
- Assigning a `0xRRGGBB` value to a BGRA matrix sets alpha to `255`. Use `{r = ..., g = ..., b = ..., a = ...}` to specify alpha explicitly.
- In `cv.in_range(mat, color, color)` on a BGRA matrix, integer color bounds also imply alpha `255`. To compare RGB alone, explicitly cover alpha values from `0` to `255`, or calculate the mask using a BGR copy.
- `cv.from_image` creates a matrix copy. In this section, `inplace = true` modifies only that copy. When `inplace` is omitted, use the returned result.

### Make Fully Transparent Pixels Black and All Others White

Use this to extract the foreground silhouette from a PNG with a transparent background, regardless of the foreground colors.

```lua
local mat = cv.from_image(img, "bgra")
local alpha = cv.extract_channel(mat, 3)
local out = cv.threshold(alpha, 0, 255, "binary", {
    return_image = true,
})
```

`alpha == 0` produces black; `alpha > 0` produces white, including partially transparent pixels. The resulting `out` image is fully opaque and contains only black and white.

To make only fully opaque pixels white, change the threshold from `0` to `254`. To make fully transparent regions white and all others black, replace `"binary"` with `"binary_inv"`.

### Keep One Color and Replace All Others

Keep red pixels and replace all non-red pixels with opaque white. Selected red pixels retain their original alpha.

```lua
local mat = cv.from_image(img, "bgra")
local keep_mask = cv.in_range(mat,
    {r = 255, g = 0, b = 0, a = 0},
    {r = 255, g = 0, b = 0, a = 255}
)
local replace_mask = cv.bitwise_not(keep_mask)
local out = cv.set_to(mat, 0xFFFFFF, replace_mask, {
    return_image = true,
})
```

This combines existing APIs to perform inverse matching. The current `img:replace_color` API has no `invert` option.

### Replace Pixels Within a Color Tolerance

Replace pixels near red with black and preserve all others. The bounds are `R = 239..255`, `G = 0..16`, and `B = 0..16`, with no alpha restriction.

```lua
local mat = cv.from_image(img, "bgra")
local mask = cv.in_range(mat,
    {r = 239, g = 0, b = 0, a = 0},
    {r = 255, g = 16, b = 16, a = 255}
)
local out = cv.set_to(mat, 0x000000, mask, {
    return_image = true,
})
```

These bounds represent a tolerance of `0x10` per channel around `0xFF0000`, clamped to `0..255`. To preserve this range and replace pixels outside it, apply `cv.bitwise_not` to `mask` before assigning the new color.

### Replace Multiple Colors with One Color

Replace both red and green with black. Convert only the copy used for matching to BGR, then assign colors on the BGRA matrix to preserve the transparency of all other pixels.

```lua
local mat = cv.from_image(img, "bgra")
local bgr = cv.cvt_color(mat, "bgra2bgr")
local red_mask = cv.in_range(bgr, 0xFF0000, 0xFF0000)
local green_mask = cv.in_range(bgr, 0x00FF00, 0x00FF00)
local mask = cv.bitwise_or(red_mask, green_mask)
local out = cv.set_to(mat, 0x000000, mask, {
    return_image = true,
})
```

To keep red and green and make everything else white, invert the combined `mask` and change the assigned color to `0xFFFFFF`.

### Apply Multiple Color Mappings Without Cascading Replacements

Map original red pixels to green and original green pixels to blue. Calculate all masks from the original image before assigning colors, so the green pixels created by the first mapping are not replaced again by the second.

```lua
local mat = cv.from_image(img, "bgra")
local bgr = cv.cvt_color(mat, "bgra2bgr")
local red_mask = cv.in_range(bgr, 0xFF0000, 0xFF0000)
local green_mask = cv.in_range(bgr, 0x00FF00, 0x00FF00)

cv.set_to(mat, 0x00FF00, red_mask, {inplace = true})
cv.set_to(mat, 0x0000FF, green_mask, {inplace = true})
local out = mat:to_image()
```

### Make a White Background Transparent

Select exact white and clear those pixels, leaving all other pixels unchanged. For backgrounds with compression noise or antialiasing, use the range-based matching shown above.

```lua
local mat = cv.from_image(img, "bgra")
local bgr = cv.cvt_color(mat, "bgra2bgr")
local mask = cv.in_range(bgr, 0xFFFFFF, 0xFFFFFF)
local out = cv.set_to(mat, {r = 0, g = 0, b = 0, a = 0}, mask, {
    return_image = true,
})
```

Save transparent results with `out:save_to_png_file(output_path)`, where `output_path` is chosen by the script. JPEG does not preserve transparency.

## image_object-centered cv APIs

See [high-level ImageObject functions](image.cv.functions.md#high-level-imageobject-functions) for complete options, return variants, and examples. These APIs accept ImageObjects rather than matrices:

- `cv.find_image(big, templ[, opts])`
- `cv.binarize(img[, threshold])` / `img:cv_binarize([threshold])`
- `cv.binarize_copy(img[, threshold])` / `img:cv_binarize_copy([threshold])`
- `cv.resize_copy(img, width, height)`
- `cv.stitch_long(images[, opts])`
- `cv.find_polygon(img, opts)`
- `cv.compare_image(img1, img2[, opts])`
- `cv.find_shapes(img, shape_image_or_contours[, opts])`
- `cv.to_shapes(img[, opts])`
- `cv.detect_templates(img, template_images_opts_table)`

```lua
local x1, y1, sim1 = cv.find_image(big, templ, {confidence_threshold = 92})
local x2, y2, sim2 = big:cv_find_image(templ, {confidence_threshold = 92})
```
