"""
This module isolates the logic to store metadata into disk.
"""
import os
import sqlite3
from typing import Iterable, Generator
from common import Metadata


class StoringException(Exception):
    """
    Base exception for extraction errors
    """
    pass


class MetadataStorageManager:
    """
    Provides the logic to store metadata into the DB and retrieve it as well
    """
    def __init__(self, database_path):
        self._db_path = database_path
        if not os.path.isfile(database_path) or os.path.getsize(database_path) == 0:
            self._create_db_schema()

    def _create_db_schema(self):
        """
        Creates the DB schema for metadata storing
        """
        try:
            with sqlite3.connect(self._db_path) as con:
                con.execute(
                    """
                    CREATE TABLE metadata (
                        id INTEGER PRIMARY KEY,
                        file_id TEXT NOT NULL,
                        field_name TEXT NOT NULL,
                        field_type TEXT CHECK( field_type IN ('I','S') ),
                        total_occurrences INTEGER CHECK( total_occurrences > 0 ) NOT NULL,
                        null_occurrences INTEGER CHECK( null_occurrences >= 0 ) NOT NULL,
                        CHECK ( total_occurrences >= null_occurrences )
                    );"""
                )
        except sqlite3.DatabaseError:
            raise StoringException("Could not create db schema. Is it a readable path?")

    def store_metadata(self, file_path: str, metadata: Iterable[Metadata]) -> None:
        """
        Store metadata into the db.

        :param file_path: the file path the metadata was obtained from
        :param metadata: the metadata to store
        :raises StoringException if storing fails
        """
        try:
            with sqlite3.connect(self._db_path) as con:
                con.executemany("insert into "
                                "metadata(file_id, field_name, field_type, total_occurrences, null_occurrences) "
                                "values (?, ?, ?, ?, ?)",
                                [(file_path,
                                  metadata.field,
                                  metadata.type,
                                  metadata.total_occurrences,
                                  metadata.null_occurrences) for metadata in metadata])
        except sqlite3.DatabaseError:
            raise StoringException("Could not store metadata into the DB. Is it corrupted?")

    def retrieve_metadata(self, file_path: str) -> Generator[Metadata, None, None]:
        """
        Retrieve metadata from db.

        :param file_path: the file path the metadata was obtained from
        :raises StoringException if retrieval fails
        """
        try:
            with sqlite3.connect(self._db_path) as con:
                con.row_factory = sqlite3.Row
                for row in con.execute("select * from metadata where file_id=?", (file_path,)):
                    yield Metadata(row["field_name"], row["field_type"],
                                   row["total_occurrences"], row["null_occurrences"])
        except sqlite3.DatabaseError:
            raise StoringException("Could not retrieve metadata from DB. Is it corrupted?")
