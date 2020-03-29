from store_manager import MetadataStoreManager
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
