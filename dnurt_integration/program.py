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

from multiprocessing import Process
from dnurt_integration.shared import updating_status

import time


def update():
    db.init_db()
    w_client.init_wos_config()
    sc_client.init_sc_config()

    system('clear')
    arg = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        update_all()

    if arg == '-cb':
        reconfigure_db()
    elif arg == '-cw':
        reconfigure_wos()
    elif arg == '-cs':
        reconfigure_scopus()

    sc_client.clear_logs()
    w_client.clear_logs()


def update_all():
    update_scopus_process.start()
    update_wos_process.start()
    update_gscholar_process.start()
    updating_progress_process.start()


def show_updating_progress():
    wos_completed = False
    gscholar_completed = False
    scopus_completed = False
    time.sleep(1)
    while True:
        system('clear')
        print('Updating scopus info...')
        print('\tscopus: updated',
              updating_status[0], '/', updating_status[1], 'authors.')
        if updating_status[0] == updating_status[1]:
            print('\tDone scopus updating.')
            scopus_completed = True
        print('Updating wos info...')
        print('\twos: updated',
              updating_status[2], '/', updating_status[3], 'authors.')
        if updating_status[2] == updating_status[3]:
            print('\tDone wos updating.')
            wos_completed = True
        print('Updating gscholar info...')
        print('\tgscholar: updated',
              updating_status[4], '/', updating_status[5], 'authors.')
        if updating_status[4] == updating_status[5]:
            print('\tDone gscholar updating.')
            gscholar_completed = True
        if scopus_completed == gscholar_completed == wos_completed is True:
            break
        time.sleep(5)


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


update_scopus_process = Process(target=sc_client.update_db)
update_wos_process = Process(target=w_client.update_db)
update_gscholar_process = Process(target=g_client.update_db)
updating_progress_process = Process(target=show_updating_progress)

if __name__ == '__main__':
    update()
