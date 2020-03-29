"""
This module isolate all the data structures shared by multiple modules
to avoid coupling.
"""
from collections import namedtuple
from typing import Union

# Normalized record that represents information retrieved from an arbitrary source. These
# are produced by extractors and consumed by crawler
MetadataRecord = namedtuple('MetadataField', 'name, value')

# Normalized metadata. These are produced by the crawler and stored in the DB
Metadata = namedtuple('Metadata', 'field, type, total_occurrences, null_occurrences')

# Mapping between supported data types and our internal representation
_RECORD_TYPE_MAPPING = {
    int: "I",
    str: "S",
    None: None
}

# Mapping between our internal data types and its human-friendly representation
_RECORD_TYPE_NAME = {
    "I": "Integer",
    "S": "String",
    None: "null"
}


def get_internal_type(a_type: Union[int, str, None]) -> str:
    """
    Translate a type into an internal type

    :param a_type: the type to translate
    :return: the internal type
    :raises: ValueError if <a_type> is unsupported
    """
    try:
        return _RECORD_TYPE_MAPPING[a_type]
    except KeyError:
        raise ValueError


def get_human_friendly_type(internal_type: str) -> str:
    """
    Get a human friendly name for an internal_type

    :param internal_type: the type to translate
    :return: the internal type
    :raises: ValueError if <a_type> is unsupported
    """
    try:
        return _RECORD_TYPE_NAME[internal_type]
    except KeyError:
        raise ValueError
