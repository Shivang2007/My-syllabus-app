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

from database import *
from functions import *

class AddQuestionBox(BoxLayout):
    pass
    
    
def hist(file,text):
    if not os.path.exists('Setting Data/pause_all_search.txt'):
        if os.path.exists('Setting Data/pause_search.txt'):
            type_search = False
        else:
            type_search = True
        ct = time.localtime()
        dt = f'{ct[2]}/{ct[1]}/{ct[0]}'
        tt = f'{ct[3]}:{ct[4]}:{ct[5]}'
        dt = f'Date-{dt} Time-{tt}'
        if file == 'Searched' and type_search == False:
            pass
        else:      
            with open(f'Setting Data/History/{text}.txt','w') as f:
                f.write(f'{file}$$&&$${dt}')
    else:
        pass      
        
MData = {}
def write_data_safe(data):
    try:
        with open("safe_data.json","w") as f:
            data = json.dumps(data, indent=4)
            f.write(data)
    except Exception as e:
        toast(f'{e}')

def make_data_recover():
    try:
        if os.path.exists("safe_data.json"):        
            with open('safe_data.json', 'r') as openfile:
                MData = json.load(openfile)
        else:
            MData = {}
        return MData
    except Exception as e:
        MData = {}
        toast('Error number 100')
        return MData
        
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


class NewChapterBox(BoxLayout):
    pass
class SendReportBox(BoxLayout):
    pass
    
    
class TasksPage(Screen):
    ww = Window.width
    Window.softinput_mode = "below_target"
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.manager.current = 'mainp'
            return True
            
    def enter(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)  
        try:
            try:
                self.ids.grid.clear_widgets()
            except:
                pass
            self.task_clk = {}
            if os.path.exists('tasks.json'):
                with open('tasks.json', 'r') as openfile:
                    data = json.load(openfile)
                
                if data == {}:
                    self.ids.grid.add_widget(MDLabel(text='No Task is there add some now',font_style='H3',halign='center',size_hint_y=None,height=300))
                else:
                    for task in data:
                        card2 = MDCard(size_hint_y=None,height="100",orientation="horizontal",on_release=self.task_complete)
                        card2.add_widget(MDLabel(text=f'{task}',halign='center',bold=True))
                        if data[task] == True:
                            card2.add_widget(Image(source='tick.jpg'))
                        else:
                            card2.add_widget(Image(source='wrong.jpg'))
                        self.ids.grid.add_widget(card2)
                        self.task_clk[str(card2)] = f'{task}'
            else:
                self.ids.grid.add_widget(MDLabel(text='No Task Is There Add Some Now',font_style='H3',halign='center',size_hint_y=None,height=300))

        except Exception as e:
            toast(f'{e}')           
            
    def task_complete(self, inst):
        task = self.task_clk[str(inst)]
        self.chap_update_dia = MDDialog(
        title="Task Update",
        text=f'Do you want to update or remove the {task} Task',
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.canchapup),
            MDRaisedButton(text="Remove",md_bg_color='red',on_release= lambda *args: self.remtask(task,*args)),
            MDRaisedButton(text="UPDATE",on_release= lambda *args: self.task_update(task,*args))])
        self.chap_update_dia.open()
    
    def canchapup(self, obj):
        self.chap_update_dia.dismiss()
        
    def remtask(self, task, obj):
        with open('tasks.json', 'r') as openfile:
            data = json.load(openfile)
        data.pop(task)
        with open('tasks.json', 'w') as f:
             data = json.dumps(data, indent=4)
             f.write(data)
        with open('opened.txt','w') as f:
             f.write('opened')
        self.enter()
        self.chap_update_dia.dismiss()
        hist('Removed a Task',f'Removed a task named {task}')
    
    def task_update(self, task, obj):
        with open('tasks.json', 'r') as openfile:
            data = json.load(openfile)
        if data[task] == True:
            data[task] = False
        else:
            data[task] = True
        with open('tasks.json', 'w') as f:
             data = json.dumps(data, indent=4)
             f.write(data)
        with open('opened.txt','w') as f:
             f.write('opened')
        self.enter()
        self.chap_update_dia.dismiss()
        hist('Updated a Task',f'Updated a task named {task}')
        
    def add_task(self, task):
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r') as openfile:
                data = json.load(openfile)
            if task in data:
                toast('Task is already there')
            else:
                data.update({f'{task}':False})
                with open('tasks.json', 'w') as f:
                    data = json.dumps(data, indent=4)
                    f.write(data)
        else:
            with open('tasks.json', 'w') as f:
                data = {f'{task}':False}
                data = json.dumps(data, indent=4)
                f.write(data)
        with open('opened.txt','w') as f:
            f.write('opened')
        self.enter()
        self.ids.taskt.text = ''
        hist('Added a Task',f'Added a task named {task}')
    
    def home(self):
        self.manager.current = 'mainp'


