@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul

:: Répertoires
set "BASE_DIR=L:\Scripts\ressources\Promotions"
set "CSV_FILE=L:\Scripts\ressources\promotions.csv"
set "SOURCE_DIR=C:\MesFichiers"

:: Vérification du fichier CSV
if not exist "%CSV_FILE%" (
    echo ❌ Fichier CSV introuvable : %CSV_FILE%
    pause
    exit /b
)

:: Boucle sur tous les fichiers de tous types
for %%F in ("%SOURCE_DIR%\*.*") do (
    set "FICHIER=%%~nxF"
    set "NOMFICHIER=%%~nF"
    set "TROUVE="
    set "PROMO="
    set "GROUPE="

    :: Cherche une promo qui matche le début du nom de fichier
    for /f "usebackq tokens=1,2 delims=;" %%A in ("%CSV_FILE%") do (
        set "PROMO=%%A"
        set "GROUPE=%%B"
        echo !NOMFICHIER! | findstr /b /c:"!PROMO!" >nul
        if !errorlevel! == 0 (
            set "TROUVE=1"
            goto :apresrecherche
        )
    )

:apresrecherche
    if defined TROUVE (
        set "DEST_BASE=%BASE_DIR%\!GROUPE!\!PROMO!"

        :: Extraire la partie restante du nom de fichier
        set "RESTE=!NOMFICHIER:%PROMO%_=!"
        set "RUBRIQUE1="
        set "RUBRIQUE2="
        for /f "tokens=1,2 delims=_" %%X in ("!RESTE!") do (
            set "RUBRIQUE1=%%X"
            set "RUBRIQUE2=%%Y"
        )

        :: Déduire la destination selon la rubrique
        set "DEST="
        if /i "!RUBRIQUE1!"=="Jury"             set "DEST=Jury"
        if /i "!RUBRIQUE1!"=="FACTURATION"      set "DEST=FACTURATION"
        if /i "!RUBRIQUE1!"=="CONTRACTUALISATION" set "DEST=CONTRACTUALISATION"
        if /i "!RUBRIQUE1!"=="PEDAGOGIE"        set "DEST=PEDAGOGIE\!RUBRIQUE2!"
        if /i "!RUBRIQUE1!"=="Blocs-Projets"    set "DEST=Blocs-Projets\!RUBRIQUE2!"

        if defined DEST (
            set "FULL_DEST=!DEST_BASE!\!DEST!"
            if exist "!FULL_DEST!" (
                echo ✅ Copie de !FICHIER! → !FULL_DEST!
                copy /Y "%%~fF" "!FULL_DEST!\" >nul
            ) else (
                echo ⚠️ Dossier inexistant : !FULL_DEST!
            )
        ) else (
            echo ❓ Rubrique inconnue pour !FICHIER! → !RUBRIQUE1!\!RUBRIQUE2!
        )
    ) else (
        echo ❌ Promotion non trouvée pour !FICHIER!
    )
)

echo.
echo ✔️ Copie terminée.
pause
