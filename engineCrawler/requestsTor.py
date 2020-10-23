from .settings import Settings

import requests
import os
from time import sleep

def getSession():
    sess = requests.session()

    if not Settings['TOR']:
        return sess

    os.popen(Settings['TOR'])
    sleep(20)

    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }

    sess.proxies = proxies

    return sess

def getFile(path, sess, url, frm=''):
    if frm:
        ext = frm
    else:
        ext = '.' + url.split('/')[-1].split('.')[-1]
    with sess.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path + ext, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)