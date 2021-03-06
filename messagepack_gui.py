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
        j = 0

        self.txt_box.delete('1.0', 'end')
        packed_datas = self.msgpack_entry.get()
        if len(packed_datas) < 1:   #1byte未満の時はクリア処理のみ実行
            self.f_msgpack_values = Tk.Frame(self)
            void_label = Tk.Label(self.f_msgpack_values,text = ' ', width=99 )
            void_label.pack(side = 'left')            
        else :  
            packed_datas = re.sub(' ', '', packed_datas)    #文字列に半角スペースが入っていた場合除外
            packed_datas = text_2_bytes(packed_datas)       #文字列からバイト列に変換
            packed_data = int.from_bytes(packed_datas, byteorder = 'big')   #Bytesからint型に変換
            unpacker = msgpack.unpackb(packed_datas, use_list=True, raw=False)
            self.txt_box.insert(1.0,'Binary: ' + hex(packed_data) + '\r\n' + 'Unpack: ' + str(unpacker)  + '\r\n' )

            value_names_dict = {}
            i = 0
            for keys in unpacker:
                value_names_dict[i] = keys #変数名を格納
                i += 1
            i = 0

            label_total_length = 0

            self.f_msgpack_values = Tk.Frame(self)
            for keys in unpacker:
                keys = value_names_dict[i]

                self.label = Tk.Label(self.f_msgpack_values,text = keys)    #ラベルを表示
                self.label.pack(side = 'left')

                label_total_length += len(keys)

                if isinstance(unpacker[keys] ,list):    #変数がリスト型だった時、多次元配列かどうかを確認　※変則的なリストには未対応
                    depth = list_depth(unpacker[keys])  #リストの深さ
                    if depth > 1:
                        factors = count_length(unpacker[keys]) 
                    else :
                        factors = len(unpacker[keys])
                    self.txt_box.insert(5.0,'list depth:' + str(depth) + ', factors' + str(factors) + ' ')
                    value_label_length = factors * 3 
                else:
                    value_label_length = len(str(unpacker[keys]))

                label_total_length += len(keys)

                self.value = Tk.Label(self.f_msgpack_values, text = str(unpacker[keys]), width = value_label_length, anchor= 'w', relief = Tk.RIDGE, bd = 2)
                self.value.pack(side = 'left')
                i += 1
                print(str(label_total_length))
                if label_total_length > 45:
                    void_label = Tk.Label(self.f_msgpack_values,text = ' ', width=99 )
                    void_label.pack(side = 'left')
                    self.f_msgpack_values.place(x=10, y=150 + j*25)
                    j += 1
                    label_total_length = 0
                    self.f_msgpack_values = Tk.Frame(self)

            void_label = Tk.Label(self.f_msgpack_values,text = ' ', width=99 )  #delete後に自動的に消去されないので空欄で埋める
            void_label.pack(side = 'left')
            if j == 0 :
                self.f_msgpack_values.place(x=10, y=150)
            else:
                self.f_msgpack_values.place(x=10, y=150 + j*25)

            for i in range(10):
                self.f_msgpack_values = Tk.Frame(self)
                void_label = Tk.Label(self.f_msgpack_values,text = ' ', width=99 )  #delete後に自動的に消去されないので空欄で埋める
                void_label.pack(side = 'left')
                self.f_msgpack_values.place(x=10, y=150 + (j+1)*25 + i*25)

    #ウィンドウ初期化
    def __init__(self, master = None):
        window_width = 550
        window_height = 250
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
        self.msgpack_entry = Tk.Entry(f_pack,width=70)
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

#リストの深さをカウントする関数
def list_depth(some_value):
    if isinstance(some_value,list): #リストの中がリストの時は再帰処理
        depth = 1 + list_depth(some_value[0])
    else:
        depth = 0
    return depth

#多次元配列の要素をカウントする関数
def count_length(l):
    count = 0
    if isinstance(l, list):
        for v in l:
            count += count_length(v)
        return count
    else:
        return 1

if __name__ == '__main__':
    #GUI展開
    f = Frame()
    f.pack()
    f.mainloop()
