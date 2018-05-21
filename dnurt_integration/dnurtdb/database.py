import json
import psycopg2
import os
from enum import Enum


DB_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'dbconfig.json')


class Column(Enum):
    """Enum for table columns"""

    FULLNAME = 'fullname'

    SCOPUS_ID = 'sc_id'
    GSCHOLAR_ID = 'gs_id'
    WOS_ID = 'wos_id'

    HIRSHA_WOS = 'h_wos'
    HIRSHA_SCOPUS = 'h_scopus'
    HIRSHA_GSCHOLAR = 'h_gscholar'

    SCOPUS_DOC_COUNT = 'sc_doc_count'
    GSCHOLAR_DOC_COUNT = 'gs_doc_count'
    WOS_DOC_COUNT = 'wos_doc_count'

    def __str__(self):
        return self.value


class Table(Enum):
    AUTHORS = 'library_science_tab_author'

    def __str__(self):
        return self.value


def get_connect_str():
    with open(DB_CONFIG_PATH, "r") as jsonFile:
        data = json.load(jsonFile)

    return "dbname={0} user={1} password={2}" \
        .format(data['dbname'], data['user'], data['password'])


conn = None


def init_db():
    with open(DB_CONFIG_PATH, "r") as jsonFile:
        data = json.load(jsonFile)

    is_initialized = data['is_initialized']
    if not is_initialized:
        print('You must input db config...')
        dbname = input('Database name: ')
        user = input('User name: ')
        password = input('Db password: ')

        data['dbname'] = dbname
        data['user'] = user
        data['password'] = password
        data['is_initialized'] = True

    with open(DB_CONFIG_PATH, "w") as jsonFile:
        json.dump(data, jsonFile)


def connect():
    global conn

    try:
        conn = psycopg2.connect(get_connect_str())
        return True
    except psycopg2.DatabaseError as e:
        print('Error: db connect()', e)
        return False


def get_cursor():
    return conn.cursor()


def disconnect():
    try:
        conn.close()
    except Exception:
        print('Error: db connection close()')


def get_sc_authors_ids():
    if connect():
        cursor = get_cursor()
        cursor.execute("""select {0} from {1}""".format(
            Column.SCOPUS_ID, Table.AUTHORS))
        return [id[0] for id in cursor.fetchall() if id[0]]


def get_gs_authors_ids():
    if connect():
        cursor = get_cursor()
        cursor.execute("""select {0} from {1}""".format(
            Column.GSCHOLAR_ID, Table.AUTHORS))
        return [id[0] for id in cursor.fetchall() if id[0]]


def get_wos_authors_ids():
    if connect():
        cursor = get_cursor()
        cursor.execute("""select {0} from {1}""".format(
            Column.WOS_ID, Table.AUTHORS))
    return [id[0] for id in cursor.fetchall() if id[0]]


def scopus_update(author):
    if connect():
        cursor = get_cursor()
        cursor.execute("""update {0} set {1}='{2}',
                                        {3}='{4}' where {5}='{6}'"""
                       .format(Table.AUTHORS,
                               Column.HIRSHA_SCOPUS, author.h_index,
                               Column.SCOPUS_DOC_COUNT, author.doc_count,
                               Column.SCOPUS_ID, author.sc_id))
    conn.commit()


def gscholar_update(author):
    if connect():
        cursor = get_cursor()
        cursor.execute("""update {0} set {1}='{2}',
                                        {3}='{4}' where {5}='{6}'"""
                       .format(Table.AUTHORS,
                               Column.HIRSHA_GSCHOLAR, author.h_index,
                               Column.GSCHOLAR_DOC_COUNT, author.doc_count,
                               Column.GSCHOLAR_ID, author.gs_id))
    conn.commit()


def wos_update(author):
    if connect():
        cursor = get_cursor()
        cursor.execute("""update {0} set {1}='{2}',
                                {3}='{4}' where {5}='{6}'"""
                       .format(Table.AUTHORS,
                               Column.HIRSHA_WOS, author.h_index,
                               Column.WOS_DOC_COUNT, author.doc_count,
                               Column.WOS_ID, author.wos_id))
    conn.commit()
