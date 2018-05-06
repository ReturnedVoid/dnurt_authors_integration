from wos import WosClient
import wos.utils

with WosClient() as client:
    print(wos.utils.query(client, 'AU=Knuth Donald'))
