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
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.utils import asynckivy as ak
from kivy.core.audio import SoundLoader
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.selectioncontrol import MDCheckbox

#from tasks import TasksPage, SubjectPage, ReportPage, AboutPage
#from login import LoginPage, SignupPage
from database import *
from functions import *    
import os 
import sys
import json
import shutil
try:
    from datetime import datetime
    import time
    from plyer import notification
    from plyer import sms
    from plyer import battery
except:
    print('Module import error')

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

def write_data(data):
    try:
        if os.path.exists("/storage/emulated/0/Documents/My Syllabus/"):
            pass
        else:
            os.makedirs("/storage/emulated/0/Documents/My Syllabus/")
        with open("/storage/emulated/0/Documents/My Syllabus/data.json","w") as f:
            data = json.dumps(data, indent=4)
            f.write(data)
    except Exception as e:
        toast(f'{e}')
        
def write_data_safe(data):
    try:
        with open("safe_data.json","w") as f:
            data = json.dumps(data, indent=4)
            f.write(data)
    except Exception as e:
        toast(f'{e}')


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
        
class NewSubjectBox(BoxLayout):
    pass
class NewChapterBox(BoxLayout):
    pass
class RemoveChapterBox(BoxLayout):
    pass
class SendReportBox(BoxLayout):
    pass
class NewTargetBox(BoxLayout):
    pass
class TimeLeftForBox(BoxLayout):
    pass
class VoiceBox(BoxLayout):
    pass
    
