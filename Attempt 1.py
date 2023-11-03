import customtkinter
import subprocess
import os
from PIL import Image
import copy

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

vba = "vba.exe"

game = "emerald.gba"

root = customtkinter.CTk()
root.geometry("1000x750")

class game:
    def __init__(self, rom, img, directory):
        self.rom = rom
        self.img = img
        self.directory = directory
files = os.listdir()
dirs = []
for f in files:
    if os.path.isdir(f):
        dirs.append(f)

games = []
for d in dirs:
    filecontent = os.listdir(d)
    rom = ""
    img = ""
    for f in filecontent:
        if '.gba' in f:
            rom = f
        elif '.jpg' in f:
            img = f
        elif '.jpeg' in f:
            img = f
        elif '.png' in f:
            img = f
    games.append(game(rom, img, d))

buttons = []

def opengame(option):
    subprocess.Popen([vba, option])
global listofroms
listofroms = []
index = 0
for g in games:
    imagedir = g.directory + "/" + g.img
    gamedir = g.directory + "/" + g.rom
    listofroms.append(gamedir)
    image = customtkinter.CTkImage(light_image=Image.open(imagedir),
                                  dark_image=Image.open(imagedir),
                                  size=(200, 200))
    buttons.append(customtkinter.CTkButton(master=root, image=image, width=200, height=200, text="", command=lambda dir=gamedir: opengame(copy.copy(dir)), border_spacing=0, border_width=0, corner_radius=0))
    # previously was a late binding issue with the lambda command where the last value of gamedir would be used for each button, but chatgpt helped fix that :)
    # i have an error where the lambda command always links to the last variables in the iterations how can i change that so each one is passed a permanent individual variable
    # ^ prompt along with code handed to the GPT

def openemerald():
    subprocess.Popen([vba, "emerald.gba"])

def openfire():
    subprocess.Popen([vba, "fire.gba"])

def openmario():
    subprocess.Popen([vba, "mario.gba"])



emerald = customtkinter.CTkImage(light_image=Image.open("image.jpeg"),
                                  dark_image=Image.open("image.jpeg"),
                                  size=(200, 200))

fire = customtkinter.CTkImage(light_image=Image.open("fireimg.jpg"),
                                  dark_image=Image.open("fireimg.jpg"),
                                  size=(200, 200))

mario = customtkinter.CTkImage(light_image=Image.open("marioparty.jpg"),
                                  dark_image=Image.open("marioparty.jpg"),
                                  size=(200, 200))

button = customtkinter.CTkButton(master=root, image=emerald, width=200, height=200, text="", command=openemerald, border_spacing=0, border_width=0, corner_radius=0)
button2 = customtkinter.CTkButton(master=root, image=fire, width=200, height=200, text="", command=openfire, border_spacing=0, border_width=0, corner_radius=0)
button3 = customtkinter.CTkButton(master=root, image=mario, width=200, height=200, text="", command=openmario, border_spacing=0, border_width=0, corner_radius=0)
#frame = customtkinter.CTkFrame(master=root)
#frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=root, text="GBA Rom Library", width=200, height=100, pady=50, font=("Roboto", 24))
label.grid(row=0, column=1)

button.grid(row=1,column=0, padx=5)
button2.grid(row=1,column=1, padx=5)
button3.grid(row=1,column=2, padx=5)
count = 0
for b in buttons:
    print(count)
    b.grid(row=2, column=count, padx=5)
    count += 1
root.mainloop()
