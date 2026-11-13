import os
import pytest
import storage
import inventory


@pytest.fixture(autouse=True)
def isolate_storage(tmp_path, monkeypatch):
    test_file = tmp_path / "data" / "inventory.json"
    monkeypatch.setattr(storage, "FILE_PATH", str(test_file))
    inventory.inventory.clear()
    yield test_file
    inventory.inventory.clear()


def test_missing_file_returns_empty_list(isolate_storage):
    assert not os.path.exists(isolate_storage)
    assert storage.load_data() == []


def test_empty_file_returns_empty_list(isolate_storage):
    os.makedirs(os.path.dirname(isolate_storage), exist_ok=True)
    isolate_storage.write_text("", encoding="utf-8")
    assert storage.load_data() == []


def test_corrupted_json_returns_empty_list(isolate_storage):
    os.makedirs(os.path.dirname(isolate_storage), exist_ok=True)
    isolate_storage.write_text("{broken_json: [1, 2", encoding="utf-8")
    assert storage.load_data() == []


def test_persistence_across_restarts(isolate_storage):
    inventory.add_record("Ноутбук", "Lenovo", "101", "исправно", "12.11.2026", "Иванов И.И.")
    inventory.inventory.clear()
    reloaded = storage.load_data()
    inventory.inventory.extend(reloaded)

    assert len(inventory.get_all()) == 1
    assert inventory.get_all()[0]["name"] == "Lenovo"
