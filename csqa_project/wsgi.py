"""
WSGI config for csqa_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

from datetime import time
import time
import os
import questions.clock as clock
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csqa_project.settings')
application = get_wsgi_application()

# while True:
#     time.sleep(5)
#     clock.sched.start()
#clock.start()

