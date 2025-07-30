@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: Répertoires
::set "root=%~dp0"
set "sourceBase=L:\Scripts\ressources\Apprenants"
set "archiveBase=L:\Scripts\ressources\Archives"
set "csvFile=L:\Scripts\ressources\etudiants.csv"
set "archivesList=L:\Scripts\ressources\archives.txt"

:: Création du fichier des archivés s’il n'existe pas
if not exist "%archivesList%" (
    type nul > "%archivesList%"
    echo Fichier d'archives créé : %archivesList%
)

:: Demander ce qu'on veut archiver
set /p "target=Entrez le nom de la PROMOTION ou le NOM Prénom d’un étudiant : "

:: Vérifier l'existence du fichier CSV
if not exist "%csvFile%" (
    echo ERREUR : Le fichier etudiants.csv est introuvable.
    pause
    exit /b
)

:: Crée le dossier d’archives s’il n’existe pas
if not exist "%archiveBase%" mkdir "%archiveBase%"

:: Obtenir la date du jour
for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set "date=%%a"

echo.
echo === Archivage ciblé sur "%target%" ===

:: Boucle sur chaque ligne du CSV (Nom;prenom;promotion)
for /f "skip=1 tokens=1,2,3 delims=;" %%A in (%csvFile%) do (
    set "nom=%%A"
    set "prenom=%%B"
    set "promo=%%C"

    :: Retirer les espaces parasites
    for /f "tokens=* delims= " %%x in ("!nom!") do set "nom=%%x"
    for /f "tokens=* delims= " %%x in ("!prenom!") do set "prenom=%%x"
    for /f "tokens=* delims= " %%x in ("!promo!") do set "promo=%%x"

    set "nomprenom=!nom! !prenom!"
    set "sourceDir=%sourceBase%\!nomprenom!"
    set "zipFile=%archiveBase%\!nomprenom!_%date%.zip"

    set "archiver=0"
    if /i "!promo!"=="%target%" (
        set "archiver=1"
    ) else if /i "!nomprenom!"=="%target%" (
        set "archiver=1"
    )

    if !archiver! equ 1 (
        if exist "!sourceDir!" (
            echo Archivage de !nomprenom!...

            powershell -NoProfile -Command ^
            "$source = '!sourceDir!';" ^
            "$destination = '!zipFile!';" ^
            "Add-Type -A 'System.IO.Compression.FileSystem';" ^
            "if (Test-Path $destination) { Remove-Item $destination };" ^
            "[System.IO.Compression.ZipFile]::CreateFromDirectory($source, $destination, 'Optimal', $true)"

            if exist "!zipFile!" (
                echo Suppression du dossier !nomprenom!...
                rmdir /s /q "!sourceDir!"
                findstr /i /x /c:"!nomprenom!" "%archivesList%" >nul || echo !nomprenom!>> "%archivesList%"
            ) else (
                echo ERREUR : Archivage échoué pour !nomprenom!.
            )
        ) else (
            echo [IGNORÉ] !nomprenom! n'a pas de dossier à archiver.
        )
    )
)

echo.
echo === Archivage terminé ===
pause
