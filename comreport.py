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
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem,TwoLineListItem, ThreeLineListItem
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

from functions import *
        
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

def get_all_file_paths(directory): 
    file_paths = [] 
    for root, directories, files in os.walk(directory): 
        for filename in files: 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
    return file_paths
    
    
class ComReportPage(Screen):
    def enter(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)  
        MData = make_data()
        self.ids.grid.bind(minimum_height=self.ids.grid.setter('height'))
        self.done_chaps = {}
        try:
            self.ids.grid.clear_widgets()
        except:
            pass
        
        self.report_card = MDCard(size_hint_y=None,height="900",orientation="vertical",md_bg_color='#f6eeee')       
        try:
            self.report_card.padding = (50,50)
        except:
            pass
        try:
            self.report_card.spacing = (0,50)
        except:
            pass
            
        gt = 0
        gc = 0
        try:
            for sub in MData:
                gt = gt + MData[sub]["Data"]["total"]
                gc = gc + MData[sub]["Data"]["completed"]
        except Exception as e:
            toast(f"{e}")
            gt = 0
            gc = 0
        
        self.final_report = {
            "total_chapters":str(gt),
            "total_completed":str(gc)
        }
        lftt = int(gt) - int(gc)
        self.lst = {}
        try:
            self.card = MDCard(size_hint_y=None,height="700",orientation='vertical',md_bg_color='#f4dedc')       
            try:
                self.card.padding =  (50,50)
            except:
                pass
            try:
                self.card.spacing = (0,50)
            except:
                pass
            self.card.add_widget(MDLabel(text=f'TOTAL',bold=True,halign='center',font_style='H3',underline=True))
            lft = int(gt) - int(gc)
            self.card.add_widget(MDLabel(text=f"Total Chapters = {gt}",halign='center'))
            self.card.add_widget(MDLabel(text=f"Total Chapters Completed = {gc}",halign='center'))
            self.card.add_widget(MDLabel(text=f"Total Chapters Left = {lft}",halign='center'))
            self.ids.grid.add_widget(self.card)
            self.lst['overall_report.png'] = self.card
            
        except:
            pass
        
        self.ids.grid.add_widget(MDRaisedButton(text='Save Report As Images',size_hint=(0.9,0.2),on_release=self.save_report_as_images))
        self.ids.grid.add_widget(MDRaisedButton(text='Save Report As PDF',size_hint=(0.9,0.2),on_release=self.save_report_as_pdf))
        
        try:
            lst = os.listdir('Report Cards')
            if len(lst) == 0:
                pass
            else:
                for file in lst:
                    os.remove(f'Report Cards/{file}')
            
        except:
            pass
        
        for sub in MData:
            self.ids.grid.add_widget(MDLabel(text='',size_hint_y=None,height='100'))
            self.card = MDCard(size_hint_y=None,height="800",orientation="vertical",md_bg_color='#f6eeee',style='elevated')
            try:
                self.card.padding =  (50,50)
            except:
                pass
            try:
                self.card.spacing = (0,50)
            except:
                pass
            self.card.add_widget(MDLabel(text=f'{sub}',halign='center',font_style='H4',underline=True))
            
            tot = MData[sub]["Data"]["total"]
            self.card.add_widget(MDLabel(text=f"Total Chapters = [b]{tot}[/b]",markup=True))
            com = MData[sub]["Data"]["completed"]
            self.card.add_widget(MDLabel(text=f"Total Chapters Completed = [b]{com}[/b]",markup=True))
            left = tot - com
            self.card.add_widget(MDLabel(text=f"Total Chapters Left = [b]{left}[/b]",markup=True))
            self.ids.grid.add_widget(self.card)
            self.lst[f'{sub}_report.png'] = self.card
            
            for chapter in MData[sub]["Chapters"]:
                card2 = MDCard(size_hint_y=None,height="100",orientation="horizontal")
                card2.add_widget(MDLabel(text=f'{chapter}',halign='center',bold=True))
                if MData[sub]["Chapters"][f'{chapter}'] == True:
                    card2.add_widget(Image(source='tick.jpg'))
                else:
                    card2.add_widget(Image(source='wrong.jpg'))
                self.ids.grid.add_widget(card2)
                self.lst[f'{sub}_{chapter}_report.png'] = card2
                
    
    def save_report_as_images(self , obj):
        for x in self.lst:
            ins = self.lst[x]
            path = os.path.join('/storage/emulated/0/Pictures/My Report Cards', x)
            ins.export_to_png(path)
        toast('Images Saved')
            
    def save_report_as_pdf(self , obj):
        toast('Saving ....')
        imgs = []
        for x in self.lst:
            ins = self.lst[x]
            path = os.path.join('Report Cards', x)
            ins.export_to_png(path)
            imgs.append(path)
        
        try:
            from PIL import Image
        except:
            res = 'Module not imported'                    
        fi = imgs[0]
        image = Image.open(fi)
        im_1 = image.convert('RGB')
        img_lst = []
        n= 0
        for img in imgs:
            n = n + 1
            pa = img
            if n == 1:
                pass
            else:
                if n % 10 == 0:
                    toast(f'Still Making ..... {n} Chapters Added in Report')
                imgn = img
                image = Image.open(imgn)
                img = image.convert('RGB')
                img_lst.append(img)
                os.remove(pa)
            im_1.save(f'/storage/emulated/0/Documents/My Report.pdf', save_all=True, append_images=img_lst)
        
        toast('PDF Report Saved In Documents Folder')
        
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.manager.current = 'mainp'
            return True
            
    def home(self):
        self.manager.current = 'mainp'