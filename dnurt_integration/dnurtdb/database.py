import json
import psycopg2
import os

# open configuration files
db_conf = open(os.path.join(os.path.dirname(__file__), 'dbconfig.json'))
db_config = json.load(db_conf)
db_conf.close()

connect_str = "dbname={0} user={1} password={2}" \
    .format(db_config['dbname'], db_config['user'], db_config['password'])

conn = None

tables = ('authors',)
columns = ('id, fullname')
sc_columns = ('sc_id', 'h_scopus', 'sc_doc_count')
gs_columns = ('gs_id', 'h_gscholar', 'gs_doc_count')
wos_columns = ('wos_id', 'h_wos', 'wos_doc_count')


def connect():
    global conn

    try:
        conn = psycopg2.connect(connect_str)
        return True
    except psycopg2.DatabaseError as e:
        print('Error: db connect()', e)
        return False


def get_cursor():
    return conn.cursor()


def disconnect():
    try:
        conn.close()
    except:
        print('Error: db connection close()')


def get_sc_authors_ids():
    if connect():
        cursor = get_cursor()
        cursor.execute("""select {0} from {1}""".format(
            sc_columns[0], tables[0]))
        ids = []
        for _id in cursor.fetchall():
            ids.append(_id[0])
        return ids


def get_gs_authors_ids():
    if connect():
        cursor = get_cursor()
        cursor.execute("""select {0} from {1}""".format(
            gs_columns[0], tables[0]))
        ids = []
        for _id in cursor.fetchall():
            ids.append(_id[0])
        return ids


def get_wos_authors_ids():
    # if connect():
    #     cursor = get_cursor()
    #     cursor.execute("""select {0} from {1}""".format(
    #         wos_columns[0], tables[0]))
    #     ids = []
    #     for _id in cursor.fetchall():
    #         ids.append(_id[0])
    #     return ids
    return ['A-7364-2016']


def scopus_update(author):
    if connect():
        cursor = get_cursor()
        cursor.execute("""update {0} set {1}='{2}', {3}='{4}' where {5}='{6}'"""
                       .format(tables[0],
                               sc_columns[1], author.h_index,
                               sc_columns[2], author.doc_count,
                               sc_columns[0], author.sc_id))
    conn.commit()


def gscholar_update(author):
    if connect():
        cursor = get_cursor()
        cursor.execute("""update {0} set {1}='{2}', {3}='{4}' where {5}='{6}'"""
                       .format(tables[0],
                               gs_columns[1], author.h_index,
                               gs_columns[2], author.doc_count,
                               gs_columns[0], author.gs_id))
    conn.commit()


def wos_update(author):
    if connect():
        cursor = get_cursor()
        cursor.execute("""update {0} set {1}='{2}', {3}='{4}' where {5}='{6}'"""
                       .format(tables[0],
                               wos_columns[1], author.h_index,
                               wos_columns[2], author.doc_count,
                               wos_columns[0], author.wos_id))
    conn.commit()
