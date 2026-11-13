import pytest
from main import error, add_item
from inventory import id_gen, get_all, inventory

@pytest.fixture(autouse=True)
def isolate_sprint2(monkeypatch):
    monkeypatch.setattr("inventory.save_data", lambda x: None)
    inventory.clear()
    inventory.extend([
        {"id": "INV0001", "type": "ПК", "name": "PC 1", "room": "101", "status": "исправно", "date_received": "2026-01-01", "responsible_person": "Иванов"},
        {"id": "INV0005", "type": "ПК", "name": "PC 2", "room": "102", "status": "исправно", "date_received": "2026-01-01", "responsible_person": "Петров"}
    ])
    yield
    inventory.clear()

def test_no_duplicate_id_generation():
    next_id = id_gen()
    assert next_id == "INV0006"

def test_empty_field_validation(monkeypatch):
    inputs = iter(["", "   ", "Ноутбук"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = error("Тест ввода: ")
    assert result == "Ноутбук"

def test_add_item_success(monkeypatch):
    inputs = iter(["Принтер", "Canon G3010", "105", "1", "2026-11-11", "Васильев В.В."])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    initial_count = len(get_all())
    inserted = add_item()
    assert len(get_all()) == initial_count + 1
    assert inserted["id"] == "INV0006"
    assert inserted["type"] == "Принтер"
    assert inserted["room"] == "105"
    assert inserted["status"] == "исправно"
