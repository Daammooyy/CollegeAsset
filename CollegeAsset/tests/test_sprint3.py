import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from main import modify, delete
from inventory import inventory, search_records

@pytest.fixture(autouse=True)
def setup_inventory(monkeypatch):
    monkeypatch.setattr("inventory.save_data", lambda x: None)
    inventory.clear()
    inventory.extend([
        {
            "id": "INV0001",
            "type": "ПК",
            "name": "Dell OptiPlex",
            "room": "101",
            "status": "исправно",
            "date_received": "01.09.2026",
            "responsible_person": "Иванов И.И."
        },
        {
            "id": "INV0002",
            "type": "Монитор",
            "name": "Samsung S24",
            "room": "205",
            "status": "требует ремонта",
            "date_received": "05.09.2026",
            "responsible_person": "Петров П.П."
        }
    ])
    yield
    inventory.clear()

# 1. Поиск по существующему номеру и кабинету
def test_search_existing():
    by_id = search_records("INV0001")
    assert len(by_id) == 1
    assert by_id[0]["name"] == "Dell OptiPlex"

    by_room = search_records("205")
    assert len(by_room) == 1
    assert by_room[0]["id"] == "INV0002"

# 2. Поиск по несуществующему запросу
def test_search_not_found():
    result = search_records("INV9999")
    assert result == []

# 3. Изменение записи (статуса)
def test_modify_status_valid(monkeypatch, capsys):
    inputs = iter(["INV0001", "1", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    modify()
    out = capsys.readouterr().out
    assert "Успешно" in out
    assert inventory[0]["status"] == "списано"

# 4. Обработка неверного номера при изменении
def test_modify_nonexistent_and_stop(monkeypatch, capsys):
    inputs = iter(["INV9999", "stop"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    modify()
    out = capsys.readouterr().out
    assert "Серийный номер не найден" in out
    assert "Отмена" in out

# 5. Отмена удаления при ответе "н"
def test_delete_cancel_no(monkeypatch, capsys):
    inputs = iter(["INV0001", "н"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    delete()
    out = capsys.readouterr().out
    assert "Отмена" in out
    assert len(inventory) == 2
