# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 06:50:27 2021

@author: tsutitire

https://ai-trend.jp/programming/python/voice-record/


"""
import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pyaudio 
import wave     
import numpy as np
import threading
import csv
import os


audios = []
data = []
iAudio = pyaudio.PyAudio()
for x in range(0, iAudio.get_device_count()): 
    audios.append(iAudio.get_device_info_by_index(x).get("name"))
isrec = True
pa = pyaudio.PyAudio()
settendev = 0
iferr = 0

def starting(fr,stream):
    global data
    
    Static6["text"] = "録音を開始しました"
    '''
    count = 0
    while stream.is_active():
        frame = stream.read(fr)
        data.append(frame)
        count = count + 1
        if count >= 1000:
            break
    '''
    frame.after_idle(update)

def update():
    global data,fr,stream
    if stream and stream.is_active():
        frames = stream.read(fr)
        data.append(frames)
        #print(data)
        if iferr == 0:
            frame.after(1, update)

def closing(filename,channel,rformat,rate,stream,pa,data):
    stream.stop_stream()
    stream.close()
    pa.terminate()
    
    try:
        waveFile = wave.open(filename, 'wb')
        waveFile.setnchannels(channel)
        waveFile.setsampwidth(pa.get_sample_size(rformat))
        waveFile.setframerate(rate)
        waveFile.writeframes(b"".join(data))
        waveFile.close()
        Static6["text"] = "正常に終了しました"
        Static6["fg"] = "#32cd32"
        Static15["bg"] = "#32cd32"
        data = []
    except:
        Static6["text"] = "ファイルの保存に失敗。読み上げ文の選択や保存先の指定を確認してください"
        Static15["bg"] = "#ff0000"
        data = []


def button1_click():
    global isrec,settendev,stream,fr,iferr
    Static1["state"] = "disabled"
    Static2["state"] = "active"
    Static2["fg"] = "#b22222"
    isrec = True
    filename = "testing"
    filename = "./" + filename + ".wav"
    #setting
    rformat = pyaudio.paInt16 
    channel = 1
    rate = 48000
    iferr = 0
    fr = 2**10 #1024
    try:
        stream = pa.open(format=rformat, channels=channel, rate=rate,
                         input=True, input_device_index=settendev, frames_per_buffer=fr)
    except OSError as e:
        if str(e).find("-9998") != -1:
            Static6["text"] = "端末不正、マイクではないデバイスを選択していないか確認してください"
        if str(e).find("-9999") != -1:
            Static6["text"] = "アクセス不可、他のアプリの使用または権限を確かめてください"
        Static15["bg"] = "#ff0000"
        iferr = 1

    try:
        stream
    except:
        return
    Static15["bg"] = "#ff8c00"
        
    starting(fr,stream)
    
def button2_click():
    global isrec,data,a_list
    isrec = False
    getfilen = Static8["text"]
    getfilei = getfilen.split(" : ")
    filename = getfilei[0]
    filename = Static14["text"] + "/" + filename + ".wav"
    #setting
    rformat = pyaudio.paInt16 
    channel = 1
    rate = 48000
    try:
        stream
    except:
        Static1["state"] = "active"
        Static2["state"] = "disabled"
        Static1["fg"] = "#32cd32"
        return
    closing(filename, channel, rformat, rate, stream, pa, data)
    
    Static1["state"] = "active"
    Static2["state"] = "disabled"
    Static1["fg"] = "#32cd32"
   
    
def button3_click():
    iAudio = pyaudio.PyAudio()
    audios = []
    for x in range(0, iAudio.get_device_count()): 
        audios.append(iAudio.get_device_info_by_index(x).get("name"))
    Static3.delete(0,'end')
    Static3.delete(0,'end')
    Static3.delete(0,'end')
    for item in audios:
        Static3.insert(tk.END, item)
        
def button4_click():
    global a_list
    file_path = Static11["text"]
    csv_file = open(file_path,'r')
    
    a_list = [[]]
    
    for row in csv.reader(csv_file):
        b_list = row
        a_list.append(b_list)  
    a_list.pop(0)
    
    Static12.delete(0,"end")
    Static12.delete(0,"end")
    Static12.delete(0,"end")
    
    Static7.delete(0,"end")
    Static7.delete(0,"end")
    Static7.delete(0,"end")
    
    for i in a_list[0]:
        c_list = i.split(" : ")
        Static12.insert(tk.END, c_list[0])
    
    
    
def button5_click():
    file_path = filedialog.askopenfilename(filetypes = [('CSV(カンマ区切り)ファイル', '*.csv')])
    Static11["text"] = ""
    Static11["text"] = file_path  
    
def button6_click():
    file_path = tk.filedialog.askdirectory(initialdir = os.getcwd())
    Static14["text"] = ""
    Static14["text"] = file_path  
    

def listbox1_select(event):
    global settendev
    Static5["text"] = audios[int(Static3.curselection()[0])]
    settendev = int(Static3.curselection()[0])
    
def listbox2_select(event):
    global a_list,settendev2
    settendev2 = int(Static12.curselection()[0])
    
    Static7.delete(0,"end")
    Static7.delete(0,"end")
    Static7.delete(0,"end")
    
    for i in a_list:
        Static7.insert(tk.END, i[settendev2])
    
def listbox3_select(event):
    global a_list
    settendev3 = int(Static7.curselection()[0])
    Static8["text"] = a_list[settendev3][settendev2]
    
    
root = tk.Tk()
frame = tk.Frame(root)
root.title(u"ATR-503 recording supporter")
root.geometry("700x370")


Static1 = tk.Button(text="録音開始", font=("",25), fg="#32cd32",
                    command=button1_click
                    )
Static1.place(x=30, y=20)

Static2 = tk.Button(text="録音停止", font=("",25), fg="#b22222",
                    command=button2_click
                    )
Static2["state"] = "disabled"
Static2.place(x=200, y=20)



Static3 = tk.Listbox(width=50,height=4)
for item in audios:
    Static3.insert(tk.END, item)
Static3.bind('<<ListboxSelect>>', listbox1_select)
Static3.place(x=380, y=10)

Static4 = tk.Button(text="デバイス更新", font=("",10),
                    command=button3_click
                    )
Static4.place(x=380, y=90)

Static5 = tk.Label(text="デバイスを選択してください", font=("",10), bg="#d3d3d3")
Static5.place(x=470, y=92)

Static6 = tk.Label(text="結果が表示されます", font=("",8), bg="#d3d3d3",width = 55)
Static6.place(x=30, y=92)


Static15 = tk.Label(bg="#708090",width = 91)
Static15.place(x=30,y=125)


Static7 = tk.Listbox(width=95,height=7)
Static7.bind('<<ListboxSelect>>', listbox3_select)
Static7.place(x=100, y=180)

Static12 = tk.Listbox(width=10,height=7)
Static12.bind('<<ListboxSelect>>', listbox2_select)
Static12.place(x=30, y=180)

Static8 = tk.Label(text="読み上げる文が表示されます", font=("",10), bg="#d3d3d3",width = 91)
Static8.place(x=30, y=160)


Static9 = tk.Button(text="ファイル読み込み", font=("",10),
                    command=button4_click
                    )
Static9.place(x=490, y=300)

Static10 = tk.Button(text="ファイル選択", font=("",10),
                    command=button5_click
                    )
Static10.place(x=400, y=300)

Static11 = tk.Label(text="ファイルを選択してください", font=("",10), bg="#d3d3d3",width = 50)
Static11.place(x=30, y=300)


Static13 = tk.Button(text="書き込みフォルダ読み込み", font=("",10),
                    command=button6_click
                    )
Static13.place(x=450, y=330)


Static14 = tk.Label(text="書き込み先フォルダを選択してください", font=("",10), bg="#d3d3d3",width = 50)
Static14.place(x=30, y=330)

root.iconbitmap('./icon.ico')
root.mainloop()
if stream.is_active():
    stream.stop_stream()
    stream.close()
    pa.terminate()
    
    
