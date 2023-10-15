import json


class JsonReader:

    @staticmethod
    def read_file(file_path: str) -> dict:
        try:
            with open(file_path) as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Не удаёться прочесть файл: {file_path}")