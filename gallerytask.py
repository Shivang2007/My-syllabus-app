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

class GalleryPage(Screen):
    def enter(self):
        self.imgno = 1
        try:
            self.mkimg()
        except:
            toast('Oops !! An Error Occured')
    
    def mkimg(self):
        lst = os.listdir("/storage/emulated/0/DCIM/JEE Prep")
        no = 0
        for file in lst:
            no = no + 1
            if self.imgno == no:
                self.ids.limg.source = f"/storage/emulated/0/DCIM/JEE Prep/{file}"
                self.current_url = f"/storage/emulated/0/DCIM/JEE Prep/{file}"
                break
                
    def previous(self):
        if self.imgno == 1:
            toast('First Image')
        else:
            self.imgno = self.imgno - 1
        self.mkimg()
    
    def next(self):
        lst = os.listdir("/storage/emulated/0/DCIM/JEE Prep")
        max = len(lst)
        if self.imgno == max:
            self.imgno = 1
        else:
            self.imgno = self.imgno + 1
        self.mkimg()
    
    def delete(self):
        if 1==1:
            self.tar_dia = MDDialog(
            title="Delete Image ?",
            text='Do you really want to delete the image ?',
            width=Window.width,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cantar),
                MDRaisedButton(text="Delete",md_bg_color='red',on_release=self.delete_final)])             
        self.tar_dia.open()
    
    def cantar(self, inst):
        self.tar_dia.dismiss()
        
    def delete_final(self, inst):
        os.remove(self.current_url)
        toast('Image Deleted')
        self.next()
        self.tar_dia.dismiss()
    
    def wall(self):
        from kvdroid.tools import set_wallpaper
        set_wallpaper(self.current_url)
        toast('Wallpaper Set') 
        
    def camera(self):
        self.manager.current = 'camp'
        
    def home(self):
        self.manager.current = 'mainp'

class CameraWin(Screen):
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        try:
            if not os.path.exists("/storage/emulated/0/DCIM/JEE Prep"):
                os.mkdir("/storage/emulated/0/DCIM/JEE Prep")
                
            camera.export_to_png(f"/storage/emulated/0/DCIM/JEE Prep/Jee_Prep_Image_{timestr}.png")
            toast('Image Captured')
        except:
            ex("Unable to save captured images")
        
        
    def home(self):
        self.manager.current = 'galleryp'