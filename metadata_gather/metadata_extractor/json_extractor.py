from collections.abc import Mapping
import json
from typing import Generator

from common import MetadataRecord

from .exceptions import ExtractionError
from .file_extractor import file_extractor


def _perform_extractor(file_path: str) -> Generator[MetadataRecord, None, None]:
    """
    Perform the extraction of records from the given JSON file.

    The returned generator object produces one MetadataRecord for each element
    in each JSON object read from file_path.

    Note: this function reads the hole JSON file and produces the records one by
    one. It must be improved to read objects lazily.

    :param file_path: the path to the file to create records from
    :return: a generator object that produces MetadataField objects
    :raises ExtractionError if extraction fails
    """
    with open(file_path, mode='r') as json_file:
        # TODO: avoid reading the hole file at once
        for obj in json.load(json_file):
            if not isinstance(obj, Mapping):
                raise ExtractionError(f'Invalid JSON structure. It must contain a list of objects')

            for key, value in obj.items():
                yield MetadataRecord(key, value)


@file_extractor("json")
def extract_data_from_json(file_path: str) -> Generator[MetadataRecord, None, None]:
    """
    Perform the extraction of records from the given JSON file.

    The returned generator object produces one MetadataRecord for each element
    in each JSON object read from file_path.

    :param file_path: the path to the file to create records from
    :return: a generator object that produces MetadataField objects
    :raises ExtractionError if extraction fails
    """
    try:
        yield from _perform_extractor(file_path)
    except ExtractionError:
        raise
    except IOError:
        raise ExtractionError(f"Could not open file '{file_path}'")
    except json.JSONDecodeError:
        raise ExtractionError(f"The file '{file_path}' is not a valid JSON file")
    except Exception:
        raise ExtractionError(f"Unexpected error while processing JSON file '{file_path}'")
