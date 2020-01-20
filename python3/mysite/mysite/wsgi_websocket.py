import os
import sys
sys.path.append('/usr/src/app/mysite')
import gevent.socket
import redis.connection
redis.connection.socket = gevent.socket
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
os.environ.update(DJANGO_SETTINGS_MODULE='mysite.settings')
from ws4redis.uwsgi_runserver import uWSGIWebsocketServer
application = uWSGIWebsocketServer()