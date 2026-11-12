
from data.sample_records import sample_records


def load_records():
    return sample_records


def search(keyword):
    results = []

    for record in load_records():
        if keyword.lower() in record["cheat_sheet"].lower():
            results.append(record)

    return results


def count_by(category):
    count = 0

    for record in load_records():
        if record["owasp_top10_category"] == category:
            count += 1

    return count


def get_by_id(record_id):
    records = load_records()

    if 1 <= record_id <= len(records):
        return records[record_id - 1]

    return None
