import json
import psycopg2

# open configuration files
db_conf = open("dnurtdb/dbconfig.json")
db_config = json.load(db_conf)
db_conf.close()

connect_str = "dbname={0} user={1} password={2}" \
    .format(db_config['dbname'], db_config['user'], db_config['password'])

conn = None
is_connected = False

tables = ('authors',)
columns = ('id', 'fullname', 'cited_by_count', 'citation_count', 'sc_id', 'hirsha', 'doc_count')


def connect():
    global conn
    global is_connected

    try:
        conn = psycopg2.connect(connect_str)
        is_connected = True
    except psycopg2.DatabaseError as e:
        is_connected = False
        print('Error: db connect()', e)


def get_cursor():
    return conn.cursor()


def disconnect():
    global is_connected
    try:
        conn.close()
        is_connected = False
    except:
        print('Error: db connection close()')


def get_author_ids():
    connect()
    if is_connected:
        cursor = get_cursor()
        cursor.execute("""select {0} from {1}""".format(columns[4], tables[0]))
        ids = []
        for id in cursor.fetchall():
            ids.append(id[0])
        return ids


def update(author):
    connect()
    if is_connected:
        cursor = get_cursor()
        cursor.execute("""update {0} set {1}='{2}', {3}='{4}', {5}='{6}', {7}='{8}', {9}='{10}' where {11}='{12}'"""
                       .format(tables[0], columns[1], author.fullname,
                               columns[2], author.cited_by_count,
                               columns[3], author.citation_count,
                               columns[5], author.h_index,
                               columns[6], author.doc_count,
                               columns[4], author.sc_id))
    conn.commit()
