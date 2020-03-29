"""
This module isolate all the data structures shared by multiple modules
to avoid coupling.
"""
from collections import namedtuple

# Normalized record that represents information retrieved from an arbitrary source. These
# are produced by extractors and consumed by crawler
MetadataRecord = namedtuple('MetadataField', 'name, value')

# Normalized metadata. These are produced by the crawler and stored in the DB
Metadata = namedtuple('Metadata', 'field, type, total_occurrences, null_occurrences')

# Mapping between supported data types and our internal representation
RECORD_TYPE_MAPPING = {
    int: "I",
    str: "S",
    None: None
}

# Mapping between our internal data types and its human-friendly representation
RECORD_TYPE_NAME = {
    "I": "Integer",
    "S": "String",
    None: "null"
}
