import customtkinter
import time
import tkinter as tk
import subprocess
from PIL import Image, ImageTk
import os

class HorizontalFrame(tk.Frame):
	def __init__(self, master, **kwargs):
		tk.Frame.__init__(self, master, **kwargs)
		self.currentButton = 0
		self.buttons = []

	def AddButton(self,image,  **kwargs):
		self.buttons.append(tk.Button(self, width=150, height=150, text="nothign", bg="blue",image=image, **kwargs))
		self.buttons[-1].place(x=150*(len(self.buttons)-1), y=0)
		self.buttons[-1].image = image

	def Scroll(self, x1):
		for b in self.buttons:
			newX = int(b.place_info()['x']) - x1
			b.place(x=newX)

	def Update(self, inc):
		self.buttons[self.currentButton].configure(bd=2)
		self.currentButton += inc
		self.buttons[self.currentButton].configure(bd=10)

	def DeselectRow(self):
		for b in self.buttons:
			b.configure(bd=2)

	def SelectRow(self):
		self.buttons[self.currentButton].configure(bd=10)

class Menu(tk.Frame): # need to add vertical functionality
	def __init__(self, master, **kwargs):
		tk.Frame.__init__(self, master, **kwargs)
		self.row_num = 0
		self.rows = [] # each are a horizontalframe class

	def AddRow(self, title):
		f = HorizontalFrame(master=self, width=900, height=150)
		f.grid(row=self.row_num, column=1)
		l = tk.Label(text=title)
		l.grid(row=self.row_num, column=0)
		self.row = 0
		self.row_num += 1
		self.rows.append(f)

	def AddButton(self, row, image, **kwargs):
		self.rows[row].AddButton(image, **kwargs)

	def Right(self):
		if int(self.rows[self.row].buttons[self.rows[self.row].currentButton].place_info()['x']) < 600 and self.rows[self.row].currentButton < len(self.rows[self.row].buttons) - 1:
			self.rows[self.row].Update(1)
		elif self.rows[self.row].currentButton < len(self.rows[self.row].buttons) - 1:
			self.rows[self.row].Scroll(150)
			self.rows[self.row].Update(1)

	def Left(self):
		if int(self.rows[self.row].buttons[self.rows[self.row].currentButton].place_info()['x']) > 100 and self.rows[self.row].currentButton > 0:
			self.rows[self.row].Update(-1)
		elif self.rows[self.row].currentButton > 0:
			self.rows[self.row].Scroll(-150)
			self.rows[self.row].Update(-1)
	
	def Down(self):
		if self.row < len(self.rows) - 1:
			self.rows[self.row].DeselectRow()
			self.row += 1
			self.rows[self.row].SelectRow()
	
	def Up(self):
		if self.row > 0:
			self.rows[self.row].DeselectRow()
			self.row -= 1
			self.rows[self.row].SelectRow()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x720")

        self.bind('<Right>',self.RightKey)
        self.bind('<Left>',self.LeftKey)
        self.bind('<Down>', self.DownKey)
        self.bind('<Up>', self.UpKey)
        self.bind('<Return>', self.EnterKey)

        self.Menu = Menu(self, width=1000, height=700)
        self.Menu.place(x=50, y=100)

        # Loading all the games
        vba = "vba.exe"
        # loads top level directories for the rows
        self.folders_1 = []
        for f in os.listdir():
        	if os.path.isdir(f):
        		self.folders_1.append(f)
        # loads a row for each folder
        count = 0
        for f in self.folders_1:
        	self.Menu.AddRow(f)
       		for game in os.listdir(f):
       			files = os.listdir(str(f + "/" + game))
       			rom = ""
       			image = ""
       			for l in files:
       				romtypes = ["gba", "gbc", "3ds", "nds"]
       				if l.split(".")[1] in romtypes:
       					rom = str(f + "/" + game + "/" + l)
       				elif ".sav" not in l:
       					image = str(f + "/" + game + "/" + l)
       			print(image, rom)
       			img = ImageTk.PhotoImage(Image.open(image).resize((150,150), Image.ANTIALIAS))

       			gbroms = ["gba", "gbc"]
       			threedsroms = ["3ds"]
       			ndsroms = ["nds"]
       			print(rom.split(".")[1])
       			if rom.split(".")[1] in gbroms:
       				emulator = "vba.exe"
       			elif rom.split(".")[1] in threedsroms:
       				emulator = r"C:\Users\raymi\AppData\Local\Citra\nightly\citra-qt.exe"
       			elif rom.split(".")[1] in ndsroms:
       				emulator = r"C:\Users\raymi\Desktop\DS EMULATOR\ds.exe"
       			self.Menu.AddButton(count, img, command=lambda file=rom, emulator=emulator: subprocess.Popen([emulator, file]))
       		count += 1

        





    def EnterKey(self, event):
    	print(self.Menu.rows[self.Menu.row].currentButton)
    	self.Menu.rows[self.Menu.row].buttons[self.Menu.rows[self.Menu.row].currentButton].invoke()
    	#self.Menu.rows[self.Menu.row].buttons[self.Menu.rows[self.Menu.row].currentButton]["command"]()
    	print("pressed")

    def RightKey(self, event):
    	self.Menu.Right()

    def LeftKey(self, event):
    	self.Menu.Left()

    def DownKey(self, event):
    	self.Menu.Down()

    def UpKey(self, event):
    	self.Menu.Up()

app = App()
app.mainloop()
