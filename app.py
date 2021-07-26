import json
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import re


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("EZ Snow Runner")
        self.root.geometry("404x400")
        self.root.iconbitmap('sricon.ico')
        self.root.resizable(False, False)
        self.running = True
        self.filedialog = StringVar()

        self.sr_image = Image.open("sr.jpeg")
        self.sr_image = self.sr_image.resize((400, 200), Image.ANTIALIAS)
        self.sr_image = ImageTk.PhotoImage(self.sr_image)
        self.sr_image_label = ttk.Label(self.root, image=self.sr_image)
        self.sr_image_label.grid(row=0, column=0, columnspan=2, rowspan=2)
        # self.label_image = PhotoImage(file=Image.open("./sr.jpeg"))
        self.label_money = ttk.Label(self.root, text="Money:")
        self.label_money.grid(row=2, column=0, sticky=E, padx=10, pady=5)
        self.money = StringVar()
        self.money_entered = ttk.Entry(self.root, width=10, textvariable=self.money)
        self.money_entered.grid(row=2, column=1, sticky=W, padx=5, pady=5)

        self.label_rank = ttk.Label(self.root, text="Rank:")
        self.label_rank.grid(row=3, column=0, sticky=E, padx=10, pady=5)
        self.rank = StringVar()
        self.rank_entered = ttk.Entry(self.root, width=10, textvariable=self.rank, state='disabled')
        self.rank_entered.grid(row=3, column=1, sticky=W, padx=5, pady=5)

        self.label_experience = ttk.Label(self.root, text="Experience:")
        self.label_experience.grid(row=4, column=0, sticky=E, padx=10, pady=5)
        self.experience = StringVar()
        self.experience_entered = ttk.Entry(self.root, width=10, textvariable=self.experience)
        self.experience_entered.grid(row=4, column=1, sticky=W, padx=5, pady=5)

        self.file_button = ttk.Button(self.root, text="Open File", command=self.open_file)
        self.file_button.grid(row=5, column=0, sticky=E, padx=10, pady=5)
        
        self.file_path = ttk.Entry(self.root, width=30)
        self.file_path.grid(row=5, column=1, sticky=W, padx=5, pady=5)


        self.save_button = ttk.Button(self.root, text="Save File", command=self.write_new_dat_file) 
        self.save_button.grid(row=6, column=1, sticky=W, padx=5, pady=10)

        self.new_file_dir = ''
        self.new_money = 0
        self.new_rank = 0
        self.new_experience = 0
        # se existe um arquivo datfile ele le o endereco e mostra na entrada do arquivo
        if os.path.isfile('./datfile'):
            with open('datfile', 'r') as dat:
                for item in dat.readlines():
                    self.file_path.insert(END, item)
        # se nao existe um arquivo datfile ele cria um arquivo vazio para ser usado quando pressionar o botao de abrir arquivo
        else:
            with open('datfile', 'w') as dat:
                dat.write('')

        self.read_file_data()
        while self.running:
            self.root.protocol("WM_DELETE_WINDOW", self.window_closed)
            self.root.mainloop()
    
    def window_closed(self):
        self.running = False
        self.root.destroy()

    def open_file(self):
        # ao abrir deleta da entrada do arquivo para nao fazer append
        self.file_path.delete(0, END)
        self.filedialog = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("dat files","*.dat"),("all files","*.*")))
        self.file_path.insert(END, self.filedialog)
       
        # se abrir um arquivo ele salva o endereco no arquivo datfile
        if self.filedialog:
            with open('datfile', 'w') as dat:
                dat.write(self.filedialog)
                if os.path.basename(self.filedialog) == 'CompleteSave.dat': # checa se arquivo é CompleteSave.dat
                    with open(self.filedialog, 'r') as file: #entao abre o arquivo CompleteSave.dat e define os valores para os campos do programa
                        dat_file = file.read()
                        money_read = re.search(r'"money":.\d+', dat_file).group(0)
                        self.money.set(re.search(r'\d+', money_read).group(0))
                        rank_read = re.search(r'"rank":\d+', dat_file).group(0)
                        self.rank.set(re.search(r'\d+', rank_read).group(0))
                        experience_read = re.search(r'"experience":.\d+', dat_file).group(0)
                        self.experience.set(re.search(r'\d+', experience_read).group(0))
                else: # se o arquivo aberto nao é CompleteSave.dat entao define os valores vazios para os campos do programa
                    self.money.set('')
                    self.rank.set('')
                    self.experience.set('')
                    
                    messagebox.showerror("Error",f"{os.path.basename(self.filedialog)} is not a expected file! \n \nCompleteSave.data usually it is on 'C:\\Users\[user]\\Documents\\My Games\\SnowRunner\\base\\storage\\[userid]'")
        # se nao abrir um arquivo ele deixa salvo o ultimo endereco aberto no arquivo datfile
        else:
            with open('datfile', 'r') as dat:
                for item in dat.readlines():
                    self.file_path.insert(END, item)

       
   
    def read_file_data(self):
        if os.path.isfile('datfile'): # checa se ja existe um arquivo datfile
            with open('datfile', 'r') as dat: # se existir abre o arquivo
                for item in dat.readlines():
                    if os.path.isfile(item): # checa se o endereco corresponde a um arquivo existente
                        with open(item, 'r') as file: # entao abre esse arquivo
                            if os.path.basename(item) == 'CompleteSave.dat': # checa se arquivo é CompleteSave.dat
                                self.new_file_dir = os.path.dirname(item)
                                # self.write_json() # se for entao chama a funcao write_json para criar o arquivo CompleteSave.json
                                # with open (item, 'r') as file:
                                dat_file = file.read()
                                money_read = re.search(r'"money":.\d+', dat_file).group(0)
                                self.money.set(re.search(r'\d+', money_read).group(0))
                                rank_read = re.search(r'"rank":\d+', dat_file).group(0)
                                self.rank.set(re.search(r'\d+', rank_read).group(0))
                                experience_read = re.search(r'"experience":.\d+', dat_file).group(0)
                                self.experience.set(re.search(r'\d+', experience_read).group(0))
                                self.root.update()
                                  

    def write_new_dat_file(self):
        with open (self.file_path.get(), 'r') as file:
            dat = file.read()
            padrao = re.compile(r'"money":.\d+')
            money = re.search(r'"money":.\d+', dat).group(0)
            self.new_money = re.sub(r'"money":.\d+', f'"money": {self.money.get()}', money)

            experience = re.search(r'"experience":.\d+', dat).group(0)
            self.new_experience = re.sub(r'"experience":.\d+', f'"experience": {self.experience.get()}', experience)
             
            with open(self.file_path.get(), 'w') as arc:
                arc.write(dat.replace(money, self.new_money).replace(experience, self.new_experience))
                messagebox.showinfo("Success", "Restart the game for changes make effect")
           
            
          
            
                      


if __name__ == "__main__":
   app = App()