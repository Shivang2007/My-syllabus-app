from kivymd.app import MDApp
from kivymd.uix.label import MDLabel, MDIcon
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.utils.set_bars_colors import set_bars_colors
from kivymd.toast import toast
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDIconButton,MDFlatButton,MDRaisedButton,MDRectangleFlatIconButton,MDRectangleFlatButton,MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.card import MDCard , MDSeparator
from kivy.properties import StringProperty , DictProperty
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem ,TwoLineListItem
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.utils import asynckivy as ak
from kivy.core.audio import SoundLoader
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.image import Image
from kivy.base import EventLoop


import os 
from os import path
import sys
import time
try:
    from datetime import datetime
except:
    toast('Module import error')
import shutil
import logging
import json
from plyer import sms
from plyer import notification
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu


from database import *


MData = {}
def make_data():
    try:
        if os.path.exists("/storage/emulated/0/Documents/My Syllabus/data.json"):        
            with open('/storage/emulated/0/Documents/My Syllabus/data.json', 'r') as openfile:
                MData = json.load(openfile)
        else:
            with open("/storage/emulated/0/Documents/My Syllabus/data.json","w") as f:
                data = {}
                data = json.dumps(data, indent=4)
                f.write(data)
            with open('/storage/emulated/0/Documents/My Syllabus/data.json', 'r') as openfile:
                MData = json.load(openfile)
        return MData
    except Exception as e:
        toast(f'{e}')
        return {}
        
def make_data_note():
    try:
        if os.path.exists("/storage/emulated/0/Documents/My Syllabus/note_data.json"):        
            with open('/storage/emulated/0/Documents/My Syllabus/note_data.json', 'r') as openfile:
                MData = json.load(openfile)
        else:
            with open("/storage/emulated/0/Documents/My Syllabus/note_data.json","w") as f:
                data = {}
                data = json.dumps(data, indent=4)
                f.write(data)
            with open('/storage/emulated/0/Documents/My Syllabus/note_data.json', 'r') as openfile:
                MData = json.load(openfile)
        return MData
    except Exception as e:
        toast(f'{e}')
        return {}

def write_data(data):
    try:
        with open("/storage/emulated/0/Documents/My Syllabus/data.json","w") as f:
            data = json.dumps(data, indent=4)
            f.write(data)
    except Exception as e:
        toast(f'{e}')

def write_data_note(data):
    try:
        with open("/storage/emulated/0/Documents/My Syllabus/note_data.json","w") as f:
            data = json.dumps(data, indent=4)
            f.write(data)
    except Exception as e:
        toast(f'{e}')

class AboutPage(Screen):
    ww = Window.width
    def enter(self):
        pass
        
    def home(self):
        self.manager.current = 'mainp'