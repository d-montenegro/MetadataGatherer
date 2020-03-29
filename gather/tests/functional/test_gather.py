import argparse

from gather import main

from tests.utils import write_csv, write_json


def test_csv_gathering(monkeypatch, temp_csv_file, temp_db_file, capsys):
    write_csv(temp_csv_file, ['field_one', 'field_two', 'field_three'], [
        {'field_one': 10, 'field_two': '"abc"', 'field_three': 'null'},
        {'field_one': 'null', 'field_two': 'null', 'field_three': 'null'},
        {'field_one': 'null', 'field_two': '"def"', 'field_three': 0},
        {'field_one': 90, 'field_two': '"jkl"', 'field_three': 120},
    ])

    def namespace(_):
        return argparse.Namespace(crawl=temp_csv_file.name, database_path=temp_db_file.name)

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", namespace)

    main()

    def namespace(_):
        return argparse.Namespace(crawl=None, describe=temp_csv_file.name, database_path=temp_db_file.name)

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", namespace)

    main()

    captured = capsys.readouterr()
    assert captured.out.split('\n') == [
        f'File: {temp_csv_file.name}',
        'Total entries: 3',
        'Fields:',
        '\tfield_one, Integer, 2, 2',
        '\tfield_two, String, 3, 1',
        '\tfield_three, Integer, 2, 2',
        '',
    ]


def test_json_gathering(monkeypatch, temp_json_file, temp_db_file, capsys):
    write_json(temp_json_file, [
        {'field_one': 10, 'field_two': 'abc', 'field_three': None},
        {'field_one': None, 'field_two': None, 'field_three': None},
        {'field_one': None, 'field_two': 'def', 'field_three': 0},
        {'field_one': 90, 'field_two': 'jkl', 'field_three': 120},
    ])

    def namespace(_):
        return argparse.Namespace(crawl=temp_json_file.name, database_path=temp_db_file.name)

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", namespace)

    main()

    def namespace(_):
        return argparse.Namespace(crawl=None, describe=temp_json_file.name, database_path=temp_db_file.name)

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", namespace)

    main()

    captured = capsys.readouterr()
    assert captured.out.split('\n') == [
        f'File: {temp_json_file.name}',
        'Total entries: 3',
        'Fields:',
        '\tfield_one, Integer, 2, 2',
        '\tfield_two, String, 3, 1',
        '\tfield_three, Integer, 2, 2',
        '',
    ]
