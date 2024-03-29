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


##############################
# KIVY MAIN APP CLASSES
##############################
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang import Builder
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.core.window import Window
from kivymd.utils import asynckivy as ak
from kivymd.toast import toast
from kivymd.uix.snackbar import Snackbar

##############################
# KIVYMD Layouts
##############################
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import GridLayout

##############################
# KIVYMD Widgets
##############################
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDIconButton,MDFlatButton,MDRaisedButton,MDRectangleFlatIconButton,MDRectangleFlatButton,MDFloatingActionButton
from kivymd.uix.card import MDCard , MDSeparator
from kivy.properties import StringProperty , DictProperty
from kivymd.uix.list import OneLineListItem, TwoLineListItem , ThreeLineListItem
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivy.core.audio import SoundLoader
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.image import Image

##############################
# MODULES
##############################
import os
import random
import json
from functions import *
import requests
import time 
import shutil



class CreatePdfBox(BoxLayout):
    pass
    
class SplitPdfBox(BoxLayout):
    pass

class MergePdfsBox(BoxLayout):
    pass

class PasswordPdfBox(BoxLayout):
    pass
    
class TextToPdfBox(BoxLayout):
    pass    
        
class PdfPage(Screen):
    def enter(self):
        try:
            self.manager_open = False
            self.file_manager = MDFileManager(
                preview=True,exit_manager=self.exit_manager, select_path=self.select_path
            )
        except:
            toast('Error no 3')
        try:
            self.manager_open_2 = False
            self.file_manager_2 = MDFileManager(
                preview=False,exit_manager=self.exit_manager_2, select_path=self.select_path_2
            )
        except:
            toast('Error no 3')
            
    
    def mysnack(self, text):
        snackbar = Snackbar(text=text,snackbar_x="0dp",snackbar_y="10dp")
        snackbar.buttons = [
        MDFlatButton(text='OK',text_color=(1, 1, 1, 1),on_release=snackbar.dismiss)]
        snackbar.open()
        
    def mkpdf(self):
        ccls=CreatePdfBox()
        if 1==1:
            self.tar_dia = MDDialog(
            title="Create PDF",
            type='custom',
            content_cls=ccls,
            width=Window.width-100,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cantar),
                MDRaisedButton(text="Create",on_release= lambda *args: self.make_pdf(ccls, *args))])             
        self.tar_dia.open()
    
    def cantar(self, obj):
        self.tar_dia.dismiss()
    
    def mrgpdf(self):
        ccls=MergePdfsBox()
        if 1==1:
            self.tar_dia = MDDialog(
            title="Merge PDFs",
            type='custom',
            content_cls=ccls,
            width=Window.width,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cantar),
                MDRaisedButton(text="Merge",on_release= lambda *args: self.merge_files(ccls, *args))])             
        self.tar_dia.open()
        
    def merge_files(self, content_cls,obj):
        textfield = content_cls.ids.tar
        tar = textfield._get_text()
        self.file_name = tar
        self.type_cm = 'mrg_pdf'
        self.file_manager_2.show('/storage/emulated/0/')
        self.manager_open_2 = True

    def make_pdf(self, content_cls,obj):
        textfield = content_cls.ids.fname
        fname = textfield._get_text()
        self.pdf_name = str(fname)       
        self.type_cm = 'create_pdf'
        self.file_manager.show('/storage/emulated/0/')
        self.manager_open = True
    
    def splitpdf(self):
        ccls=SplitPdfBox()
        if 1==1:
            self.tar_dia = MDDialog(
            title="Split PDF",
            type='custom',
            content_cls=ccls,
            width=Window.width-100,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cantar),
                MDRaisedButton(text="Split",on_release= lambda *args: self.split_pdf_final(ccls, *args))])             
        self.tar_dia.open()
    
    def enc(self):
        ccls=PasswordPdfBox()
        if 1==1:
            self.tar_dia = MDDialog(
            title="Add Password To PDF",
            type='custom',
            content_cls=ccls,
            width=Window.width-100,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cantar),
                MDRaisedButton(text="Set Password",on_release= lambda *args: self.add_passw(ccls, *args))])             
        self.tar_dia.open()
    
    def add_passw(self, content_cls,obj):
        textfield = content_cls.ids.fname
        self.password = textfield._get_text()
        textfield = content_cls.ids.file
        self.file = textfield._get_text()
        self.type_cm = 'password_pdf'
        self.file_manager_2.show('/storage/emulated/0/')
        self.manager_open_2 = True
        
    def split_pdf_final(self, content_cls,obj):
        textfield = content_cls.ids.fname
        fname = textfield._get_text()
        textfield = content_cls.ids.fn
        self.fn = textfield._get_text()
        textfield = content_cls.ids.tn
        self.tn = textfield._get_text()
        self.pdf_name = str(fname)
        self.type_cm = 'split_pdf'
        self.file_manager_2.show('/storage/emulated/0/')
        self.manager_open_2 = True
        
    def textpdf(self):
        ccls=TextToPdfBox()
        if 1==1:
            self.tar_dia = MDDialog(
            title="Text To PDF",
            type='custom',
            content_cls=ccls,
            width=Window.width,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cantar),
                MDRaisedButton(text="Choose File",md_bg_color="#ff4d5b",on_release= lambda *args: self.text_file_pdf(ccls, *args)),
                MDRaisedButton(text="Create",on_release= lambda *args: self.text_pdf(ccls, *args))])             
        self.tar_dia.open()
    
    def text_file_pdf(self, content_cls,obj):
        textfield = content_cls.ids.fname
        fname = textfield._get_text()
        if len(fname) == 0:
            fname = 'New.pdf'
        self.pdf_name = str(fname)
        self.type_cm = 'text_pdf'
        self.file_manager_2.show('/storage/emulated/0/')
        self.manager_open_2 = True
   
    def text_pdf(self, content_cls,obj):
        textfield = content_cls.ids.fname
        fname = textfield._get_text()
        textfield = content_cls.ids.ttext
        text = textfield._get_text()
        if len(fname) == 0:
            fname = 'New.pdf'
        try:
            text_to_pdf(text, os.path.join('/storage/emulated/0/',fname))
            self.mysnack('PDF Made and saved')
        except:
            toast('Oops an error occured')
        
    def select_path(self, path: str):
        try:
            if os.path.isdir(path):
                if self.type_cm == 'create_pdf':
                    if len(os.listdir(path)) > 101:
                        toast('Folder Size Is too large')
                    else:
                        self.exit_manager()
                        toast('Making PDF')
                        crpdf(path,self.pdf_name)
                        self.mysnack('File saved in your internal storage')                          
            else:
                toast('Choose a folder not file')
        except Exception as e:
            toast(f'{e}')
    
    def select_path_2(self, path: str):
        try:
            if not os.path.isdir(path):
                if self.type_cm == 'split_pdf':
                    toast('Making New PDF .....')
                    res = split_pdf(path, int(self.fn), int(self.tn) ,'/storage/emulated/0/'+self.pdf_name)
                    if res == 'Done':
                        self.mysnack('File Splitted')
                        self.exit_manager_2('Hello')
                    else:
                        toast('Oops!! an error occured')
                        
                elif self.type_cm == 'password_pdf':
                    res = encryp(path, self.password , os.path.join('/storage/emulated/0/',self.file))
                    if res == True:
                        self.mysnack('Password Added To PDF File')
                        self.exit_manager_2('Hello')
                    else:
                        print(res)
                        toast('Opps an error occured')
                    
                elif self.type_cm == 'text_pdf':
                    with open(path, 'r') as f:
                        text = f.read()
                    try:
                        text_to_pdf(text, os.path.join('/storage/emulated/0/',self.pdf_name))
                        self.mysnack('PDF File Made and saved')
                    except:
                        toast('Oops an Error Occured')
                    
                elif self.type_cm == 'mrg_pdf':
                    toast('Choose Main File')
                    self.first_path = path
                    self.exit_manager_2('Hello')
                    tar = self.file_name
                    lst = [path]
                    for x in tar.split(','):
                        lst.append(x)
                    res = merge_all_files(lst, path)
                    if res:                        
                        self.mysnack('Files Merged Successfully')
                else:
                    toast(f'{self.type_cm}')             
            else:
                toast('Choose a file not folder')
        except Exception as e:
            toast(f'{e}')
        
    def exit_manager(self, *args):
        try:
            self.manager_open = False
            self.file_manager.close()
        except:
            toast('Error no 4 occured')
    
    def exit_manager_2(self, *args):
        try:
            self.manager_open_2 = False
            self.file_manager_2.close()
        except:
            toast('Error no 4 occured')
    
    def home(self):
        self.manager.current = 'mainp'
        
class AboutPage(Screen):
    ww = Window.width
    def enter(self):
        pass
        
    def home(self):
        self.manager.current = 'mainp'