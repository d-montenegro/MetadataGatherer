from csv import Error, DictReader, QUOTE_NONE
from typing import Generator, Type, Union

from common import MetadataRecord

from .exceptions import ExtractionError
from .file_extractor import file_extractor


def _sanitize_key(column_name: str) -> str:
    """
    Sanitize a column_name read from a CSV file, by removing leading and trailing spaces
    and quotes.

    :param column_name: the column_name read from a CSV file
    :return: sanitized column name
    """
    return column_name.strip('" ')


def _sanitize_value(value: str) -> Union[int, str, None]:
    """
    Sanitize a value read from a CSV file as following:
     * if its equal to 'null' -> None
     * if starts with quote -> str
     * otherwise -> int - if casting fails, a ValueError is raised

    :param value: the value to sanitize
    :return: sanitized value
    """
    value = value.strip(' ')
    if value.startswith('"'):
        # it's a string
        return value.strip('"')

    if value.lower() == 'null':
        return None

    return int(value)


def _perform_extraction(file_path: str) -> Generator[Type[MetadataRecord], None, None]:
    """
    Perform the extraction of records from the given CSV file.

    The returned generator object produces N * M MetadataRecord for a CSV
    with N columns and M rows.

    :param file_path: the path to the file to create records from
    :return: a generator object that produces MetadataField objects
    :raises ExtractionError if extraction fails
    """
    with open(file_path, newline='', mode='r') as csv_file:
        csv_reader = DictReader(csv_file, delimiter=',', quoting=QUOTE_NONE)
        for row in csv_reader:
            for key, value in row.items():
                try:
                    key = _sanitize_key(key)
                except AttributeError:
                    raise ExtractionError(f"Missing column name for value {value} at line {csv_reader.line_num}")

                try:
                    value = _sanitize_value(value)
                except ValueError:
                    if not value:
                        raise ExtractionError(f"Missing value for column '{key}' at line {csv_reader.line_num}")
                    else:
                        raise ExtractionError(f"Unknown type for value '{value}' (column '{key}') at line "
                                              f"{csv_reader.line_num}")

                yield MetadataRecord(key, value)


@file_extractor("csv")
def extract_data_from_csv(file_path: str) -> Generator[Type[MetadataRecord], None, None]:
    """
    Perform the extraction of records from the given CSV file.

    The returned generator object produces N * M MetadataRecord for a CSV
    with N columns and M rows.

    :param file_path: the path to the file to create records from
    :return: a generator object that produces MetadataField objects
    :raises ExtractionError if extraction fails
    """
    try:
        yield from _perform_extraction(file_path)
    except ExtractionError:
        raise
    except IOError:
        raise ExtractionError(f"Could not open file '{file_path}'")
    except Error:
        raise ExtractionError(f"The file '{file_path}' is not a valid CSV")
    except Exception:
        raise ExtractionError(f"Unexpected error while processing CSV file '{file_path}'")
