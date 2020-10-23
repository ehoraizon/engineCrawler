import os
import threading
import imagehash
from PIL import Image, UnidentifiedImageError

def slices(lista, steps=5):
    x = len(lista)
    sl = []
    bef_steps = 0
    curr_steps = steps

    while True:
        sl.append(lista[bef_steps:curr_steps])
        if curr_steps + steps > x - 1:
            sl.append(lista[curr_steps:])
            break
        bef_steps = curr_steps
        curr_steps += steps

    return sl

HASHING_METHODS = {
    "AHASHING" : imagehash.average_hash,
    "PHASHING" : imagehash.phash,
    "DHASHING" : imagehash.dhash,
    "WHASHING" : imagehash.whash,
    "COLORHASHING" : imagehash.colorhash
}

class DuplInFolder:
    files = []
    checked = []
    current = None
    current_dt = None
    rm_paths = []

    def __init__(self, path, hash_method="AHASHING", similarity=50):
        self.path = path
        self._getFiles()
        self.hashing = HASHING_METHODS[hash_method]
        self.similarity = similarity

    def _getFiles(self):
        self.files = [
            os.path.join(self.path, x) 
            for x in os.listdir(self.path) 
            if os.path.isfile(self.path + os.sep + x) and \
               os.path.join(self.path, x) not in self.checked and \
               '.json' not in x
        ]
        if len(self.files):
            self.current = self.files[0]
            self.files = self.files[1:]
            self.checked.append(self.current)

    def _load(self, file):
        loaded = None
        try:
            loaded = self.hashing(Image.open(file)) #no need to convert to array
        except UnidentifiedImageError: #eliminate the image
            self.rm_paths.append(file)
        finally:
            return loaded

    def _rm(self):
        _cach = os.listdir(self.path)
        [os.remove(x) for x in set(self.rm_paths) if x.split('\\')[-1] in _cach]
        self.rm_paths = []

    def cmp(self, file): #use hash methods
        if type(file) != type(None):
            if self.current_dt - file > self.similarity or \
               self.current_dt == file:
                return True
        return False

    def _thread(self, file):
        def _work(file):
            fl = self._load(file)
            if file:
                if self.cmp(fl):
                    self.rm_paths.append(file)

        return threading.Thread(target=_work, args=(file,))

    def dupl(self):
        self.current_dt = self._load(self.current)

        if type(self.current_dt) != type(None):
            fls = slices(self.files)

            for _fls in fls:
                threads = [self._thread(x) for x in _fls]
                [x.start() for x in threads]
                [x.join() for x in threads]

        self._rm()

    def check(self):
        while len(self.files) > 0:
            self.dupl()
            self._getFiles()