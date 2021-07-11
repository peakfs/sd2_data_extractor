from abc import ABC


class BaseStorage(ABC):
    _data = {}
    last_item = None

    @property
    def data(self):
        return self._data
