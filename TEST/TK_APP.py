import sys
from tkinter import *

ABOUT_TEXT = """About

SPIES will search your chosen directory for photographs containing
GPS information. SPIES will then plot the co-ordinates on Google
maps so you can see where each photograph was taken."""

DISCLAIMER = """
Disclaimer

Simon's Portable iPhone Exif-extraction Software (SPIES)
software was made by Simon. This software
comes with no guarantee. Use at your own risk"""


def clickAbout():
    toplevel = Toplevel()
    label1 = Label(toplevel, text=ABOUT_TEXT, height=0, width=100)
    label1.pack()
    label2 = Label(toplevel, text=DISCLAIMER, height=0, width=100)
    label2.pack()


app = Tk()
app.title("SPIES")
app.geometry("500x100+200+200")

label = Label(
    app, text="Please browse to the directory you wish to scan", height=0, width=100)
b = Button(app, text="Quit", width=20, command=app.destroy)
button1 = Button(app, text="About SPIES", width=20, command=clickAbout)
label.pack()
b.pack(side='bottom', padx=5, pady=8)
button1.pack(side='bottom', padx=5, pady=0)

app.mainloop()

# clickAbout()
