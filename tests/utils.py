import csv
import json


def write_csv(file_like, fieldnames, rows):
    writer = csv.DictWriter(file_like, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)


def write_json(file_like, mapping):
    json.dump(mapping, file_like)
    file_like.flush()
