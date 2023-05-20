from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
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
from kivymd.uix.list import OneLineAvatarIconListItem, TwoLineListItem
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.utils import asynckivy as ak
from kivy.core.audio import SoundLoader
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.selectioncontrol import MDCheckbox

from database import *

try:
    from android.permissions import request_permissions, Permission, check_permission
except Exception as e:
    toast('Error no 1 occured')
    
try:
    request_permissions([Permission.INTERNET,Permission.CAMERA,Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE,Permission.SET_WALLPAPER])
except Exception as Argument:
    toast('Error no 2 occured')
    
import os 
import sys
import json
try:
    from datetime import datetime
    import time
    from plyer import notification
    from plyer import sms
    from plyer import battery
except:
    toast('Module import error')
from os.path import join, dirname

files = ['/storage/emulated/0/Documents/My Syllabus/','text_files','json_files']

for file in files:
    try:
        if os.path.exists(f'{file}'):
            pass
        else:
            os.makedirs(f'{file}')
    except Exception as e:
        toast(f'{e}')


from home import Main

from tasks import TasksPage, SubjectPage, ReportPage, CameraWin, AboutPage, NotePage, GalleryPage
from login import LoginPage, SignupPage

from chat import ChatPage,ExamPage



class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        
        try:
            with open('/storage/emulated/0/Documents/My Syllabus/theme.txt','r') as f:
                wcolor = f.read()
                self.theme_cls.primary_palette = str(wcolor)
        except:
            self.theme_cls.primary_palette = f"Blue"
        set_bars_colors(self.theme_cls.primary_color, self.theme_cls.primary_color,"Light")
        self.theme_cls.theme_style = "Light"
        
        sm=ScreenManager()
        sc_lst = [
        Main(name='mainp'),
        SubjectPage(name='subp'),
        ReportPage(name='reportp'),
        TasksPage(name='tasksp'),
        AboutPage(name='aboutp'),
        LoginPage(name='loginp'),
        SignupPage(name='signupp'),
        ChatPage(name='chatp'),
        ExamPage(name='examp'),
        NotePage(name='notep'),
        GalleryPage(name='galleryp'),
        CameraWin(name='camp')
        ]

        try:
            for sc in sc_lst:
                sm.add_widget(sc)
        except Exception as e:
            toast('screen error')
            toast(f'{e}')            
        return sm
        
    def change_theme(self, text):
        with open('/storage/emulated/0/Documents/My Syllabus/theme.txt','w') as f:
            f.write(f'{text}')
        try:
            self.theme_cls.primary_palette = str(text)
            set_bars_colors(self.theme_cls.primary_color, self.theme_cls.primary_color,"Light")
        except:
            toast('Theme Color Not Available')

MainApp().run()