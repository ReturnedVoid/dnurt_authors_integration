# Executive module
import sys
from os import system
import json

from dnurt_integration.scopus import client as sc_client
from dnurt_integration.web_of_science import client as w_client
from dnurt_integration.gooscholar import client as g_client
from dnurt_integration.dnurtdb import database as db

from dnurt_integration.dnurtdb.database import DB_CONFIG_PATH
from dnurt_integration.web_of_science.client import WOS_CONFIG_PATH
from dnurt_integration.scopus.client import SCOPUS_CONFIG_PATH


def update():
    db.init_db()
    w_client.init_wos_config()
    sc_client.init_sc_config()

    system('clear')
    arg = None
    if sys.argv[1]:
        arg = sys.argv[1]

    if arg == '-s':
        update_scopus()
    elif arg == '-g':
        update_gscholar()
    elif arg == '-w':
        update_wos()
    elif arg == '-cb':
        reconfigure_db()
    elif arg == '-cw':
        reconfigure_wos()
    elif arg == '-cs':
        reconfigure_scopus()
    else:
        update_all()

    sc_client.clear_logs()
    w_client.clear_logs()


def update_scopus():
    print('Updating scopus info...')
    sc_client.update_db()
    print('Done.')


def update_all():
    update_scopus()
    update_gscholar()
    update_wos()


def update_gscholar():
    print('Updating gscholar info...')
    g_client.update_db()
    print('Done.')


def update_wos():
    print('Updating wos info...')
    w_client.update_db()
    print('Done.')


def reconfigure_db():
    with open(DB_CONFIG_PATH, "r") as jsonFile:
        data = json.load(jsonFile)

    data['is_initialized'] = False

    with open(DB_CONFIG_PATH, "w") as jsonFile:
        json.dump(data, jsonFile)
    db.init_db()


def reconfigure_wos():
    with open(WOS_CONFIG_PATH, "r") as jsonFile:
        data = json.load(jsonFile)

    data['is_initialized'] = False

    with open(WOS_CONFIG_PATH, "w") as jsonFile:
        json.dump(data, jsonFile)
    w_client.init_wos_config()


def reconfigure_scopus():
    with open(SCOPUS_CONFIG_PATH, "r") as jsonFile:
        data = json.load(jsonFile)

    data['is_initialized'] = False

    with open(SCOPUS_CONFIG_PATH, "w") as jsonFile:
        json.dump(data, jsonFile)
    sc_client.init_sc_config()


if __name__ == '__main__':
    update()
