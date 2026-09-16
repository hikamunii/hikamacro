from __future__ import annotations
import base64
import gzip
from pathlib import Path


def restore(pattern: str, output: str, compressed: bool = True) -> None:
    parts = sorted(Path().glob(pattern))
    if not parts:
        raise SystemExit(f"no packed parts found for {pattern}")
    text = "".join(p.read_text(encoding="ascii").strip() for p in parts)
    raw = base64.b64decode(text, validate=True)
    if compressed:
        raw = gzip.decompress(raw)
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    print(f"restored {output}: {len(raw):,} bytes from {len(parts)} part(s)")


restore("src/packed/main.*", "src/main.rs")
restore("src/packed/setup.*", "src/setup.rs")
restore("assets/packed/icon.*", "assets/Hika.ico", compressed=False)
