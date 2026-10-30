import json
import os
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "datapack")
BUILD = os.path.join(ROOT, "build")
VERSION = open(os.path.join(ROOT, "version.txt"), encoding="utf-8").read().strip()
ZIP = os.path.join(BUILD, f"Mystical_Realms_Data_Pack-{VERSION}.zip")


def validate_json_files():
    for dirpath, _, filenames in os.walk(SRC):
        for name in filenames:
            if name.endswith(".json"):
                path = os.path.join(dirpath, name)
                with open(path, encoding="utf-8") as f:
                    json.load(f)


def main():
    validate_json_files()

    if os.path.exists(ZIP):
        os.remove(ZIP)
    os.makedirs(BUILD, exist_ok=True)

    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, _, filenames in os.walk(SRC):
            for name in filenames:
                full = os.path.join(dirpath, name)
                arcname = os.path.relpath(full, SRC)
                z.write(full, arcname)

    print(f"OK -> {ZIP}")


if __name__ == "__main__":
    main()