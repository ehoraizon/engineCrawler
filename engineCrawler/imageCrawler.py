import threading
import os
import json
import random
import secrets

from time import sleep
from base64 import decodebytes

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.keys import Keys

from engineCrawler.requestsTor import getSession, getFile
from engineCrawler.selenTor import prepareTor, scrollToBtt
from engineCrawler.util import slices, DuplInFolder, HASHING_METHODS

ENGINES = {
    'duckduckgo' : {
        'url' : 'https://duckduckgo.com',
        'input_s' : '#search_form_input_homepage',
        'images_butt_x' : '//a[text()="Images"]',
        'img' : 'div div span img.tile--img__img',
        'autocompl' : '.search__autocomplete div div'
    },
    'google' : {
        'url' : 'https://images.google.com/',
        'input_s' : 'input[type="search"]',
        'img' : 'div a div img',
        'autocompl' : 'ul li div div span'
    },
    'aut' : [' with ', ' in ', ' on ', ' for ']
}

class CrawlerEngine:

    ban_format = ['ico', 'svg', 'data:image/gif;base64']
    base64 = 'data:image/jpeg;base64,'

    current_path = None
    engine = None
    cont = 0
    last_src = None
    last_pst = None
    aut = True
    finish = False ##check this
    keys_file = 'keys.json'
    aut_save = []

    def __init__(self, args):
        self.sess = getSession()
        self.driver = prepareTor()
        self.engine = args.engine
        self.n = args.amount
        self.keys = args.keys
        self.sleep_t = args.sleep_time
        ENGINES['aut'] = args.autocomplt

    def _go_search(self, keys):
        self.driver.get(ENGINES[self.engine]['url'])
        input = self.driver.find_element_by_css_selector(ENGINES[self.engine]['input_s'])
        input.send_keys(keys)
        
        sleep(self.sleep_t + random.random())

        ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

        sleep(self.sleep_t + random.random())

        if self.engine != 'google':
            img_butt = self.driver.find_element_by_xpath(ENGINES[self.engine]['images_butt_x'])
            ActionChains(self.driver).click(img_butt).perform()

        sleep(self.sleep_t + random.random())

        if not os.path.isdir('engines'):
            os.mkdir('engines')
        
        if not os.path.isdir('engines' + os.sep + keys.split()[0]):
            os.mkdir('engines' + os.sep + keys.split()[0])

        self.current_path = 'engines' + os.sep + keys.split()[0]

    def _get_thread(self, name, url, frm='.jpg'):
        if self.base64 in url:
            return threading.Thread(
                target=self._decoded, args=(
                    url.replace(self.base64, ''),
                    self.current_path + os.sep + str(name) + frm
                )
            )

        return threading.Thread(
            target=getFile,
            args=(
                self.current_path + os.sep + str(name),
                self.sess, url, frm)
            )

    def _get_urls(self):
        img = self.driver.find_elements_by_css_selector(ENGINES[self.engine]['img'])
        src = [x.get_property('src') for x in img if x.get_property('src')]
        _src = []
        for x in src:
            appd = True
            for y in self.ban_format:
                if y in x:
                    appd = False
                    break
            if appd:                
                _src.append(x)

        src = _src
        src_len = len(src)
        if self.last_pst:
            src = src[self.last_pst:]
        self.last_pst = src_len
        return src

    def _decoded(self, base, pathfile):
        with open(pathfile, 'wb') as fl:
            fl.write(decodebytes(base.encode("ascii")))

    def get_autoc(self, keys):
        self.driver.get(ENGINES[self.engine]['url'])
        input_field = self.driver.find_element_by_css_selector(ENGINES[self.engine]['input_s'])

        self.aut_list = [keys]
        for x in ENGINES['aut']:
            input_field.send_keys(keys + x)

            sleep(self.sleep_t)

            aut = self.driver.find_elements_by_css_selector(
                ENGINES[self.engine]['autocompl']
            )

            self.aut_list.extend(
                [item.text for item in aut if item.text]
            )

            input_field.clear()

        print('Select by number the queries to ignore:')
        for i, x in enumerate(self.aut_list):
            print(' (',i,') ', x)
        res = input()
        try:
            res = list(map(int, res.split()))
        except ValueError as e:
            print('ValueError : ', e.args[0], '\nProceeding with scraping.')
        else:
            self.aut_list = [
                x 
                for i, x in enumerate(self.aut_list)
                if i not in res
            ]

    def _work(self, keys):

        self._go_search(keys)

        print('Start with {} download {} at {}'.format(
            keys, self.n, self.current_path
        ))

        while self.cont < self.n:

            print('{}%'.format(
                self.cont*100/self.n
            ), end='\r')

            urls = self._get_urls()
            if not len(urls):
                break
            urls = (urls if len(urls) + self.cont < self.n else urls[:self.n - self.cont])
            self.cont += len(urls)

            urls = slices(urls)
            for sli in urls:
                threads = [self._get_thread('_'.join(keys.split()) + '-' + secrets.token_urlsafe(8), x) for x in sli]
                [x.start() for x in threads]
                [x.join() for x in threads]

            scrollToBtt(self.driver)
            sleep(self.sleep_t + random.random())

        self.last_pst = None
        if self.cont >= self.n:
            self.finish = True

        print('End {}%'.format(
            self.cont*100/self.n
        ))

    def _save_keys(self):
        file = self.current_path + os.sep + self.keys_file
        if os.path.isfile(file):
            saved = []
            with open(file, 'r') as fl:
                saved = json.load(fl)
            saved.extend([x for x in self.aut_save if x not in saved])
            with open(file, 'w') as fl:
                json.dump(saved, fl)
        else:
            with open(file, 'w') as fl:
                json.dump(self.aut_save, fl)

    def crawl(self):
        for key in self.keys:
            if self.aut:
                self.get_autoc(key)
                for x in self.aut_list:
                    self.aut_save.append(x)
                    self._work(x)
                    if self.finish:
                        break
            else:
                self._work(key)
            self.cont = 0
            self.finish = False
        if len(self.aut_save):
            self._save_keys()

    def close(self):
        self.driver.delete_all_cookies()
        self.driver.quit()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description = "Engine image crawler")
    parser.add_argument('-k', '--keys', type=str, nargs='+',
                        required=True, help='Keys to crawl.')
    parser.add_argument('-a', '--autocomplt', type=str, 
                    nargs="+", required=False, default=ENGINES['aut'], 
                    help="A word to add after a key for autocomplete.") 
    parser.add_argument('-e', '--engine', type=str, required=False, default='duckduckgo',
                    help="The name of the website to crawl of(google, duckduckgo).") #change
    parser.add_argument('-s', '--similarity', type=int, required=False, default=65,
                    help="The difference between two images hashes. If the amount provided is exceeded the second image will be deleted.")
    parser.add_argument('-hs', '--hashing', type=str, required=False, default=list(HASHING_METHODS.keys())[0],
                    help="Type of hash method to use.\n {}".format(' '.join(
                        HASHING_METHODS.keys()
                    )))
    parser.add_argument('-am', '--amount', type=int, required=False, default=6000,
                    help="Limit the amount of images to crawl")
    parser.add_argument('-sl', '--sleep_time', type=int, required=False, default=2,
                    help="Sleep time for the crawler.")

    args = parser.parse_args()

    crawler = CrawlerEngine(args)
    crawler.crawl()
    crawler.close()

    print('Searching duplicated...')

    crr_dir = os.getcwd()
    paths = [crr_dir + os.sep + 'engines' + os.sep + x for x in args.keys]
    for folder in paths:
        dupl = DuplInFolder(folder, args.hashing, args.similarity)
        dupl.check()

    print('END')