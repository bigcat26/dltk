import lmdb
from .interface.record import Record
from .interface.database_reader import DatabaseReader

class LMDBDatabaseReader(DatabaseReader):    
    def __init__(self, path: str, map_size: int = 1099511627776):
        self.path = path
        self.map_size = map_size

    def _rebuild_index_cache(self):
        with self.env.begin(write=False) as txn:
            self.keys = list(txn.cursor().iternext(values=False))

    def __enter__(self):
        self.env = lmdb.open(self.path, map_size=self.map_size)
        self.txn = self.env.begin(write=False)
        self._rebuild_index_cache()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.keys = list()
        self.env.close()

    def __len__(self):
        return self.env.stat()['entries']

    def __repr__(self):
        return self.__class__.__name__ + ' (' + self.db_path + ')'

    def __getitem__(self, index):
        return self.txn.get(self.keys[index])

