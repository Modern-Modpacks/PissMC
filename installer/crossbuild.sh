#!/bin/bash

rm -rf dist
mkdir dists

pyinstaller -F src/pissmc-installer.py
mv dist/pissmc-installer dists
rm -rf build dist

wine64 pyinstaller.exe -F src/pissmc-installer.py
mv dist/pissmc-installer.exe dists
rm -rf build dist

mv dists dist