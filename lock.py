from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.toast import toast
from kivymd.uix.snackbar import Snackbar

import os
from functions import *
import logging
import sys
import time

def get_all_file_paths(directory): 
    file_paths = [] 
    for root, directories, files in os.walk(directory): 
        for filename in files: 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
    return file_paths
    
class LockScreen(Screen):
    def make(self):
        self.attempt = 0
        self.ids.img.icon = 'lock'
        self.ids.bg.source = ''
        
    def forgot(self):
        self.manager.current = 'forgotpasp'
        
    def enter(self, text):
        data = get_data('/storage/emulated/0/Documents/My Syllabus/app_lock.json')
        if data['password'] == text:
            if os.path.exists('text_files/lock_to_where.txt'):
                with open('text_files/lock_to_where.txt','r') as f:
                    where = f.read()
                self.ids.pas.text = ''
                self.manager.current = where
            else:
                self.manager.current = 'mainp'
        else:
            self.attempt = self.attempt + 1
            if self.attempt == 1:
                self.ids.img.icon = 'lock-alert'
                toast('3 Attempts Left')
            elif self.attempt == 2:
                self.ids.img.icon = ''
                self.ids.bg.source = 'red_alert.jpg'
                toast('2 Attempts Left')
            elif self.attempt ==3:
                ct = time.localtime()
                dt = f'{ct[2]}/{ct[1]}/{ct[0]}'
                tt = f'{ct[3]}:{ct[4]}:{ct[5]}'
                data = get_data('Setting Data/App_Data.json')
                data['last_failed_lock_attempt'] = {'date':dt,'time':tt}
                write_json(data,'Setting Data/App_Data.json')
                toast('1 Attempts Left')
            elif self.attempt == 4:
                sys.exit()

class AppSecurityScreen(Screen):
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.home()
            return True 
            
    def make(self):
        if os.path.exists('Setting Data/App_Data.json'):
            data = get_data('Setting Data/App_Data.json')
            data = data['last_failed_lock_attempt']
            self.ids.last_attempt.text = f"Last Failed Attempt - \nTime - {data['date']}\nDate - {data['time']}"
        else:
            self.ids.last_attempt.text = 'No Failed Attempt Till Now.'
        
    def secret_folder_zip(self):
        from zipfile import ZipFile
        directory = '/storage/emulated/0/Documents/My Syllabus/My Syllabus Secret Folder'
        file_paths = get_all_file_paths(directory) 
        place = os.path.join('/storage/emulated/0/Documents/My Syllabus/','SecretFolder.zip')   
        if os.path.exists(place):
            os.remove(place)
        with ZipFile(place,'w') as zip: 
            for file in file_paths: 
                zip.write(file)
        toast('Zip File Made in Documents Folder')
        
    def secret_folder(self, status):
        import shutil
        if status == "Unlock Secret Folder (Currently Locked)":
            shutil.copytree('My Syllabus Secret Folder',"/storage/emulated/0/My Syllabus Secret Folder", dirs_exist_ok=True)
            self.ids.secret_gal_btn.text = "Lock Secret Folder (Currently Unlocked)"
        else:
            shutil.copytree("/storage/emulated/0/My Syllabus Secret Folder",'My Syllabus Secret Folder', dirs_exist_ok=True)
            shutil.rmtree("/storage/emulated/0/My Syllabus Secret Folder")
            self.ids.secret_gal_btn.text =  "Unlock Secret Folder (Currently Locked)"
            
    def rmpass(self):
        if os.path.exists('/storage/emulated/0/Documents/My Syllabus/app_lock.json'):
            os.remove('/storage/emulated/0/Documents/My Syllabus/app_lock.json')
            toast('Password Removed')
        else:
            toast('No Password Is There')
            
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
        except Exception as e:
            print(e)
            toast('Unable to backup your data')
            
    def home(self):
        self.manager.current = 'mainp' 
        
    def set_pas(self):
        self.manager.current = 'setpasp'
        
        
class ForgotPasPage(Screen):
    def enter(self):
        data = get_data('/storage/emulated/0/Documents/My Syllabus/app_lock.json')
        qu = data['question']
        self.ids.que.text = f'Question - \n{qu}'
    
    def reset(self):
        ans = self.ids.pas.text
        data = get_data('/storage/emulated/0/Documents/My Syllabus/app_lock.json')
        if ans == data['answer']:
            self.manager.current = 'setpasp'
        else:
            toast('Wrong Answer')
    
class SetPasPage(Screen):
    def set_new_pas(self, pas, cpas, que, ans):
        if pas == cpas:
            if len(pas) == 0:
                toast('Type Password')
            elif len(que) == 0:
                toast('Type Question')
            elif len(ans) == 0:
                toast('Type Answer')
            else:
                data = {
                'password':str(pas),
                'question':str(que),
                'answer':str(ans)
                }
                write_json(data,'/storage/emulated/0/Documents/My Syllabus/app_lock.json')
                toast('My Syllabus App Is Now Protected')
                self.manager.current = 'mainp' 
        else:
            toast('Password and confirm password do not match')
            
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.home()
            return True 
    
    def home(self):
        self.manager.current = 'mainp' 