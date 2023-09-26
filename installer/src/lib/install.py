from tkinter import *
from os import path, chdir, getcwd, mkdir
from shutil import copy
from subprocess import run, DEVNULL
from tempfile import TemporaryDirectory
from urllib import request
from zipfile import ZipFile

from .utils import _show_err, _clean_path, _get_patch_command

def start_install(win:Tk, instancedir:str, channel:str) -> None:
    instancedir = path.sep.join(_clean_path(instancedir).split(path.sep)[:-1])

    if not instancedir: 
        _show_err(win, "Path must not be empty.")
        return
    if not path.exists(instancedir):
        _show_err(win, "Unknown path.\nPlease check if it's correct.")
        return
    if run(("java", "-version"), stderr=DEVNULL).returncode!=0:
        _show_err(win, "Java not found or your default installation is broken.")
        return
    if run((_get_patch_command(), "-v"), stdout=DEVNULL).returncode!=0:
        _show_err(win, "Patch command not found. If you are on Windows, please install git first.")
        return

    multimcdir = path.sep.join(instancedir.split(path.sep)[:-2])

    rdfile = path.join(multimcdir, "libraries", "com", "mojang", "minecraft", "rd-132211", "minecraft-rd-132211-client.jar")
    if not path.exists(rdfile): 
        _show_err(win, "Vanilla rd-132211 jar not found, launch an instance with that version at least once.")
        return
    gsonfile = path.join(multimcdir, "libraries", "com", "google", "code", "gson", "gson", "2.10", "gson-2.10.jar")
    if not path.exists(gsonfile): 
        _show_err(win, "Gson 2.10 not found.")
        return
    lwjglfile = path.join(multimcdir, "libraries", "org", "lwjgl", "lwjgl", "lwjgl", "2.9.4-nightly-20150209", "lwjgl-2.9.4-nightly-20150209.jar")
    if not path.exists(lwjglfile): 
        _show_err(win, "Lwjgl 2.9.4 not found.")
        return

    loading=Toplevel(win)
    loading.resizable(False, False)
    loading.geometry("250x150")
    loading.title("Installing PissMC")
    loading.grab_set()
    mainlabel = Label(loading, text="Installing...")
    mainlabel.pack(expand=True)

    mainlabel.after(10, lambda: _install_pissmc(rdfile, channel, gsonfile, lwjglfile))

def _install_pissmc(rdfile:str, channel:str, gsonfile:str, lwjglfile:str) -> None:
    with TemporaryDirectory() as tempdir:
        chdir(tempdir)
        _download_files(rdfile, channel)
        _patch_jar(gsonfile, lwjglfile)

        print(tempdir)

        while 1: pass

def _download_files(rdfile:str, channel:str) -> None:
    copy(rdfile, getcwd())
    request.urlretrieve(f"https://raw.githubusercontent.com/Modern-Modpacks/PissMC/main/modloader/pissmc-{channel}.patch", "piss.patch")
    request.urlretrieve(f"https://github.com/intoolswetrust/jd-cli/releases/download/jd-cli-1.2.0/jd-cli-1.2.0-dist.zip", "jd-cli.zip")

    with ZipFile("jd-cli.zip") as f: f.extract("jd-cli.jar")
def _patch_jar(gsonfile:str, lwjglfile:str) -> None:
    run(("java", "-jar", "jd-cli.jar", "minecraft-rd-132211-client.jar", "-od", "src"))
    chdir(path.join("src", "com"))
    mkdir("lib")
    copy(gsonfile, path.join(getcwd(), "lib"))
    copy(lwjglfile, path.join(getcwd(), "lib"))

    run(_get_patch_command()+" -s -p0 < "+path.join("..", "..", "piss.patch"), shell=True)