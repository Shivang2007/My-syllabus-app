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

from tasks import TasksPage, SubjectPage


try:
    from android.permissions import request_permissions, Permission, check_permission
except Exception as e:
    toast('Error no 1 occured')
    
try:
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE, Permission.SEND_SMS])
except Exception as Argument:
    toast('Error no 2 occured')
    
import os 
import sys
import json
from plyer import sms
from plyer import notification
from os.path import join, dirname

files = ['/storage/emulated/0/My Syllabus/']

for file in files:
    try:
        if os.path.exists(f'{file}'):
            pass
        else:
            os.makedirs(f'{file}')
    except Exception as e:
        toast(f'{e}')

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
    def enter(self):
        global MData
        MData = make_data()
        try:
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
            'TO-DO': ['list-box-outline',"on_release" ,lambda x: self.todo()]
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
        
        self.report = {
            "total_chapters":str(gt),
            "total_completed":str(gc)
        }
        try:
            card = MDCard(size_hint_y=None,height="700",orientation='vertical',md_bg_color='#f4dedc')       
            card.add_widget(MDLabel(text=f'TOTAL',bold=True,halign='center',font_style='H3',underline=True))
            lft = int(gt) - int(gc)
            card.add_widget(MDLabel(text=f"Total Chapters = {gt}",halign='center'))
            card.add_widget(MDLabel(text=f"Total Chapters Completed = {gc}",halign='center'))
            card.add_widget(MDLabel(text=f"Total Chapters Left = {lft}",halign='center'))
            
            abtn = MDRaisedButton(text="Send Report",size_hint=(1,0.1),md_bg_color='#f0b41d',on_release=self.send_report)
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
                card.padding =  ('0','50')
            except:
                pass
            try:
                card.spacing = ('0','50')
            except:
                pass
            card.add_widget(MDLabel(text=f'{sub}',halign='center',font_style='H3',underline=True))
            
            tot = MData[sub]["Data"]["total"]
            card.add_widget(MDLabel(text=f"Total Chapters = {tot}"))
            com = MData[sub]["Data"]["completed"]
            card.add_widget(MDLabel(text=f"Total Chapters Completed = {com}"))
            left = tot - com
            card.add_widget(MDLabel(text=f"Total Chapters Left = {left}"))
            
            abtn = MDRaisedButton(text="Open Subject",size_hint=(1,0.1),on_release=self.open_sub)
            card.add_widget(abtn)
            self.subject_clk[str(abtn)] = str(sub)
            
            abtn = MDRaisedButton(text="Delete Subject",size_hint=(1,0.1),md_bg_color="red",on_release=self.dele_sub)
            card.add_widget(abtn)
            self.subject_clk[str(abtn)] = str(sub)
            self.ids.grid.add_widget(card)
            
    def send_report(self, inst):
        ccls=SendReportBox()
        self.report_dia = MDDialog(
        title="Send Report",
        type='custom',
        content_cls=ccls,
        width=Window.width,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.canrep),
            MDRaisedButton(text="Send Report",md_bg_color='#f0b41d',on_release= lambda *args: self.send_f_report(ccls,*args))])
        self.report_dia.open()
        
    def send_f_report(self, content_cls, obj):
        textfield = content_cls.ids.num
        num = textfield._get_text()
        try:
            int(num)
            if len(num) <= 9:
                toast('Length should be atlest 10 digits')
            else:
                self.confirm_report(num)
        except Exception as e:
            toast("Number should be an integer")
        
    def canrep(self, obj):
        self.report_dia.dismiss()
    
    def confirm_report(self, num):
        self.report_dia.dismiss()
        self.report_dia = MDDialog(
        title="Send SMS Report ?",
        text=f"Are you sure you want to send a report to the number - {num}",
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.canrep),
            MDRaisedButton(text="Send Final",md_bg_color='red',on_release= lambda *args: self.send_final_report(num,*args))])
        self.report_dia.open()
    
    def send_final_report(self, num, obj):
        gt = self.report["total_chapters"]
        gc = self.report["total_completed"]
        cont = f"Dear Parents\nYour ward has completed {gc} chapters out of a total of {gt} chapters\nThank You"
        try:
            sms.send(num,cont)
            kwargs = {'title':'Syllabus Report' , 'message':cont, 'ticker':'Report Made'}
            notification.notify(**kwargs)
            Snackbar(text='SMS Report has been sent',md_bg_color='#f0b41d').open()
        except Exception as e:
            toast(f'SMS Not send because of {e}')
            
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
        self.enter()

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
            self.enter()
        
    def cansub(self, inst):
        self.sub_dia.dismiss()    
          
############## SIDE FUNCTIONS #########
    def todo(self):
        self.manager.current = 'tasksp'
    
    def clnb(self):
        self.ids.nav_drawer.set_state("close")
        
    def recover(self):
        write_data(make_data_recover())
        toast('Data Recovered')
        self.enter()
    
    def exit(self):
        sys.exit()

TasksPage()
SubjectPage()


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        
        self.theme_cls.primary_palette = f"Blue"
        set_bars_colors(self.theme_cls.primary_color, self.theme_cls.primary_color,"Light")
        self.theme_cls.theme_style = "Light"
        sm=ScreenManager()
        sc_lst = [
        Main(name='mainp'),
        SubjectPage(name='subp'),
        TasksPage(name='tasksp')
        ]
        try:
            self.Export()
        except Exception as e:
            pass
        try:
            for sc in sc_lst:
                sm.add_widget(sc)
        except Exception as e:
            toast('screen error')
            toast(f'{e}')
            
        return sm
    
    def Export(self):
        path = join(dirname(self.user_data_dir))
        with open('/storage/emulated/0/path.txt','w') as f:
            f.write(path)

MainApp().run()