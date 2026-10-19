from __future__ import annotations
import hashlib
import pathlib
import struct
import sys

MAGIC = b"HIKAPLD1"


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: package.py <setup-stub.exe> <payload.exe> <output.exe>")
        return 2
    stub_path = pathlib.Path(sys.argv[1])
    payload_path = pathlib.Path(sys.argv[2])
    output_path = pathlib.Path(sys.argv[3])
    stub = stub_path.read_bytes()
    payload = payload_path.read_bytes()
    if not stub.startswith(b"MZ") or not payload.startswith(b"MZ"):
        raise SystemExit("Both setup stub and payload must be Windows PE files")
    digest = hashlib.sha256(payload).digest()
    trailer = MAGIC + struct.pack("<Q", len(payload)) + digest
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(stub + payload + trailer)
    print(f"created {output_path} ({output_path.stat().st_size:,} bytes)")
    print(f"payload sha256: {digest.hex()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
