import lmdb
from .interface.record import Record
from .interface.database_writer import DatabaseWriter

class LMDBDatabaseWriter(DatabaseWriter):
    def __init__(self, path: str, map_size: int = 1099511627776):
        self.path = path
        self.map_size = map_size

    def store(self, key: list[str], record: list[Record]):
        for i in range(len(key)):
            self.txn.put(key[i].encode("ascii"), record[i].dumps())
            # self.keys.append(key[i].encode("ascii"))

    def abort(self):
        self.txn.abort()
        self.txn = None

    def commit(self):
        self.txn.commit()

    def __enter__(self):
        self.env = lmdb.open(self.path, map_size=self.map_size)
        self.txn = self.env.begin(write=True)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.txn:
            self.txn.commit()
            self.txn = None
        self.env.sync()
        self.env.close()

    def __repr__(self):
        return self.__class__.__name__ + ' (' + self.db_path + ')'
