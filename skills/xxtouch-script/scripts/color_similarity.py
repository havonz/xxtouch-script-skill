#!/usr/bin/env python3
"""Compute single or batch RGB color similarities using XXTouch algorithms; output JSON."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path


def parse_color(value: object) -> int:
    if type(value) is int and 0 <= value <= 0xFFFFFF:
        return value
    if isinstance(value, str):
        text = value.strip()
        if re.fullmatch(r"(?:0[xX][0-9a-fA-F]{1,6}|#?[0-9a-fA-F]{6})", text):
            return int(text.removeprefix("0x").removeprefix("0X").removeprefix("#"), 16)
    raise ValueError(f"Invalid RGB color: {value!r}; use 0xRRGGBB, #RRGGBB, RRGGBB, or a JSON integer")


def color_similarity(color_a: int, color_b: int, algorithm: int = 0) -> int:
    dr = abs(((color_a >> 16) & 0xFF) - ((color_b >> 16) & 0xFF))
    dg = abs(((color_a >> 8) & 0xFF) - ((color_b >> 8) & 0xFF))
    db = abs((color_a & 0xFF) - (color_b & 0xFF))
    if algorithm == 0:
        similarity = (((255 - dr) * (255 - dg) * (255 - db) * 100) >> 24) + 2
        return similarity if similarity > 2 else 0
    if algorithm == 1:
        return ((765 - dr - dg - db) * 8600) >> 16
    if algorithm == 2:
        # Preserve the lookup constant and add-then-truncate order to keep threshold boundaries consistent.
        similarity = max(0.0, (1.0 - math.sqrt(dr * dr + dg * dg + db * db) / 441.6729559) * 100.0)
        return int(similarity + 0.5)
    raise ValueError(f"Unsupported csim_algorithm: {algorithm}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("colors", nargs="*", help="Two hexadecimal RGB colors for a single comparison")
    parser.add_argument("--input", help="JSON file containing color pairs; use - for stdin")
    parser.add_argument("--algorithm", choices=("0", "1", "2", "all"), default="0",
                        help="csim_algorithm: 0 default, 1 Manhattan, 2 Euclidean; all computes all three")
    parser.add_argument("--threshold", type=int, help="Optional effective threshold (-100 to 100); negative means anti-match")
    args = parser.parse_args()

    if args.threshold is not None and not -100 <= args.threshold <= 100:
        parser.error("--threshold must be between -100 and 100")
    if args.input is not None:
        if args.colors:
            parser.error("--input cannot be combined with positional colors")
        payload = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
        pairs = json.loads(payload)
        if not isinstance(pairs, list) or not pairs:
            parser.error("Batch input must be a non-empty array of color pairs, e.g. [[\"0x112233\", \"0x112234\"]]")
    else:
        if len(args.colors) != 2:
            parser.error("Provide two colors, or use --input for a batch of color pairs")
        pairs = [args.colors]

    # Validate the entire batch before emitting results so invalid later entries cannot leave partial output.
    parsed_pairs = []
    for index, pair in enumerate(pairs, 1):
        if not isinstance(pair, list) or len(pair) != 2:
            parser.error(f"Entry {index} must be an array containing two RGB colors")
        try:
            parsed_pairs.append((parse_color(pair[0]), parse_color(pair[1])))
        except ValueError as error:
            parser.error(f"Entry {index}: {error}")

    algorithms = (0, 1, 2) if args.algorithm == "all" else (int(args.algorithm),)
    results = []
    for color_a, color_b in parsed_pairs:
        for algorithm in algorithms:
            similarity = color_similarity(color_a, color_b, algorithm)
            result = {"color_a": f"0x{color_a:06x}", "color_b": f"0x{color_b:06x}",
                      "algorithm": algorithm, "similarity": similarity}
            if args.threshold is not None:
                result["threshold"] = args.threshold
                if args.threshold < 0:
                    result["matched"] = similarity < -args.threshold
                elif args.threshold == 100:
                    # find_color compares RGB directly at a positive threshold of 100; near colors can also score 100.
                    result["matched"] = color_a == color_b
                else:
                    result["matched"] = similarity >= args.threshold
            results.append(result)
    print(json.dumps({"results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from None
