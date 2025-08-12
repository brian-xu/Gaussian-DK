import json
import sys
from argparse import ArgumentParser
from pathlib import Path

if __name__ == "__main__":
    parser = ArgumentParser(description="Training script parameters")
    parser.add_argument("--source", "-s", type=str)

    args = parser.parse_args(sys.argv[1:])
    root_dir = Path(args.source)
    raw_dir = root_dir / "raw"

    metadata = {}

    for json_path in raw_dir.glob("*.json"):
        with open(json_path) as json_data:
            data_dict = json.load(json_data)[0]
            filename, exposure, fnumber, iso = (
                data_dict["FileName"],
                data_dict["ExposureTime"],
                data_dict["FNumber"],
                data_dict["ISO"],
            )
            filename = filename.replace(".dng", ".jpg")
            metadata[filename] = {
                "ExposureTime": eval(exposure),
                "FNumber": fnumber,
                "ISOSpeedRatings": iso / 1000,
            }

    with open(root_dir / "dense/metadata.json", "w") as f:
        json.dump(metadata, f)
