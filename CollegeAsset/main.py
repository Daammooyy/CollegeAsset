from inventory import get_all, inventory

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
    if not inventory:
        return "INV" + "1".zfill(4)

    max_id = max(int(item["id"].replace("INV", "")) for item in inventory) 

    return "INV" + str(max_id + 1).zfill(4)

#Вывод всего оборудования
def show_all():
    items = get_all()
    if not items:
        print("\nИнвентарь пуст")
        return
        
    print("\n------------------- Список оборудования -------------------")
    for x, item in enumerate(items, start=1):
        print("№",x)
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

    print("Статус: 1 - исправно, 2 - Требует ремонта, 3 - списано")
    while True:
        choice = input("Выберите статус: ").strip()
        if choice == "1":
            status = "исправно"
            break
        if choice == "2":
            status = "Требует ремонта"
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
    
    inventory.append(new_item)
    print(f"\nДобавлено: {new_id}")
    return new_item

def delete():
    if not inventory:
        print("\nПусто")
        return
    
    show_all()

    while True:
        num_inp = input("\nВведите номер оборудования для удаления или 'stop' для отмены: ")

        if num_inp.lower().strip() == "stop":
            print("Отмена")
            return

        if num_inp.isdigit():
            num = int(num_inp)

            if 1 <= num <= len(inventory):
                removed = inventory[num - 1]

                while True:
                    confirm = input(f"Вы точно хотите удалить {removed['name']}? (д/н): ").strip().lower()
                    if confirm == "д":
                        inventory.pop(num - 1)
                        print("Удалено")
                        return
                    elif confirm == "н":
                        print("Отмена")
                        return
                    else:
                        print("Введите только 'д' или 'н'")
                        continue

            else: print(f"\nВведите число от 1 до {len(inventory)}")
        else: print(f"\nВведите число от 1 до {len(inventory)} или 'stop'")
                    
def modify():
    if not inventory:
        print("\nПусто")
        return
    
    show_all()

    while True:
        num_inp = input("\nВведите номер оборудования для изменения или 'stop' для отмены: ").strip()

        if num_inp.lower() == "stop":
            print("Отмена")
            return

        if num_inp.isdigit():
            num = int(num_inp)

            if 1 <= num <= len(inventory):
                item = inventory[num - 1]
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
                                item['status'] = "исправно"
                                print("Успешно")
                                return
                            elif inp == "2":
                                item['status'] = "требует ремонта"     
                                print("Успешно")
                                return                                           
                            elif inp == "3":
                                item['status'] = "списано"
                                print("Успешно")
                                return                            
                            else:
                                print("Введите корректное число")

                    elif choice == "2":
                        while True:
                            classroom = input("\nНовый кабинет: ").strip()
                            if classroom.isdigit():
                                item["room"] = classroom
                                print("Успешно")
                                return
                            print("Введите число")

                    elif choice == "0":
                        print("Обратно")
                        return
                    else: print("Введите 1, 2, 0")

            else: print(f"\nВведите число от 1 до {len(inventory)}")
        else: print(f"\nВведите число от 1 до {len(inventory)} или 'stop'")



def main():
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()
        
        if choice == "1":
            show_all()
        elif choice == "2":
            add_item()
        elif choice == "4":
            modify()
        elif choice == "5":
            delete()
        elif choice in "3":
            print(f"\nПотом")
        elif choice == "0":
            print("\nЗавершение работы программы")
            break
        else:
            print("\nОшибка, введите пункт от 1 до 5")

if __name__ == "__main__":
    main()