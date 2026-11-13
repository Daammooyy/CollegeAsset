import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from main import modify, delete
from inventory import inventory

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

def test_modify_status_valid(monkeypatch, capsys):
    inputs = iter(["INV0001", "1", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    modify()
    out = capsys.readouterr().out
    assert "Успешно" in out
    assert inventory[0]["status"] == "списано"

def test_modify_room_valid_and_invalid_input(monkeypatch, capsys):
    inputs = iter(["INV0002", "2", "абв", "310"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    modify()

    out = capsys.readouterr().out
    assert "Введите число" in out
    assert "Успешно" in out
    assert inventory[1]["room"] == "310"

def test_modify_nonexistent_and_stop(monkeypatch, capsys):
    inputs = iter(["INV9999", "stop"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    modify()
    out = capsys.readouterr().out
    assert "Серийный номер не найден" in out
    assert "Отмена" in out

def test_modify_empty_list(capsys):
    inventory.clear()
    modify()

    out = capsys.readouterr().out
    assert "Пусто" in out

def test_delete_confirm_yes(monkeypatch, capsys):
    inputs = iter(["INV0001", "д"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    delete()
    out = capsys.readouterr().out
    assert "Удалено" in out
    assert len(inventory) == 1
    assert inventory[0]["id"] == "INV0002"

def test_delete_cancel_no(monkeypatch, capsys):
    inputs = iter(["INV0001", "н"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    delete()

    out = capsys.readouterr().out
    assert "Отмена" in out
    assert len(inventory) == 2

def test_delete_invalid_id(monkeypatch, capsys):
    inputs = iter(["INV0000", "stop"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    delete()

    out = capsys.readouterr().out
    assert "Серийный номер не найден" in out
    assert len(inventory) == 2
