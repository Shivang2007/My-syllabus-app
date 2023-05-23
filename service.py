from time import sleep
import os
from jnius import autoclass

import logging

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)

try:
    sleep(20)
    from kivymd.toast import toast
    toast('Service Starting.....')
except Exception as e:
    with open("/storage/emulated/0/service.txt",'w') as f:
        f.write(str(e))