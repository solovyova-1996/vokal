import json
import os


class DbWork:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_json_file(self):
        try:
            with open(self.file_name, 'r', encoding="utf-8") as json_file:
                data = json.load(json_file)
                return data
        except FileNotFoundError:
            print(f"File '{self.file_name}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from '{self.file_name}'. Check if the file contains valid JSON.")
            return None

    def read_category(self):
        data = self.read_json_file()
        result = []
        if data is not None:
            for d in data:
                result.extend(d["params"])
            return list(set(result))
        else:
            return []

    def audio_for_category(self, name_category):
        data = self.read_json_file()
        result = []
        for d in data:

            if name_category in d["params"]:
                result.append(d["file"])
        return result

    def append_to_json(self, data):
        try:
            with open(self.file_name, 'r+') as file:
                # Загружаем существующие данные из файла
                file_data = json.load(file)

                # Добавляем новые данные к существующим
                file_data.append(data)

                # Перематываем файл в начало и перезаписываем данные
                file.seek(0)
                json.dump(file_data, file, indent=4)
                file.truncate()
        except FileNotFoundError:
            # Если файл не существует, создаем его и записываем данные
            with open(self.file_name, 'w') as file:
                json.dump([data], file, indent=4)

    def delete_item_from_json(self, key_to_delete):
        try:
            with open(self.file_name, 'r') as json_file:
                data_list = json.load(json_file)
            for data in data_list:
                file_name = data.get("file")
                if os.path.exists(file_name):
                    os.remove(file_name)
                    print(f"Файл {file_name} успешно удален.")
                else:
                    print(f"Файл {file_name} не найден.")
                if key_to_delete == data.get("name"):
                    data_list.remove(data)

            with open(self.file_name, 'w') as json_file:
                json.dump(data_list, json_file, indent=4)

            print(f"Key '{key_to_delete}' deleted from JSON file.")
        except FileNotFoundError:
            print("JSON file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def check_name(self, name):
        result = False
        with open(self.file_name, 'r') as json_file:
            data_list = json.load(json_file)
        for data in data_list:
            if data["name"] == name:
                result = True
        return result

    def update_params_by_name(self, target_name, new_params):
        print(new_params, "new", target_name)
        with open(self.file_name, 'r') as file:
            data = json.load(file)

        for item in data:
            if item['name'] == target_name.rstrip().lstrip():
                print(item['params'])
                item['params'] = new_params
                print(item['params'], "d")
        print(data)
        with open(self.file_name, 'w') as file:
            json.dump(data, file, indent=4)


if __name__ == "__main__":
    db = DbWork("../../db.json")
    print(db.read_json_file())
    db.delete_item_from_json("For_hard")