class SubjectPage(Screen):    
    data = DictProperty()    
    def enter(self):
        global MData
        MData = make_data()        
        self.makepage()
    
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.home()
            return True 
            
    def makepage(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)  
        with open('subject_open.txt','r') as f:
            sub = f.read()            
        self.ids.tbar.title = sub
        self.ids.grid.bind(minimum_height=self.ids.grid.setter('height'))
        self.data = {
            'New Chapter': ['book',"on_release" ,lambda x: self.newchap(sub)],
            }
        self.done_chaps = {}
        try:
            self.ids.grid.clear_widgets()
        except:
            pass
        self.subject_clk = {}
        
        self.report_card = MDCard(size_hint_y=None,height="900",orientation="vertical",md_bg_color='#f6eeee')       
        try:
            self.report_card.padding = (50,50)
        except:
            pass
        try:
            self.report_card.spacing = (0,50)
        except:
            pass
            
        self.report = f'*{sub} Report*\n\n'
        self.report_card.add_widget(MDLabel(text=f'{sub}',halign='center',font_style='H3',underline=True))
        tot = MData[sub]["Data"]["total"]
        self.report_card.add_widget(MDLabel(text=f"Total Chapters - {tot}"))
        com = MData[sub]["Data"]["completed"]
        self.report_card.add_widget(MDLabel(text=f"Total Chapters Completed - {com}"))
        left = tot - com
        self.report_card.add_widget(MDLabel(text=f"Total Chapters Left - {left}"))        
        self.ids.grid.add_widget(self.report_card)
        
        self.report = self.report + f"Total Chapters - {tot}\nTotal Chapters Completed - {com}\nTotal Chapters Left - {left}\n\n"
        self.ids.grid.add_widget(MDLabel(text='',size_hint_y=None,height='75'))
        
        sbtn = MDRaisedButton(text="Show Report",size_hint=(1,0.1),md_bg_color='#f0b41d',on_release=self.show_report)
        self.report_card.add_widget(sbtn)
        abtn = MDRaisedButton(text="Send Report",size_hint=(1,0.1),md_bg_color='#f0b41d',on_release=self.send_report)
        self.report_card.add_widget(abtn)
        
        self.ids.grid.add_widget(MDSeparator())
        self.ids.grid.add_widget(MDLabel(text='',size_hint_y=None,height='75'))
        self.report = self.report + f"\n*Detailed Report -*\n\n"
        completed = []
        leftover = []
        for chapter in MData[sub]["Chapters"]:
            card2 = MDCard(size_hint_y=None,height="100",orientation="horizontal",on_release=self.chap_complete)
            card2.add_widget(MDLabel(text=f'{chapter}',halign='center',bold=True))
            if MData[sub]["Chapters"][f'{chapter}'] == True:
                card2.add_widget(Image(source='tick.jpg'))
                completed.append(chapter)
            else:
                card2.add_widget(Image(source='wrong.jpg'))
                leftover.append(chapter)
            self.ids.grid.add_widget(card2)
            self.subject_clk[str(card2)] = f'{sub}$&${chapter}'
        self.report = self.report + '*Chapters Completed -*\n'
        for x in completed:
            self.report = self.report + f'{x}\n'
        self.report = self.report + '\n\n*Chapters Left -*\n'
        for x in leftover:
            self.report = self.report + f'{x}\n'
        
        self.ids.grid.add_widget(MDLabel(text='',size_hint_y=None,height='100'))    
        self.ids.grid.add_widget(MDSeparator())
        card = MDCard(size_hint_y=None,height="100",orientation="vertical",md_bg_color='red',on_release=self.go_to_top)
        card.add_widget(MDLabel(text=f'You have reached the end',halign='center',underline=True,italic=True,bold=True))
        self.ids.grid.add_widget(card)

