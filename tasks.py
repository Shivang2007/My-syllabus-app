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


MData = {}
def make_data():
    try:
        if os.path.exists("/storage/emulated/0/My Syllabus/data.json"):        
            with open('/storage/emulated/0/My Syllabus/data.json', 'r') as openfile:
                MData = json.load(openfile)
        else:
            with open("/storage/emulated/0/My Syllabus/data.json","w") as f:
                data = {}
                data = json.dumps(data, indent=4)
                f.write(data)
            with open('/storage/emulated/0/My Syllabus/data.json', 'r') as openfile:
                MData = json.load(openfile)
        return MData
    except Exception as e:
        toast(f'{e}')
        return {}

def write_data(data):
    try:
        with open("/storage/emulated/0/My Syllabus/data.json","w") as f:
            data = json.dumps(data, indent=4)
            f.write(data)
    except Exception as e:
        toast(f'{e}')


class NewChapterBox(BoxLayout):
    pass
    
    
class TasksPage(Screen):
    ww = Window.width
    Window.softinput_mode = "below_target"
    def enter(self):
        try:
            try:
                if os.path.exists(f'Setting Data/Tasks/'):
                    pass
                else:
                    os.makedirs(f'Setting Data/Tasks/')
                    toast('File Made')
            except Exception as e:
                toast(f'{e}')
                
            if os.path.exists('Setting Data/name_radius.txt'):
                rl = [25, 25, 25, 25]
            else:
                rl = [0, 0, 0, 0]
            lst = os.listdir(f'Setting Data/Tasks/')
            try:
                self.ids.flist.clear_widgets()
            except:
                pass
            for task in lst:
                task = task.split(".")[0]
                task = task.replace('&','/')
                task = task.replace('$','\\')
                task = task.replace('@','"')
                task = task.replace(']',"'")
                self.ids.flist.add_widget(OneLineListItem(text=f"{task}",radius=rl,on_release=self.open)) 
        except Exception as e:
            toast(f'{e}')
    
    def open(self, inst):
        tin = inst
        bottom_sheet_menu = MDListBottomSheet()
        fname = inst.text
        bottom_sheet_menu.add_item(f"Remove Task",lambda x ,y = tin: self.rm_task(str(y),fname))
        bottom_sheet_menu.open()
        
    def rm_task(self, tin, task):
        task = task.replace('/','&')
        task = task.replace('\\','$')
        task = task.replace('"','@')
        task = task.replace("'",']')
        os.remove(f'Setting Data/Tasks/{task}.txt')
        self.enter()
        
    def add_task(self):
        task = self.ids.taskt.text
        task = task.replace('/','&')
        task = task.replace('\\','$')
        task = task.replace('"','@')
        task = task.replace("'",']')
        try:
            if os.path.exists(f'Setting Data/Tasks/{task}.txt'):
                toast('This Task is already there')
            else:
                with open(f'Setting Data/Tasks/{task}.txt','w') as f:
                    f.write('Task')
                toast('Task Added')
        except Exception as e:
            toast(f'{e} Try changing the task text')
        self.enter()
        self.ids.taskt.text = ''
    
    def home(self):
        self.manager.current = 'mainp'


class SubjectPage(Screen):    
    data = DictProperty()    
    def enter(self):
        global MData
        MData = make_data()        
        self.makepage()
        
    def makepage(self):
        with open('subject_open.txt','r') as f:
            sub = f.read()            
        self.ids.tbar.title = sub
        self.ids.grid.bind(minimum_height=self.ids.grid.setter('height'))
        self.data = {
            'New Chapter': ['book-plus',"on_release" ,lambda x: self.newchap(sub)],
            }
            
        self.done_chaps = {}
        try:
            self.ids.grid.clear_widgets()
        except:
            pass
        self.subject_clk = {}
        
        card = MDCard(size_hint_y=None,height="500",orientation="vertical",md_bg_color='#f6eeee')
        card.add_widget(MDLabel(text=f'{sub}',halign='center',font_style='H3',underline=True))
        tot = MData[sub]["Data"]["total"]
        card.add_widget(MDLabel(text=f"Total Chapters => {tot}",halign='center'))
        com = MData[sub]["Data"]["completed"]
        card.add_widget(MDLabel(text=f"Total Chapters Completed => {com}",halign='center'))
        left = tot - com
        card.add_widget(MDLabel(text=f"Total Chapters Left => {left}",halign='center'))        
        self.ids.grid.add_widget(card)         
        for chapter in MData[sub]["Chapters"]:
            card2 = MDCard(size_hint_y=None,height="100",orientation="horizontal",on_release=self.chap_complete)
            card2.add_widget(MDLabel(text=f'{chapter}',halign='center',bold=True))
            if MData[sub]["Chapters"][f'{chapter}'] == True:
                card2.add_widget(MDCheckbox(active=True))
            else:
                card2.add_widget(MDCheckbox(active=False))     
            self.ids.grid.add_widget(card2)
            print(card2)
            self.subject_clk[str(card2)] = f'{sub}$&${chapter}'
        for x in self.subject_clk:
            print(x)
            
        self.ids.grid.add_widget(MDLabel(text=f'You have reached the end',size_hint_y=None,height="500",halign='center',underline=True,italic=True,bold=True))


