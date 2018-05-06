# Executive module
import sys

from os import system

from dnurt_integration.scopus import client as sc_client
from dnurt_integration.web_of_science import client as w_client
from dnurt_integration.gooscholar import client as g_client


def update():
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
    else:
        update_all()


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
    # g_client.update_db()
    print('Done.')


def update_wos():
    print('Updating wos info...')
    # w_client.update_db()
    print('Done.')


if __name__ == '__main__':
    update()
