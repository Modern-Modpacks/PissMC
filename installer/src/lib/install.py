from tkinter import *
from os import path, chdir, getcwd, makedirs
from shutil import copy, move
from subprocess import run, DEVNULL
from tempfile import TemporaryDirectory
from urllib import request
from zipfile import ZipFile
from platform import system

from .utils import _show_err, _clean_path

PATCH_COMMAND = "patch" if system().lower()!="windows" else "C:\\Program Files\\Git\\usr\\bin\\patch.exe"

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
    if run((PATCH_COMMAND, "-v"), stdout=DEVNULL).returncode!=0:
        _show_err(win, "Patch command not found. If you are on Windows, please install git first.")
        return

    multimcdir = path.sep.join(instancedir.split(path.sep)[:-2])

    rdfile = path.join(multimcdir, "libraries", "com", "mojang", "minecraft", "rd-132211", "minecraft-rd-132211-client.jar")
    if not path.exists(rdfile): 
        _show_err(win, "Vanilla rd-132211 jar not found, launch an instance with that version at least once.")
        return

    loading=Toplevel(win)
    loading.resizable(False, False)
    loading.geometry("250x150")
    loading.title("Installing PissMC")
    loading.grab_set()
    mainlabel = Label(loading, text="Installing...")
    mainlabel.pack(expand=True)

    mainlabel.after(10, lambda: _install_pissmc(rdfile, channel))

def _install_pissmc(rdfile:str, channel:str) -> None:
    with TemporaryDirectory() as tempdir:
        chdir(tempdir)
        _download_files(rdfile, channel)
        _patch_jar()

        print(tempdir)

        while 1: pass

def _download_files(rdfile:str, channel:str) -> None:
    WRAPPER_PATH = path.join("gradle", "wrapper")
    makedirs(WRAPPER_PATH, exist_ok=True)

    copy(rdfile, getcwd())
    request.urlretrieve(f"https://raw.githubusercontent.com/Modern-Modpacks/PissMC/main/modloader/pissmc-{channel}.patch", "piss.patch")
    request.urlretrieve(f"https://raw.githubusercontent.com/Modern-Modpacks/PissMC/main/modloader/gradle/gradlew", "gradlew")
    request.urlretrieve(f"https://raw.githubusercontent.com/Modern-Modpacks/PissMC/main/modloader/gradle/gradlew.bat", "gradlew.bat")
    request.urlretrieve(f"https://raw.githubusercontent.com/Modern-Modpacks/PissMC/main/modloader/gradle/build.gradle", "build.gradle")
    request.urlretrieve(f"https://raw.githubusercontent.com/Modern-Modpacks/PissMC/main/modloader/gradle/settings.gradle", "settings.gradle")
    request.urlretrieve(f"https://raw.githubusercontent.com/Modern-Modpacks/PissMC/main/modloader/gradle/wrapper.jar", path.join(WRAPPER_PATH, "gradle-wrapper.jar"))
    request.urlretrieve(f"https://raw.githubusercontent.com/Modern-Modpacks/PissMC/main/modloader/gradle/wrapper.properties", path.join(WRAPPER_PATH, "gradle-wrapper.properties"))
    request.urlretrieve(f"https://github.com/intoolswetrust/jd-cli/releases/download/jd-cli-1.2.0/jd-cli-1.2.0-dist.zip", "jd-cli.zip")

    with ZipFile("jd-cli.zip") as f: f.extract("jd-cli.jar")
def _patch_jar() -> None:
    run(("java", "-jar", "jd-cli.jar", "minecraft-rd-132211-client.jar", "-od", "decomp"), stdout=DEVNULL)

    makedirs(path.join("src", "main", "java"), exist_ok=True)
    makedirs(path.join("src", "main", "resources"), exist_ok=True)
    move(path.join("decomp", "com"), path.join("src", "main", "java"))
    move(path.join("decomp", "terrain.png"), path.join("src", "main", "resources"))

    run(PATCH_COMMAND+" -s -p0 < piss.patch", shell=True, stdout=DEVNULL)

