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

from tasks import TasksPage, SubjectPage, ReportPage, AboutPage
from login import LoginPage, SignupPage
from database import *
    
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
        if os.path.exists("/storage/emulated/0/My Syllabus/"):
            pass
        else:
            os.makedirs("/storage/emulated/0/My Syllabus/")
        with open("/storage/emulated/0/My Syllabus/data.json","w") as f:
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

class NewSubjectBox(BoxLayout):
    pass

class NewChapterBox(BoxLayout):
    pass

class RemoveChapterBox(BoxLayout):
    pass

class SendReportBox(BoxLayout):
    pass
    
class Main(Screen):
    ww = Window.width
    data = DictProperty()
    sub_dia = None
    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')
    
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
        toast('Data Saved You are safe now')
        
    def make(self):
        self.ids.grid.bind(minimum_height=self.ids.grid.setter('height'))
        self.data = {
            'Create New Subject': ['book',"on_release" ,lambda x: self.newsub()],
            'TO-DO': ['list-box-outline',"on_release" ,lambda x: self.todo()],
            'Chat': ['message-reply-text-outline',"on_release" ,lambda x: self.go_to_chat()]
            }
        self.done_chaps = {}
        try:
            self.ids.grid.clear_widgets()
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
            
        self.subject_clk = {}
        
        self.ids.grid.add_widget(MDLabel(text='',size_hint_y=None,height='100'))
        self.ids.grid.add_widget(MDSeparator())
        for sub in MData:
            self.ids.grid.add_widget(MDLabel(text='',size_hint_y=None,height='100'))
            card = MDCard(size_hint_y=None,height="800",orientation="vertical",md_bg_color='#f6eeee')
            try:
                card.padding =  (50,50)
            except:
                pass
            try:
                card.spacing = (0,50)
            except:
                pass
            card.add_widget(MDLabel(text=f'{sub}',halign='center',font_style='H3',underline=True))
            
            tot = MData[sub]["Data"]["total"]
            card.add_widget(MDLabel(text=f"Total Chapters = {tot}"))
            com = MData[sub]["Data"]["completed"]
            card.add_widget(MDLabel(text=f"Total Chapters Completed = {com}"))
            left = tot - com
            card.add_widget(MDLabel(text=f"Total Chapters Left = {left}"))
            
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
            
        self.update_parent()

    def refresh(self):
        with open('opened.txt','w') as f:
            f.write('opened')
        self.enter()
                    
    def show_overall_report(self, inst):
        with open('report.txt','w') as f:
            f.write(str(self.report_text))
        with open('label.txt','w') as f:
            f.write(str(self.label_text))
        self.manager.current = 'reportp'
    
    def update_parent(self):
        async def openfun(self):
            try:
                toast('Updating your data')
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
                if os.path.exists('tasks.json'):
                    with open('tasks.json', 'r') as openfile:
                        taskdata = json.load(openfile)
                    data[name]['tasks'] = taskdata
                else:
                     data[name]['tasks'] = {}
                  
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
        self.refresh()    

    def open_sub(self, inst):
        sub = self.subject_clk[str(inst)]
        with open('subject_open.txt','w') as f:
            f.write(sub)
        self.manager.current = 'subp'
        
############## SUBJECT FUNCTIONS #########    
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
            with open("/storage/emulated/0/My Syllabus/data.json","w") as f:
                Data = json.dumps(MData, indent=4)
                f.write(Data)
            self.sub_dia.dismiss()
            Snackbar(text=f'Subject named - {sub} Created').open()
            toast('Make sure to save your data')
            self.refresh()    
        
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
        toast('Data Recovered')
        self.enter()
        
    def about(self):
        self.manager.current = 'aboutp'
    
    def exit(self):
        sys.exit()