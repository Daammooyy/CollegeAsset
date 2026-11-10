import pytest
from main import add_item
from inventory import get_all

def test_add_item_success(monkeypatch):
    inputs = iter([
        "Ноутбук",
        "Lenovo ThinkPad",
        "104",
        "1",
        "2026-11-10",
        "Петров П.П."
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    initial_count = len(get_all())
    
    inserted_item = add_item()
    
    assert len(get_all()) == initial_count + 1
    assert inserted_item["type"] == "Ноутбук"
    assert inserted_item["room"] == "104"

def test_add_item_validation_room(monkeypatch):
    inputs = iter([
        "Монитор",
        "Samsung 27",
        "abc",
        "105",
        "1", 
        "2026-11-10", 
        "Иванов И.И."
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    inserted_item = add_item()
    assert inserted_item["room"] == "105"
