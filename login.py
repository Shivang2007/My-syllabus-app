from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.toast import toast
from kivymd.uix.snackbar import Snackbar

import os
from database import *

class LoginPage(Screen):
    def login(self):
        name = self.ids.sname.text
        name = str(name)
        if '/' in name:
            toast('Do not use slashes')
        elif name == '':
            toast('Write Something')
        else:
            toast('Loading please wait')
            data = ask()
            if name in data:
                with open('logined.txt','w') as f:
                    f.write(f"{name}")
                with open('opened.txt','w') as f:
                    f.write('opened')
                self.manager.current = 'mainp'
                Snackbar(text='Logined Successfully').open()
            else:
                toast('Account Does not exist')
    
    def back(self):
        self.manager.current = 'mainp'
    
    def sign(self):
        self.manager.current = 'signupp'
        
class SignupPage(Screen):
    def signup(self):
        name = self.ids.sname.text
        name = str(name)
        if '/' in name:
            toast('Do not use slashes')
        elif name == '':
            toast('Write Something')
        else:
            toast('Loading please wait')
            data = ask()
            if name in data:
                toast('Account Already Exists')
            else:
                ndata = {
                    name:{
                    'name':name,
                    'report':'',
                    'data':{
                        'time':'No Data',
                        'date':'No Data',
                        'battery_per':'No Data',
                        'battery_state':'No Data',
                        'location':'No Location Data Is There'
                        },
                    'tasks':{},
                    'chats':{},
                    'exams':{}
                    }
                }
                place(ndata)
                self.manager.current = 'loginp'
                Snackbar(text='Account Made Successfully').open()
                with open('opened.txt','w') as f:
                    f.write('opened')
    
    def back(self):
        self.manager.current = 'mainp'
    
    def log(self):
        self.manager.current = 'loginp'