class Main(Screen):
    ww = Window.width
    data = DictProperty()
    sub_dia = None
    
    with open('opened.txt','w') as f:
        f.write('opened')
        
    def enter(self):
        global MData
        MData = make_data()
        try:
            if os.path.exists('opened.txt'):
                os.remove('opened.txt')
                self.check()
                self.make()
        except Exception as e:
            toast(f'{e}')
    
    def save_data(self):
        write_data_safe(make_data())
        shutil.copy('/storage/emulated/0/Documents/My Syllabus/note_data.json','json_files/safe_note_data.json')
        shutil.copy('/storage/emulated/0/Documents/My Syllabus/target_data.json','json_files/safe_target_data.json')
        hist('Data Saved',f'Secured his data by saving it')
        toast('Data Saved You are safe now')
        
    def make(self):
        self.ids.grid.bind(minimum_height=self.ids.grid.setter('height'))
        self.data = {
            'New Audio Book': ['microphone',"on_release" ,lambda x: self.voice()],
            'Set Target': ['target',"on_release" ,lambda x: self.settar()],
            'Create New Subject': ['book',"on_release" ,lambda x: self.newsub()],
            'TO-DO': ['list-box-outline',"on_release" ,lambda x: self.todo()],
            'Chat': ['message-reply-text-outline',"on_release" ,lambda x: self.go_to_chat()]
            }
        self.done_chaps = {}
        try:
            self.ids.grid.clear_widgets()
        except:
            pass
            
        if os.path.exists("/storage/emulated/0/Documents/My Syllabus/target_data.json"):        
            with open("/storage/emulated/0/Documents/My Syllabus/target_data.json", 'r') as openfile:
                current_data = json.load(openfile)
        else:
            current_data = {}
        self.ids.grid.add_widget(MDLabel(text=f"Your Targets",font_style="H4",halign='center',bold=True,underline=True,size_hint_y=None,height=100))
        if current_data == {}:
            self.ids.grid.add_widget(MDLabel(text=f"Currently there is no target",font_style="H5",halign='center',size_hint_y=None,height=100))
            self.ids.grid.add_widget(MDSeparator())
        else:
            for target in current_data:
                date = current_data[target]['date']
                added = current_data[target]['added']
                self.ids.grid.add_widget(ThreeLineListItem(text=f"{target}",secondary_text=f"{date}",tertiary_text=f"{added}",font_style="H6",on_release=self.change_tar))
        
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
        
        self.label_text = f"[color=#f50213][size=100][b][u]My Report[/u][/b][/size][/color]\n\n\n[color=#f74040][size=40][b]Total Chapters = {gt}\nTotal Chapters Completed = {gc}\nTotal Left = {lftt}\n\n\n[/b][/size][/color] &&$$&&"
        self.report_text = f"My Report\nTotal Chapters = {gt}\nTotal Chapters Completed = {gc}\nTotal Left = {lftt}\n\n"
        
        try:
            card = MDCard(size_hint_y=None,height="700",orientation='vertical',md_bg_color='#f4dedc')       
            try:
                card.padding =  (50,50)
            except:
                pass
            try:
                card.spacing = (0,50)
            except:
                pass
            card.add_widget(MDLabel(text=f'TOTAL',bold=True,halign='center',font_style='H3',underline=True))
            lft = int(gt) - int(gc)
            card.add_widget(MDLabel(text=f"Total Chapters = {gt}",halign='center'))
            card.add_widget(MDLabel(text=f"Total Chapters Completed = {gc}",halign='center'))
            card.add_widget(MDLabel(text=f"Total Chapters Left = {lft}",halign='center'))
            
            abtn = MDRaisedButton(text="Send Report",size_hint=(1,0.1),md_bg_color='#f0b41d',on_release=self.send_report)
            card.add_widget(abtn)
            
            abtn = MDRaisedButton(text="Show Overall Report",size_hint=(1,0.1),md_bg_color='#f0b41d',on_release=self.show_overall_report)
            card.add_widget(abtn)
            
            self.ids.grid.add_widget(card)
        except Exception as e:
            toast(f"{e}")
        
        try:
            card = MDCard(orientation='vertical',elevation=5,size_hint_y=None,padding=(50,50),height=800,md_bg_color='#f4dedc')
            card.add_widget(MDLabel(text=f"Today's Tasks",halign="center",font_style="H4",bold=True,underline=True,size_hint_y=None,height=100))
            
            if os.path.exists(f'/storage/emulated/0/Documents/My Tasks/Tasks/Today'):
                tdata = get_tasks_data()
                if tdata == []:
                    card.add_widget(MDLabel(text=f"No Task Is There",halign='center'))
                else:
                    n = 0
                    for task in tdata:
                        n = n + 1
                        card.add_widget(MDLabel(text=f"{task}",halign='left'))
                        if n == 5:
                            break
            else:
                card.add_widget(MDLabel(text=f"No Task Is There",halign='center'))   
            self.ids.grid.add_widget(card)
        except Exception as e:
            print(e)
            
        try:
            pth = '/storage/emulated/0/Documents/My Syllabus/extra_questions.json'
            if os.path.exists(pth):
                if os.path.exists('Setting Data/qsubject.txt'):
                    if os.path.exists('Setting Data/qchoice.txt'):
                        with open('Setting Data/qsubject.txt', 'r') as f:
                            sub = f.read()
                        with open('Setting Data/qchoice.txt', 'r') as f:
                            cho = f.read()
                        data = get_data(pth)
                        data = data[str(sub)][str(cho)]
                        card = MDCard(orientation='vertical',elevation=5,size_hint_y=None,padding=(50,50),height=750,md_bg_color='#f4dedc')
                        card.add_widget(MDLabel(text=f"{cho} Questions",halign="center",font_style="H4",bold=True,underline=True,size_hint_y=None,height=100))
                        self.question_label = MDLabel(text=f"No Question Is There",halign="center")
                        card.add_widget(self.question_label)
                        self.answer_label = MDLabel(text=f"",halign="center",size_hint_y=None,height=80)
                        card.add_widget(self.answer_label)
                        grid = GridLayout(cols=3,size_hint_y=None,height=100,padding=(0,20),spacing=(50,0))
                        grid.add_widget(MDRaisedButton(text="Previous",on_release=lambda x: self.change_question('previous')))
                        self.qbtn = MDRaisedButton(text="Answer",on_release=self.show_answer)
                        grid.add_widget(self.qbtn)
                        
                        grid.add_widget(MDRaisedButton(text="Next",on_release=lambda x: self.change_question('next')))
                        card.add_widget(grid)
                        self.ids.grid.add_widget(card)
                        
                        self.qno = 1
                        self.make_question()
                    else:
                        card = MDCard(orientation='vertical',elevation=5,size_hint_y=None,padding=(50,50),height=300,md_bg_color='#f4dedc')
                        card.add_widget(MDLabel(text=f"No Chapter Has Been Choosen",halign="center"))
                        card.add_widget(MDRaisedButton(text='Choose Chapter',size_hint=(1,0.2),on_release=self.open_settings))
                        self.ids.grid.add_widget(card)
                else:
                    card = MDCard(orientation='vertical',elevation=5,size_hint_y=None,padding=(50,50),height=300,md_bg_color='#f4dedc')
                    card.add_widget(MDLabel(text=f"No Subject Has Been Choosen",halign="center"))
                    card.add_widget(MDRaisedButton(text='Choose Chapter',size_hint=(1,0.2),on_release=self.open_settings))
                    self.ids.grid.add_widget(card)
            else:
                card = MDCard(orientation='vertical',elevation=5,size_hint_y=None,padding=(50,50),height=300,md_bg_color='#f4dedc')
                card.add_widget(MDLabel(text=f"No Question Has Been Added Add One Now",halign="center"))
                card.add_widget(MDRaisedButton(text='Add Question',size_hint=(1,0.1),on_release=self.add_question_ind))
                self.ids.grid.add_widget(card)            
        except Exception as e:
            print(e)
         
        self.subject_clk = {}
        
        self.ids.grid.add_widget(MDLabel(text='',size_hint_y=None,height='100'))
        self.ids.grid.add_widget(MDSeparator())
        for sub in MData:
            self.ids.grid.add_widget(MDLabel(text='',size_hint_y=None,height='100'))
            card = MDCard(size_hint_y=None,height="800",orientation="vertical",md_bg_color='#f6eeee',style='elevated')
            try:
                card.padding =  (50,50)
            except:
                pass
            try:
                card.spacing = (0,50)
            except:
                pass
            card.add_widget(MDLabel(text=f'{sub}',halign='center',font_style='H4',underline=True))
            
            tot = MData[sub]["Data"]["total"]
            card.add_widget(MDLabel(text=f"Total Chapters = [b]{tot}[/b]",markup=True))
            com = MData[sub]["Data"]["completed"]
            card.add_widget(MDLabel(text=f"Total Chapters Completed = [b]{com}[/b]",markup=True))
            left = tot - com
            card.add_widget(MDLabel(text=f"Total Chapters Left = [b]{left}[/b]",markup=True))
            
            self.label_text = self.label_text  + f"[color=#f50213][size=75][u]{sub}[/u][/size][/color]\n\n[size=35]Total Chapters = {tot}\nTotal Chapters Completed = {com}\nTotal Left = {left}\n\n[/size]"
            self.report_text = self.report_text  + f"\n{sub}\nTotal Chapters = {tot}\nTotal Chapters Completed = {com}\nTotal Left = {left}\n"
        
            abtn = MDRaisedButton(text="Open Subject",size_hint=(1,0.1),on_release=self.open_sub)
            card.add_widget(abtn)
            self.subject_clk[str(abtn)] = str(sub)
            
            abtn = MDRaisedButton(text="Delete Subject",size_hint=(1,0.1),md_bg_color="red",on_release=self.dele_sub)
            card.add_widget(abtn)
            self.subject_clk[str(abtn)] = str(sub)
            self.ids.grid.add_widget(card)
            
        self.ids.grid.add_widget(MDLabel(text='',size_hint_y=None,height='100'))    
        self.ids.grid.add_widget(MDSeparator())
        card = MDCard(size_hint_y=None,height="100",orientation="vertical",md_bg_color='red',on_release=self.go_to_top)
        card.add_widget(MDLabel(text=f'You have reached the end',halign='center',underline=True,italic=True,bold=True))
        self.ids.grid.add_widget(card)
    
    def voice(self):
        ccls=VoiceBox()
        if 1==1:
            self.tar_dia = MDDialog(
            title="Speak What ?",
            type='custom',
            content_cls=ccls,
            width=Window.width-100,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cantar),
                MDRaisedButton(text="Speak",on_release= lambda *args: self.speakup(ccls, *args))])             
        self.tar_dia.open()
    
    def speakup(self, content_cls,obj):
        try:
            textfield = content_cls.ids.tar
            tar = textfield._get_text()
            cont = tar
            from kvdroid.tools import speech
            speech(cont, "en")
        except:
            toast('Oops an error occured')
        
    def show_answer(self, inst):
        if inst.text.lower() == 'answer':
            self.qbtn.text = 'Hide'
            self.answer_label.text = self.answer
        else:
            self.qbtn.text = 'Answer'
            self.answer_label.text = ''
            
    def make_question(self):
        pth = '/storage/emulated/0/Documents/My Syllabus/extra_questions.json'
        with open('Setting Data/qchoice.txt', 'r') as f:
            cho = f.read()
        with open('Setting Data/qsubject.txt', 'r') as f:
            sub = f.read()
        data = get_data(pth)
        data = data[sub][str(cho)]
        n = 0
        self.max_que = len(data)
        for que in data:
            n = n + 1
            if n == self.qno:
                self.question_label.text = str(que)
                self.answer = data[str(que)]['answer']
            else:
                pass
    
    def change_question(self, type):
        if type == 'next':
            if self.qno == self.max_que:
                self.qno = 1
                self.make_question()
            else:
                self.qno = self.qno + 1
                self.make_question()
        elif type == 'previous':
            if self.qno == 1:
                self.qno = self.max_que
                self.make_question()
            else:
                self.qno = self.qno - 1
                self.make_question()
        elif type == 'delete':
            if 1==1:
                self.tar_dia = MDDialog(
                    title="Delete Current Question ?",
                    text= 'Are you sure you want to delete this question you can not go back',
                    buttons=[
                        MDFlatButton(text="Cancel",on_release=self.cantar),
                        MDRaisedButton(text="Delete Question",on_release= lambda *args: self.delete_question_final(*args))])             
                self.tar_dia.open()
        else:
            pass
    
    def delete_question_final(self, inst):
        try:
            pth = '/storage/emulated/0/Documents/My Syllabus/extra_questions.json'
            with open('Setting Data/qsubject.txt', 'r') as f:
                sub = f.read()
            with open('Setting Data/qchoice.txt', 'r') as f:
                cho = f.read()
            data = get_data(pth)
            data[sub][str(cho)].pop(self.question_label.text)
            write_json(data, pth)
            toast('Question Deleted')
            self.make()
            self.tar_dia.dismiss()
        except:
            toast('Oops an error occured')
            
    def set_time_left_for(self, inst):
        ccls=TimeLeftForBox()
        if 1==1:
            self.tar_dia = MDDialog(
            title="Set Time Left For",
            type='custom',
            content_cls=ccls,
            width=Window.width-100,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cantar),
                MDRaisedButton(text="Done",on_release= lambda *args: self.set_time_left_for_final(ccls, *args))])             
        self.tar_dia.open()
    
    def set_time_left_for_final(self, content_cls,obj):
        textfield = content_cls.ids.fname
        fname = textfield._get_text()
        textfield = content_cls.ids.dt
        dt = textfield._get_text()       
        lst = dt.split('/')
        if len(lst) == 3:
            try:
                dd = lst[0]
                mm = lst[1]
                yy = lst[-1]
                with open('Setting Data/time_for.txt','w') as f:
                    f.write(f'{fname}$$&&$${dd}/{mm}/{yy}')
                self.tar_dia.dismiss()
                toast('Done')
                self.make()
            except:
                toast('Date Should Be Made Up Of Integers')
        else:
            toast('Write Date in given format')

    def change_tar(self, inst):
        chapter = inst.text
        self.subdel_dia = MDDialog(
        title="Remove Target",
        text=f"Do you want to remove {chapter} from your targets.",
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.candel),
            MDRaisedButton(text="Remove",md_bg_color='red',on_release= lambda *args: self.delete_tar(chapter,*args))])
        self.subdel_dia.open()
        
    def delete_tar(self, chapter, inst):
        toast('Removing Chapter...')
        with open("/storage/emulated/0/Documents/My Syllabus/target_data.json", 'r') as openfile:
            data = json.load(openfile)
        if chapter in data:
            data.pop(chapter)
        with open("/storage/emulated/0/Documents/My Syllabus/target_data.json", 'w') as f:
            data = json.dumps(data, indent=4)
            f.write(data)
        self.make()
        toast('Target Removed')
        hist('Removed A Target',f'Removed a target titled {chapter}')
        self.subdel_dia.dismiss()
        
    def refresh(self):
        self.update_parent()
        with open('opened.txt','w') as f:
            f.write('opened')
        hist('Updated Parents',f'Updated his data for parents')
        self.enter()
                    
    def show_overall_report(self, inst):
        with open('report.txt','w') as f:
            f.write(str(self.report_text))
        with open('label.txt','w') as f:
            f.write(str(self.label_text))
        self.manager.current = 'reportp'
    
    def setting(self):
        self.manager.current = 'settp'
    def history(self):
        self.manager.current = 'hisp'
    def show_test(self):
        self.manager.current = 'testmenup'
    def open_settings(self, inst):
        self.manager.current = 'settp'
    def pdfp(self):
        self.manager.current = 'pdfp'
        
    def update_parent(self):
        async def openfun(self):
            try:
                toast('Updating your data.....')
                data =  ask()
                rt = self.label_text
                with open('logined.txt','r') as f:
                    name = f.read()
                data[name]['report'] = str(rt)
                try:
                    ct = time.localtime()
                    dt = f'{ct[2]}/{ct[1]}/{ct[0]}'
                    tt = f'{ct[3]}:{ct[4]}:{ct[5]}'
                    data[name]['data']['time'] = f"Last Updated Time - {tt}"
                    data[name]['data']['date'] = f"Last Updated Date - {dt}"
                except:
                    pass
                try:
                    batp = battery.status['percentage']
                    bats = battery.status['isCharging']
                    data[name]['data']['battery_per'] = f"Battery Is {batp}% Charged"
                    if bats == True:
                        data[name]['data']['battery_state'] = 'Battery is currently charging'
                    else:
                        data[name]['data']['battery_state'] = 'Battery is currently not charging'
                except:
                    pass
                try:
                    data[name]['data']['current_chapter'] = chap 
                except:
                    pass
                
                if os.path.exists('tasks.json'):
                    with open('tasks.json', 'r') as openfile:
                        taskdata = json.load(openfile)
                    data[name]['tasks'] = taskdata
                else:
                     data[name]['tasks'] = {}
                     
                if os.path.exists("json_files/current.json"):        
                    with open("json_files/current.json", 'r') as openfile:
                        data[name]['current_chapters'] = json.load(openfile)
                else:
                    data[name]['current_chapters'] = {}
                 
                toast('Still Updating your data....')
                place(data)
                toast('Done')
            except Exception as e:
                toast(f"{e}")
        
        if os.path.exists('logined.txt'):
            ak.start(openfun(self))
        else:
            toast('Login to update your data')
    
        
    def check(self):
        if os.path.exists('logined.txt'):
            self.ids.lgt.text = 'Logout'
            return True
        else:
            self.ids.lgt.text = 'Login/Signup'
            return False
            
    def learnpic(self):
        self.manager.current = 'galleryp'
    
    def version_tell(self):
        hist('Version Check','Checked the version of the app')
        toast('Vesrion :- 4.0.0')
        
    def login(self, type):
        if type == 'Login/Signup':
            self.manager.current = 'loginp'
        else:
            os.remove('logined.txt')
            self.refresh()     
        
    def send_report(self, inst):
        try:
            from kvdroid.tools import share_text
            share_text(self.report_text, title="Share", chooser=False, app_package=None,call_playstore=False, error_msg="application unavailable")
        except:
            toast('Unable to send report')
            
    def dele_sub(self, inst):
        sub = self.subject_clk[str(inst)]
        self.subdel_dia = MDDialog(
        title="SUBJECT DELETE",
        text=f'Do you want to delete the {sub} subject, you can not undo the process',
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.candel),
            MDRaisedButton(text="DELETE",md_bg_color='red',on_release= lambda *args: self.subject_delete(sub,*args))])
        self.subdel_dia.open()
    
    def candel(self, inst):
        self.subdel_dia.dismiss()
    
    def subject_delete(self, subject, inst):
        MData.pop(f'{subject}')
        write_data(MData)
        Snackbar(text=f'Subject {subject} Deleted').open()
        self.subdel_dia.dismiss()
        hist('Deleted a Subject',f'Deleted a subject named {subject}')
        self.make()

    def open_sub(self, inst):
        sub = self.subject_clk[str(inst)]
        with open('subject_open.txt','w') as f:
            f.write(sub)
        self.manager.current = 'subp'
        
    def settar(self):
        ccls=NewTargetBox()
        if 1==1:
            self.tar_dia = MDDialog(
            title="New Target",
            type='custom',
            content_cls=ccls,
            width=Window.width-100,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cantar),
                MDRaisedButton(text="Create",on_release= lambda *args: self.create_tar(ccls, *args))])             
        self.tar_dia.open()
        
    def create_tar(self, content_cls,obj):
        textfield = content_cls.ids.tar
        tar = textfield._get_text()
        textfield = content_cls.ids.date
        date = textfield._get_text()
        try:
            if os.path.exists("/storage/emulated/0/Documents/My Syllabus/"):
                pass
            else:
                os.makedirs("/storage/emulated/0/Documents/My Syllabus/")
            
            ct = time.localtime()
            dt = f'{ct[2]}/{ct[1]}/{ct[0]}'
            tt = f'{ct[3]}:{ct[4]}:{ct[5]}'
            ad = f"Added On - {dt}"
            data = {str(tar):{'date':str(date),'added':str(ad)}}
            with open("/storage/emulated/0/Documents/My Syllabus/target_data.json","w") as f:
                data = json.dumps(data, indent=4)
                f.write(data)
        except Exception as e:
            toast(f'{e}')
        self.make()
        toast('Task Made')
        hist('Target Created',f'Created a new target for {tar}')
        self.tar_dia.dismiss()
    
    def cantar(self, inst):
        self.tar_dia.dismiss()
        
    def newsub(self):
        ccls=NewSubjectBox()
        if self.sub_dia == None:
            self.sub_dia = MDDialog(
            title="New Subject",
            type='custom',
            content_cls=ccls,
            width=Window.width-100,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.cansub),
                MDRaisedButton(text="Create",on_release= lambda *args: self.create_sub(ccls, *args))])
        else:
            pass
        self.sub_dia.open()
    
    def create_sub(self, content_cls,obj):
        textfield = content_cls.ids.subname
        sub = textfield._get_text()
        if sub in MData:
            toast('Subject already exists')
        else:
            MData[f"{sub}"] = {
            "Chapters":{},
            "Data":{"total":0,"completed":0}
            }
            with open("/storage/emulated/0/Documents/My Syllabus/data.json","w") as f:
                Data = json.dumps(MData, indent=4)
                f.write(Data)
            self.sub_dia.dismiss()
            Snackbar(text=f'Subject named - {sub} Created').open()
            toast('Make sure to save your data')
            self.make()
            hist('New Subject',f'Made a new subject named {sub}')
        
    def cansub(self, inst):
        self.sub_dia.dismiss()    
          
############## SIDE FUNCTIONS #########
    def go_to_top(self, inst):
        self.ids.scroll.scroll_y = 1
        
    def todo(self):
        self.manager.current = 'tasksp'
    
    def clnb(self):
        self.ids.nav_drawer.set_state("close")
        
    def go_to_chat(self):
        if os.path.exists('logined.txt'):
            self.manager.current = "chatp"
        else:
            toast('Login Needed')
            self.manager.current = "loginp"
    
    def go_to_exam(self):
        if os.path.exists('logined.txt'):
            self.manager.current = "examp"
        else:
            toast('Login Needed')
            self.manager.current = "loginp"
        
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
        
    def about(self):
        self.manager.current = 'aboutp'
    
    def exit(self):
        sys.exit()