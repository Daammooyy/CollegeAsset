import pytest
from inventory import get_all

def test_returns_list():
    items = get_all()
    assert isinstance(items, list)
    assert len(items) > 0

def test_item_structure():
    items = get_all()
    first_item = items[0]
    expected_keys = {'id', 'type', 'name', 'room', 'status', 'date_received', 'responsible_person'}
    assert expected_keys.issubset(first_item.keys())

def test_specific_item_data():
    items = get_all()
    first_item = items[0]
    assert first_item['id'] == "INV0001"
    assert first_item['type'] == "ПК"
    assert first_item['room'] == "101"
    assert first_item['status'] == "исправно"
