
import os
import site
import sys

site.addsitedir("/usr/local/lib/python3.5/site-packages")

sys.path.append('/usr/src/app/mysite')



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
