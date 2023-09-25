from tkinter import *
from os import path
from .utils import _show_err, _clear_whitespace

def install(win:Tk, multidir:str, instancedir:str) -> None:
    if not (_clear_whitespace(multidir) and _clear_whitespace(instancedir)): 
        _show_err(win, "Paths must not be empty")
        return

    rdfile = path.join(multidir, "libraries", "com", "mojang", "minecraft", "rd-132211", "minecraft-rd-132211-client.jar")
    if not path.exists(rdfile): 
        _show_err(win, "Vanilla rd-132211 jar not found, launch an instance with that version at least once")
        return