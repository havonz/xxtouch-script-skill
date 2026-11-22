# Color Similarity and Anti-Match Checks

Use `scripts/color_similarity.py` for single or batch RGB color comparisons. It uses only the Python standard library and requires no device or control-center connection. Paths below are Skill-relative; invoke the helper using its installed absolute path.

## Single and Batch Calculations

```bash
python3 scripts/color_similarity.py 0xec1c23 0xed1d24
python3 scripts/color_similarity.py '#ec1c23' '#ed1d24' --algorithm all
python3 scripts/color_similarity.py 0xffffff 0xeeeeee --threshold -90
python3 scripts/color_similarity.py --input colors.json --algorithm 2 --threshold 90
```

`--input` accepts a non-empty JSON array of color pairs. Use `--input -` to read the same format from stdin:

```json
[
  ["0xec1c23", "0xed1d24"],
  ["#ffffff", "eeeeee"],
  [0, 16777215]
]
```

Color strings accept `0x` followed by 1 to 6 hexadecimal digits, `#RRGGBB`, or six-digit `RRGGBB`. Bare six-digit strings are always hexadecimal; use JSON integers for decimal color values. Only 24-bit RGB values are accepted, without alpha, negative values, floats, or booleans. Quote colors starting with `#` in shell commands.

Output is always `{"results": [...]}`. Each result contains normalized `color_a`, `color_b`, `algorithm`, and integer `similarity`. With `--threshold`, it also contains `threshold` and boolean `matched`. `--algorithm all` emits algorithms `0`, `1`, and `2` for each pair, in that order.

## Algorithms and Matching Semantics

The helper follows the `csim_algorithm` values and integer scoring rules used by `screen.find_color` and `ImageObject:find_color`.

Let `dr`, `dg`, and `db` be the absolute differences between the RGB channels:

| `csim_algorithm` | Calculation |
| --- | --- |
| `0` (default) | `s = (((255-dr)*(255-dg)*(255-db)*100) >> 24) + 2`; return `0` when `s <= 2` |
| `1` (Manhattan) | `((765-dr-dg-db)*8600) >> 16`, preserving the fixed-point approximation |
| `2` (Euclidean) | `int(max(0, (1-sqrt(dr²+dg²+db²)/441.6729559)*100) + 0.5)`, preserving the constant and rounding order |

Do not substitute a generic RGB percentage formula or Python `round()`. A score of `100` does not guarantee identical RGB values.

`--threshold` represents the **effective threshold** for one point in `find_color` similarity mode:

- Negative threshold: `similarity < abs(threshold)`, strictly less than. Equality fails the anti-match check.
- Non-negative threshold below `100`: `similarity >= threshold`.
- Positive threshold of `100`: compare RGB values for exact equality.

For a non-negative point similarity, the effective threshold is `min(global_similarity, point_similarity)`. Negative point thresholds are independent of the global threshold. The helper computes scores and individual point checks; it does not simulate a whole search, coordinates, or `max_miss`.

## `find_color` Anti-Match Example

```lua
local x, y = screen.find_color({
    csim_algorithm = 0,
    {0, 0, 0xec1c23, 90},
    {12, -3, 0xffffff, -90},
}, 90, 0, 0, 100, 100)
```

This requires the anchor to match red and the point 12 pixels right and 3 pixels up to have a similarity to white strictly below `90`. To check the latter condition, compare its sampled color against `0xffffff` with `--threshold -90`. `ImageObject:find_color` uses the same similarity and anti-match rules. The anchor point also supports negative similarity.
