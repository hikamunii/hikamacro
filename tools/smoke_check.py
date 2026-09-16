from __future__ import annotations
import hashlib
import pathlib
import struct
import sys

MAGIC = b"HIKAPLD1"
TRAILER = 48


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: smoke_check.py <installer.exe>")
        return 2
    path = pathlib.Path(sys.argv[1])
    data = path.read_bytes()
    if len(data) <= TRAILER or not data.startswith(b"MZ"):
        raise SystemExit("installer is not a valid packaged PE")
    trailer = data[-TRAILER:]
    if trailer[:8] != MAGIC:
        raise SystemExit("missing Hika payload trailer")
    payload_len = struct.unpack("<Q", trailer[8:16])[0]
    expected = trailer[16:48]
    start = len(data) - TRAILER - payload_len
    if start <= 0:
        raise SystemExit("invalid payload offset")
    payload = data[start : start + payload_len]
    if not payload.startswith(b"MZ"):
        raise SystemExit("embedded payload is not a PE file")
    actual = hashlib.sha256(payload).digest()
    if actual != expected:
        raise SystemExit("embedded payload hash mismatch")
    forbidden = [b"powershell", b".ps1", b"PresentationFramework"]
    lowered = data.lower()
    for item in forbidden:
        if item.lower() in lowered:
            raise SystemExit(f"runtime installer contains forbidden dependency marker: {item!r}")
    print("installer smoke check passed")
    print(f"embedded payload bytes: {payload_len:,}")
    print(f"payload sha256: {actual.hex()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
