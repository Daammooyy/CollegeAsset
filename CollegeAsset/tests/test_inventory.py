"""Автотесты спринта 1: загрузка данных, просмотр, обработка меню."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import handle_choice
from storage import load_items
from inventory import show_items, find_by_number


def test_load_demo_data_returns_five_records():
    items = load_items()
    assert len(items) == 5
    for item in items:
        assert item["inventory_number"]
        assert item["type"] in ("ПК", "Монитор", "Принтер", "Ноутбук")
        assert item["status"] in ("исправно", "требует ремонта", "списано")


def test_show_items_contains_all_numbers():
    items = load_items()
    output = show_items(items)
    for item in items:
        assert item["inventory_number"] in output
        assert item["name"] in output


def test_unknown_menu_choice_does_not_crash():
    result = handle_choice("9", load_items())
    assert "Неизвестный пункт меню" in result


def test_find_by_number_found_and_not_found():
    items = load_items()
    found = find_by_number(items, "ИВ-0003")
    assert found is not None and found["type"] == "Монитор"
    assert find_by_number(items, "ИВ-9999") is None
