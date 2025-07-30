@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: Répertoire racine
set "root=L:\Scripts\ressources"
::set "root=%root:~0,-1%"
set "baseDir=L:\Scripts\ressources\Apprenants"
set "archivesFile=%root%\archives.txt"

echo Dossier racine détecté : %root%

:: Vérification des fichiers requis
if not exist "%root%\Structure.csv" (
  echo Le fichier Structure.csv est introuvable.
  pause & exit /b
)
if not exist "%archivesFile%" (
  type nul > "%archivesFile%"
)

:: Création du dossier Apprenants si nécessaire
if not exist "%baseDir%" mkdir "%baseDir%"

:: Boucle sur chaque ligne (étudiant)
for /f "usebackq skip=1 tokens=1,2,3 delims=;" %%A in ("%root%\Etudiants.csv") do (
    set "nom=%%A"
    set "prenom=%%B"

    :: Nettoyage des espaces superflus au début/fin
    set "nom=!nom:~0!"
    set "prenom=!prenom:~0!"

    :: Concaténer avec un espace
    set "nomprenom=!nom! !prenom!"
    set "etudiantDir=%baseDir%\!nomprenom!"

    :: Vérifier s’il est déjà archivé
    set "ignore=0"
    for /f "usebackq delims=" %%Z in ("%archivesFile%") do (
        if /i "%%Z"=="!nomprenom!" set "ignore=1"
    )

    if !ignore! equ 1 (
        echo [ARCHIVÉ] !nomprenom! – ignoré.
    ) else (
        echo === Création pour !nomprenom! ===

        :: Création des sous-dossiers selon structure.csv
        for /f "usebackq skip=1 tokens=* delims=" %%L in ("%root%\Structure.csv") do (
            set "path=%%L"
            set "path=!path:"=!"
            mkdir "!etudiantDir!\!path!" >nul 2>&1
        )
    )
)