# MetadataGatherer

A toy CLI utility to gather metadata from files in local file-system and store it in a SQL DB.

## Using MetadataGatherer

### Prerequisites

This utility requires Python 3.6. Although it should work in any version >= 3.0, it has been developed 
and tested only in version 3.6.

### Usage

To run the utility, simply invoke the script _gather.py_ in _metadata_gather_ folder. See the following
examples:
```bash
# see help
python gather.py -h

# gather metadata from examples/metadata.csv
python gather.py -c examples/metadata.csv --database-path metadata_gather.db

# describe metadata from examples/metadata.csv
python gather.py -d examples/metadata.csv --database-path metadata_gather.db
```

The _--database-path_ is optional, and its default value is _metadata_gather.db_.

## Tests

Running the test is straightforward. Although is not mandatory, it's advised to create a virtual environment 
dedicated to this project.
```bash
python3.6 -m venv ~/.virtualenvs/metadata_gather # create a virtualenv in the desired destination
source ~/.virtualenvs/metadata_gather/bin/activate # activate the new virtual env way
```
Now, you can install all the dependencies for the project using pip and run the tests in the following way.
```bash
cd metadata_gather
pip install -r requirements_dev.txt
pytest
```

## Architecture

This utility has three totally uncoupled layers:
 * Metadata extraction: contains the logic to extract records from arbitrary sources. The supported ones 
 are JSON and CSV file, but can be extended in the future. It's implemented in the package 
 _metadata_extractor_ and produces list of _MetadataRecord_.
 * Crawling: contains the logic to summarize records into the metadata that needs to be stored. It's implemented
 in the module _crawler.py_, and summarizes a list of _MetadataRecord_ into _Metadata_ objects.
 * Storing: contains the logic to store metadata into a DB and retrieve them from it. It's implemented module
 _store_manager.py_, and stores and retrieves _Metadata_ objects.

Both _MetadataRecord_ and _Metadata_ are just immutable tuples. The first one is of size, describing a field name
and a field value. The second one is of size 4, and contains the fields _field_, _type_, _total_occurrences_ abd 
_null_occurrences_.

## Disclaimer

### DB Schmea not optimum
The DB schema for this application consists of a single table with the following fields:

* id: the primary key
* file_id: an identifier for the source of the metadata
* field_name: metadata's field
* field_type: the type of the field
* total_occurrences: the total occurrences of this field
* null_occurrences: the null occurrences of this field

As it can be easily seen, the file_id value is repeated for all the fields extracted from the same source
which is a waste of space. This can be solved by splitting this table into two. The first must containing 
only the file_id, and the second should contain all of the rest of the fields with foreign key to the first one.

In this version of the application, the file_id is the absolute path of the file the fields were extracted
from. To optimize space, this can be improved by translating it to a shorter form. For instance, it can 
be encoded in base64.

### JSON Reader space complexity

In the current version of this utility, the logic to extract metadata from JSON files needs to read the
hole file in memory. An optimal approach should read object by object. This can be achieved by reading the
file character by character, an getting an object when curly brackets get balanced.