############## Chapter update ###############
    def canchapup(self, obj):
        self.chap_update_dia.dismiss()
    
    def show_report(self, inst):
        #self.report_card.export_to_png('/storage/emulated/0/test.png')
        self.manager.current = 'show_report_p'
        
    def send_report(self, inst):
        try:
            from kvdroid.tools import share_text
            share_text(self.report, title="Share", chooser=False, app_package=None,call_playstore=False, error_msg="application unavailable")
        except:
            toast('Unable to send report')
            
    def chap_complete(self, inst):
        line = self.subject_clk[str(inst)]
        sub = line.split('$&$')[0]
        chap = line.split('$&$')[-1]
        bottom_sheet_menu = MDListBottomSheet()
        
        bottom_sheet_menu.add_item(f"UPDATE",lambda  *args: self.chapter_update(sub,chap ,*args))
        bottom_sheet_menu.add_item(f"Add A Question",lambda  *args: self.add_question(sub,chap ,*args))
        bottom_sheet_menu.add_item(f"Tests",lambda  *args: self.test_show(sub,chap ,*args))
        bottom_sheet_menu.add_item(f"Notes",lambda  *args: self.notes_update(sub,chap ,*args))
        bottom_sheet_menu.add_item(f"Remove",lambda *args: self.remchap(sub, chap, *args))
        
        bottom_sheet_menu.open()
    
    def add_question(self, sub, chap, inst):
        self.sub = sub
        self.chap = chap
        ccls=AddQuestionBox()
        if 1==1:
            self.tar_dia = MDDialog(
            title=f"Add Question To {chap}",
            type='custom',
            content_cls=ccls,
            width=Window.width-100,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cantar),
                MDRaisedButton(text="Add Question",on_release= lambda *args: self.add_question_final(ccls,*args))])             
        self.tar_dia.open()

    def add_question_final(self, content_cls,obj):
        sub = self.sub
        chap = self.chap
        textfield = content_cls.ids.que
        que = textfield._get_text()
        textfield = content_cls.ids.ans
        ans = textfield._get_text()
        pth = '/storage/emulated/0/Documents/My Syllabus/extra_questions.json'
        data = get_data(pth)
        if sub in data:
            pass
        else:
            data[sub] = {}
        if chap in data[sub]:
            pass
        else:
            data[sub][chap] = {}
        if que in data[sub][chap]:
            toast('Question Already Exists')
        else:
            data[sub][chap][que] = {'answer':str(ans)}
            toast('Question Added')
            write_json(data, pth)
            self.tar_dia.dismiss()
            
    def cantar(self, inst):
        self.tar_dia.dismiss()
        
    def notes_update(self, sub, chapter, inst):
        with open('note_path.txt','w') as f:
            f.write(f'{sub}$$&&$${chapter}')
        self.manager.current = 'notep'
        
    def test_show(self, sub, chapter, inst):
        with open('text_files/test_chapter.txt','w') as f:
            f.write(f"{chapter}")
        with open('text_files/test_subject.txt','w') as f:
            f.write(f"{sub}")
        self.manager.current = 'testmenup'
        
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
        self.enter()
        with open('opened.txt','w') as f:
            f.write('opened')
        hist('Updated a chapter',f'Updated a chapter named {chapter}')
        
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
            with open('opened.txt','w') as f:
                f.write('opened')
            
    def canchap(self, inst):
        self.chap_dia.dismiss()   

    def remchap(self, sub, chap, inst):
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
            with open('opened.txt','w') as f:
                f.write('opened')
        
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
            with open('opened.txt','w') as f:
                f.write('opened')
            
    def canremchap(self, inst):
        self.rem_chap.dismiss()
     
    def go_to_top(self, inst):
        self.ids.scroll.scroll_y = 1
           
    def home(self):
        self.manager.current = 'mainp'
        
