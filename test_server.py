import sys
import threading
from app import app

def run():
    app.run(port=5050)

thread = threading.Thread(target=run)
thread.daemon = True
thread.start()

import time
import urllib.request
time.sleep(2)
try:
    print(urllib.request.urlopen("http://127.0.0.1:5050/pdf/pdf-editor").getcode())
except Exception as e:
    print(e)
