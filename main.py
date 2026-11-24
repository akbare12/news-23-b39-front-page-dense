"""news-23 b39 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

MAX_BYTES = 1024 * 1024


def check_png(data):
    """Validate the PNG: signature, IHDR 1024x1024, well-formed IEND trailer."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if len(data) < 33:
        raise ValueError("PNG too short for IHDR")
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    if data[12:16] != b"IHDR" or ihdr_len != 13:
        raise ValueError("missing IHDR chunk")
    width, height, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        raise ValueError(f"expected 1024x1024, got {width}x{height}")
    if depth != 8 or ctype not in (2, 6):
        raise ValueError(f"unexpected bit depth {depth} / colour type {ctype}")
    if len(data) < 12 or data[-12:-8] != b"\x00\x00\x00\x00" or data[-8:-4] != b"IEND":
        raise ValueError("missing well-formed IEND trailer")
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    width, height = check_png(data)
    src_sha = hashlib.sha256(data).hexdigest()
    print(f"source entry.png: {len(data)} bytes, sha256 {src_sha}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        raise ValueError("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(here)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        raise ValueError("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("output does not match source byte-for-byte")
    check_png(written)
    print(f"wrote {dst} ({width}x{height}, {len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()})")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
