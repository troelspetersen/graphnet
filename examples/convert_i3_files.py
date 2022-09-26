"""Minimum working example (MWE) to use ParquetDataConverter."""

import logging
import os

from graphnet.utilities.logging import get_logger

from graphnet.data.extractors import (
    I3FeatureExtractorIceCubeUpgrade,
    I3RetroExtractor,
    I3TruthExtractor,
    I3GenericExtractor,
)
from graphnet.data.parquet import ParquetDataConverter
from graphnet.data.sqlite import SQLiteDataConverter

logger = get_logger(level=logging.INFO)

CONVERTER_CLASS = {
    "sqlite": SQLiteDataConverter,
    "parquet": ParquetDataConverter,
}


def main_icecube86(backend: str):
    """Convert IceCube-86 I3 files to intermediate `backend` format."""
    # Check(s)
    assert backend in CONVERTER_CLASS

    inputs = ["./test_data/"]
    outdir = "./temp/test_ic86"

    converter = CONVERTER_CLASS[backend](
        [
            I3GenericExtractor(
                keys=[
                    "SRTInIcePulses",
                    "I3MCTree",
                ]
            ),
        ],
        outdir,
    )
    converter(inputs)
    converter.merge_files(os.path.join(outdir, "merged"))


def main_icecube_upgrade(backend: str):
    """Convert IceCube-Upgrade I3 files to intermediate `backend` format."""
    # Check(s)
    assert backend in CONVERTER_CLASS

    inputs = ["test_data_upgrade_2"]
    outdir = "./temp/test_upgrade"
    workers = 1

    converter = CONVERTER_CLASS[backend](
        [
            I3TruthExtractor(),
            I3RetroExtractor(),
            I3FeatureExtractorIceCubeUpgrade(
                "I3RecoPulseSeriesMapRFCleaned_mDOM"
            ),
            I3FeatureExtractorIceCubeUpgrade(
                "I3RecoPulseSeriesMapRFCleaned_DEgg"
            ),
        ],
        outdir,
        workers=workers,
        # nb_files_to_batch=10,
        # sequential_batch_pattern="temp_{:03d}",
        # input_file_batch_pattern="[A-Z]{1}_[0-9]{5}*.i3.zst",
        icetray_verbose=1,
    )
    converter(inputs)
    converter.merge_files(os.path.join(outdir, "merged"))


if __name__ == "__main__":
    # backend = "parquet"
    backend = "sqlite"
    main_icecube86(backend)
    # main_icecube_upgrade(backend)
