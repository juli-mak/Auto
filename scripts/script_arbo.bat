@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: Dossier du script
set "baseDir=%~dp0"
set "promotionsDir=L:\Scripts\ressources\Promotions"
set "csv=L:\Scripts\ressources\promotions.csv"

if not exist "%csv%" (
    echo Le fichier promotions.csv est introuvable dans %baseDir%.
    pause
    exit /b
)

:: Sous-dossiers à créer pour chaque promotion
set "subsfile=%temp%\subfolders.txt"
(
echo Blocs-Projets\DossierTemplate\Ressources locales
echo Blocs-Projets\DossierTemplate\Livrables
echo Blocs-Projets\DossierTemplate\Grilles Evaluation
echo Blocs-Projets\DossierTemplate\Fiches Preparation et Deroulement
echo Blocs-Projets\Anglais
echo Blocs-Projets\Qualigs
echo Jury
echo Suivi Scolarite
echo Pilotage\Bilan-Briefing
echo Pilotage\Comportement Ingenieur
echo Pilotage\Referentiel
) > "%subsfile%"

:: Lecture du CSV ligne par ligne (avec séparation par point-virgule)
for /f "skip=1 tokens=1,2 delims=;" %%A in (%csv%) do (
    set "promo=%%A"
    set "groupe=%%B"
    set "promo=!promo:"=!"
    set "groupe=!groupe:"=!"

    echo Création pour !promo! dans !groupe!

    echo !promo! | find /I "Sessions Closes" >nul
    if errorlevel 1 (
        for /f "usebackq delims=" %%D in ("%subsfile%") do (
            mkdir "%promotionsDir%\!groupe!\!promo!\%%D" >nul 2>&1
        )
    ) else (
        mkdir "%promotionsDir%\!groupe!\!promo!" >nul 2>&1
    )
)

echo.
echo ✅ Arborescences créées dans : %promotionsDir%
pause
