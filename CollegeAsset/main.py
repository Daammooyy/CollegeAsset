from inventory import get_all, inventory, add_record, search_records, update_record, delete_record, filter_records

# Меню
def show_menu():
    print("\n===== CollegeAsset =====")
    print("1. Показать всё оборудование")
    print("2. Добавить новую запись")
    print("3. Поиск оборудования")
    print("4. Изменить запись")
    print("5. Удалить запись")
    print("6. Фильтрация оборудования")
    print("0. Выход")
    print("===========================")

# Проверка ввода
def error(text_input: str) -> str:
    while True:
        user = input(text_input)
        clean = user.strip()

        if 1 <= len(clean) <= 50:
            return clean

        print("Введите от 1 до 50 символов\n")

# Общий вывод списка
def print_items(items: list):
    for x, item in enumerate(items, start=1):
        print("№", x)
        print(f"Сер. номер:    {item['id']} | Статус: {item['status']}")
        print(f"Оборудование:  {item['type']} - {item['name']}")
        print(f"Расположение:  Кабинет {item['room']}")
        print(f"Ответственный: {item['responsible_person']} (от {item['date_received']})")
        print("-" * 60)

# Вывод всего оборудования
def show_all():
    items = get_all()
    if not items:
        print("\nИнвентарь пуст")
        return
        
    print("\n------------------- Список оборудования -------------------")
    print_items(items)


# Добавление оборудования
def add_item():
    print("\n--- Новое оборудование ---")
    item_type = error("Тип: ")
    name = error("Название: ")

    while True:
        room = input("Кабинет: ").strip()
        if room.isdigit():
            break
        print("Введите число")
    
    print("Статус: 1 - исправно, 2 - требует ремонта, 3 - списано")
    while True:
        choice = input("Выберите статус: ").strip()
        if choice == "1":
            status = "исправно"
            break
        elif choice == "2":
            status = "требует ремонта"
            break
        elif choice == "3":
            status = "списано"
            break
        else:
            print("Введите 1-3")
        
    date_received = error("Дата поступления: ").strip()
    responsible_person = error("Ответственный: ").strip()

    new_item = add_record(item_type, name, room, status, date_received, responsible_person)
    print(f"\nДобавлено: {new_item['id']}")
    return new_item

# Удаление
def delete():
    if not inventory:
        print("\nПусто")
        return
    
    show_all()
    print("\n--- Удаление оборудования ---")
    while True:
        num_inp = input("\nВведите серийный номер оборудования для удаления или 'stop' для отмены: ").strip()

        if num_inp.lower() == "stop":
            print("Отмена")
            return

        target_index = -1
        for i, item in enumerate(inventory):
            if item["id"].lower() == num_inp.lower():
                target_index = i
                break

        if target_index != -1:
            removed = inventory[target_index]
            while True:
                confirm = input(f"Вы точно хотите удалить {removed['name']}? (д/н): ").strip().lower()
                if confirm == "д":
                    delete_record(target_index)
                    print("Удалено")
                    return
                elif confirm == "н":
                    print("Отмена")
                    return
                else:
                    print("Введите только 'д' или 'н'")
        else:
            print("\nСерийный номер не найден или введите 'stop'")

# Изменение
def modify():
    if not inventory:
        print("\nПусто")
        return
    show_all()
    print("\n--- Изменение оборудования ---")

    while True:
        num_inp = input("\nВведите серийный номер оборудования для изменения или 'stop' для отмены: ").strip()
        if num_inp.lower() == "stop":
            print("Отмена")
            return
        target_index = -1
        for i, item in enumerate(inventory):
            if item["id"].lower() == num_inp.lower():
                target_index = i
                break

        if target_index != -1:
            item = inventory[target_index]
            print(f"\nВыбрано:  {item['id']}")
            print(f"Название: {item['name']}")
            print(f"Кабинет:  {item['room']}")
            print(f"Статус:   {item['status']}")

            while True:
                choice = input("\n1 - Статус \n2 - Кабинет \n0 - Обратно \nВыберите что изменить: ").strip()

                if choice == "1":
                    while True:
                        inp = input("\n1 - Исправно \n2 - Требует ремонта \n3 - Списано \nНовый статус: ").strip()
                        if inp == "1":
                            update_record(target_index, "status", "исправно")
                            print("Успешно")
                            return
                        elif inp == "2":
                            update_record(target_index, "status", "требует ремонта")
                            print("Успешно")
                            return                                           
                        elif inp == "3":
                            update_record(target_index, "status", "списано")
                            print("Успешно")
                            return                            
                        else:
                            print("Введите корректное число")

                elif choice == "2":
                    while True:
                        classroom = input("\nНовый кабинет: ").strip()
                        if classroom.isdigit():
                            update_record(target_index, "room", classroom)
                            print("Успешно")
                            return
                        print("Введите число")

                elif choice == "0":
                    print("Обратно")
                    return
                else:
                    print("Введите 1, 2, 0")
        else:
            print("\nСерийный номер не найден или введите 'stop'")

# Поиск
def search():
    if not inventory:
        print("\nИнвентарь пуст")
        return

    print("\n--- Поиск ---")
    query = input("Введите запрос для поиска: ").strip()
    if not query:
        print("Запрос не может быть пустым")
        return

    result = search_records(query)

    if not result:
        print("\nНичего не найдено")
    else:
        print(f"\n------------------- Найдено записей: {len(result)} -------------------")
        print_items(result)

# Фильтрация
def filter_items():
    if not inventory:
        print("\nИнвентарь пуст")
        return

    print("\n--- Фильтрация ---")
    print("1 - По кабинету")
    print("2 - По состоянию")
    print("0 - Обратно")

    while True:
        choice = input("Выберите фильтр: ").strip()
        if choice == "1":
            while True:
                room = input("Введите номер кабинета: ").strip()
                if room.isdigit():
                    result = filter_records(room=room)
                    break
                print("Введите число")
            break
        elif choice == "2":
            print("1 - исправно, 2 - требует ремонта, 3 - списано")
            while True:
                st = input("Выберите статус: ").strip()
                if st == "1":
                    result = filter_records(status="исправно")
                    break
                elif st == "2":
                    result = filter_records(status="требует ремонта")
                    break
                elif st == "3":
                    result = filter_records(status="списано")
                    break
                print("Введите 1-3")
            break
        elif choice == "0":
            return
        else:
            print("Введите 1, 2 или 0")

    if not result:
        print("\nНичего не найдено")
    else:
        print(f"\n------------------- Найдено записей: {len(result)} -------------------")
        print_items(result)
        
# Выбор действия
def main():
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()
        
        if choice == "1":
            show_all()
        elif choice == "2":
            add_item()
        elif choice == "3":
            search()
        elif choice == "4":
            modify()
        elif choice == "5":
            delete()
        elif choice == "6":
            filter_items()
        elif choice == "0":
            print("\nЗавершение работы программы")
            break
        else:
            print("\nОшибка, введите пункт от 0 до 6")

if __name__ == "__main__":
    main()
