import argparse
import os
import sys
from typing import List, Type

from metadata_extractor import extract_metadata_from_file, ExtractionError
from crawler import crawl, CrawlingError
from store_manager import MetadataStoreManager, StoringException
from common import Metadata, RECORD_TYPE_NAME


def absolute_path(file_path: str) -> str:
    """
    Return the absolute path for a given relative path
    :param file_path: a relative path
    :return: the absolute path corresponding to that relative path
    """
    return os.path.abspath(os.path.expanduser(file_path))


def readable_file(file_path: str) -> str:
    """
    Check if a given file path is readable.

    :param file_path: the path to check
    :return the absolute path
    :raises ArgumentTypeError if the given path is not readable
    """
    abs_path = absolute_path(file_path)
    if os.access(abs_path, os.R_OK):
        return abs_path

    raise argparse.ArgumentTypeError(f"The entered path '{file_path}' is not readable")


def is_already_crawled(store_manager: MetadataStoreManager, file_path: str) -> bool:
    """
    Whether a given file was already crawled

    :param store_manager: an instance of the store manager to check metadata
    :param file_path: a path
    :return: True if that file was already crawled. False otherwise.
    """
    try:
        next(store_manager.retrieve_metadata(file_path))
    except StopIteration:
        return False
    else:
        return True


def perform_crawling(abs_path: str, db_path: str) -> None:
    """
    Extract metadata from abs_path and store it.

    :param abs_path: the file to extract metadata from
    :param db_path: path to the store file. It's created if it doesn't exists.
    """
    s = MetadataStoreManager(db_path)
    if is_already_crawled(s, abs_path):
        print(f"File '{abs_path}' already crawled", file=sys.stderr)
        sys.exit(1)

    records = extract_metadata_from_file(abs_path)
    crawled_data = crawl(records)
    s.store_metadata(abs_path, crawled_data)


def perform_describe(abs_path: str, db_path: str) -> None:
    """
    Print metadata extracted from a given source file.

    :param abs_path: the file the metadata was extracted from
    :param db_path: path to the store file. It's created if it doesn't exists.
    """
    s = MetadataStoreManager(db_path)
    metadata = list(s.retrieve_metadata(abs_path))
    if not metadata:
        print('Could not find metadata for the entered path', file=sys.stderr)
        sys.exit(1)
    pretty_print(abs_path, metadata)


def pretty_print(abs_path: str, metadata: List[Type[Metadata]]) -> None:
    """
    Print a list of metadata objects

    :param abs_path: the file the metadata was extracted from
    :param metadata: the list of registries to print
    """
    print(f'File: {abs_path}')
    print(f'Total entries: {len(metadata)}')
    print('Fields:')
    for m in metadata:
        print(f'\t{m.field}, {RECORD_TYPE_NAME[m.type]}, '
              f'{m.total_occurrences - m.null_occurrences}, {m.null_occurrences}')


def main():
    parser = argparse.ArgumentParser(description='Metadata gather')
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-c', '--crawl', metavar='FILE_PATH',
                       type=readable_file, help='metadata file to process')
    group.add_argument('-d', '--describe', metavar='FILE_PATH',
                       type=absolute_path, help='metadata file to describe')

    parser.add_argument('--database-path', default='metadata_gather.db',
                        type=absolute_path,
                        help="The database path, metadata_gather.db in your current"
                             "working directory by default")

    args = parser.parse_args()

    if args.crawl:
        perform_crawling(args.crawl, args.database_path)
    else:
        perform_describe(args.describe, args.database_path)


if __name__ == '__main__':
    try:
        main()
    except (ExtractionError, CrawlingError, StoringException) as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except Exception:
        print('Unexpected error occurred.', file=sys.stderr)
        sys.exit(1)
