import pytest

from crawler import crawl, CrawlingError
from common import MetadataRecord, Metadata


@pytest.mark.parametrize('scenario, expected_result', [
    ([], []),
    ([MetadataRecord('field', 30)], [Metadata('field', 'I', 1, 0)]),
    ([MetadataRecord('field', 'abc')], [Metadata('field', 'S', 1, 0)]),
    ([MetadataRecord('field', None)], [Metadata('field', None, 1, 1)]),
    ([MetadataRecord('field', 30)] * 10 + [MetadataRecord('field', None)] * 5,
     [Metadata('field', 'I', 15, 5)]),
    ([MetadataRecord('field', 'abc')] * 10 + [MetadataRecord('field', None)] * 5,
     [Metadata('field', 'S', 15, 5)]),
    ([MetadataRecord('f1', 1)] * 5 +
     [MetadataRecord('f2', 'abc')] * 5 +
     [MetadataRecord('f1', 2)] * 10 +
     [MetadataRecord('f2', None)] * 5, [Metadata('f1', 'I', 15, 0), Metadata('f2', 'S', 10, 5)]),
])
def test_crawling_mixed_fields(scenario, expected_result):
    assert sorted(list(crawl(scenario))) == sorted(expected_result)


def test_type_inconsistency():
    scenario = [MetadataRecord('wrong_field', 20), MetadataRecord('wrong_field', 'abc')]

    with pytest.raises(CrawlingError) as exc:
        list(crawl(scenario))

    info = exc.value
    assert info.args[0] == "The type of field 'wrong_field' is not consistent"


def test_invalid_type():
    scenario = [MetadataRecord('wrong_field', [1, 2, 3])]

    with pytest.raises(CrawlingError) as exc:
        list(crawl(scenario))

    info = exc.value
    assert info.args[0] == "The type of field 'wrong_field' is unknown"
