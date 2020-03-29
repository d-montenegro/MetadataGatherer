"""
This module isolates the logic to summarize records provided by an arbitrary sources into
normalized metadata.
"""
from typing import Generator, Iterable

from common import Metadata, MetadataRecord, get_internal_type


class CrawlingError(Exception):
    """
    Base exception for crawling errors
    """
    pass


class _MetadataAggregator:
    """
    Help class to provide the logic to summarize individual records into normalized metadata.

    This class is intended to use inside this module only.
    """
    __slots__ = 'field_name', 'type_', 'occurrences', 'nulls'

    def __init__(self, field_name):
        self.field_name = field_name
        self.type_ = None
        self.occurrences = 0
        self.nulls = 0

    @property
    def type(self):
        return self.type_

    @type.setter
    def type(self, t):
        try:
            t = get_internal_type(t)
        except ValueError:
            raise CrawlingError(f"The type of field '{self.field_name}' is unknown")

        if self.type_ is None:
            self.type_ = t
        elif self.type_ != t:
            raise CrawlingError(f"The type of field '{self.field_name}' is not consistent")

    def increment_nulls(self):
        self.nulls += 1

    def increment_occurrences(self):
        self.occurrences += 1


def crawl(records: Iterable[MetadataRecord]) -> Generator[Metadata, None, None]:
    """
    Summarize an iterable of records into normalized metadata.

    :param records: an iterable of records to summarize
    :raises: Crawling error if anything goes wrong. For instance, if any record
    has an unsupported type.
    """
    aggregations = dict()

    for (record_name, record_value) in records:
        # get an aggregator for this record, or create one there isn't.
        try:
            aggr = aggregations[record_name]
        except KeyError:
            aggr = _MetadataAggregator(record_name)
            aggregations[record_name] = aggr

        aggr.increment_occurrences()
        if record_value is None:
            aggr.increment_nulls()
        else:
            aggr.type = type(record_value)

    yield from (Metadata(aggr.field_name, aggr.type, aggr.occurrences, aggr.nulls)
                for aggr in aggregations.values())
