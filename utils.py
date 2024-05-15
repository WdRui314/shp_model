
import time
import json


class Doc:
    def __init__(self, path, encoding="utf-8"):
        self.path = path
        self.encoding = encoding

    def get_js(self):
        with open(self.path, mode="r", encoding=self.encoding) as f:
            data = f.read()
        data_js = json.loads(data)
        return data_js

    def to_js(self, data, ensure_ascii=False):
        data_js = json.dumps(data, ensure_ascii=ensure_ascii)
        with open(self.path, mode="w", encoding=self.encoding) as f:
            f.write(data_js)

    def read(self):
        with open(self.path, mode="r", encoding=self.encoding) as f:
            data = f.read()
        return data

    def log(self, info, split: str = "\n", istime=True):
        data = f"{time.ctime()}, {info}" if istime else info
        with open(self.path, mode="a", encoding=self.encoding) as f:
            f.write(data)
            f.write(split)


def shrink_list(lst: list):
    match len(lst):
        case 0:
            return None
        case 1:
            return lst[0]
        case _:
            return lst


def separator(notice="-"):
    print("{:-^50}".format(notice))

