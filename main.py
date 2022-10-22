#!/usr/bin/env python3
import os
import argparse
from functools import reduce
from tqdm import tqdm

import dltk

# https://zhuanlan.zhihu.com/p/388983712


# def data2lmdb(dpath, name="train", write_frequency=5000, num_workers=8):
#     # 获取自定义的COCO数据集（就是最原始的那个直接从磁盘读取image的数据集）
#     dataset=COCO2014(root="/data/jxzhang/coco/",phase=name)
#     data_loader = DataLoader(dataset, num_workers=8, collate_fn=lambda x: x)

#     lmdb_path = osp.join(dpath,"%s.lmdb" % name)
#     isdir = os.path.isdir(lmdb_path)

#     print("Generate LMDB to %s" % lmdb_path)
#     db = lmdb.open(lmdb_path, subdir=isdir,
#                    map_size=1099511627776 * 2, readonly=False,
#                    meminit=False, map_async=True)
#     txn = db.begin(write=True)
#     for idx, data in enumerate(data_loader):
#         image, label, _ = data[0]
#         temp = LMDB_Image(image,label)
#         txn.put(u'{}'.format(idx).encode('ascii'), pickle.dumps(temp))
#         if idx % write_frequency == 0:
#             print("[%d/%d]" % (idx, len(data_loader)))
#             txn.commit()
#             txn = db.begin(write=True)

#     # finish iterating through dataset
#     txn.commit()
#     keys = [u'{}'.format(k).encode('ascii') for k in range(idx + 1)]
#     with db.begin(write=True) as txn:
#         txn.put(b'__keys__', pickle.dumps(keys))
#         txn.put(b'__len__', pickle.dumps(len(keys)))

#     print("Flushing database ...")
#     db.sync()
#     db.close()


def folder2lmdb(folder: str, db: str, exts=['jpg', 'png']):
    with dltk.LMDBDatabaseWriter(db) as writer:
        with tqdm(total=1) as pbar:
            for root, _, files in os.walk(folder):
                pbar.total += len(files)
                pbar.refresh()
                # print(f'root={root} basename={os.path.basename(root)}')
                for name in files:
                    pbar.update(1)
                    match = reduce((lambda x, y: x or y), [
                                   name.endswith(ext) for ext in exts])
                    if not match:
                        print(f'file {name} skipped')
                        continue
                    label = os.path.basename(root)
                    key = f'{label}/{name}'
                    full_path = os.path.join(root, name)
                    # print(f'path={full_path} key={key} label={label}')
                    rec = dltk.ImageRecord.from_image(label, full_path)
                    writer.store([key], [rec])


folder2lmdb('/mnt/dataset/CASIA-WebFaces/datasets/', 'CASIA-WebFaces')

# def lmdb2folder(db: str, folder: str):
#     with dltk.LMDBDatabaseReader(db) as reader:
#         print(len(reader))

# lmdb2folder('CASIA-WebFaces', 'extract')
# from PIL import Image

# with dltk.LMDBDatabaseReader("./db") as reader:
#     print(f'len = {len(reader)}')
#     rec = dltk.ImageRecord.loads(reader[0])
#     print(f'0 label={rec.get_label()}')
#     im = Image.fromarray(rec.get_image())
#     im.save('hi.jpg')


def main():
    parser = argparse.ArgumentParser(description='folder2lmdb')

    parser.add_argument('-i', '--input', type=str,
                        help='input image folder path')
    parser.add_argument('-o', '--output', default='db',
                        type=str, help='output database path')
    parser.add_argument('-e', '--exts-list', default=['png', 'jpg'])

    # parser.add_argument('--network', default='resnet50', help='Backbone network mobile0.25 or resnet50')
    # parser.add_argument('--cpu', action="store_true", default=False, help='Use cpu inference')
    # parser.add_argument('--confidence_threshold', default=0.02, type=float, help='confidence_threshold')
    # parser.add_argument('--top_k', default=5000, type=int, help='top_k')
    # parser.add_argument('--nms_threshold', default=0.4, type=float, help='nms_threshold')
    # parser.add_argument('--keep_top_k', default=750, type=int, help='keep_top_k')
    # parser.add_argument('-s', '--save_image', action="store_true", default=True, help='show detection results')
    # parser.add_argument('--vis_thres', default=0.6, type=float, help='visualization_threshold')
    # parser.add_argument('folders', nargs='*', help='input ')
    args = parser.parse_args()

    if not args.input:
        raise ValueError("invalid input parameter")

    if not args.output:
        raise ValueError("invalid output parameter")


if __name__ == '__main__':
    # img = cv2.imread('../FaceProject/third_party/opencv/doc/tutorials/viz/images/facedetect.jpg')
    # rec = NumpyDataRecord("l", "d")
    # raw = rec.serialize()
    # obj = NumpyDataRecord.unserialize(raw)
    # print(raw)
    # print(obj.label)
    # print(obj.data)
    pass

# path = "images/.lmdb"
    # transform = Resize((224,224))
    # dst = ImageFolderLMDB(path, transform, None)
    # loader = DataLoader(dst, batch_size=2)
    # for x in loader:
    #     print(x.shape)
