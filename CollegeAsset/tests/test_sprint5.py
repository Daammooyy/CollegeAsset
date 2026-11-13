import pytest
from inventory import inventory, filter_records


@pytest.fixture(autouse=True)
def setup_sprint5():
    inventory.clear()
    inventory.extend([
        {"id": "INV0001", "type": "ПК", "name": "PC 1", "room": "101", "status": "исправно", "date_received": "2026-09-01", "responsible_person": "Иванов"},
        {"id": "INV0002", "type": "Монитор", "name": "Mon 1", "room": "101", "status": "требует ремонта", "date_received": "2026-09-01", "responsible_person": "Иванов"},
        {"id": "INV0003", "type": "Принтер", "name": "Prn 1", "room": "202", "status": "исправно", "date_received": "2026-09-01", "responsible_person": "Петров"}
    ])
    yield
    inventory.clear()


def test_filter_by_room():
    res = filter_records(room="101")
    assert len(res) == 2
    assert all(item["room"] == "101" for item in res)


def test_filter_by_status():
    res = filter_records(status="требует ремонта")
    assert len(res) == 1
    assert res[0]["id"] == "INV0002"


def test_filter_no_matches():
    res = filter_records(room="999")
    assert res == []
