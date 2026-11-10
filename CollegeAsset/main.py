# main.py
from inventory import get_all_items

def show_menu():
    print("\n===== CollegeAsset =====")
    print("1. Показать всё оборудование")
    print("2. Добавить новую запись")
    print("3. Поиск оборудования")
    print("4. Изменить запись")
    print("5. Удалить запись")
    print("0. Выход")
    print("===========================")

def display_inventory():
    items = get_all_items()
    if not items:
        print("\n[!] Инвентарь пуст.")
        return
        
    print("\nСписок оборудования:")
    print(f"{'№ Инв.':<10} | {'Тип':<10} | {'Наименование':<40} | {'Каб.':<6} | {'Статус':<16}")
    for item in items:
        print(f"{item['id']:<10} | {item['type']:<10} | {item['name']:<40} | {item['room']:<6} | {item['status']:<16}")

def main():
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()
        
        if choice == "1":
            display_inventory()
        elif choice in ["2", "3", "4", "5"]:
            print(f"\n[i] Эта функция будет реализована в следующих спринтах.")
        elif choice == "0":
            print("\nЗавершение работы программы. До свидания!")
            break
        else:
            print("\n[!] Неверный ввод. Пожалуйста, выберите пункт от 0 до 5.")

if __name__ == "__main__":
    main()

