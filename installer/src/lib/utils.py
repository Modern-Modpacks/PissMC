from tkinter import *
from platform import system

def _clean_path(string:str) -> str: return string.replace("\n", "")
def _is_windows() -> bool: system().lower()=="windows"

def _show_err(win:Tk, err:str) -> None:
    popup=Toplevel(win)
    popup.resizable(False, False)
    popup.geometry("250x150")
    popup.title("Error")
    popup.grab_set()

    Label(popup, text=err, wraplength=200).pack(expand=True)
    Button(popup, text="OK", command=lambda: (popup.grab_release() or popup.destroy())).pack(side=BOTTOM, pady=10)