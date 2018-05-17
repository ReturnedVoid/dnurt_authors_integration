from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium.common.exceptions import NoSuchElementException
from dnurt_integration.dnurtdb import database as db
import json
import os

from pathlib import Path
from dnurt_integration.shared import updating_status

WOS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'wos_config.json')
MAX_WAIT_TIME = 60
HIRSHA_XPATH = '//*[@id="metrics_hindex"]'
DOC_COUNT_XPATH = '//*[@id="metrics_totalArticleCount"]'

browser = None


class WOSAuthor:
    def __init__(self, _id):
        self.wos_id = _id
        self.h_index = 0
        self.doc_count = 0

    @property
    def wos_id(self):
        return self._wos_id

    @wos_id.setter
    def wos_id(self, val):
        self._wos_id = val

    @property
    def doc_count(self):
        return self._doc_count if self._doc_count else 0

    @doc_count.setter
    def doc_count(self, val):
        self._doc_count = val

    @property
    def h_index(self):
        return self._h_index

    @h_index.setter
    def h_index(self, val):
        self._h_index = val


def get_browser():
    web_driver_path = os.path.join(
        os.path.dirname(__file__), '..', 'geckodriver')

    with open(WOS_CONFIG_PATH, "r") as jsonFile:
        data = json.load(jsonFile)
    firefox_bin_path = data['firefox_bin']

    firefox_binary = FirefoxBinary(firefox_bin_path)
    return webdriver.Firefox(
        firefox_binary=firefox_binary, executable_path=web_driver_path)


def get_author_by_id(_id):
    global browser

    if browser is None:
        browser = get_browser()
    browser.get('http://www.researcherid.com/rid/{}'.format(_id))
    div = browser.find_element_by_class_name('publistSet')
    links = div.find_elements_by_tag_name('a')
    links[1].click()

    hirsha = 0
    doc_count = 0
    slept = 2

    time.sleep(slept)

    while True and slept <= MAX_WAIT_TIME:
        try:
            hirsha = browser.find_element_by_xpath(HIRSHA_XPATH).text
            doc_count = browser.find_element_by_xpath(DOC_COUNT_XPATH).text
            break
        except NoSuchElementException:
            time.sleep(1)
            slept += 1

    author = WOSAuthor(_id)
    author.h_index = hirsha if hirsha else 0
    author.doc_count = doc_count if doc_count else 0
    return author


def update_db():
    ids = db.get_wos_authors_ids()
    lend = len(ids)
    updating_status[3] = lend
    current = 1
    for id in ids:
        author = get_author_by_id(id)
        db.wos_update(author)
        updating_status[2] = current
        current += 1
    browser.quit()
    db.disconnect()


def init_wos_config():
    with open(WOS_CONFIG_PATH, "r") as jsonFile:
        data = json.load(jsonFile)

    is_initialized = data['is_initialized']
    if not is_initialized:
        print('You must input firefox bin path...')
        firefox_bin = input(
            'Firefox bin path: (normally it`s /usr/bin/firefox): ')

        data['firefox_bin'] = firefox_bin
        data['is_initialized'] = True

    with open(WOS_CONFIG_PATH, "w") as jsonFile:
        json.dump(data, jsonFile)


def clear_logs():
    path = str(Path.home())
    logs_path = '{0}/geckodriver.log'.format(path)
    try:
        os.remove(logs_path)
    except Exception as e:
        pass
