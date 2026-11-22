# cv.mat: Working Guide and Method Reference

Version requirement: **XXTouch later than 20260402 is required.** This applies to every method and example below. The signatures follow the XXTouch Lua binding, which differs from OpenCV's Python and C++ APIs.

For loading the module and ImageObject operations, see [image.cv](image.cv.md). For module-only functions, see the [cv.* function reference](image.cv.functions.md). For color replacement and transparency recipes, see its [practical examples](image.cv.md#practical-examples-color-replacement-inverse-matching-and-transparency).

Read the relevant section:

- [Creation, calls, and ownership](#creation-calls-and-ownership)
- [Inspection, copying, and conversion](#inspection-copying-and-conversion)
- [Color spaces and channels](#color-spaces-and-channels)
- [Masks and selective assignment](#masks-and-selective-assignment)
- [Resize, crop, and geometric transforms](#resize-crop-and-geometric-transforms)
- [Arithmetic and comparisons](#arithmetic-and-comparisons)
- [Statistics and reductions](#statistics-and-reductions)
- [Thresholding and filters](#thresholding-and-filters)
- [Edges and morphology](#edges-and-morphology)
- [Contours, components, and moments](#contours-components-and-moments)
- [Template matching and histograms](#template-matching-and-histograms)
- [Lines, circles, corners, and distance maps](#lines-circles-corners-and-distance-maps)
- [Flood fill](#flood-fill)
- [Motion and vector fields](#motion-and-vector-fields)
- [Drawing and annotation](#drawing-and-annotation)

## Creation, Calls, and Ownership

```lua
local cv = require("image.cv")
local img = screen.image()
local mat = cv.from_image(img, "gray")

local blurred = mat:gaussian_blur(5, 5)
local edges = blurred:canny(80, 160)
local out = edges:to_image()
```

`cv.mat` is a userdata containing an image or a numerical matrix. Create it with `cv.from_image(img[, mode])`, `img:cv_to_mat([mode])`, or another CV operation. `cv.mat` itself is a table exposing `cv.mat.is(value)`, not a constructor. This binding does not expose NumPy-style indexing, `mat:get`, `mat:at`, `mat:zeros`, or arbitrary Lua-table construction. Use ImageObject pixel APIs when individual pixel access is necessary.

The method tables give the complete module signature alongside each shared matrix method. `src` is an ImageObject or matrix; `channel` is a single-channel source matrix; `x`/`magnitude` identify vector components. For ImageObject inputs, module functions can differ in default return type; see the [function calling rules](image.cv.functions.md#shared-image-and-matrix-functions). Additional images or matrices are ordinary arguments. `alpha:insert_channel(dst, 3)` inserts the receiver into `dst`, not the other way around.

The snippets below assume `cv` is loaded and `img` is an existing ImageObject. Examples requiring another image use `other_img` or `template_img` explicitly. Coordinates are image-local, with `(0, 0)` at the top left. Lua arrays start at `1`; CV channel indices start at `0`.

### Results and Mutation

- Matrix-producing operations return a new `cv.mat` by default. Capture the result or chain another method on it.
- Methods with a trailing `opts` parameter generally support `return_image = true`; this returns an ImageObject and ends a matrix-method chain. Methods returning numbers or Lua tables keep those return types.
- `cv.from_image` and `mat:clone()` copy pixel data. `local alias = mat` shares the same userdata; it does not copy anything.
- `inplace = true` changes the existing matrix only on methods that explicitly support it. Existing aliases observe the change. It does not make `cv.from_image` write back to the source ImageObject.
- Matrices are released by Lua garbage collection. Drop unneeded references between iterations of long-running image loops. There is no public `mat:destroy()` method.

Methods supporting `inplace`: `cvt_color`, `insert_channel` (modifies its destination), `rotate`, `flip`, `transpose`, `resize`, `copy_to`, `set_to`, `threshold`, `blur`, `gaussian_blur`, `median_blur`, `erode`, `dilate`, `morphology_ex`, `flood_fill`, and all drawing methods listed below.

`repeat`, `reduce`, `remap`, `warp_perspective`, `warp_affine`, `pyr_down`, `pyr_up`, and `get_rect_sub_pix` explicitly reject `inplace = true`. Other methods that do not implement in-place processing can ignore that option; do not use it as a general guarantee.

```lua
local original = cv.from_image(img, "gray")
local alias = original
local independent = original:clone()

original:threshold(127, 255, "binary", {inplace = true})
local binary_img = alias:to_image()
local unchanged_img = independent:to_image()
```

## Inspection, Copying, and Conversion

| Matrix call | Module call | Result and meaning |
| --- | --- | --- |
| `mat:type()` | Method only | String including depth and channels, such as `uint8C4` or `float32C1`. |
| `mat:depth()` | Method only | `uint8`, `int8`, `uint16`, `int16`, `int32`, `float32`, or `float64`. |
| `mat:channels()` | Method only | Number of channels. Gray and masks normally have `1`; BGR has `3`; BGRA has `4`. |
| `mat:size()` | Method only | Two integers: `width, height`, equivalently `cols, rows`. |
| `mat:shape()` | Method only | Table `{rows, cols, channels}` with the same named fields. Its first two entries have the opposite order from `size()`. |
| `mat:clone()` | Method only | Independent matrix copy. |
| `mat:astype(type_name[, opts])` | Method only | New matrix with converted numeric depth. Use `"float32"` to preserve signed/fractional results or `"uint8"` for ordinary pixels. |
| `mat:to_image([opts])` | `cv.to_image(src[, opts])` | New displayable ImageObject. Float matrices are normalized to `0..255` by default; use `{normalize = false}` to convert without normalization. |

`astype` converts numeric storage, not color spaces or channel layouts. Even a type string with a `C` suffix does not replace `cvt_color`, `extract_channel`, or `merge`. Numeric conversion does not automatically scale `0..255` to `0..1`.

`to_image` displays single-channel data as opaque grayscale, three-channel data as BGR, and four-channel data as BGRA. Convert HSV, Lab, RGB, or RGBA results to the corresponding BGR/BGRA layout before export. Keep float response maps, histograms, and label matrices as matrices for analysis; converting them to an image can discard numerical information.

```lua
local mat = cv.from_image(img, "bgr")
local width, height = mat:size()
local shape = mat:shape()
assert(shape.cols == width and shape.rows == height)
assert(cv.mat.is(mat) and cv.type(mat) == "cv.mat")

local gray = mat:cvt_color("bgr2gray")
local unit = gray:astype("float32"):divide(255)
local average = unit:mean()[1]
local out = unit:multiply(255):to_image({normalize = false})
```

## Color Spaces and Channels

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:cvt_color(code[, opts])` | `cv.cvt_color(src, code[, opts])` | Converted matrix, for example `"bgra2gray"`, `"bgra2bgr"`, `"bgr2hsv"`, `"hsv2bgr"`, `"bgr2lab"`, or `"lab2bgr"`. |
| `mat:split()` | `cv.split(src)` | Lua array of single-channel matrix copies in storage order. BGRA produces blue, green, red, alpha. |
| `mat:extract_channel(coi[, opts])` | `cv.extract_channel(src, coi[, opts])` | One channel as a matrix. `coi` is zero-based. |
| `mat:insert_channel(dst, coi[, opts])` | `cv.insert_channel(channel, dst, coi[, opts])` | Destination matrix with the single-channel receiver inserted at `coi`. Source and destination dimensions must match. |

Combine channels with the module function `cv.merge(channel_array[, opts])`; there is no `mat:merge()` method. Channels must have compatible dimensions and depth. Integer colors are interpreted as RGB and converted to BGR/BGRA scalars. Scalar arrays `{R, G, B[, A]}` are also reordered by this binding. For HSV bounds, use explicit storage-slot keys: `{b = H, g = S, r = V}`.

```lua
local mat = cv.from_image(img, "bgra")
local parts = mat:split()
local swapped = cv.merge({parts[3], parts[2], parts[1], parts[4]})
local out = swapped:to_image()

local alpha = mat:extract_channel(3)
local restored = alpha:insert_channel(swapped, 3)
```

The array indices above are one-based even though the extracted alpha channel index is `3`.

## Masks and Selective Assignment

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:in_range(lower, upper[, opts])` | `cv.in_range(src, lower, upper[, opts])` | Single-channel `uint8` mask: `255` when every channel lies inside its inclusive bounds, `0` otherwise. |
| `mat:set_to(value[, mask][, opts])` | `cv.set_to(src, value[, mask][, opts])` | Set selected pixels to a scalar color/value; unselected pixels remain unchanged. With no mask, fill the whole matrix. |
| `mat:copy_to([mask][, opts])` | `cv.copy_to(src[, mask][, opts])` | Matrix copy. The current binding starts from a full source copy, so an optional mask does **not** black out unselected pixels or name a separate destination. Use `set_to` for selective changes. |
| `mat:bitwise_and(other[, mask][, opts])` | `cv.bitwise_and(src, other[, mask][, opts])` | Bitwise intersection. Use with two `0/255` masks to require both conditions. |
| `mat:bitwise_or(other[, mask][, opts])` | `cv.bitwise_or(src, other[, mask][, opts])` | Bitwise union. Use with masks to accept either condition. |
| `mat:bitwise_xor(other[, mask][, opts])` | `cv.bitwise_xor(src, other[, mask][, opts])` | Bits that differ; for masks, selects exactly one condition. |
| `mat:bitwise_not([mask][, opts])` | `cv.bitwise_not(src[, mask][, opts])` | Bitwise inversion. On a `0/255` mask, exchanges selected and unselected pixels. |

Masks should be single-channel `uint8` matrices with the same width and height as the target; nonzero values select pixels. `in_range` makes suitable masks directly. Bitwise binary methods require two image/matrix operands of compatible size and type, not scalar colors. An optional mask on a bitwise operation limits computation; it is different from combining two masks as operands.

When omitting a mask from `set_to`, `copy_to`, or a bitwise method, pass `opts` directly in its place, such as `mat:set_to(0, {inplace = true})`. Do not assume a `nil` placeholder shifts `opts` to the following position.

On BGRA data, an integer bound implies alpha `255`. Ignore alpha by explicitly spanning `0..255`, or calculate the mask on BGR data. Single-channel scalar `255` means intensity `255`; on BGR/BGRA data the same integer is an RGB color.

```lua
local mat = cv.from_image(img, "bgra")
local bgr = mat:cvt_color("bgra2bgr")
local red = bgr:in_range(0xFF0000, 0xFF0000)
local green = bgr:in_range(0x00FF00, 0x00FF00)
local selected = red:bitwise_or(green)
local width, height = selected:size()
local coverage = selected:count_non_zero() / (width * height)
local out = mat:set_to(0x000000, selected, {return_image = true})
```

## Resize, Crop, and Geometric Transforms

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:resize(width, height[, interpolation][, opts])` | `cv.resize(src, width, height[, interpolation][, opts])` | Resized matrix. Explicit dimensions may change aspect ratio; use `0, 0, {fx = ..., fy = ...}` for scale factors. |
| `mat:rotate(code[, opts])` | `cv.rotate(src, code[, opts])` | Quarter-turn rotation: `"90clockwise"`, `"180"`, or `"90counterclockwise"`. |
| `mat:flip(code[, opts])` | `cv.flip(src, code[, opts])` | Mirror using `"horizontal"`, `"vertical"`, or `"both"`. |
| `mat:transpose([opts])` | `cv.transpose(src[, opts])` | Exchange rows and columns. |
| `mat["repeat"](mat, ny, nx[, opts])` | `cv["repeat"](src, ny, nx[, opts])` | Tile the entire matrix `ny` times vertically and `nx` times horizontally. `repeat` is a Lua keyword, so colon/dot syntax is invalid. |
| `mat:pyr_down([opts])` | `cv.pyr_down(src[, opts])` | Gaussian pyramid reduction, about half the width/height by default. |
| `mat:pyr_up([opts])` | `cv.pyr_up(src[, opts])` | Pyramid expansion, about twice the width/height by default. |
| `mat:get_rect_sub_pix(width, height, center[, opts])` | `cv.get_rect_sub_pix(src, width, height, center[, opts])` | Bilinearly sampled patch centered at `{x, y}`. Use one-channel or three-channel input. |
| `mat:copy_make_border(top, bottom, left, right[, border_type][, value][, opts])` | `cv.copy_make_border(src, top, bottom, left, right[, border_type][, value][, opts])` | Add border pixels. Pass a numeric color for `value` in this positional form. |
| `mat:warp_affine(matrix, width, height[, interpolation][, border_type][, border_value][, opts])` | `cv.warp_affine(src, matrix, width, height[, interpolation][, border_type][, border_value][, opts])` | Apply a 2-by-3 affine transform. |
| `mat:warp_perspective(matrix, width, height[, interpolation][, border_type][, border_value][, opts])` | `cv.warp_perspective(src, matrix, width, height[, interpolation][, border_type][, border_value][, opts])` | Apply a 3-by-3 projective transform. |
| `mat:remap(map1[, map2][, interpolation][, opts])` | `cv.remap(src, map1[, map2][, interpolation][, opts])` | Sample using coordinate maps; output dimensions come from the maps. |

Interpolation names include `nearest`, `linear`, `cubic`, `area`, and `lanczos4`. Use `nearest` when resizing binary masks; interpolating mask values changes their meaning. `resize` also accepts `opts.interpolation`. `pyr_down`/`pyr_up` allow `opts.width` and `opts.height` within OpenCV's pyramid size constraints, rather than arbitrary resize dimensions.

For warp methods, interpolation, border type, and numeric border color are positional arguments. Passing `opts.border_type` alone does not configure those methods. `remap` does read `opts.interpolation`, `opts.border_type`, and `opts.border_value`, and accepts `nil` to skip `map2`. A pair of single-channel `float32` maps stores source x and y coordinates for every destination pixel; this binding has no generic coordinate-map constructor.

Use `cv.get_rotation_matrix_2d`, `cv.get_affine_transform`, or `cv.get_perspective_transform` to create transform matrices. Affine/projective methods also accept numeric tables of the required shape.

```lua
local mat = cv.from_image(img, "bgr")
local width, height = mat:size()
local half = mat:resize(0, 0, {fx = 0.5, fy = 0.5, interpolation = "area"})
local patch = mat:get_rect_sub_pix(64, 48, {
    x = (width - 1) / 2, y = (height - 1) / 2,
})
local padded = patch:copy_make_border(8, 8, 8, 8, "constant", 0xFFFFFF)
local tiled = padded["repeat"](padded, 2, 3)
local preview = tiled:rotate("90clockwise"):flip("horizontal"):to_image()
```

For a straight crop without interpolation, crop the ImageObject first with its documented `crop` method, then convert it to a matrix.

```lua
local mat = cv.from_image(img, "bgr")
local width, height = mat:size()
local center = {x = (width - 1) / 2, y = (height - 1) / 2}
local transform = cv.get_rotation_matrix_2d(center, 12, 1)
local rotated = mat:warp_affine(transform, width, height,
    "linear", "constant", 0xFFFFFF)
local translated = mat:warp_perspective({
    {1, 0, 10}, {0, 1, 20}, {0, 0, 1},
}, width, height, "nearest", "constant", 0x000000)
```

## Arithmetic and Comparisons

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:absdiff(other[, opts])` | `cv.absdiff(src, other[, opts])` | Absolute difference. Requires identical dimensions and matrix type. |
| `mat:add(rhs[, opts])` | `cv.add(src, rhs[, opts])` | Elementwise addition; `rhs` may be a scalar or matching image/matrix. |
| `mat:subtract(rhs[, opts])` | `cv.subtract(src, rhs[, opts])` | Elementwise subtraction. Unsigned outputs saturate at zero. |
| `mat:multiply(rhs[, scale][, opts])` | `cv.multiply(src, rhs[, scale][, opts])` | Elementwise product times `scale`, default `1`; not matrix multiplication. |
| `mat:divide(rhs[, scale][, opts])` | `cv.divide(src, rhs[, scale][, opts])` | Elementwise `mat / rhs * scale`, default scale `1`. |
| `mat:compare(rhs, op[, opts])` | `cv.compare(src, rhs, op[, opts])` | Per-channel `0/255` comparison using `eq`, `ne`, `lt`, `le`, `gt`, or `ge`. |
| `mat:add_weighted(alpha, other, beta[, gamma][, opts])` | `cv.add_weighted(src, alpha, other, beta[, gamma][, opts])` | Weighted blend `alpha * mat + beta * other + gamma`; matrices must have identical dimensions and type. |

For `add`, `subtract`, `multiply`, `divide`, and `compare`, matrix operands need matching dimensions and channel counts; the right-hand depth is converted to the receiver's depth. Convert both operands to `float32` **before** arithmetic when preserving negatives, fractions, or large values matters. `opts.dtype` selects output depth on arithmetic methods except `absdiff` and `compare`. With `multiply`/`divide`, supply the scale before `opts`; with `add_weighted`, supply `gamma` before `opts`.

`compare` on a multichannel matrix returns a multichannel result, not a single pixel mask. Use grayscale comparison or `in_range` when constructing a mask for `set_to`.

```lua
local a = cv.from_image(img, "gray")
local width, height = a:size()
local b = cv.from_image(other_img, "gray"):resize(width, height)
local diff = a:absdiff(b)
local changed = diff:compare(20, "gt")
local changed_fraction = changed:count_non_zero() / (width * height)
local blended = a:add_weighted(0.7, b, 0.3, 0)
local signed = a:astype("float32"):subtract(b:astype("float32"))
```

## Statistics and Reductions

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:sum()` | `cv.sum(src)` | Per-channel sums as a table. |
| `mat:mean([mask])` | `cv.mean(src[, mask])` | Per-channel means, optionally restricted to a mask. |
| `mat:mean_std_dev([mask])` | `cv.mean_std_dev(src[, mask])` | Two per-channel tables: mean, then standard deviation. |
| `mat:count_non_zero()` | `cv.count_non_zero(src)` | Integer count; use a single-channel mask to count selected pixels. |
| `mat:norm([norm_type][, mask])` | `cv.norm(src[, norm_type][, mask])` | Numeric norm of one matrix; default is `l2`. |
| `mat:norm(other[, norm_type][, mask])` | `cv.norm(src, other[, norm_type][, mask])` | Numeric norm of the difference from another matrix. |
| `mat:reduce(dim, op[, opts])` | `cv.reduce(src, dim, op[, opts])` | Row/column reduction matrix; `op` is `sum`, `avg`, `min`, or `max`. |

Per-channel tables use storage order: `[1]` for gray; `[1]=B, [2]=G, [3]=R, [4]=A` for BGRA, with matching `b/g/r/a` fields. For HSV or other layouts, use numeric indices; field labels do not change with the color space. `count_non_zero` converts multichannel input to grayscale, so it should not be used to count matching colors directly.

`reduce(0, ...)` collapses rows into one row; `reduce(1, ...)` collapses columns into one column. For an 8-bit image, use `{dtype = "float32"}` with sum/average reductions to avoid unsupported output types or lost range. Norm names are `inf`, `l1`, and `l2`; use `minmax` with `normalize`, not with `norm`.

```lua
local gray = cv.from_image(img, "gray")
local mask = gray:in_range(180, 255)
local mean, stddev = gray:mean_std_dev(mask)
local total = gray:sum()[1]
local columns = gray:reduce(0, "sum", {dtype = "float32"})
local rows = gray:reduce(1, "avg", {dtype = "float32"})
print(mean[1], stddev[1], total, columns:size(), rows:size())
```

## Thresholding and Filters

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:threshold(thresh, maxval, type[, opts])` | `cv.threshold(src, thresh, maxval, type[, opts])` | Thresholded matrix. `binary` uses `maxval` when input is strictly greater than `thresh`, else zero. |
| `mat:adaptive_threshold(maxval, method, type, block_size, c[, opts])` | `cv.adaptive_threshold(src, maxval, method, type, block_size, c[, opts])` | Local thresholding with `mean` or `gaussian`; use `binary`/`binary_inv` and odd block size greater than `1`. |
| `mat:blur(ksize[, opts])` | `cv.blur(src, ksize[, opts])` | Square mean filter. |
| `mat:gaussian_blur(kx, ky[, sigma_x][, sigma_y][, opts])` | `cv.gaussian_blur(src, kx, ky[, sigma_x][, sigma_y][, opts])` | Gaussian smoothing; odd positive kernel dimensions, sigma defaults to `0`. |
| `mat:median_blur(ksize[, opts])` | `cv.median_blur(src, ksize[, opts])` | Median filter; use an odd kernel size greater than `1`. |
| `mat:bilateral_filter(d, sigma_color, sigma_space[, opts])` | `cv.bilateral_filter(src, d, sigma_color, sigma_space[, opts])` | Edge-preserving smoothing; use one-channel or three-channel 8-bit/float32 input, not BGRA. |
| `mat:equalize_hist([opts])` | `cv.equalize_hist(src[, opts])` | Global histogram equalization; output is 8-bit grayscale. |
| `mat:clahe([clip_limit][, tile_width][, tile_height][, opts])` | `cv.clahe(src[, clip_limit][, tile_width][, tile_height][, opts])` | Local contrast enhancement; tile counts default to `8, 8`, clip limit to `40`. |
| `mat:normalize([opts])` | `cv.normalize(src[, opts])` | Rescale numerical values. Defaults to min/max normalization over `0..255`; accepts `alpha`, `beta`, `norm_type`, and `dtype`. |

Use an 8-bit grayscale input for binary/OTSU image workflows. `adaptive_threshold`, `equalize_hist`, and `clahe` convert their input to 8-bit grayscale. `threshold` itself does not automatically convert a color matrix to grayscale.

`threshold(..., {return_threshold = true})` returns **`used_threshold, result`**. Without that option, it returns just the result. Other threshold types are `binary_inv`, `trunc`, `tozero`, and `tozero_inv`. `"binary|otsu"` and `"binary|triangle"` select an automatic threshold.

```lua
local gray = cv.from_image(img, "gray")
local contrast = gray:clahe(2.0, 8, 8)
local smooth = contrast:gaussian_blur(3, 3)
local used, binary = smooth:threshold(0, 255, "binary|otsu", {
    return_threshold = true,
})
local local_binary = contrast:adaptive_threshold(255, "gaussian",
    "binary", 21, 5)
local out = binary:to_image()
```

For numerical maps, normalize only a display copy; retain the original values for analysis:

```lua
local gray = cv.from_image(img, "gray")
local gradient = gray:sobel(1, 0, {ddepth = "float32"})
local display = gradient:normalize({
    alpha = 0, beta = 255, norm_type = "minmax", dtype = "uint8",
}):to_image()
```

## Edges and Morphology

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:canny(threshold1, threshold2[, opts])` | `cv.canny(src, threshold1, threshold2[, opts])` | Single-channel 8-bit edge map. These thresholds are pixel-gradient thresholds, not percentages. |
| `mat:sobel(dx, dy[, opts])` | `cv.sobel(src, dx, dy[, opts])` | Signed derivative, default depth `int16`. `ddepth`, `ksize`, `scale`, `delta`, and `border_type` are options. |
| `mat:scharr(dx, dy[, opts])` | `cv.scharr(src, dx, dy[, opts])` | Scharr derivative; `dx, dy` should be `(1, 0)` or `(0, 1)`. Supports `ddepth`, `scale`, `delta`, and `border_type`. |
| `mat:laplacian([opts])` | `cv.laplacian(src[, opts])` | Second spatial derivative; options include `ddepth`, `ksize`, `scale`, `delta`, and `border_type`. |
| `mat:convert_scale_abs([alpha][, beta][, opts])` | `cv.convert_scale_abs(src[, alpha][, beta][, opts])` | Convert `abs(alpha * value + beta)` to 8-bit values, useful for displaying signed derivatives. |
| `mat:erode(kernel[, iterations][, opts])` | `cv.erode(src, kernel[, iterations][, opts])` | Shrink nonzero foreground in a binary mask. |
| `mat:dilate(kernel[, iterations][, opts])` | `cv.dilate(src, kernel[, iterations][, opts])` | Expand foreground. |
| `mat:morphology_ex(op, kernel[, iterations][, opts])` | `cv.morphology_ex(src, op, kernel[, iterations][, opts])` | `open`, `close`, `gradient`, `tophat`, or `blackhat`. |

The derivative and Canny wrappers first convert input to 8-bit grayscale. Their positional signatures do **not** include the C++ `ddepth` argument. Pass it in `opts`, such as `gray:sobel(1, 0, {ddepth = "float32"})`.

Create a kernel with `cv.get_structuring_element("rect" | "ellipse" | "cross", width, height)`. Morphology options include `anchor_x`, `anchor_y`, `border_type`, `border_value`, and in-place/return options. Supply `iterations` explicitly before `opts`.

```lua
local gray = cv.from_image(img, "gray")
local binary = gray:threshold(127, 255, "binary")
local kernel = cv.get_structuring_element("rect", 3, 3)
local clean = binary:morphology_ex("open", kernel, 1)
local joined = clean:morphology_ex("close", kernel, 1)
local outline = joined:canny(50, 150)
local gx = gray:sobel(1, 0)
local gradient_preview = gx:convert_scale_abs():to_image()
```

## Contours, Components, and Moments

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:find_contours([mode][, method][, opts])` | `cv.find_contours(src[, mode][, method][, opts])` | Array of contours, each an array of `{x, y}` points. Use a binary mask. |
| `mat:connected_components_with_stats([connectivity][, ltype])` | `cv.connected_components_with_stats(src[, connectivity][, ltype])` | Table with `count`, `labels`, `stats`, `centroids`, and `components`. Connectivity is `4` or `8`; label type is `"int32"` or `"uint16"`. |
| `mat:find_non_zero()` | `cv.find_non_zero(src)` | Array of `{x, y}` points for nonzero grayscale pixels. Use `count_non_zero` when only the count is needed. |
| `mat:moments([binary_image])` | `cv.moments(src[, binary_image])` | Table of spatial, central, and normalized moments, including `m00`, `m10`, and `m01`. |
| `mat:hu_moments([binary_image])` | `cv.hu_moments(src[, binary_image])` | Array of seven Hu moments computed directly from the image/mask, not from a moments table. |

Contour modes: `external`, `list`, `ccomp`, `tree`. Approximation methods: `none`, `simple`, `tc89l1`, `tc89kcos`. With `{return_hierarchy = true}`, `find_contours` returns `contours, hierarchy`. Hierarchy fields `next`, `prev`, `first_child`, and `parent` are one-based contour indices, with `0` meaning absent.

Component `count` includes background. Each component has `label`, `left`, `top`, `width`, `height`, `area`, and `centroid = {x, y}`. The component array is one-based, but `label == 0` identifies background. The `labels`/`stats`/`centroids` results are matrices, not Lua tables to index directly.

```lua
local gray = cv.from_image(img, "gray")
local binary = gray:threshold(127, 255, "binary")
local components = binary:connected_components_with_stats(8, "int32")
local marked = cv.from_image(img, "bgr")
for _, component in ipairs(components.components) do
    if component.label ~= 0 and component.area >= 50 then
        marked:rectangle(component.left, component.top,
            component.left + component.width - 1,
            component.top + component.height - 1,
            0x00FF00, 2, {inplace = true})
    end
end
local out = marked:to_image()
```

Contour geometry functions such as `cv.bounding_rect(contour)` and `cv.contour_area(contour)` are module functions rather than matrix methods:

```lua
local gray = cv.from_image(img, "gray")
local binary = gray:threshold(127, 255, "binary")
local contours, hierarchy = binary:find_contours("external", "simple", {
    return_hierarchy = true,
})
local marked = cv.from_image(img, "bgr"):draw_contours(contours, 0x00FF00, 2)
local m = binary:moments(true)
if m.m00 > 0 then
    local cx, cy = m.m10 / m.m00, m.m01 / m.m00
    marked = marked:circle(math.floor(cx + 0.5), math.floor(cy + 0.5),
        4, 0xFF0000, -1)
end
local hu = binary:hu_moments(true)
local out = marked:to_image()
```

## Template Matching and Histograms

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:match_template(templ[, method][, mask])` | `cv.match_template(src, templ[, method][, mask])` | Float response matrix, not coordinates or a confidence percentage. Default method is `ccoeff_normed`. |
| `mat:min_max_loc([mask])` | `cv.min_max_loc(src[, mask])` | Table `{min_val, max_val, min_loc = {x, y}, max_loc = {x, y}}`; input must be single-channel. |
| `mat:calc_hist([opts])` | `cv.calc_hist(src[, opts])` | Single-channel float histogram matrix for one chosen input channel. |
| `mat:compare_hist(other[, method])` | `cv.compare_hist(src, other[, method])` | Numeric histogram similarity/distance, with meaning determined by the method. |

Search and template must have compatible depth/channels; the template must fit inside the search image. Matching strips BGRA alpha; it does not automatically use alpha as a mask. An explicit mask must match template dimensions, and its support depends on the chosen OpenCV method. `sqdiff` and `sqdiff_normed` use the **minimum** response; `ccorr`, `ccorr_normed`, `ccoeff`, and `ccoeff_normed` use the **maximum**. Coordinates give the top-left template position. Standard normalized scores are not the `0..100` thresholds used by `cv.find_image`.

```lua
local search = cv.from_image(img, "gray")
local templ = cv.from_image(template_img, "gray")
local response = search:match_template(templ, "sqdiff_normed")
local best = response:min_max_loc()
local x, y, score = best.min_loc.x, best.min_loc.y, best.min_val
local width, height = templ:size()
local out = cv.from_image(img, "bgr"):rectangle(x, y,
    x + width - 1, y + height - 1, 0x00FF00, 2):to_image()
```

Histogram options: `channel` (zero-based, default `0`), `hist_size` (default `256`), `ranges = {min, max}` (default `{0, 256}`, upper endpoint excluded), and optional `mask`. Use the same bins, range, and normalization when comparing histograms. Comparison methods include `correl`, `chisqr`, `intersect`, `bhattacharyya`, `chisqralt`, and `kldiv`. Correlation/intersection favor larger values; distance methods favor smaller values.

```lua
local a = cv.from_image(img, "gray")
local b = cv.from_image(other_img, "gray")
local opts = {hist_size = 32, ranges = {0, 256}}
local ha = a:calc_hist(opts):normalize({alpha = 1, norm_type = "l1"})
local hb = b:calc_hist(opts):normalize({alpha = 1, norm_type = "l1"})
local similarity = ha:compare_hist(hb, "correl")
```

## Lines, Circles, Corners, and Distance Maps

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:hough_lines_p(rho, theta, threshold[, min_line_length][, max_line_gap])` | `cv.hough_lines_p(src, rho, theta, threshold[, min_line_length][, max_line_gap])` | Array of segments with `x1, y1, x2, y2` fields and the same four array entries. Input should be an edge map; `theta` is in radians. |
| `mat:hough_circles(method, dp, min_dist[, param1][, param2][, min_radius][, max_radius])` | `cv.hough_circles(src, method, dp, min_dist[, param1][, param2][, min_radius][, max_radius])` | Array of `{x, y, radius}` circles. Use grayscale input and method `"gradient"`. |
| `mat:good_features_to_track(max_corners, quality_level, min_distance[, mask][, block_size][, use_harris][, k])` | `cv.good_features_to_track(src, max_corners, quality_level, min_distance[, mask][, block_size][, use_harris][, k])` | Array of `{x, y}` corner points. `quality_level` is a fraction in `0..1`; `min_distance` is in pixels. |
| `mat:distance_transform([distance_type][, mask_size][, opts])` | `cv.distance_transform(src[, distance_type][, mask_size][, opts])` | Distance from each nonzero mask pixel to the nearest zero pixel. Default is `l2`, mask size `3`, float32 output; `opts.dst_type` selects output type. |

```lua
local gray = cv.from_image(img, "gray")
local edges = gray:canny(80, 160)
local lines = edges:hough_lines_p(1, math.pi / 180, 40, 30, 5)
local corners = gray:good_features_to_track(100, 0.01, 8)
local circles = gray:gaussian_blur(5, 5):hough_circles("gradient",
    1, 20, 100, 30, 5, 60)
local binary = gray:threshold(127, 255, "binary")
local distances = binary:distance_transform("l2", 3)
local distance_preview = distances:to_image()
```

For masked corner detection, pass the mask before `block_size`. Without a mask, the next positional argument is `block_size`; omit it entirely to use defaults. Distances remain numeric in `distances`; the preview is only a normalized display.

## Flood Fill

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:flood_fill(seed_point, new_value[, lo_diff][, up_diff][, opts])` | `cv.flood_fill(src, seed_point, new_value[, lo_diff][, up_diff][, opts])` | Two results: `filled_matrix, info`. Fill a connected region near the seed, rather than every pixel with the same color. |

Use one-channel or three-channel input, not BGRA.

`info.area` is the number of filled pixels; `info.rect` is `{x, y, width, height}`. With `opts.return_mask = true`, `info.mask` is a matrix with the image dimensions. Options include `connectivity` (`4` or `8`), `fixed_range`, `mask_only`, `new_mask_val`, `mask`, `inplace`, and `return_image`. A supplied mask can have image dimensions or a one-pixel border on every side; nonzero supplied mask pixels block filling.

The positional `lo_diff`/`up_diff` form currently accepts numeric scalars; do not pass color tables there, because the binding treats a table as `opts`. For grayscale, numeric tolerances are intensity differences. With `fixed_range = true`, compare against the seed value; otherwise compare against neighboring pixels accepted during filling.

```lua
local gray = cv.from_image(img, "gray")
local filled, info = gray:flood_fill({x = 0, y = 0}, 0, 8, 8, {
    fixed_range = true,
    return_mask = true,
    new_mask_val = 255,
})
local out = filled:to_image()
local region = info.mask
print(info.area, info.rect.width, info.rect.height)
```

## Motion and Vector Fields

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:phase_correlate(other[, window])` | `cv.phase_correlate(src, other[, window])` | Table `{x, y, response}` describing translation and correlation response. Use equally sized grayscale frames. |
| `mat:magnitude(y[, opts])` | `cv.magnitude(x, y[, opts])` | Float magnitude from x/y component matrices. |
| `mat:phase(y[, angle_in_degrees][, opts])` | `cv.phase(x, y[, angle_in_degrees][, opts])` | Float angles from x/y components; default unit is radians. |
| `mat:cart_to_polar(y[, angle_in_degrees][, opts])` | `cv.cart_to_polar(x, y[, angle_in_degrees][, opts])` | Two matrices: magnitude, then angle. |
| `mat:polar_to_cart(angle[, angle_in_degrees][, opts])` | `cv.polar_to_cart(magnitude, angle[, angle_in_degrees][, opts])` | Two matrices: x component, then y component; receiver holds magnitude. |

Component inputs must be equally sized and single-channel; the vector wrappers convert them to float32. Supply the degree/radian boolean before `opts` when passing options. `cart_to_polar` and `polar_to_cart` apply `return_image` to both returned results. Keep them as matrices for subsequent calculations.

```lua
local gray = cv.from_image(img, "gray")
local gx = gray:sobel(1, 0, {ddepth = "float32"})
local gy = gray:sobel(0, 1, {ddepth = "float32"})
local strength = gx:magnitude(gy)
local direction = gx:phase(gy, true)
local magnitude, angle = gx:cart_to_polar(gy, true)
local restored_x, restored_y = magnitude:polar_to_cart(angle, true)
local out = strength:to_image()
```

```lua
local a = cv.from_image(img, "gray")
local width, height = a:size()
local b = cv.from_image(other_img, "gray"):resize(width, height)
local window = cv.create_hanning_window(width, height, "float32")
local shift = a:phase_correlate(b, window)
print(shift.x, shift.y, shift.response)
```

## Drawing and Annotation

| Matrix call | Module call | Result and use |
| --- | --- | --- |
| `mat:rectangle(x1, y1, x2, y2, color[, thickness][, opts])` | `cv.rectangle(src, x1, y1, x2, y2, color[, thickness][, opts])` | Draw a rectangle; `x2, y2` are endpoint coordinates, not width/height. Negative thickness fills it. |
| `mat:circle(x, y, radius, color[, thickness][, opts])` | `cv.circle(src, x, y, radius, color[, thickness][, opts])` | Draw a circle; negative thickness fills it. |
| `mat:line(x1, y1, x2, y2, color[, thickness][, opts])` | `cv.line(src, x1, y1, x2, y2, color[, thickness][, opts])` | Draw a line segment. |
| `mat:polylines(contours, closed, color[, thickness][, line_type][, opts])` | `cv.polylines(src, contours, closed, color[, thickness][, line_type][, opts])` | Draw multiple point paths; `contours` is an array of arrays of `{x, y}` points. |
| `mat:fill_poly(contours, color[, line_type][, opts])` | `cv.fill_poly(src, contours, color[, line_type][, opts])` | Fill polygon interiors. |
| `mat:draw_contours(contours, color[, thickness][, opts])` | `cv.draw_contours(src, contours, color[, thickness][, opts])` | Draw all supplied contours; negative thickness fills them. |
| `mat:put_text(text, org, font_face, font_scale, color[, thickness][, line_type][, bottom_left_origin][, opts])` | `cv.put_text(src, text, org, font_face, font_scale, color[, thickness][, line_type][, bottom_left_origin][, opts])` | Draw Hershey text. `org` is the baseline anchor at the lower-left of the text, not its upper-left corner. |

Drawing on a matrix returns a matrix. Capture each result, chain calls, or explicitly use `inplace`. For in-place drawing, supply the preceding positional arguments before the options table. Line types include `4`, `8`, and `aa`. Hershey fonts are suitable for ASCII labels; use ImageObject text rendering when Unicode text is required.

```lua
local marked = cv.from_image(img, "bgr")
local polygon = {
    {x = 10, y = 10}, {x = 60, y = 10}, {x = 35, y = 45},
}
marked:rectangle(5, 5, 70, 55, 0x00FF00, 2, {inplace = true})
marked:polylines({polygon}, true, 0xFF0000, 1, "aa", {inplace = true})
marked:put_text("OK", {x = 10, y = 70}, "simplex", 0.7,
    0xFFFFFF, 1, "aa", false, {inplace = true})
local out = marked:to_image()
```

Choose coordinates that fit the input image. To obtain text dimensions before placement, call the module function `cv.get_text_size(text, font_face, font_scale[, thickness])`, which returns `{width, height, baseline}`.
