from storage import load_data, save_data

inventory = load_data()

def get_all() -> list:
    return inventory


def id_gen() -> str:
    if not inventory:
        return "INV" + "1".zfill(4)

    max_id = max(int(item["id"].replace("INV", "")) for item in inventory)
    return "INV" + str(max_id + 1).zfill(4)


def add_record(item_type: str, name: str, room: str, status: str, date_received: str, responsible_person: str) -> dict:
    new_item = {
        "id": id_gen(),
        "type": item_type,
        "name": name,
        "room": room,
        "status": status,
        "date_received": date_received,
        "responsible_person": responsible_person
    }
    inventory.append(new_item)
    save_data(inventory)
    return new_item


def search_records(query: str) -> list:
    words = query.strip().lower().split()
    result = []

    for item in inventory:
        full_info = (
            f"{item['id']} {item['type']} {item['name']} "
            f"{item['room']} {item['status']} {item['responsible_person']}"
        ).lower()

        if all(word in full_info for word in words):
            result.append(item)

    return result


def update_record(index: int, field: str, value: str) -> dict:
    item = inventory[index]
    item[field] = value
    save_data(inventory)
    return item


def delete_record(index: int) -> dict:
    removed = inventory.pop(index)
    save_data(inventory)
    return removed