class ReportPage(Screen):
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.home()
            return True 
            
    def enter(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)  
        
        menu_items = [
            {"viewclass": "OneLineListItem","text": f"Home","height": dp(56),"on_release": lambda x=f"home": self.menu_callback(x)},
            {"viewclass": "OneLineListItem","text": f"Screen Shot","height": dp(56),"on_release": lambda x=f"getimg": self.menu_callback(x)},
            {"viewclass": "OneLineListItem","text": f"Copy To Clipboard","height": dp(56),"on_release": lambda x=f"copy": self.menu_callback(x)},
        ]
         
        self.menu = MDDropdownMenu(items=menu_items,width_mult=4,border_margin=dp(36),background_color='#33adff')
        with open('label.txt','r') as f:
            report_text = f.read()
            
        report_text = report_text.replace('&&$$&&','')
        self.ids.cont.text = report_text
    
    def menu_callback(self, item):
        self.menu.dismiss()
        item = str(item)
        if item == 'home':
            self.manager.current = 'mainp'
        elif item =='getimg':
            try:
                file_path='/storage/emulated/0/Documents/My Syllabus/report.png'
                self.ids.board.export_to_png(file_path)                
                toast('Image Captured and stored in My Syllabus folder')
            except Exception as e:
                toast(f'{e}')
        elif item == 'copy':
            from kivy.core.clipboard import Clipboard
            with open('report.txt','r') as f:
                text = f.read()
            Clipboard.copy(text)
            toast('Copyied to clipboard')        
        else:
            pass 
     
    def menu_open(self, button):
        async def open(self):
            self.menu.caller = button
            self.menu.open()
        ak.start(open(self))
        
    def home(self):
        self.manager.current = 'mainp'
        
class NotePage(Screen):
    def enter(self):
        Data = make_data_note()
        with open('note_path.txt','r') as f:
            path = f.read()
        sub = path.split('$$&&$$')[0]
        chap = path.split('$$&&$$')[-1]
        self.ids.tbar.title = chap       
        if sub in Data:
            if chap in Data[sub]:
                self.ids.main_text.text = Data[sub][chap]['note']
            else:
                self.ids.main_text.text = 'No Note Is There'
                Data[sub][chap] = {'note':'No Note Is There'}
                write_data_note(Data)
        else:
            Data[sub] = {}
            Data[sub][chap] = {'note':'No Note Is There'}
            self.ids.main_text.text = 'No Note Is There'
            write_data_note(Data)            
    
    def save(self):
        Data = make_data_note()
        with open('note_path.txt','r') as f:
            path = f.read()
        sub = path.split('$$&&$$')[0]
        chap = path.split('$$&&$$')[-1]
        Data[sub][chap] = {'note':str(self.ids.main_text.text)}
        write_data_note(Data)
    
    def share(self):
        text = self.ids.main_text.text
        try:
            from kvdroid.tools import share_text
            share_text(text, title="Share", chooser=False, app_package=None,call_playstore=False, error_msg="application unavailable")
        except:
            toast('Unable to send report')
        
    def home(self):
        self.manager.current = 'subp'


