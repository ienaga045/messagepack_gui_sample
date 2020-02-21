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

class Frame(Tk.Frame):

    #ボタンクリック時動作
    def button_msgpack_depack_clicked(self):
        self.txt_box.delete('1.0', 'end')
        packed_datas = text_2_bytes(self.msgpack_entry.get())
        packed_data = int.from_bytes(packed_datas, byteorder = 'big')
        unpacker = msgpack.unpackb(packed_datas, use_list=True, raw=False)
        self.txt_box.insert(1.0,'Binary: ' + hex(packed_data) + '\r\n' + 'Unpack: ' + str(unpacker))

    #ウィンドウ初期化
    def __init__(self, master = None):
        window_width = 500
        window_height =150
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

    #GUI展開
    f = Frame()
    f.pack()
    f.mainloop()
