#!/bin/bash

rm -rf dist
mkdir dists

pyinstaller -F pissmc-installer.spec
mv dist/pissmc-installer dists
rm -rf build dist

wine64 pyinstaller.exe -F pissmc-installer.spec
mv dist/pissmc-installer.exe dists
rm -rf build dist

mv dists dist