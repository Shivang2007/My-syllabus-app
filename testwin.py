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
from kivymd.uix.list import OneLineAvatarIconListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.utils import asynckivy as ak
from kivy.core.audio import SoundLoader
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.image import Image

import time
import sys
import os
import json
import logging
import shutil

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

def write_data(data):
    try:
        with open("/storage/emulated/0/Documents/My Syllabus/data.json","w") as f:
            data = json.dumps(data, indent=4)
            f.write(data)
    except Exception as e:
        toast(f'{e}')
        
class NewTestBox(BoxLayout):
    pass
    
class TestMenu(Screen):
    def enter(self):
        global MData
        MData = make_data()
        with open('text_files/test_chapter.txt','r') as f:
            chapter = f.read()
        with open('text_files/test_subject.txt','r') as f:
            subject = f.read()
            
        cchapter = chapter.capitalize()
        self.ids.tbar.title = f"{cchapter} Tests"
        try:
            self.ids.flist.clear_widgets()
        except:
            pass
        try:           
            for test in MData[str(subject)]['Tests'][str(chapter)]:
                self.ids.flist.add_widget(ThreeLineListItem(text=f'{test}',secondary_text=str(MData[str(subject)]['Tests'][str(chapter)][test]['desc']),tertiary_text='Published On : '+str(MData[str(subject)]['Tests'][str(chapter)][test]['date']),bg_color='#c6ddf5',on_release=self.open_test_options))
        except Exception as e:
            self.ids.flist.add_widget(TwoLineListItem(text='No Test',secondary_text='No test is there add on now',bg_color='red'))
            hist('Test Error',f'{e}')
    
    def open_test_options(self, inst):
        with open('text_files/test_chapter.txt','r') as f:
            chapter = f.read()
        with open('text_files/test_subject.txt','r') as f:
            subject = f.read()
        tname = inst.text
        
        bottom_sheet_menu = MDListBottomSheet()
        
        bottom_sheet_menu.add_item(f"Give Test",lambda  *args: self.give_test(subject,chapter ,tname,*args))
        bottom_sheet_menu.add_item(f"Add Question",lambda  *args: self.add_question_test(subject,chapter ,tname,*args))
        bottom_sheet_menu.add_item(f"Show Result",lambda  *args: self.result_test(subject,chapter ,tname,*args))
        bottom_sheet_menu.add_item(f"Remove",lambda *args: self.rem_test(subject,chapter ,tname, *args))
        bottom_sheet_menu.open()
    
    def give_test(self,subject,chapter ,tname,inst):
        with open('text_files/test_name.txt','w') as f:
            f.write(str(tname))
        self.manager.current = 'testgp'
    
    def add_question_test(self,subject,chapter ,tname,inst):
        with open('text_files/test_name.txt','w') as f:
            f.write(str(tname))
        self.manager.current = 'testquep'
    
    def result_test(self,subject,chapter ,tname,inst):
        with open('text_files/test_name.txt','w') as f:
            f.write(str(tname))
        self.manager.current = 'testrp'
        
    def rem_test(self , subject,chapter ,tname, inst):
        if 1==1:
            self.tar_dia = MDDialog(
            title="Remove Test ?",
            text='are you sure you want to delete this test',
            width=Window.width,
            buttons=[
                MDRaisedButton(text="Cancel",on_release=self.cantar),
                MDFlatButton(text="Remove Test",md_bg_color='red',on_release= lambda *args: self.remove_test(subject,chapter ,tname, *args))])             
        self.tar_dia.open()
    
    def remove_test(self,subject,chapter ,tname,inst):
        Data = make_data()
        Data[subject]['Tests'][chapter].pop(tname)
        write_data(Data)
        toast('Test Removed')
        self.enter()
    
    def home(self):
        self.manager.current = 'subp'
    
    def add_exam(self):
        ccls=NewTestBox()
        if 1==1:
            self.tar_dia = MDDialog(
            title="New Test",
            type='custom',
            content_cls=ccls,
            width=Window.width,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cantar),
                MDRaisedButton(text="Create",on_release= lambda *args: self.create_tar(ccls, *args))])             
        self.tar_dia.open()
    
    def create_tar(self, content_cls,obj):
        global MData
        MData = make_data()
        textfield = content_cls.ids.tname
        tname = textfield._get_text()
        textfield = content_cls.ids.dname
        dname = textfield._get_text()
        try:
            if len(tname) == 0:
                toast('Write the name of the test')
            else:
                ct = time.localtime()
                dt = f'{ct[2]}/{ct[1]}/{ct[0]}'
                tt = f'{ct[3]}:{ct[4]}:{ct[5]}'
                ad = f"Added On - {dt}"
                with open('text_files/test_chapter.txt','r') as f:
                    chapter = f.read()
                with open('text_files/test_subject.txt','r') as f:
                    subject = f.read()
                
                if 'Tests' in MData[str(subject)]:
                    pass
                else:
                    MData[str(subject)]['Tests'] = {}
                if str(chapter) in MData[str(subject)]['Tests']:
                    pass
                else:
                    MData[str(subject)]['Tests'][str(chapter)] = {}
                
                if str(tname) in MData[str(subject)]['Tests'][str(chapter)]:
                    toast(f'Test named {tname} is already there')
                else:
                    MData[str(subject)]['Tests'][str(chapter)][str(tname)] = {'date':dt,'time':tt,'name':str(tname),'desc':str(dname),'questions':{},'result':{'correct':0,'wrong':0,'unattempted':0}}   
                    write_data(MData)
                    toast('Test Made')
                    hist('New Test Made',f"Made a new {chapter} test named {tname}")
                    self.tar_dia.dismiss()
                    self.enter()
                    #self.manager.current = 'testmakep'
        except Exception as e:
            toast(f'{e}')
    
    def cantar(self, inst):
        self.tar_dia.dismiss()

