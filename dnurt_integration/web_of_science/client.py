from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium.common.exceptions import NoSuchElementException
from dnurtdb import database as db

firefox_binary = FirefoxBinary("/snap/firefox/85/firefox")
browser = webdriver.Firefox(firefox_binary=firefox_binary)


class WOSAuthor:
    def __init__(self, _id):
        self.wos_id = _id
        self.h_index = 0
        self.doc_count = 0

    @property
    def wos_id(self):
        return self._wos_id

    @wos_id.setter
    def sc_id(self, val):
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


def get_author_by_id(_id):
    browser.get('http://www.researcherid.com/rid/{}'.format('A-7364-2016'))
    div = browser.find_element_by_class_name('publistSet')
    links = div.find_elements_by_tag_name('a')
    links[1].click()

    hirsha = 0
    slept = 2

    time.sleep(slept)

    while True and slept <= 60:
        try:
            print('in try, slept = ', slept)
            hirsha = browser.find_element_by_xpath('//*[@id="metrics_hindex"]')
            break
        except NoSuchElementException:
            print('in except, slept = ', slept)
            time.sleep(1)
            slept += 1

    browser.quit()
    author = WOSAuthor(_id)
    author.h_index = hirsha
    return author


def update_db():
    ids = db.get_sc_authors_ids()
    for id in ids:
        author = get_author_by_id(id)
        db.scopus_update(author)

    db.disconnect()
