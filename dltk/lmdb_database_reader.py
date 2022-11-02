import copy
import lmdb
import numpy as np
from .data.record import Record
from .data.database_reader import DatabaseReader

class LMDBDatabaseReader(DatabaseReader):
    def __init__(self, path: str, map_size: int = 1099511627776):
        self._path = path
        self._env = lmdb.open(self._path, map_size=map_size)
        self._txn = self._env.begin(write=False)
        self._rebuild_index_cache()

    def _rebuild_index_cache(self):
        self._keys = list(self._txn.cursor().iternext(values=False))

    def close(self):
        self._env.close()
        self._env = None

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def __len__(self):
        return len(self._keys)

    def __repr__(self):
        return self.__class__.__name__ + ' (' + self._path + ')'

    def __getitem__(self, index) -> Record:
        return self._txn.get(self._keys[index])

    def shuffle(self):
        """
        shuffle records
        """
        np.random.seed(10101)
        np.random.shuffle(self._keys)
        np.random.seed(None)

    def split(self, ratio):
        keys_total = len(self._keys)
        ratio_total = sum(ratio)
        prev_size = 0
        dataset = []
        for r in ratio:
            cur_size = prev_size + int(keys_total * r / ratio_total)
            dataset_id = len(dataset)
            dataset.append(copy.copy(self))
            dataset[dataset_id]._keys = copy.deepcopy(self._keys)[prev_size:cur_size]
            # print(f'range={prev_size}-{cur_size}, len={len(dataset[dataset_id]._keys)}')
            prev_size = cur_size

        return dataset