class TestQuestion(Screen):
    wwidth = Window.width
    wheight = Window.height
    def enter(self):
        self.quest_pic = ''
        self.ids.quest_pic.source = 'white.jpg'
        self.ids.opta.text= ''
        self.ids.optb.text= ''
        self.ids.optc.text= ''
        self.ids.optd.text= ''
        self.ids.copt.text= ''
        self.ids.que.text = ''
    
    def choose_pic(self):
        try:
            self.manager_open = False
            self.file_manager = MDFileManager(
                preview=True,exit_manager=self.exit_manager, select_path=self.select_path
            )
            self.file_manager.show('/storage/emulated/0/')
            self.manager_open = True
        except:
            toast('Error no 3')
    
    def select_path(self, path: str):
        self.quest_pic = path
        self.ids.quest_pic.source = path
        try:
            self.manager_open = False
            self.file_manager.close()
        except:
            toast('Error no 4 occured')
    
    def exit_manager(self, *args):
        try:
            self.manager_open = False
            self.file_manager.close()
        except:
            toast('Error no 4 occured')
            
    def set_quest(self):
        with open('text_files/test_chapter.txt','r') as f:
            chapter = f.read()
        with open('text_files/test_subject.txt','r') as f:
            subject = f.read()
        with open('text_files/test_name.txt','r') as f:
            tname = f.read()
            
        Data = make_data()
        
        A = self.ids.opta.text
        B = self.ids.optb.text
        C = self.ids.optc.text
        D = self.ids.optd.text
        Cor = self.ids.copt.text
        poc = self.quest_pic
        que = self.ids.que.text
        
        ct = time.localtime()
        dt = f'{ct[2]}d{ct[1]}d{ct[0]}'
        tt = f'{ct[3]}t{ct[4]}t{ct[5]}'
        
        if len(poc) == 0 and len(que) !=0:
            Data[subject]['Tests'][chapter][tname]['questions'][f'{subject}_{chapter}_{tname}_Question_{dt}_{tt}'] = {'source':'None','text':str(que),'options':{'A':A,'B':B,'C':C,'D':D},'Answer':Cor,'Your_answer':'','status':'unattempted'}
            Data[subject]['Tests'][chapter][tname]['result']['unattempted'] = int(Data[subject]['Tests'][chapter][tname]['result']['unattempted']) + 1
            write_data(Data)
            toast('Question Added You can add Another One Now')
            self.enter()
            
        elif len(poc) != 0 and len(que) == 0:
            ext = poc.split('.')[-1]
            shutil.copy(poc,f"/storage/emulated/0/Documents/My Syllabus/Test Questions/{subject}_{chapter}_{tname}_Question_{dt}_{tt}.{ext}")
            Data[subject]['Tests'][chapter][tname]['questions'][f'{subject}_{chapter}_{tname}_Question_{dt}_{tt}'] = {'source':f"/storage/emulated/0/Documents/My Syllabus/Test Questions/{subject}_{chapter}_{tname}_Question_{dt}_{tt}.{ext}",'text':'None','options':{'A':A,'B':B,'C':C,'D':D},'Answer':Cor,'Your_answer':'','status':'unattempted'}
            Data[subject]['Tests'][chapter][tname]['result']['unattempted'] = int(Data[subject]['Tests'][chapter][tname]['result']['unattempted']) + 1
            write_data(Data)
            toast('Question Added You can add Another One Now')
            self.enter()
            
        elif len(poc) != 0 and len(que) !=0:
            ext = poc.split('.')[-1]
            shutil.copy(poc,f"/storage/emulated/0/Documents/My Syllabus/Test Questions/{subject}_{chapter}_{tname}_Question_{dt}_{tt}.{ext}")
            Data[subject]['Tests'][chapter][tname]['questions'][f'{subject}_{chapter}_{tname}_Question_{dt}_{tt}'] = {'source':f"/storage/emulated/0/Documents/My Syllabus/Test Questions/{subject}_{chapter}_{tname}_Question_{dt}_{tt}.{ext}",'text':str(que),'options':{'A':A,'B':B,'C':C,'D':D},'Answer':Cor,'Your_answer':'','status':'unattempted'}
            Data[subject]['Tests'][chapter][tname]['result']['unattempted'] = int(Data[subject]['Tests'][chapter][tname]['result']['unattempted']) + 1
            write_data(Data)
            toast('Question Added You can add Another One Now')
            self.enter()
            
        else:
            toast('Please set a question first')
    
    def home(self):
        self.manager.current = 'testmenup'

    
