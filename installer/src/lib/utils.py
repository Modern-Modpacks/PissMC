from tkinter import *

def _clear_whitespace(string:str) -> str: return string.replace("\n", "").replace(" ", "")

def _show_err(win:Tk, err:str) -> None:
    popup=Toplevel(win)
    popup.resizable(False, False)
    popup.geometry("250x150")
    popup.title("Error")

    Label(popup, text=err, wraplength=150).pack(expand=True)
    Button(popup, text="OK", command=lambda: popup.destroy()).pack(side=BOTTOM, pady=10)