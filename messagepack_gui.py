#messagepack_gui.py
#
#Copyright (c) 2020 ienaga045
#
#This software is released under the MIT License.
#http://opensource.org/licenses/mit-license.php
#

import tkinter as Tk
from tkinter import ttk
from tkinter import messagebox
import msgpack
import binascii
import re

class Frame(Tk.Frame):
    #ボタンクリック時動作
    def button_msgpack_depack_clicked(self):
        global init_flag

        self.txt_box.delete('1.0', 'end')
        packed_datas = self.msgpack_entry.get()
        if len(packed_datas) < 1:
            self.f_msgpack_values = Tk.Frame(self)
            void_label = Tk.Label(self.f_msgpack_values,text = ' ', width=99 )
            void_label.pack(side = 'left')            
        else :
            packed_datas = re.sub(' ', '', packed_datas)    #文字列に半角スペースが入っていた場合除外
            packed_datas = text_2_bytes(packed_datas)       #文字列からバイト列に変換
            packed_data = int.from_bytes(packed_datas, byteorder = 'big')   #Bytesからint型に変換
            unpacker = msgpack.unpackb(packed_datas, use_list=True, raw=False)
            self.txt_box.insert(1.0,'Binary: ' + hex(packed_data) + '\r\n' + 'Unpack: ' + str(unpacker) + '\r\n' + 'List num: ' + str(len(unpacker)))

            value_names_dict = {}
            i = 0
            for keys in unpacker:
                value_names_dict[i] = keys 
                i += 1
                
            i = 0
            self.f_msgpack_values = Tk.Frame(self)
            for keys in unpacker:
                keys = value_names_dict[i]
                self.label = Tk.Label(self.f_msgpack_values,text = keys)
                self.label.pack(side = 'left')
                self.value = Tk.Label(self.f_msgpack_values, text = str(unpacker[keys]), width = len(str(unpacker[keys])), anchor= 'w', relief = Tk.RIDGE, bd = 2)
                self.value.pack(side = 'left')
                i += 1
            
            void_label = Tk.Label(self.f_msgpack_values,text = ' ', width=99 )  #delete後に自動的に消去されないので空欄で埋める
            void_label.pack(side = 'left')
            init_flag = True
    
        self.f_msgpack_values.place(x=10, y=150)

    #ウィンドウ初期化
    def __init__(self, master = None):
        window_width = 500
        window_height = 200
        Tk.Frame.__init__(self, master, height = window_height, width = window_width)
        self.master.title('MessagePack & Tk sample')

        #テキストボックス
        txt_box_width = window_width-10
        txt_box_height = 100
        f_txt_box = Tk.Frame(self,relief = Tk.RIDGE, bd = 2,  width = txt_box_width, height = txt_box_height)
        self.txt_box = Tk.Text(f_txt_box) 
        self.txt_box.insert(1.0, "UnPack Message\n")
        self.txt_box.place(width = txt_box_width-4, height = txt_box_height-4)
        f_txt_box.place(x=5, y=5)

        #パックされたメッセージを入れるフォーム
        f_pack = Tk.Frame(self)
        label = Tk.Label(f_pack,text = 'Bin')
        label.pack(side = 'left')
        self.msgpack_entry = Tk.Entry(f_pack,width=66)
        self.msgpack_entry.pack(side = 'left')
        button_msgpack_depack = Tk.Button(f_pack, text = 'UnPack', width = 6, command = self.button_msgpack_depack_clicked)
        button_msgpack_depack.pack(side = 'left')

        f_pack.place(x=10, y=110)

#文字列をHexで返す関数
def text_2_bytes(text_datas):
    text_datas = text_odd_2_even(text_datas)
    text_datas = text_datas.encode('utf-8')
    return binascii.unhexlify(text_datas)

#奇数の桁だった時に先頭に'0'を付与する関数
def text_odd_2_even(text_datas):
    if (len(text_datas) % 2) == 1 : 
        text_datas = '0' + text_datas
    return text_datas

if __name__ == '__main__':

    init_flag = False
    #GUI展開
    f = Frame()
    f.pack()
    f.mainloop()
