from tkinter import *
from os import path, chdir, getcwd, makedirs, name
from shutil import copy, move
from subprocess import run, DEVNULL
from tempfile import TemporaryDirectory
from urllib import request
from zipfile import ZipFile
from json import load, dump

from .utils import _show_err, _clean_path

PATCH_COMMAND = "patch" if name!="nt" else "\"C:\\Program Files\\Git\\usr\\bin\\patch.exe\""

def start_install(win:Tk, instancedir:str, javabin:str, channel:str) -> None:
    if not (_clean_path(instancedir).replace(" ", "") or _clean_path(javabin).replace(" ", "")): 
        _show_err(win, "Paths must not be empty.")
        return

    if name=="nt":
        instancedir = instancedir.replace("/", "\\")
        javabin = javabin.replace("/", "\\")
    instancedir = path.sep.join(_clean_path(instancedir).split(path.sep)[:-1])
    javabin = _clean_path(javabin)

    if not path.exists(instancedir):
        _show_err(win, "Unknown path \".minecraft\" path.\nPlease check if it's correct.")
        return
    if not path.exists(javabin):
        _show_err(win, "Unknown path Java binary path.\nPlease check if it's correct.")
        return
    if run((javabin, "-version"), stderr=DEVNULL).returncode!=0:
        _show_err(win, "Incorrect Java path or your installation is broken.")
        return
    if run(PATCH_COMMAND+" -v", stdout=DEVNULL, shell=True).returncode!=0:
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
    label = StringVar()
    label.set("Installing...")
    mainlabel = Label(loading, textvariable=label)
    mainlabel.pack(expand=True)

    mainlabel.after(10, lambda: _install_pissmc(rdfile, channel, instancedir, javabin, loading, label))

def _install_pissmc(rdfile:str, channel:str, instancedir:str, javabin:str, loading:Toplevel, label:StringVar) -> None:
    with TemporaryDirectory() as tempdir:
        chdir(tempdir)
        _download_files(rdfile, channel)
        _patch_jar(instancedir, javabin)

    label.set("Install successful!")
    loading.after(3000, lambda: (loading.grab_release() or loading.destroy()))

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
def _patch_jar(instancedir:str, javabin:str) -> None:
    run(("java", "-jar", "jd-cli.jar", "minecraft-rd-132211-client.jar", "-od", "decomp"), stdout=DEVNULL)

    makedirs(path.join("src", "main", "java"), exist_ok=True)
    makedirs(path.join("src", "main", "resources"), exist_ok=True)
    move(path.join("decomp", "com"), path.join("src", "main", "java"))
    move(path.join("decomp", "terrain.png"), path.join("src", "main", "resources"))

    run(PATCH_COMMAND+" -s -p0 < piss.patch", shell=True, stdout=DEVNULL)

    if name=="nt": run(f"gradlew.bat shadowJar -Dorg.gradle.java.home=\"{path.sep.join(javabin.split(path.sep)[:-2])+path.sep}", shell=True, stdout=DEVNULL)
    else:
        run(("chmod", "+x", "gradlew"))
        run(f"./gradlew shadowJar -Dorg.gradle.java.home=\"{path.sep.join(javabin.split(path.sep)[:-2])+path.sep}\"", shell=True, stdout=DEVNULL)

    pissjar = path.join(getcwd(), "build", "libs", "pissmc-all.jar")

    chdir(instancedir)
    makedirs("patches", exist_ok=True)
    makedirs("libraries", exist_ok=True)

    request.urlretrieve(f"https://raw.githubusercontent.com/Modern-Modpacks/PissMC/main/modloader/customjar.json", path.join("patches", "customjar.json"))
    copy(pissjar, path.join("libraries", "customjar-1.jar"))

    json = load(open("mmc-pack.json"))
    json["components"].append({
        "cachedName": "PissMC",
        "uid": "customjar"
    })
    with open("mmc-pack.json", "w") as f: dump(json, f)
