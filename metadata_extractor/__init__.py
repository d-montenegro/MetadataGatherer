"""
This module isolates all the logic to extract metadata records from allowed sources.
It exposes the following:
   - extract_metadata_from_file() -> reads a given file and produces the corresponding MetadataRecords
   - ExtractionError -> the exception raised when anything goes wrong
"""
from typing import Generator

from common import MetadataRecord

from . import csv_extractor
from . import json_extractor
from .exceptions import ExtractionError
from .file_extractor import file_extractors


def extract_metadata_from_file(file_path: str) -> Generator[MetadataRecord, None, None]:
    """
    Extract metadata from a given file.

    The extractor is selected according to the extension of the provided file. Allowed
    extensions are ".csv" and ".json"

    :param file_path: the path to the file to extract metadata from
    :return: a generator object that produces MetadataField objects
    :raises ExtractionError if extraction fails
    """
    try:
        _, extension = file_path.rsplit(".", 1)
    except ValueError:
        raise ExtractionError(f"The file '{file_path}' does not have an extension")

    try:
        yield from file_extractors[extension](file_path)
    except KeyError:
        raise ExtractionError(f"Unsupported extension '{extension}'. "
                              f"Allowed extensions are: {', '.join(file_extractors.keys())}")


__all__ = [extract_metadata_from_file, ExtractionError]