class TestGive(Screen):
    wwidth = Window.width
    wheight = Window.height
    def enter(self):
        self.qno = 1
        self.make_question()
    
    def delete(self):
        if 1==1:
            self.tar_dia = MDDialog(
            title="Delete Question",
            text='Are you sure you want to remove this question ?',
            width=Window.width,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cantar),
                MDRaisedButton(text="Remove",on_release= lambda *args: self.remove_question(*args))])             
        self.tar_dia.open()
    
    def remove_question(self,inst):
        with open('text_files/test_chapter.txt','r') as f:
            chapter = f.read()
        with open('text_files/test_subject.txt','r') as f:
            subject = f.read()
        with open('text_files/test_name.txt','r') as f:
            tname = f.read()
        Data = make_data()
        if Data[subject]['Tests'][chapter][tname]['questions'][self.qid]['status'] == 'correct':
            Data[subject]['Tests'][chapter][tname]['result']['correct'] = Data[subject]['Tests'][chapter][tname]['result']['correct'] - 1
        elif Data[subject]['Tests'][chapter][tname]['questions'][self.qid]['status'] == 'wrong':
            Data[subject]['Tests'][chapter][tname]['result']['wrong'] = Data[subject]['Tests'][chapter][tname]['result']['wrong'] - 1
        elif Data[subject]['Tests'][chapter][tname]['questions'][self.qid]['status'] == 'unattempted':
            Data[subject]['Tests'][chapter][tname]['result']['unattempted'] = Data[subject]['Tests'][chapter][tname]['result']['unattempted'] - 1
        else:
            pass
        Data[subject]['Tests'][chapter][tname]['questions'].pop(self.qid)
        write_data(Data)
        toast('Question Removed')
        self.next('Next')
    
    def cantar(self, inst):
        self.tar_dia.dismiss()
        
    def make_question(self):
        with open('text_files/test_chapter.txt','r') as f:
            chapter = f.read()
        with open('text_files/test_subject.txt','r') as f:
            subject = f.read()
        with open('text_files/test_name.txt','r') as f:
            tname = f.read()
        self.ids.tbar.title = tname
        Data = make_data()
        UseData = Data[subject]['Tests'][chapter][tname]['questions']
        n = 0
        
        try:
            self.ids.main_grid.clear_widgets()
            self.remove_widget(self.pre_btn)
            self.remove_widget(self.next_btn)
        except:
            pass
        
        def add(wid):
            self.ids.main_grid.add_widget(wid)
        
        add(MDLabel(text=f'Question No. {self.qno}',halign='center',font_style='H4'))
        max = 0
        for question in UseData:
            max = max  + 1
        self.max = max 
        
        for question in UseData:
            n = n + 1
            qd = UseData[question]
            if n == self.qno:
                self.qid = question
                try:
                    if qd['source'] == 'None':
                        pass
                    else:
                        add(Image(source=qd['source'],size_hint=(None,None),height=700,width=Window.width-100))
                except Exception as e:
                    print(e)
                    toast('Unable to load image')
                    
                try:
                    if qd['text'] == 'None':
                        pass
                    else:
                        add(MDLabel(text = qd['text']))
                except:
                    toast('Unable to load image')
                
                for opt in qd['options']:
                    te = qd['options'][opt]
                    add(MDRaisedButton(text=f"{opt} :- {te}",pos_hint={"center_x": .1, "center_y": .1},on_release=self.answered))
                
                add(MDLabel(text='',font_style='H1'))
                add(MDLabel(text='',font_style='H1'))
                
                self.pre_btn = MDRaisedButton(text='Previous',pos_hint={"center_x": .15, "center_y": .1},on_release=self.previous)
                self.next_btn = MDRaisedButton(text='Next',pos_hint={"center_x": .8, "center_y": .1},on_release=self.next)
                self.add_widget(self.pre_btn)
                self.add_widget(self.next_btn)                      
            else:
                pass
     
    def answered(self, inst):
        opt = inst.text
        opt = opt.split(' :- ')[0].lower()
        
        with open('text_files/test_chapter.txt','r') as f:
            chapter = f.read()
        with open('text_files/test_subject.txt','r') as f:
            subject = f.read()
        with open('text_files/test_name.txt','r') as f:
            tname = f.read()
        self.ids.tbar.title = tname
        Data = make_data()
        UseData = Data[subject]['Tests'][chapter][tname]['questions'][self.qid]
        Ans = UseData['Answer'].lower()
        if opt == Ans:
            ak.start(self.show('Correct Answer'))
            if Data[subject]['Tests'][chapter][tname]['questions'][self.qid]['status'] == 'unattempted':
                cor = Data[subject]['Tests'][chapter][tname]['result']['correct']
                Data[subject]['Tests'][chapter][tname]['questions'][self.qid]['status'] = 'correct'
                Data[subject]['Tests'][chapter][tname]['result']['correct'] = int(cor) + 1
                Data[subject]['Tests'][chapter][tname]['result']['unattempted'] = int(Data[subject]['Tests'][chapter][tname]['result']['unattempted']) - 1
                write_data(Data)
            
        else:
            ak.start(self.show('Wrong Answer'))
            if Data[subject]['Tests'][chapter][tname]['questions'][self.qid]['status'] == 'unattempted':
                cor = Data[subject]['Tests'][chapter][tname]['result']['wrong']
                Data[subject]['Tests'][chapter][tname]['questions'][self.qid]['status'] = 'wrong'
                Data[subject]['Tests'][chapter][tname]['result']['wrong'] = int(cor) + 1
                Data[subject]['Tests'][chapter][tname]['result']['unattempted'] = int(Data[subject]['Tests'][chapter][tname]['result']['unattempted']) - 1
                write_data(Data)
            
    async def show(self,type):
        label = MDLabel(text=type,halign='center',font_style='H3')
        self.add_widget(label)
        await ak.sleep(4)
        self.remove_widget(label)
        
    def home(self):
        self.manager.current = 'testmenup'
        
    def next(self, inst):
        if self.qno == self.max:
            self.qno = 1
        else:
            self.qno = self.qno + 1
        self.make_question()       
                   
    def previous(self, inst):
        if self.qno == 1:
            self.qno = self.max
        else:
            self.qno = self.qno - 1
        self.make_question()        


