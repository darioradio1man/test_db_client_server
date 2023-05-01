from datetime import datetime
import json


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CustomDB(metaclass=MetaSingleton):
    records_db = []
    logs = []

    def __init__(self, *args):
        self.id = 0
        self.columns = args
        self.record_time = None

    def add_records(self, **kwargs):
        """
        Добавление записей в БД
        :param kwargs: значения передаются по типу "ключ-значение"
        :return:
        """
        self.id += 1
        self.record_time = datetime.now()
        try:
            keys = [str(x) for x in kwargs.keys()]
            if keys == self.columns:
                for key, value in kwargs.items():
                    CustomDB.records_db.append({'id': self.id, key: value, 'timestamp': self.record_time})
                    CustomDB.logs.append(f'The record with {self.id} was created in {self.record_time}')
            else:
                raise KeyError
        except KeyError:
            print("Mismatch keys")

    def update_records(self, target_id: int, **kwargs):
        """

        :param target_id: id в котором нужно обновить запись
        :param kwargs: ключ-значение
        :return:
        """
        try:
            keys = [x for x in kwargs.keys()]
            if target_id < self.id:
                if keys in self.columns:
                    for key, value in kwargs.items():
                        CustomDB.records_db[target_id - 1][key] = value
                    record_time = datetime.now()
                    CustomDB.logs.append(f'The record with {target_id} was updated in {record_time}')
                else:
                    raise KeyError
            else:
                raise ValueError
        except (KeyError, ValueError):
            print("Mismatch keys or values")

    def delete_records(self, target_id: int):
        try:
            if target_id < self.id:
                del CustomDB.records_db[target_id - 1]
                record_time = datetime.now()
                CustomDB.logs.append(f'The record with {target_id} was deleted in {record_time}')
                return f'The record with {target_id} was deleted in {record_time}'
            else:
                return f"Key {target_id} doesn't exist"
        except KeyError:
            print("Mismatch keys or values")

    def __str__(self):
        return json.dumps(dict(CustomDB.records_db), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def save_db(location: str):
        try:
            json.dump(CustomDB.records_db, open(location))
            return True
        except SystemError:
            return False

    @staticmethod
    def show_last_changes(num_for_show: int):
        """
        Функция, позволяющая отсмотреть последние num_for_show записей
        :param num_for_show: сколько записей мы можем просмотреть
        :return: срез списка с последними записями
        """
        if len(CustomDB.logs) != 0:
            return CustomDB.logs[-num_for_show:-1]
        return []

    @staticmethod
    def sliding_window(cursor: float = 0.0, direction: str = None, pagination: int = 100):
        """
        Функция, позволяющая отсматривать часть записей БД с указанной позицией курсора
        :param cursor: от 0 до 1. Где 0 - начало БД, а 1 - конец БД
        :param direction: 'down' - прокрутка вниз, 'up' - прокрутка вверх
        :param pagination: Количество записей, которые мы можем отсмотреть
        :return:
        """
        if pagination >= len(CustomDB.records_db):
            if direction == 'down':
                cursor += (1 / len(CustomDB.records_db)) + 1
                return CustomDB.records_db[
                       int(cursor * len(CustomDB.records_db)):int(cursor * len(CustomDB.records_db)) + pagination]
            elif direction == 'up':
                cursor -= (1 / len(CustomDB.records_db)) - 1
                if cursor < 0.0:
                    cursor = 0.0
                return CustomDB.records_db[
                       int(cursor * len(CustomDB.records_db)):int(cursor * len(CustomDB.records_db)) + pagination]
        return CustomDB.records_db
