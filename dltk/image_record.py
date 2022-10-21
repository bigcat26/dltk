import pickle
import numpy as np
from PIL import Image
from .interface import Record

class ImageRecord(Record):
    def __init__(self, label, image: np.array):
        self.label = label
        self.data = image.tobytes()
        self.channels = image.shape[2] if len(image.shape) > 2 else 1
        self.size = image.shape[:2]

    def get_label(self):
        return self.label

    def get_image(self):
        image = np.frombuffer(self.data, dtype=np.uint8)
        return image.reshape(*self.size, self.channels)

    def dumps(self):
        return pickle.dumps(self)

    def __repr__(self):
        return f'{self.__class__.__name__} (image channels={self.channels} size={self.size} len={len(self.data)})'

    @staticmethod
    def loads(data):
        return pickle.loads(data)

    @staticmethod
    def from_image(label, file: str):
        data = np.array(Image.open(file), np.uint8)
        return ImageRecord(label, data)