class Setting(Screen):
    wh = Window.height
    ww = Window.width
    def chapters_menu_open(self):
        try:
            pth = '/storage/emulated/0/Documents/My Syllabus/extra_questions.json'
            data = get_data(pth)
            with open('Setting Data/qsubject.txt','r') as f:
                sub = f.read()
            chapters = []
            for x in data[sub]:
                chapters.append(x)
            chap_items = [{"viewclass": "OneLineListItem","text": f"{i}","height": dp(56),"on_release": lambda x=f"{i}": self.change_chapters_topic(x),} for i in chapters] 
            self.chapters_menu = MDDropdownMenu(items=chap_items,position="center",width_mult=4)
            self.chapters_menu.caller = self.ids.cbtn
            self.chapters_menu.open()
        except Exception as e:
            print(e)
            
    def subject_menu_open(self):
        try:
            chapters = []
            pth = '/storage/emulated/0/Documents/My Syllabus/extra_questions.json'
            data = get_data(pth)
            if data == []:
                chapters = []
            else:
                for chap in data:
                    chapters.append(chap)
            chap_items = [{"viewclass": "OneLineListItem","text": f"{i}","height": dp(56),"on_release": lambda x=f"{i}": self.change_subject_topic(x),} for i in chapters] 
            self.subject_menu = MDDropdownMenu(items=chap_items,position="center",width_mult=4)
            self.subject_menu.caller = self.ids.sbtn
            self.subject_menu.open()
        except Exception as e:
            print(e)
    
    def change_subject_topic(self, text_item):
        with open('Setting Data/qsubject.txt','w') as f:
            f.write(str(text_item))
        self.subject_menu.dismiss()
        toast('Subject Changed')
        
    def change_chapters_topic(self, text_item):
        with open('Setting Data/qchoice.txt','w') as f:
            f.write(str(text_item))
        self.chapters_menu.dismiss()
        toast('Topic Changed')
     
    def history(self):
        self.manager.current = 'hisp'  
    
    def bkup_data(self):
        try:
            from zipfile import ZipFile
            directory = '/storage/emulated/0/Documents/My Syllabus/'
            file_paths = get_all_file_paths(directory) 
            place = os.path.join('/storage/emulated/0/Documents/My Syllabus/','AppData.zip')   
            if os.path.exists(place):
                os.remove(place)
            with ZipFile(place,'w') as zip: 
                for file in file_paths: 
                    zip.write(file) 
            from kvdroid.tools import share_file
            share_file(place, title='Share My Syllabus App Data', chooser=True, app_package=None,call_playstore=False, error_msg="application unavailable")
            toast('App Data File Also Saved In Documents Folder')
        except:
            toast('Unable to backup your data')
    def save_data(self):
        write_data_safe(make_data())
        shutil.copy('/storage/emulated/0/Documents/My Syllabus/note_data.json','json_files/safe_note_data.json')
        shutil.copy('/storage/emulated/0/Documents/My Syllabus/target_data.json','json_files/safe_target_data.json')
        hist('Data Saved',f'Secured his data by saving it')
        toast('Data Saved You are safe now')
        
    def recover(self):
        write_data(make_data_recover())
        if os.path.exists('/storage/emulated/0/Documents/My Syllabus/note_data.json'):
            os.remove('/storage/emulated/0/Documents/My Syllabus/note_data.json')
        if os.path.exists('/storage/emulated/0/Documents/My Syllabus/target_data.json'):
            os.remove('/storage/emulated/0/Documents/My Syllabus/target_data.json')
            
        shutil.copy('json_files/safe_note_data.json','/storage/emulated/0/Documents/My Syllabus/note_data.json')
        shutil.copy('json_files/safe_target_data.json','/storage/emulated/0/Documents/My Syllabus/target_data.json')
        
        toast('Data Recovered')
        hist('Recovered Data',f'Recovered your data')
        self.make()
        
    def home(self):
        self.manager.current = 'mainp'
    
    def dlset(self):
        if os.path.exists('Setting Data/dark_mode.txt'):
            return True
        else:
            return False
            
    def asset(self):
        if os.path.exists('Setting Data/app_style.txt'):
            return True
        else:
            return False
            
    def nrset(self):
        if os.path.exists('Setting Data/name_radius.txt'):
            return True
        else:
            return False
    
    def pausesearchset(self):
        if os.path.exists('Setting Data/pause_search.txt'):
            return True
        else:
            return False
            
    def pause_search(self, instance_switch, active_value: bool):
        if active_value == True:
            with open('Setting Data/pause_search.txt','w') as f:
                f.write('Pause search')
        else:
            os.remove('Setting Data/pause_search.txt')
            
    def pauseset(self):
        if os.path.exists('Setting Data/pause_all_search.txt'):
            return True
        else:
            return False
            
    def pause_all_search(self, instance_switch, active_value: bool):
        if active_value == True:
            with open('Setting Data/pause_all_search.txt','w') as f:
                f.write('Pause search')
        else:
            os.remove('Setting Data/pause_all_search.txt')

