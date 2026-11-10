from datetime import date
from inventory import get_all, demo_inventory

#Меню
def show_menu():
    print("\n===== CollegeAsset =====")
    print("1. Показать всё оборудование")
    print("2. Добавить новую запись")
    print("3. Поиск оборудования")
    print("4. Изменить запись")
    print("5. Удалить запись")
    print("0. Выход")
    print("===========================")

#Проверка ввода
def error(text_input: str) -> str:
    while True:
        user = input(text_input)
        clean = user.strip()

        if 2 <= len(clean) <= 50:
            return clean

        print("Введите от 2 до 50 символов\n")

#Генерация ID
def id_gen():
    if not demo_inventory:
        return "INV" + "1".zfill(4)

    max_id = max(int(item["id"].replace("INV", "")) for item in demo_inventory) 

    return "INV" + str(max_id + 1).zfill(4)

#Вывод всего оборудования
def show_all():
    items = get_all()
    if not items:
        print("\nИнвентарь пуст")
        return
        
    print("\n------------------- Список оборудования -------------------")
    for item in items:
        print(f"Сер. номер:    {item['id']} | Статус: {item['status']}")
        print(f"Оборудование:  {item['type']} - {item['name']}")
        print(f"Расположение:  Кабинет {item['room']}")
        print(f"Ответственный: {item['responsible_person']} (от {item['date_received']})")
        print("-" * 60)


#Добавление оборудования
def add_item():
    print("\n--- Новое оборудование ---")
    item_type = error("Тип: ")
    name = error("Название: ")
    while True:
        room = input("Кабинет: ").strip()
        if room.isdigit():
            break
        print("Введите число")

    print("Статус: 1 - исправно, 2 - в ремонте, 3 - списано")
    while True:
        choice = input("Выберите статус: ").strip()
        if choice == "1":
            status = "исправно"
            break
        if choice == "2":
            status = "в ремонте"
            break
        elif choice == "3":
            status = "списано"
            break
        else:
            print("Введите 1-3")
        
    date_received = error("Дата поступления: ").strip()
    responsible_person = error("Ответственный: ").strip()

    new_id = id_gen()
    
    new_item = {
        "id": new_id,
        "type": item_type,
        "name": name,
        "room": room,
        "status": status,
        "date_received": date_received,
        "responsible_person": responsible_person
    }
    
    demo_inventory.append(new_item)
    print(f"\nДобавлено: {new_id}")
    return new_item


def main():
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()
        
        if choice == "1":
            show_all()
        if choice == "2":
            add_item()
        elif choice in ["3", "4", "5"]:
            print(f"\nПотом")
        elif choice == "0":
            print("\nЗавершение работы программы")
            break
        else:
            print("\nОшибка, введите пункт от 1 до 5")

if __name__ == "__main__":
    main()