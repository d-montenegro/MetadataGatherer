import pytest

from common import MetadataRecord
from metadata_extractor.json_extractor import extract_data_from_json, ExtractionError

from tests.utils import write_json


def test_json_with_single_int_field(temp_json_file):
    write_json(temp_json_file, [{'field': 50}])
    records = list(extract_data_from_json(temp_json_file.name))
    assert records == [MetadataRecord('field', 50)]


def test_json_with_several_int_fields(temp_json_file):
    write_json(temp_json_file, [{'field': idx} for idx in range(100)])
    records = list(extract_data_from_json(temp_json_file.name))
    assert sorted(records) == sorted([
        MetadataRecord('field', idx) for idx in range(100)])


def test_json_with_single_str_field(temp_json_file):
    write_json(temp_json_file, [{'field': 'string_value'}])
    records = list(extract_data_from_json(temp_json_file.name))
    assert records == [MetadataRecord('field', 'string_value')]


def test_json_with_several_str_field(temp_json_file):
    write_json(temp_json_file, [{'field': f'{idx}'} for idx in range(100)])
    records = list(extract_data_from_json(temp_json_file.name))
    assert sorted(records) == sorted([
        MetadataRecord('field', f'{idx}') for idx in range(100)])


def test_json_with_single_null_field(temp_json_file):
    write_json(temp_json_file, [{'field': None}])
    records = list(extract_data_from_json(temp_json_file.name))
    assert records == [MetadataRecord('field', None)]


def test_json_with_several_nulls_field(temp_json_file):
    write_json(temp_json_file, [{'field': None} for _ in range(100)])
    records = list(extract_data_from_json(temp_json_file.name))
    assert records == [MetadataRecord('field', None)] * 100


def test_json_with_multiple_fields(temp_json_file):
    write_json(temp_json_file, [{'field_one': 'abc', 'field_two': 50, 'field_three': None}])
    records = list(extract_data_from_json(temp_json_file.name))
    assert sorted(records) == sorted([
        MetadataRecord('field_one', 'abc'),
        MetadataRecord('field_two', 50),
        MetadataRecord('field_three', None),
    ])


def test_json_with_multiple_fields_multiple_rows(temp_json_file):
    write_json(temp_json_file, [{'field_one': 'abc', 'field_two': 50} for _ in range(1000)])

    records = list(extract_data_from_json(temp_json_file.name))
    assert sorted(records) == sorted([MetadataRecord('field_one', 'abc')] * 1000 +
                                     [MetadataRecord('field_two', 50)] * 1000,
                                     )


def test_json_unicode_column_name(temp_json_file):
    write_json(temp_json_file, [{'短消息': 50}])
    records = list(extract_data_from_json(temp_json_file.name))
    assert records == [MetadataRecord('短消息', 50)]


def test_json_unicode_value(temp_json_file):
    write_json(temp_json_file, [{'field': '短消息'}])
    records = list(extract_data_from_json(temp_json_file.name))
    assert records == [MetadataRecord('field', '短消息')]


def test_unexpected_json_structure(temp_json_file):
    write_json(temp_json_file, {'field': 'value'})
    with pytest.raises(ExtractionError) as exc:
        list(extract_data_from_json(temp_json_file.name))

    info = exc.value
    assert info.args[0] == 'Invalid JSON structure. It must contain a list of objects'


def test_non_json_file(temp_json_file):
    temp_json_file.write("This is a not JSON content")
    with pytest.raises(ExtractionError) as exc:
        list(extract_data_from_json(temp_json_file.name))

    info = exc.value
    assert info.args[0] == f"The file '{temp_json_file.name}' is not a valid JSON file"


def test_missing_file():
    with pytest.raises(ExtractionError) as exc:
        list(extract_data_from_json("missing.json"))

    info = exc.value
    assert info.args[0] == "Could not open file 'missing.json'"
