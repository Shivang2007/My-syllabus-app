import json
import os
import logging



def encryp(path, pas, new):
    try:                
        from pypdf import PdfReader, PdfWriter        
        reader = PdfReader(path)        
        writer = PdfWriter()
        writer.append_pages_from_reader(reader)
        writer.encrypt(pas)       
        with open(new, "wb") as out_file:
            writer.write(out_file)
        return True
    except Exception as e:
        return e
        
def merge_all_files(lst, path):
    try:
        from pypdf import PdfMerger
        pdfs = lst
        merger = PdfMerger()        
        for pdf in pdfs:
            merger.append(os.path.join('/storage/emulated/0/',pdf))        
        merger.write("/storage/emulated/0/result.pdf")
        merger.close()
        return True
    except Exception as e:
        print(e)
        toast(f'Oops an error occured {e}')

def get_data(path):
    try:
        if os.path.exists(path):        
            with open(path, 'r') as openfile:
                MData = json.load(openfile)
        else:
            with open(path,"w") as f:
                data = {}
                data = json.dumps(data, indent=4)
                f.write(data)
            with open(path, 'r') as openfile:
                MData = json.load(openfile)
        return MData
    except Exception as e:
        print(e)
        return {}

def write_json(data, path):
    try:
        with open(path,"w") as f:
            data = json.dumps(data, indent=4)
            f.write(data)
    except Exception as e:
        toast(f'{e}')

def ex(text):
    with open('errors.txt','a') as f:
        f.write(f'{text}\n')
        
def crpdf(path, fname):
    try:
        if os.path.isdir(path):
            lst = os.listdir(path)
            img_ext = ['jpg','jpeg','png']
            imgs =[]
            for file in lst:
                ext = file.split('.')[-1]
                if ext in img_ext:
                    imgs.append(file)
                else:
                    pass
            if imgs == []:
                res = 'no file'
            else:
                try:
                    from PIL import Image
                except:
                    res = 'Module not imported'                    
                fi = imgs[0]
                image = Image.open(os.path.join(path, fi))
                im_1 = image.convert('RGB')
                img_lst = []
                n= 0
                for img in imgs:
                    n = n + 1
                    if n == 1:
                        pass
                    else:
                        imgn = os.path.join(path, img)
                        image = Image.open(imgn)
                        img = image.convert('RGB')
                        img_lst.append(img)
                im_1.save(f'/storage/emulated/0/{fname}', save_all=True, append_images=img_lst)               
                res = 'done'
        else:
            res = 'given path is not a folder'
    except Exception as e:
        res = str(e)
    return res

def split_pdf(path, fro, to , fname):
    try:
        fro = fro - 1
        to = to - 1
        from PyPDF2 import PdfWriter, PdfReader       
        inputpdf = PdfReader(open(f"{path}", "rb"))           
        output = PdfWriter()
        print(len(inputpdf.pages))
        for i in range(len(inputpdf.pages)):
            i = i + 1
            print(i)
            if i < fro:
                print('Passed')
            elif i > to:
                print('Large so broke')
            elif i <= to and i >= fro:
                print(i)
                output.add_page(inputpdf.pages[i])          
                with open(f"{fname}", "wb") as outputStream:
                    output.write(outputStream)
                print('Page Added')               
            else:
                pass
        print('Complete') 
        res = 'Done'
        return res
    except Exception as e:
       print(e)
       res = 'Error'
       return res
       

def text_to_pdf(text, filename):
    import textwrap
    from fpdf import FPDF
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)
    splitted = text.split('\n')
    for line in splitted:
        lines = textwrap.wrap(line, width_text)
        if len(lines) == 0:
            pdf.ln()
        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')


def get_tasks_data():
    try:
        lst = os.listdir(f'/storage/emulated/0/Documents/My Tasks/Tasks/Today')
        if 'color.color' in lst:
            lst.remove('color.color')   
        if 'desc.color' in lst:
            lst.remove('desc.color')
        if 'time.color' in lst:
            lst.remove('time.color')   
        if 'super_label.color' in lst:
            lst.remove('super_label.color')   
            
        data = []
        for task in lst:
            task = task.split(".")[0]
            task = task.replace('&','/')
            task = task.replace('$','\\')
            task = task.replace('@','"')
            task = task.replace(']',"'")
            data.append(str(task))
        return data
    except:
        data = ['There Was An Error']
        return data