from elsapy.elsclient import ElsClient
from elsapy.elsdoc import AbsDoc
from elsapy.elsprofile import ElsAuthor
from elsapy.elssearch import ElsSearch

from dnurtdb import database as db

import json

con_file = open("scopus/config.json")
config = json.load(con_file)
con_file.close()

# -----------constants--------------
API_KEY = config['apikey']
DNURT_SCOPUS_ID = config['dnurt_id']
# ----------------------------------

# get API client using API_KEY
api_client = ElsClient(API_KEY)


class ScopusAuthor:
    def __init__(self, data, _id):
        self.author_data = data
        self.sc_id = _id

    @property
    def fullname(self):
        fname = '{} {}'.format(self.author_data['author-profile']['preferred-name']['surname'],
                              self.author_data['author-profile']['preferred-name']['initials'])

        is_aped = True if "'" in fname else False
        if is_aped:
            spl = fname.split("'")
            k = []
            for i in range(0, len(spl)):
                if i == (len(spl) - 1):
                    k.append(spl[i])
                else:
                    k.append(spl[i])
                    k.append("''")

            return ''.join(k)
        else:
            return fname

    @property
    def sc_id(self):
        return self._sc_id

    @sc_id.setter
    def sc_id(self, val):
        self._sc_id = val

    @property
    def doc_count(self):
        count = self.author_data['coredata']['document-count']
        return count if count else 0

    @property
    def cited_by_count(self):
        cbc = self.author_data['coredata']['cited-by-count']
        return cbc if cbc else 0

    @property
    def citation_count(self):
        cc = self.author_data['coredata']['citation-count']
        return cc if cc else 0

    @property
    def docs(self):
        return fetch_docs_by_author_id(self.sc_id)

    @property
    def citations(self):
        cit = []
        for i in self.docs:
            cited = i['citedby-count']
            cit.append(cited) if cited else cit.append(0)
        for i in range(0, len(cit)):
            cit[i] = int(cit[i])
        return cit

    @property
    def h_index(self):
        return sum(x >= i + 1 for i, x in enumerate(sorted(self.citations, reverse=True)))

    def __str__(self):
        return '{0} {1} {2} {3} {4}' \
            .format(self.fullname, self.sc_id, self.doc_count, self.cited_by_count, self.citation_count)


def get_dnurt_authors():
    """get all DNURT authors"""
    srch = ElsSearch('AF-ID({})'.format(DNURT_SCOPUS_ID), 'author')
    srch.execute(api_client, get_all=True)

    info = []
    for author in srch.results:
        a_info = get_author(author)
        info.append(a_info)
    return info


def get_author(adata):
    """parse search result and return compact info"""
    scopus_author_id = adata['dc:identifier'].split(':')[1]
    return get_author_by_id(scopus_author_id)


def get_author_by_id(_id):
    my_auth = ElsAuthor(
        uri='https://api.elsevier.com/content/author/author_id/{0}'.format(_id))
    if my_auth.read(api_client):
        return ScopusAuthor(my_auth.data, my_auth.int_id)
    else:
        print("Read author failed.")


def get_doc(idd):
    scp_doc = AbsDoc(scp_id='{0}'.format(idd))
    if scp_doc.read(api_client):
        print("scp_doc.title: ", scp_doc.data)
    else:
        print("Read document failed.")


def fetch_docs_by_author_id(id):
    doc_srch = ElsSearch('AU-ID({0})'.format(id), 'scopus')
    doc_srch.execute(api_client, get_all=True)
    return doc_srch.results


def update_bd(ids):
    for id in ids:
        author = get_author_by_id(id)
        db.update(author)

    db.disconnect()


# TODO
# Add search by info from DB
