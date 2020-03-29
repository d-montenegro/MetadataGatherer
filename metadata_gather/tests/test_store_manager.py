import os
from stat import S_IREAD, S_IRGRP, S_IROTH

import pytest

from store_manager import MetadataStoreManager, StoringException
from common import Metadata


def test_successfully_storing_one_metadata(temp_db_file):
    s = MetadataStoreManager(temp_db_file.name)
    m = Metadata('field', 'I', 10, 0)
    s.store_metadata("abc", [m])

    assert [m] == list(s.retrieve_metadata("abc"))


def test_storing_several_fields(temp_db_file):
    s = MetadataStoreManager(temp_db_file.name)
    m1 = Metadata('field_1', 'I', 10, 0)
    m2 = Metadata('field_2', 'S', 10, 5)
    m3 = Metadata('field_3', None, 10, 10)
    s.store_metadata("abc", [m1, m2, m3])

    assert sorted([m1, m2, m3]) == sorted(list(s.retrieve_metadata("abc")))


def test_successfully_storing_several_metadata(temp_db_file):
    s = MetadataStoreManager(temp_db_file.name)
    m = [Metadata(f'f_{idx}', 'I', 10, 0) for idx in range(1000)]
    s.store_metadata("abc", m)

    assert m == list(s.retrieve_metadata("abc"))


def test_successfully_retrieving_by_key(temp_db_file):
    s = MetadataStoreManager(temp_db_file.name)
    m1 = Metadata('field_1', 'I', 10, 0)
    m2 = Metadata('field_2', 'S', 10, 5)
    m3 = Metadata('field_3', None, 10, 10)
    s.store_metadata("abc", [m1])
    s.store_metadata("def", [m2])
    s.store_metadata("ghi", [m3])

    assert [m1] == list(s.retrieve_metadata("abc"))
    assert [m2] == list(s.retrieve_metadata("def"))
    assert [m3] == list(s.retrieve_metadata("ghi"))


def test_corrupted_db_file(temp_db_file):
    temp_db_file.write("This is some content")
    temp_db_file.flush()
    s = MetadataStoreManager(temp_db_file.name)
    with pytest.raises(StoringException) as exc:
        s.store_metadata("abc", [Metadata('field_1', 'I', 10, 0)])

    info = exc.value
    assert info.args[0] == "Could not store metadata into the DB. Is it corrupted?"


def test_non_writable_db_file(temp_db_file):
    # set temp_db_file non-writable
    os.chmod(temp_db_file.name, S_IREAD | S_IRGRP | S_IROTH)
    with pytest.raises(StoringException) as exc:
        MetadataStoreManager(temp_db_file.name)

    info = exc.value
    assert info.args[0] == "Could not create db schema. Is it a readable path?"
