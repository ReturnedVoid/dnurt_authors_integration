import bs4 as bs
from dnurt_integration.dnurtdb import database as db
import urllib.request


class GscholarAuthor:
    def __init__(self, _id):
        self.gs_id = _id
        self.doc_count = 0
        self.h_index = 0

    @property
    def gs_id(self):
        return self._gs_id

    @gs_id.setter
    def gs_id(self, val):
        self._gs_id = val

    @property
    def doc_count(self):
        return self._doc_count

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
    source = urllib \
        .request.urlopen('https://scholar.google.com.ua/citations?user={}&hl=en'
                         .format(_id)).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    tds = soup.find_all('td')

    author = GscholarAuthor(_id)
    author.h_index = tds[4].string
    #TODO how to get doc_coount ?
    # author.doc_count = '2'
    return author


def update_db():
    ids = db.get_gs_authors_ids()
    for _id in ids:
        if _id:
            author = get_author_by_id(_id)
            db.gscholar_update(author)

    db.disconnect()
