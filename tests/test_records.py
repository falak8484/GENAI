
from app import records as records_module
from data.sample_records import sample_records


def test_load_records_returns_list():
    result = records_module.load_records()

    assert isinstance(result, list)
    assert len(result) > 0


def test_search_finds_matching_cheat_sheet():
    keyword = sample_records[0]["cheat_sheet"]

    result = records_module.search(keyword)

    assert len(result) > 0
    assert result[0]["cheat_sheet"] == keyword


def test_search_is_case_insensitive():
    keyword = sample_records[0]["cheat_sheet"].upper()

    result = records_module.search(keyword)

    assert len(result) > 0


def test_count_by_returns_correct_count():
    category = sample_records[0]["owasp_top10_category"]

    expected = sum(
        1
        for record in sample_records
        if record["owasp_top10_category"] == category
    )

    assert records_module.count_by(category) == expected


def test_get_by_id_returns_correct_record():
    result = records_module.get_by_id(1)

    assert result == sample_records[0]


def test_get_by_id_returns_none_for_invalid_id():
    assert records_module.get_by_id(0) is None
    assert records_module.get_by_id(len(sample_records) + 1) is None
