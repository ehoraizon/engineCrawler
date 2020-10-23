from .settings import Settings

import random

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def prepareTor():

    if not Settings['TOR']:
        profile = FirefoxProfile()
    else:
        profile = (
            FirefoxProfile(Settings['PROFILE_PATH']) if Settings['PROFILE_PATH']
            else FirefoxProfile()
        )
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9050)
        profile.set_preference('network.proxy.socks_remote_dns', False)

    random.shuffle(Settings['USER_AGENTS'])
    profile.set_preference("general.useragent.override", Settings['USER_AGENTS'][0])
    profile.set_preference("intl.accept_languages", "en-US")
    profile.update_preferences()

    driver = webdriver.Firefox(firefox_profile = profile,
    executable_path=Settings['GECKO_DRIVER'])

    driver.get("http://check.torproject.org")
    driver.implicitly_wait(10)
    return driver

def scrollToBtt(driver):
    driver.execute_script("window.scrollTo(0, 999999999)")#document.body.offsetHeight)")