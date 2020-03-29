import csv

import pytest

from common import MetadataRecord

from metadata_extractor.csv_extractor import extract_data_from_csv
from metadata_extractor.exceptions import ExtractionError

from tests.utils import write_csv


def test_csv_with_single_int_field(temp_csv_file):
    write_csv(temp_csv_file, ['field'], [{'field': 50}])
    records = list(extract_data_from_csv(temp_csv_file.name))
    assert records == [MetadataRecord('field', 50)]


def test_csv_with_several_int_fields(temp_csv_file):
    write_csv(temp_csv_file, ['field'], [{'field': idx} for idx in range(100)])
    records = list(extract_data_from_csv(temp_csv_file.name))
    assert sorted(records) == sorted([
        MetadataRecord('field', idx) for idx in range(100)])


def test_csv_with_single_str_field(temp_csv_file):
    write_csv(temp_csv_file, ['field'], [{'field': '"string_value"'}])
    records = list(extract_data_from_csv(temp_csv_file.name))
    assert records == [MetadataRecord('field', "string_value")]


def test_csv_with_several_str_field(temp_csv_file):
    write_csv(temp_csv_file, ['field'], [{'field': f'"{idx}"'} for idx in range(100)])
    records = list(extract_data_from_csv(temp_csv_file.name))
    assert sorted(records) == sorted([
        MetadataRecord('field', f'{idx}') for idx in range(100)])


def test_csv_with_single_null_field(temp_csv_file):
    write_csv(temp_csv_file, ['field'], [{'field': 'null'}])
    records = list(extract_data_from_csv(temp_csv_file.name))
    assert records == [MetadataRecord('field', None)]


def test_csv_with_several_nulls_field(temp_csv_file):
    write_csv(temp_csv_file, ['field'], [{'field': 'null'} for _ in range(100)])
    records = list(extract_data_from_csv(temp_csv_file.name))
    assert records == [MetadataRecord('field', None)] * 100


def test_csv_with_multiple_fields(temp_csv_file):
    write_csv(temp_csv_file, ['field_one', 'field_two', 'field_three'],
              [{'field_one': '"abc"', 'field_two': 50, 'field_three': 'null'}])
    records = list(extract_data_from_csv(temp_csv_file.name))
    assert sorted(records) == sorted([
        MetadataRecord('field_one', 'abc'),
        MetadataRecord('field_two', 50),
        MetadataRecord('field_three', None),
    ])


def test_csv_with_multiple_fields_multiple_rows(temp_csv_file):
    write_csv(temp_csv_file, ['field_one', 'field_two'],
              [{'field_one': '"abc"', 'field_two': 50} for _ in range(1000)])

    records = list(extract_data_from_csv(temp_csv_file.name))
    assert sorted(records) == sorted([MetadataRecord('field_one', 'abc')] * 1000 +
                                     [MetadataRecord('field_two', 50)] * 1000,
                                     )


def test_csv_missing_value_for_column(temp_csv_file):
    write_csv(temp_csv_file, ['field_one', 'field_two'],
              [{'field_one': '"abc"', }])
    with pytest.raises(ExtractionError) as exc:
        list(extract_data_from_csv(temp_csv_file.name))

    info = exc.value
    assert info.args[0] == "Missing value for column 'field_two' at line 2"


def test_csv_missing_column_for_value(temp_csv_file):
    writer = csv.writer(temp_csv_file)
    writer.writerow(['field_one', 'field_two'])
    writer.writerow(['"abc"', 50, 100])
    temp_csv_file.flush()

    with pytest.raises(ExtractionError) as exc:
        list(extract_data_from_csv(temp_csv_file.name))

    info = exc.value
    assert info.args[0] == "Missing column name for value ['100'] at line 2"


def test_csv_invalid_string_format(temp_csv_file):
    write_csv(temp_csv_file, ['field_one'], [{'field_one': 'abc', }])
    with pytest.raises(ExtractionError) as exc:
        list(extract_data_from_csv(temp_csv_file.name))

    info = exc.value
    assert info.args[0] == "Unknown type for value 'abc' (column 'field_one') at line 2"


def test_csv_unicode_column_name(temp_csv_file):
    write_csv(temp_csv_file, ['短消息'], [{'短消息': 50}])
    records = list(extract_data_from_csv(temp_csv_file.name))
    assert records == [MetadataRecord('短消息', 50)]


def test_csv_unicode_value(temp_csv_file):
    write_csv(temp_csv_file, ['field'], [{'field': '"短消息"'}])
    records = list(extract_data_from_csv(temp_csv_file.name))
    assert records == [MetadataRecord('field', '短消息')]


def test_missing_file():
    with pytest.raises(ExtractionError) as exc:
        list(extract_data_from_csv("missing.csv"))

    info = exc.value
    assert info.args[0] == "Could not open file 'missing.csv'"
