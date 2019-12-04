import tkinter as tk
from tkinter import ttk
import os
import pickle
from queue import Queue
import threading
import psutil
from tkinter import *

win = tk.Tk()
win.title("TacoTuesTTS")

tabControl = ttk.Notebook(win)

tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Text To Speech')
tabControl.pack(expand=1, fill="both")

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='Streamlabs')
tabControl.pack(expand=1, fill="both")

label_1 = Label(tab2, text="Streamlabs Access Token")
label_1.grid(row=0, column=0, sticky=W)

label_2 = Label(tab2, text="Minimum donation for TTS")
label_2.grid(row=6, column=0, sticky=W)

label_3 = Label(tab2, text="Streamlabs Logs")
label_3.grid(row=10, column=0, sticky=W)

btn1t2 = ttk.Entry(tab2, show="•")
btn1t2.grid(row=1, column=0, sticky=W)

btn2t2 = ttk.Entry(tab2)
btn2t2.grid(row=7, column=0, sticky=W)

btn3t2 = Text(tab2, height=20, width=70)
btn3t2.grid(row=11, column=0, sticky=W)
btn3t2.config(state="disabled")

#clicked = StringVar()
#clicked.set("Poor Quality")
#drop = OptionMenu(tab1, clicked, "Poor Quality", "Medium Quality", "Higher Quality")
#drop.grid(row=0, column=0, sticky=W)

def savekey():
    thekey = btn1t2.get()
    pickle_out = open("savekey.pickle", "wb")
    pickle.dump(thekey, pickle_out)
    pickle_out.close()

try:
    pickle_in = open("savekey.pickle","rb")
    thekey = pickle.load(pickle_in)
    btn1t2.insert(tk.END, thekey)
except EOFError:
    pass
except IOError:
    pass

button1 = Button(tab2, text="Connect", command=savekey)
button1.grid(row=2,column=0, sticky=W)

label2_1 = Label(tab1, text="Enter text")
label2_1.grid(row=1, column=0, sticky=W)

btn1t1 = Text(tab1, height=22, width=65, font="Arial")
btn1t1.grid(row=2,column=0, sticky=W)

def startkey():
    themessage = btn1t1.get("1.0","end-1c")
    os.system('python gen_tacotron.py --input_text ' + '"' + themessage + '"')
    btn1t1.delete('1.0', END)

btn2t1 = Button(tab1, text="Start", command=startkey)
btn2t1.grid(sticky=SW)

def savevalue():
    firstminvalue = float(btn2t2.get())
    twodec = ("{:.2f}".format(firstminvalue))
    pickle_out = open("minvalue.pickle", "wb")
    pickle.dump(twodec, pickle_out)
    pickle_out.close()

btn4t2 = Button(tab2, text="Save Minimum Donation Value", command=savevalue)
btn4t2.grid(row=9, sticky=W)
q = Queue()
qname = Queue()
previousid = [0]
for x in previousid:
    def donations():
        global previousid
        threading.Timer(1, donations).start()
        global q
        global qname
        import requests
        try:
            url = "https://streamlabs.com/api/donations"
            querystring = {"access_token": {"" + btn1t2.get() + ""}}
            response = requests.request("GET", url, params=querystring)
            test = str(response.text)
            EndMessage = test.split('{')[-2] + test.split('{')[-1]
        except IndexError:
            pass
        try:
            minvalue = float(btn2t2.get())
            MinMin = EndMessage.split(',')
            MinMin = MinMin[2].split('"')
            MinMin = float(MinMin[3])
            if MinMin >= minvalue:
                text = EndMessage.split(',"')
                currentid = text[0].split(':')
                currentid = int(currentid[1])
                if currentid != previousid:
                    btn3t2.config(state="normal")
                    global MessageInsertFixed1
                    global MessageInsertFixed
                    btn3t2.insert(tk.INSERT, "Message:\n")
                    Tester = str(text)
                    Inserter = Tester.split(", '")
                    PrintofMessage = Inserter[7].split('"')
                    MessageInsert = PrintofMessage[2]
                    btn3t2.insert(tk.INSERT, MessageInsert + "\n")
                    MessageInsertFixed = MessageInsert.replace("""\\\\/""" """\\\\\\\\""", "Slash")
                    MessageInsertFixed = MessageInsertFixed.replace("*", "")
                    MessageInsertFixed1 = MessageInsert.replace("elon::", "")
                    MessageInsertFixed1 = MessageInsertFixed1.replace("train::", "")
                    btn3t2.insert(tk.INSERT, "Donation Amount:\n")
                    btn3t2.insert(tk.INSERT, str(MinMin) + "\n")
                    btn3t2.insert(tk.INSERT, "Name:\n")
                    PrintofMessage2 = Inserter[6].split('"')
                    Nametoinsert = PrintofMessage2[2]
                    btn3t2.insert(tk.INSERT, Nametoinsert + "\n")
                    btn3t2.insert(tk.INSERT, "---------------------------------------------------------------------\n")
                    qname.put(MessageInsertFixed)
                    q.put(MessageInsertFixed1)
                    btn3t2.see("end")
                    btn3t2.config(state="disabled")
                    previousid = currentid
            process = "cmd.exe" in (p.name() for p in psutil.process_iter())
            if process == False:
                os.chdir(os.getcwd().replace("\\RealTTS", ""))
                os.chdir(os.getcwd().replace("\\trainTTS", ""))
                btn1t1.delete('1.0', END)
                namePick = qname.get()
                queMessage = str(q.get())
                if 'elon::' in namePick:
                    btn1t1.delete('1.0', END)
                    btn1t1.insert(tk.INSERT, queMessage)
                    os.system('python elon.py --input_text ' + '"' + queMessage + '"')
                if 'train::' in namePick:
                    btn1t1.delete('1.0', END)
                    os.chdir(os.getcwd() + "\\trainTTS")
                    btn1t1.insert(tk.INSERT, queMessage)
                    os.system('python trainTTS.py --input_text ' + '"' + queMessage + '"')
                if 'train::' not in namePick:
                    if "elon::" not in namePick:
                        os.chdir(os.getcwd().replace("\\RealTTS", ""))
                        os.chdir(os.getcwd().replace("\\trainTTS", ""))
                        os.chdir(os.getcwd() + "\\RealTTS")
                        btn1t1.delete('1.0', END)
                        btn1t1.insert(tk.INSERT, queMessage)
                        os.system('python default.py --input_text ' + '"' + queMessage + '"')
            elif process == True:
                print("process is true")
                #btn1t1.config(state="disabled")
                #btn2t1.config(state="disabled")
            if process == False:
                btn1t1.config(state="normal")
                btn2t1.config(state="normal")
        except ValueError:
            print(ValueError)

def stopkey():
    os.system('taskkill /f /IM cmd.exe /t')

btn3t1 = Button(tab1, text="Stop Message", command=stopkey)
btn3t1.grid(sticky=SW)

donations()

try:
    pickle_in = open("minvalue.pickle", "rb")
    firstminvalue = pickle.load(pickle_in)
    btn2t2.insert(tk.END, firstminvalue)
except EOFError:
    pass
except IOError:
    pass

win.mainloop()