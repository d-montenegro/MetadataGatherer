# MetadataGatherer

A toy CLI utility to gather metadata from files in local file-system and store it in a SQLite DB.

## Using MetadataGatherer

### Prerequisites

This utility requires _Python 3.6_. Although it should work in any version >= 3.0, it has been developed
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

The _--database-path_ is optional, and its default value is _metadata_gather.db_ in the current working
directory.

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

## Design

This utility has three totally uncoupled layers. The first reads data from a file and produces records. The second
summarizes those records into normalized metadata. The third one stores that metadata into a SQLite DB.

### Producing Records

The logic to produce records is isolated in package _metadata_extractor_. It exposes only one function,
_extract_metadata_from_file_, that receives the path to a local file and produces records in lazily way.
The records are implemented as instances of _MetadataRecord_, a simple tuple of size two representing a
pair field name - field value.

There are only two file formats supported, _CSV_ and _JSON_. In order to simplify the addition of new file
formats, an _Strategy_-like pattern is implemented with a decorator. The decorator allows the registering
of functions into a mapping by extension, and the choice of the strategy is made internally using that mapping.

### Summarizing Records

The logic to perform summarizing is isolated in module _crawler.py_. It exposes only one function,
_crawl_, that summarizes a sequence of records into normalized data. This data is represented as a
list of _Metadata_, a tuple of size four with the following attributes:

* field
* type
* total_occurrences
* null_occurrences

all of them are self-explanatory.

### Storing Metadata

The logic to store and retrieve metadata into SQLite DB is isolated in module _store_manager.py_. It
exposes the class _MetadataStoreManager_, with two public methods:
 * store_metadata: stores a sequence of _Metadata_ objects
 * retrieve_metadata: retrieves a sequence of _Metadata_ objects

## Disclaimer

### DB Schema is not optimum
The DB schema for this application consists of a single table with the following fields:

* id: the primary key
* file_id: an identifier for the source of the metadata
* field_name: metadata's field
* field_type: the type of the field
* total_occurrences: the total occurrences of this field
* null_occurrences: the null occurrences of this field

As it can be easily seen, the file_id value is repeated for all the fields extracted from the same source,
which is a waste of space. This can be solved by splitting this table into two. The first must containing 
only the file_id, and the second should contain all of the rest of the fields with foreign key to the first one.

In this version of the application, the file_id is the absolute path of the file the fields were extracted
from. To optimize space, this can be improved by translating it to a shorter form.

### JSON Reader space complexity

In the current version of this utility, the logic to extract metadata from JSON files needs to read the
hole file in memory. An optimal approach should read object by object. This can be achieved by reading the
file character by character, and getting an object when curly brackets get balanced.
