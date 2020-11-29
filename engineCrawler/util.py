import os
import threading
import imagehash
import numpy as np
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
    def __init__(self, hash_method="AHASHING", similarity=50):
        self.hashing = HASHING_METHODS[hash_method]
        self.similarity = similarity
    
    def setPath(self, path):
        self.path = path

    def getFiles(self):
        files = [
            os.path.join(self.path, x)
            for x in os.listdir(self.path) 
            if os.path.isfile(self.path + os.sep + x) and \
                '.json' not in x
        ]
        _files = list(range(len(files)))
        hashings = []
        rm_ind = set()

        for sli in slices(_files):
            ths = [
                threading.Thread(self._load(files[i], rm_ind, hashings, i))
                for i in sli
            ]
            [x.start() for x in ths]
            [x.join() for x in ths]
        
        self.erase([files[i] for i in rm_ind])

        files = np.array([x for i,x in enumerate(files) if i not in rm_ind])

        self.similarity = hashings[0].shape[0]*hashings[0].shape[1]*self.similarity/100

        return files, np.array(hashings)

    def _load(self, file, rm_files, hashings, n):
        loaded = None
        try:
            loaded = self.hashing(Image.open(file)).hash
        except UnidentifiedImageError:
            print('No image format : ', file)
            rm_files.add(n)
        except:
            rm_files.add(n)
        else:
            hashings.append(loaded)

    def erase(self, rm_files):
        def rm(file_path):
            os.remove(file_path)
        rm_files = slices(rm_files)
        for sli in rm_files:
            ths = [
                threading.Thread(target=rm, args=(x,)) 
                for x in sli
            ]
            [x.start() for x in ths] 
            [x.join() for x in ths] 

    def check(self):
        file_paths, hashing = self.getFiles()

        base_dt = file_paths[0].split(os.sep)[-1].split('-')[0]+'-'
        ind = sum([1 for x in file_paths if base_dt in x])

        res = np.unique(
                 np.where(
                    np.array(
                        [
                            np.sum(np.sum(x == hashing, axis=1),axis=1)
                            for x in hashing
                        ]
                    ) > self.similarity
                )[1],
                return_counts=True
            )

        self.erase(
            list(
                file_paths[res[0][ind:][np.where(res[1][ind:] > 1)]]
            )
        )