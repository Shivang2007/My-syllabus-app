from time import sleep
import os
from jnius import autoclass

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)

try:
    sleep(20)
    from kivymd.toast import toast
    toast('Service Starting.....')
except:
    pass