class HistoryPage(Screen):
    def enter(self):
        print('Entered History Page')
        lst = os.listdir('Setting Data/History/')
        try:
            self.ids.flist.clear_widgets()
        except:
            pass
            
        if len(lst) > 100:
            toast('List too long wait a minute')
            for i in lst:
                if os.path.exists('Setting Data/name_radius.txt'):
                    rl = [25, 25, 25, 25]
                else:
                    rl = [0, 0, 0, 0]
                with open(f'Setting Data/History/{i}','r') as f:
                    sec = f.read()
                i = i.replace('.txt','')
                lst2 = i.split('$$&&$$')
                mt = lst2[0]
                dt = lst2[-1]
                self.ids.flist.add_widget(ThreeLineListItem(text=f"{mt}",secondary_text=f'{i}',tertiary_text=f'{dt}',bg_color='#d9d9d9',radius=rl,on_release=self.hopen))
        elif lst == []:
            if os.path.exists('Setting Data/name_radius.txt'):
                rl = [25, 25, 25, 25]
            else:
                rl = [0, 0, 0, 0]
            self.ids.flist.add_widget(TwoLineListItem(text=f"No History Is There",secondary_text=f'No History',bg_color='#d9d9d9',radius=rl))
        
        else:
            for i in lst:
                if os.path.exists('Setting Data/name_radius.txt'):
                    rl = [25, 25, 25, 25]
                else:
                    rl = [0, 0, 0, 0]
                with open(f'Setting Data/History/{i}','r') as f:
                    sec = f.read()
                i = i.replace('.txt','')
                lst2 = sec.split('$$&&$$')
                mt = lst2[0]
                dt = lst2[-1]
                self.ids.flist.add_widget(ThreeLineListItem(text=f"{mt}",secondary_text=f'{i}',tertiary_text=f'{dt}',bg_color='#d9d9d9',radius=rl,on_release=self.hopen))
    
        if os.path.exists('Setting Data/pause_all_search.txt'):
            try:
                self.ids.flist.clear_widgets()
            except:
                pass
            self.ids.flist.add_widget(OneLineListItem(text=f"Search History Is Paused",bg_color='#ff4d4d'))
        else:
            pass        
    
    def trash(self):
        self.trash_dia = MDDialog(
            title="Delete History",
            text='Do you want to delete all the history',
            width=Window.width-100,
            buttons=[
                MDFlatButton(text="Cancel",on_release= self.cancel),
                MDRaisedButton(text="Delete",on_release=self.deleteall)]
            )
        self.trash_dia.open()
        
    def cancel(self,obj):
        self.trash_dia.dismiss()
        
    def deleteall(self,obj):
        shutil.rmtree('Setting Data/History/')
        toast('History Deleted')
        os.mkdir('Setting Data/History/')
        self.enter()
        self.trash_dia.dismiss()
        Snackbar(text='All your history has been deleted',md_bg_color='red').open()
    
    def hopen(self, inst):
        query = inst.secondary_text
        bottom_sheet_menu = MDListBottomSheet()
        bottom_sheet_menu.add_item(f"Delete",lambda x, y=query: self.delhis(f"{y}"))
        bottom_sheet_menu.open()     
    
    def delhis(self, query):
        os.remove(f'Setting Data/History/{query}.txt')
        self.enter()
                
    def home(self):
        self.manager.current = 'mainp'