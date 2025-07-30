@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

set "csvFile=L:\Scripts\promotions_terminees.csv"

for /f "usebackq skip=1 tokens=1,* delims=;" %%A in ("%csvFile%") do (
    echo PROMO = %%A
    echo GROUPE = %%B
)
pause
