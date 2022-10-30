import dltk
import numpy as np

def generate_database(path, records):
    with dltk.LMDBDatabaseWriter(path) as writer:
        for i in range(records):
            rec = dltk.ImageRecord(f'label{i}', np.random.random((224, 224, 3)))
            writer.store([f'key{i}'], [rec])
        writer.commit()
