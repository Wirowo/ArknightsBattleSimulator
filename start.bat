@echo off
@title ArknightsBattleSimulator

py -m venv env && env\scripts\activate.bat && pip install -r requirements.txt -U && ^
start cmd.exe /c "@title Arknights Crisis Simulator - mitmdump && mitmdump.exe -s ak.py" && ^
cls && py server\app.py