############## Chapter update ###############
    def canchapup(self, obj):
        self.chap_update_dia.dismiss()
        
    def chap_complete(self, inst):
        line = self.subject_clk[str(inst)]
        sub = line.split('$&$')[0]
        chap = line.split('$&$')[-1]        
        self.chap_update_dia = MDDialog(
        title="Chapter Update",
        text=f'Do you want to update the {chap} chapter',
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.canchapup),
            MDRaisedButton(text="Remove",md_bg_color='red',on_release= lambda *args: self.remchap(sub,chap ,*args)),
            MDRaisedButton(text="UPDATE",on_release= lambda *args: self.chapter_update(sub,chap ,*args))])
        self.chap_update_dia.open()
    
    def chapter_update(self, sub, chapter, inst):
        if MData[sub]["Chapters"][f'{chapter}'] == True:
            MData[sub]["Chapters"][f'{chapter}'] = False
            MData[sub]["Data"]["completed"] = int(MData[sub]["Data"]["completed"]) - 1
        else:
            MData[sub]["Chapters"][f'{chapter}'] = True
            MData[sub]["Data"]["completed"] = int(MData[sub]["Data"]["completed"]) + 1
            Snackbar(text=f'Congratulations a chapter completed',md_bg_color='blue').open()
            toast('One step ahead towards your goal')
        write_data(MData)
        self.chap_update_dia.dismiss()
        self.enter()
        

############## New Chapter ###############
    def newchap(self, sub):
        ccls=NewChapterBox()
        self.chap_dia = MDDialog(
        title="New Chapter",
        type='custom',
        content_cls=ccls,
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.canchap),
            MDRaisedButton(text="Create",on_release= lambda *args: self.add_chapter(ccls,sub ,*args))])
        self.chap_dia.open()
    
    def add_chapter(self, content_cls , sub , inst):
        textfield = content_cls.ids.cname
        chapter = textfield._get_text()
        if chapter in MData[f"{sub}"]["Chapters"]:
            toast("Chapter already exists")
        else:
            MData[f"{sub}"]["Chapters"].update({f"{chapter}":False})
            MData[sub]["Data"]["total"] = int(MData[sub]["Data"]["total"]) + 1
            try:
                write_data(MData)
            except Exception as e:
                toast(f'{e}')        
            Snackbar(text=f"Chapter {chapter} created in {sub}").open()
            self.chap_dia.dismiss()
            self.enter()
            
    def canchap(self, inst):
        self.chap_dia.dismiss()   


############## Remove Chapter ###############
    def remchap(self, sub, chap, inst):    
        self.chap_update_dia.dismiss()
        self.rem_chap = MDDialog(
        title="Remove Chapter",
        text=f"Do you want to remove the chapter named {chap}",
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.canremchap),
            MDRaisedButton(text="Remove",md_bg_color='red',on_release= lambda *args: self.remove_chapter_final(sub,chap ,*args))
            ])
        self.rem_chap.open()
    
    def remove_chapter_final(self,sub ,chapter, obj):
        if not chapter in MData[f"{sub}"]["Chapters"]:
            toast("Chapter does not exists")
        else:
            comp = MData[f"{sub}"]["Chapters"][f"{chapter}"]        
            MData[f"{sub}"]["Chapters"].pop(f"{chapter}")
            MData[sub]["Data"]["total"] = int(MData[sub]["Data"]["total"]) - 1
            if comp == True:
                MData[sub]["Data"]["completed"] = int(MData[sub]["Data"]["completed"]) - 1
            else:
                pass
            write_data(MData)
            self.rem_chap.dismiss()
            Snackbar(text=f"Chapter named {chapter} Removed",md_bg_color="red").open()
            self.enter()
        
    def remove_chapter(self, content_cls , sub , inst):
        textfield = content_cls.ids.cname
        chapter = textfield._get_text()
        if not chapter in MData[f"{sub}"]["Chapters"]:
            toast("Chapter does not exists")
        else:
            comp = MData[f"{sub}"]["Chapters"][f"{chapter}"]        
            MData[f"{sub}"]["Chapters"].pop(f"{chapter}")
            MData[sub]["Data"]["total"] = int(MData[sub]["Data"]["total"]) - 1
            if comp == True:
                MData[sub]["Data"]["completed"] = int(MData[sub]["Data"]["completed"]) - 1
            else:
                pass
            write_data(MData)
            Snackbar(text=f"Chapter {chapter} Removed in {sub}").open()
            self.rem_chap.dismiss()
            
    def canremchap(self, inst):
        self.rem_chap.dismiss()
        
    def home(self):
        self.manager.current = 'mainp'