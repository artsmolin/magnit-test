from magnit_test import models


class Memory:
    """
    Простейшее хранилище для созданных клиентом тасков
    """
    def __init__(self):
        self._data: dict[str, models.Task] = {}

    def get(self, key: str) -> models.Task:
        """Получить таск по ключу"""
        return self._data[key]

    def set(self, key: str, value: models.Task):
        """Сохранить таск"""
        self._data[key] = value

    def get_collection(self) -> list[models.Task]:
        """Вернуть все таски"""
        return list(self._data.values())

    def flush(self) -> None:
        """Очистить хранилище"""
        self._data = {}


tasks_storage = Memory()
