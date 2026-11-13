"""Download and validate the Steam Games dataset from Google Drive."""

import argparse
import os
from pathlib import Path

import gdown
import pyarrow.parquet as pq

FILE_ID = "1vpHJJoH_e0UwlueVYfMfPD_ViFNoS1RI"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = PROJECT_ROOT / "datasets" / "games.parquet"

REQUIRED_COLUMNS = {
    "AppID",
    "Name",
    "Price",
    "Positive",
    "Negative",
}


def validate_dataset(path: Path) -> None:
    """Verify that the downloaded file is a valid, non-empty Parquet dataset."""

    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError("Dataset file is missing or empty.")

    parquet_file = pq.ParquetFile(path)
    available_columns = set(parquet_file.schema_arrow.names)

    missing = REQUIRED_COLUMNS - available_columns

    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    if parquet_file.metadata.num_rows == 0:
        raise ValueError("Dataset contains no records.")


def download_dataset(
    output_path: str | Path = DEFAULT_OUTPUT,
    force: bool = False,
) -> Path:
    """Download the dataset unless a valid local copy already exists."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not force:
        validate_dataset(output_path)
        print(f"DATASET: Valid local copy already exists: {output_path}")
        return output_path

    temporary_path = output_path.with_name(output_path.name + ".part")

    print("DATASET: Downloading from Google Drive...")

    try:
        result = gdown.download(
            id=FILE_ID,
            output=str(temporary_path),
            quiet=False,
        )

        if result is None or not temporary_path.is_file():
            raise RuntimeError("Google Drive download failed.")

        validate_dataset(temporary_path)

        os.replace(temporary_path, output_path)

    finally:
        if temporary_path.exists():
            temporary_path.unlink()

    print(f"DATASET: Download completed: {output_path}")
    print(f"DATASET: Size: {output_path.stat().st_size:,} bytes")

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download the Steam Games Parquet dataset."
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Destination path for the Parquet dataset.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Download again even if a valid local dataset exists.",
    )

    args = parser.parse_args()

    download_dataset(
        output_path=args.output,
        force=args.force,
    )


if __name__ == "__main__":
    main()
