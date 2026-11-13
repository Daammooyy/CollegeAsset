import os
import tempfile
import unittest
from unittest.mock import patch

import inventory
import storage
import main  # Замените на имя вашего файла с меню, если оно отличается


class TestCollegeAssetQA(unittest.TestCase):
    def setUp(self):
        # Создаём временную папку для изоляции тестов от реальных данных
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "data", "inventory.json")

        # Подменяем FILE_PATH в модуле storage
        self.patcher = patch.object(storage, "FILE_PATH", self.test_file)
        self.patcher.start()

        # Очищаем список в памяти перед каждым тестом
        inventory.inventory.clear()

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_01_missing_file_no_crash(self):
        """Критерий DoD: отсутствие файла не вызывает сбой, возвращается пустой список."""
        self.assertFalse(os.path.exists(self.test_file))
        data = storage.load_data()
        self.assertEqual(data, [])

    def test_02_empty_file_handling(self):
        """Проверка пустого файла: не падает, возвращает пустой список."""
        os.makedirs(os.path.dirname(self.test_file), exist_ok=True)
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("")

        data = storage.load_data()
        self.assertEqual(data, [])

    def test_03_corrupted_json_handling(self):
        """Критерий DoD: повреждённый JSON обрабатывается безопасно без сбоя."""
        os.makedirs(os.path.dirname(self.test_file), exist_ok=True)
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("{broken_json: [1, 2, ")

        data = storage.load_data()
        self.assertEqual(data, [])

    def test_04_persistence_across_restarts(self):
        """Критерий DoD: сохранение данных между запусками программы."""
        # 1. Первый запуск: добавляем запись через inventory.py
        added = inventory.add_record(
            item_type="Ноутбук",
            name="Lenovo ThinkPad",
            room="101",
            status="исправно",
            date_received="12.11.2026",
            responsible_person="Иванов И.И.",
        )
        self.assertEqual(added["id"], "INV0001")

        # 2. Имитация перезапуска: очищаем оперативную память и загружаем с диска заново
        inventory.inventory.clear()
        reloaded_data = storage.load_data()
        inventory.inventory.extend(reloaded_data)

        self.assertEqual(len(inventory.get_all()), 1)
        self.assertEqual(inventory.get_all()[0]["name"], "Lenovo ThinkPad")

    def test_05_cli_flow_and_relaunch(self):
        """Интеграционный тест консольного меню (добавление -> поиск -> выход -> повторный запуск)."""
        # Имитируем ввод пользователя:
        # 2 (Добавить) -> Тип -> Название -> Кабинет -> 1 (исправно) -> Дата -> Ответственный -> 0 (Выход)
        user_inputs = [
            "2",
            "Проектор",
            "Epson EB-X41",
            "205",
            "1",
            "13.11.2026",
            "Петров П.П.",
            "0",
        ]

        with patch("builtins.input", side_effect=user_inputs):
            main.main()

        # Проверяем, что запись физически сохранилась после завершения main()
        saved_after_exit = storage.load_data()
        self.assertEqual(len(saved_after_exit), 1)
        self.assertEqual(saved_after_exit[0]["room"], "205")

        # Повторный запуск меню: 3 (Поиск по "Epson") -> 0 (Выход)
        relaunch_inputs = ["3", "Epson", "0"]
        with patch("builtins.input", side_effect=relaunch_inputs):
            main.main()


if __name__ == "__main__":
    unittest.main(verbosity=2)