class TestResult(Screen):
    wwidth = Window.width
    wheight = Window.height
    def enter(self):
        with open('text_files/test_chapter.txt','r') as f:
            chapter = f.read()
        with open('text_files/test_subject.txt','r') as f:
            subject = f.read()
        with open('text_files/test_name.txt','r') as f:
            tname = f.read()
        self.ids.tbar.title = tname +' Result'
        Data = make_data()
        UseData = Data[subject]['Tests'][chapter][tname]['result']
        Cor = int(UseData['correct'])
        Wor = int(UseData['wrong'])
        un = int(UseData['unattempted'])
        ps = Cor * 4
        score = int(Cor)*4 - int(Wor)
        total_questions = Cor + Wor + un
        total = total_questions * 4
        
        self.report = f"Test Name - {tname}\n\nSubject - {subject}\n\nChapter - {chapter}\n\nTotal Questions - {total_questions}\n\nMaximum Marks - {total}\n\nYour Marks - {score}\n\nCorrect Questions - {Cor}\n\nIncorrect Questions - {Wor}\n\nUnattempted Questions - {un}\n\nPositive Score - {ps}\n\nNegative Score - {Wor}"
        self.ids.result_card.text = self.report
        
    def share(self):
        try:
            from kvdroid.tools import share_text
            share_text(self.report, title="Share", chooser=False, app_package=None,call_playstore=False, error_msg="application unavailable")
        except:
            toast('Unable to send report')
            
    def save(self):
        with open('text_files/test_chapter.txt','r') as f:
            chapter = f.read()
        with open('text_files/test_subject.txt','r') as f:
            subject = f.read()
        with open('text_files/test_name.txt','r') as f:
            tname = f.read()
            
        file_path = f'/storage/emulated/0/Pictures/{subject}_{chapter}_{tname}_Report.png'
        self.ids.rcard.export_to_png(file_path)
        file_path = f'/storage/emulated/0/DCIM/{subject}_{chapter}_{tname}_Report.png'
        self.ids.rcard.export_to_png(file_path)
        file_path = f'/storage/emulated/0/Documents/My Syllabus/Report Cards/{subject}_{chapter}_{tname}_Report.png'
        self.ids.rcard.export_to_png(file_path)
        toast('Report Card Saved To Gallery')
    
    def home(self):
        self.manager.current = 'testmenup'
        
    def share_card(self):
        with open('text_files/test_chapter.txt','r') as f:
            chapter = f.read()
        with open('text_files/test_subject.txt','r') as f:
            subject = f.read()
        with open('text_files/test_name.txt','r') as f:
            tname = f.read()
        file_path = f'/storage/emulated/0/Documents/My Syllabus/Report Cards/{subject}_{chapter}_{tname}_Report.png'
        self.ids.rcard.export_to_png(file_path)
        from kvdroid.tools import share_file
        share_file(file_path, title='Share', chooser=False, app_package=None,call_playstore=False, error_msg="application unavailable")    