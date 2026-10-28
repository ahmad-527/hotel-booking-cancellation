"""Extract or verify the fixed input snapshot, without accepting different bytes."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def check_inputs(extract=False):
    manifest = json.loads((ROOT / "data/inputs.json").read_text(encoding="utf-8"))
    archive = ROOT / manifest["archive"]["path"]
    if extract:
        with archive.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if digest != manifest["archive"]["sha256"]:
            raise SystemExit("Input snapshot archive checksum mismatch")
        with ZipFile(archive) as source:
            if set(source.namelist()) != {item["path"] for item in manifest["files"]}:
                raise SystemExit("Unexpected archive member list")
    for item in manifest["files"]:
        destination = ROOT / item["path"]
        if not destination.exists():
            if not extract:
                raise SystemExit(f"Missing {item['path']}; run python scripts/data.py --extract")
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_suffix(destination.suffix + ".part")
            try:
                with ZipFile(archive) as source, source.open(item["path"]) as member, temporary.open("wb") as output:
                    while chunk := member.read(1024 * 1024):
                        output.write(chunk)
                with temporary.open("rb") as stream:
                    digest = hashlib.file_digest(stream, "sha256").hexdigest()
                if digest != item["sha256"]:
                    raise SystemExit(f"Snapshot member checksum mismatch: {item['path']}")
                temporary.replace(destination)
            finally:
                temporary.unlink(missing_ok=True)
        with destination.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if digest != item["sha256"]:
            raise SystemExit(f"Checksum mismatch: {item['path']}")
        print(f"Verified {item['path']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extract", action="store_true", help="Extract missing files from the fixed archive; never replace existing inputs.")
    check_inputs(parser.parse_args().extract)
