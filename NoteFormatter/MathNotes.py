# -*- coding: utf-8 -*-

import configparser
import io
import tkinter as tk
from tkinter import *

def readFile(file):
    with open(file, 'r') as f:
        return f.read()


def writeFile(file, text, append, useUtf = False):
    if append:
        if useUtf:
            with io.open(file, 'a', encoding="utf-8") as f:
                f.write(text)

        else:

            with open(file, 'a') as f:
                f.write(text)

    else:
        if useUtf:
            with io.open(file, 'w', encoding="utf-8") as f:
                f.write(text)
        else:

            with open(file, 'w') as f:
                f.write(text)

config = configparser.ConfigParser()
config.read_file(io.open("config.ini", 'r', encoding="utf-8"))
DELIMITERS = []
REPLACEMENTS = {}

master = tk.Tk()
if config['DEFAULT'] == config['CUSTOM']:
    #If the default config and the custom config are the same, initialize default config and pass the keys to DELIMITERS
    config['DEFAULT'] = {"sqrt" : "√", "eZ" : "∈Z", "equiv" : "≡", "implies" : "⇒", "alpha" : "α", "omega" : "Ω", "sigma" : "σ", "sum" : "Σ", "product" : "∏", "smiley" : "😀"}
    DELIMITERS = config['DEFAULT'].keys()
    configInUse = 'DEFAULT'
    #I really dont think this is necessary but hey it's here just in case something fucks up so
    with io.open('config.ini','w', encoding="utf-8") as configfile:
        config.write(configfile)

else:
    #If the CUSTOM config is different from DEFAULT, load its keys into DELIMITERS instead
    DELIMITERS = config['CUSTOM'].keys()
    configInUse = 'CUSTOM'


for x in DELIMITERS:
    REPLACEMENTS[x] = config[configInUse][x]


def findDelims(string):
    #This is just some weirdness with capitalization
    #Gonna make it programatic in the future but this works so eh
    for x in DELIMITERS:
        if x == "ez":
            str = "eZ"
        else:
            str = x
        repl = "{" + str + "}"
        print(repl)
        string = string.replace(repl, REPLACEMENTS[x])

    return string
        #...holy fuck
        #python is actually a god langage
        #these 4 lines take well over 150 in java
        #what the fuck

def process_input(TextArea):
    input = TextArea.get("1.0",END)

    processed = findDelims(input)

    set_text_box(TextArea, processed)

def set_text_box(TextArea, text):
    TextArea.delete("1.0", END)
    TextArea.insert("1.0", text)

def change_config_window():
    configGUI = tk.Tk()

    rows = []
    keys = config[configInUse].keys()

    configLen = len(config[configInUse])
    for i in range(configLen):

        print()


def run_gui(inpRoot):
    inpRoot.title("Math Notes Converter")

    #Creating text box and scrollbar
    TextArea = Text()
    ScrollBar = Scrollbar(inpRoot)
    ScrollBar.config(command=TextArea.yview)
    TextArea.config(yscrollcommand=ScrollBar.set)
    ScrollBar.pack(side=RIGHT, fill=Y)
    TextArea.pack(expand=YES, fill=BOTH)

    ConvertButton = Button(inpRoot,height = 1, width = 10, text="Convert!",command=lambda:process_input(TextArea))
    ConfigButton = Button(inpRoot, height = 1, width = 10, text="Settings",command=change_config_window, state=DISABLED)
    ConvertButton.pack()
    ConfigButton.pack()

    patchNotes = "================\nPATCH 0.0.1:\n================\n\n- Settings menu is disabled for now! Cant get it to work quite yet.\n- Made it so you can add your own unicode characters easily by adding your own \ndelimiter to the custom config ini area!"

    set_text_box(TextArea, "You can either type your notes here, or you can copy and paste them in!\n\nTo use a special symbol, just use its delimiter (located in config.ini) wrapped \nin {curly braces}!\n\nLike this: So {sqrt}2 {equiv} k^(1/2) where k{eZ}\n(Hit convert and watch how it changes!)\n\n" + patchNotes)

    inpRoot.mainloop()

#writeFile("noteFile.txt", findDelims("So {sqrt}2 {equiv} k^(1/2), where k {eZ}"), False, True)

run_gui(master)


#TODO:
#Add a "how to" window
#Add settings and an easy way to add/remove new characters or restore to defaults
#Direct import/export with txt files (possibly more in the future)
