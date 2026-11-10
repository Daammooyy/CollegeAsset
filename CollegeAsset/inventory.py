# inventory.py

# В первом спринте используем демонстрационные данные в оперативной памяти
# Структура: unique_id, type, name, room, status, date_received, responsible_person
demo_inventory = [
    {
        "id": "INV001",
        "type": "ПК",
        "name": "Intel Core i5 / 16GB / 512GB SSD",
        "room": "101",
        "status": "исправно",
        "date_received": "2026-09-01",
        "responsible_person": "Иванов И.И."
    },
    {
        "id": "INV002",
        "type": "Монитор",
        "name": "FullHD 24'' Asus",
        "room": "101",
        "status": "исправно",
        "date_received": "2026-09-01",
        "responsible_person": "Иванов И.И."
    },
    {
        "id": "INV003",
        "type": "Принтер",
        "name": "HP LaserJet Pro",
        "room": "102",
        "status": "требует ремонта",
        "date_received": "2025-12-15",
        "responsible_person": "Петров П.П."
    },
    {
        "id": "INV004",
        "type": "ПК",
        "name": "AMD Ryzen 5 / 8GB / 256GB SSD",
        "room": "103",
        "status": "исправно",
        "date_received": "2026-01-10",
        "responsible_person": "Сидоров С.С."
    },
    {
        "id": "INV005",
        "type": "Монитор",
        "name": "FullHD 21.5'' LG",
        "room": "103",
        "status": "списано",
        "date_received": "2024-05-20",
        "responsible_person": "Сидоров С.С."
    }
]

def get_all_items():
    """Возвращает текущий список всего оборудования."""
    return demo_inventory

