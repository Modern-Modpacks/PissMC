from tkinter import *
from os import path, chdir
from pkgutil import get_data
from PIL import Image, ImageTk

from lib import start_install

chdir(path.dirname(path.abspath(__file__)))

app = Tk()
app.title("PissMC Installer")
app.geometry("600x400")
app.resizable(False, False)

logo = ImageTk.PhotoImage(Image.open("assets/logo.png").resize((50, 50)))

heading = Frame(app)
heading.pack(pady=10)
logowidget = Label(heading, image=logo)
logowidget.grid(column=0, row=0, padx=5)
logowidget.image = logo
Label(heading, text="PissMC Installer", font=("Helvetica bold", 20)).grid(column=1, row=0)
Label(app, text="One step away from getting the (self-proclaimed) best modloader on the market...", font=("Helvetica bold", 10)).pack()

inputs = Frame(app)
inputs.pack(expand=True)
Label(inputs, text="Select the version channel you want to install:").pack()
channel = StringVar()
choices = ["Stable (Recommended)", "Latest (Beta)"]
channel.set(choices[0])
OptionMenu(inputs, channel, *choices).pack()
Label(inputs, text="Path to your \".minecraft\" folder (must be a multimc/prism instance):").pack()
mcdir = Text(inputs, height=1, width=70, wrap="none")
mcdir.pack()
mcdir.bind("<Return>", lambda _: "break")

Button(app, text="Submit", command=lambda: start_install(app, mcdir.get("1.0", END), channel.get().lower().split(" ")[0])).pack(side=BOTTOM, pady=10)

try: app.mainloop()
except KeyboardInterrupt: exit(0)