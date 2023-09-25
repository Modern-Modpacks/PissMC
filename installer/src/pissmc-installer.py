from tkinter import *
from os import path, chdir
from pkgutil import get_data
from PIL import Image, ImageTk

from lib import install

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
initchoice = StringVar()
initchoice.set("Stable")
OptionMenu(inputs, initchoice, *["Stable", "Latest"]).pack()
Label(inputs, text="Path to your \"multimc\"/\"PrismLauncher\" folder (the parent of your \"instances\" directory):").pack()
multidir = Text(inputs, height=1, width=70, wrap="none")
multidir.pack()
multidir.bind("<Return>", lambda _: "break")
Label(inputs, text="Path to your instance folder (the parent of your \".minecraft\" directory):").pack()
instancedir = Text(inputs, height=1, width=70, wrap="none")
instancedir.pack()
instancedir.bind("<Return>", lambda _: "break")

Button(app, text="Submit", command=lambda: install(app, multidir.get("1.0", END), instancedir.get("1.0", END))).pack(side=BOTTOM, pady=10)

try: app.mainloop()
except KeyboardInterrupt: exit(0)