import pytest
from main import id_gen, error, add_item
from inventory import get_all, inventory

def test_id_correct_format():
    next_id = id_gen()
    assert next_id == "INV0006"

def test_errors_on_short(monkeypatch):
    inputs = iter(["", "Ноут"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = error("Тест ввода: ")
    assert result == "Ноут"


def test_add_item(monkeypatch):
    inputs = iter(
        [
            "Принтер",
            "Canon G3010",
            "105",
            "1",
            "2026-11-11",
            "Васильев В.В.",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    initial_count = len(get_all())
    inserted_item = add_item()

    assert len(get_all()) == initial_count + 1
    assert inserted_item["id"] == "INV0006"
    assert inserted_item["type"] == "Принтер"
    assert inserted_item["status"] == "исправно"
    assert inserted_item["room"] == "105"
