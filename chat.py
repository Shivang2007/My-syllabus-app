##############################
# KIVY MAIN APP CLASSES
##############################
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang import Builder
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

##############################
# KIVYMD WIDGETS 
##############################
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton,MDFlatButton,MDRaisedButton,MDRectangleFlatIconButton
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivy.properties import DictProperty
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.clock import Clock
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem,TwoLineListItem,ThreeLineListItem
from kivy.base import EventLoop

##############################
# MODULES
##############################
import os
from os import path
import random
import sys
import json
import time
import logging
from database import *



class ChatPage(Screen):
    ww = Window.width
    Window.softinput_mode = "below_target"
    
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.manager.current = 'mainp'
            return True
            
    def enter(self):
        self.ids.grid.bind(minimum_height=self.ids.grid.setter('height'))
        self.ids.loader.active = True
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
        with open('logined.txt','r') as f:
            name = f.read()
        data = ask()
        try:
            self.ids.grid.clear_widgets()
        except:
            pass
            
        try:
            if data[name]['chats'] == {}:
                self.ids.grid.add_widget(MDLabel(text='No Chat Is There',font_style='H3',halign='center',size_hint_y=None,height=300))
            else:
                curd = ''
                for da_ti in data[name]['chats']:
                    dt = da_ti.split('&&')[0]
                    if curd == dt:
                        pass
                    else:
                        curd = dt
                        ctt = time.localtime()
                        today = f'{ctt[2]}-{ctt[1]}-{ctt[0]}'
                        if dt == today:
                            dt = 'Today'
                        self.ids.grid.add_widget(MDLabel(text=f'{dt}   \n----------------------------------------',halign='left',font_style='H6',size_hint_y=None,height=150,bold=True))
                    
                    tt = da_ti.split('&&')[-1]
                    chat = data[name]['chats'][da_ti]['msg']
                    by = data[name]['chats'][da_ti]['by']
                    
                    ##### design ########
                    ch = int(len(chat))*2 + 200
                    boldornot = False
                    
                    card = GridLayout(cols=2,size_hint_y=None,height=ch)
                    
                    pr = [30,30,0,30]
                    cr = [0,30,30,30]
                    if by == 'child':
                        card.add_widget(MDLabel(text=f'',halign='left',size_hint_x=None,width=150))
                        card2 = MDCard(radius=pr,size_hint_y=None,height=ch,orientation="horizontal",padding=(50,50),md_bg_color="#c6ffad")
                        card2.add_widget(MDLabel(text=f'{tt}\n\n{chat}',halign='left',bold=boldornot))
                        card.add_widget(card2)
                        
                    elif by == 'parent':
                        card2 = MDCard(radius=cr,size_hint_y=None,height=ch,orientation="horizontal",padding=(50,50),md_bg_color="#ffb0b5")
                        card2.add_widget(MDLabel(text=f'{tt}\n\n{chat}',halign="left",bold=boldornot))
                        card.add_widget(card2)
                        card.add_widget(MDLabel(text=f'',halign='left',size_hint_x=None,width=150))
                        
                    elif by == 'company':
                        card2 = MDCard(size_hint_y=None,height=ch,orientation="horizontal",padding=(50,50),md_bg_color="#e4d6ff")
                        card2.add_widget(MDLabel(text=f'{tt}\n\n{chat}',halign='center',bold=boldornot))
                        card.add_widget(card2)
                        card.add_widget(MDLabel(text=f'',halign='left',size_hint_x=None,width=100))
                        
                    self.ids.grid.add_widget(card)
                    
                self.ids.loader.active = False
        except:
            self.ids.grid.add_widget(MDLabel(text='No Chat Is There',font_style='H3',halign='center',size_hint_y=None,height=300))
        
        
    def send(self, msg):
        toast('Sending')
        self.ids.taskt.text = ''
        
        ct = time.localtime()
        dt = f'{ct[2]}-{ct[1]}-{ct[0]}'
        tt = f'{ct[3]}:{ct[4]}:{ct[5]}'
        with open('logined.txt','r') as f:
            name = f.read()
        data = ask()
        
        if 'chats' in data[name]:
            pass
        else:
            data[name]['chats'] = {}
        data[name]['chats'][f'{dt}&&{tt}'] = {'msg':str(msg),'by':'child'}
        place(data)
        toast('Sent')
        self.enter()
        
    def home(self):
        self.manager.current = "mainp"
        
