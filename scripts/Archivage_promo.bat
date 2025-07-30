@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: === Déclaration des chemins ===
set "promotionsDir=L:\Scripts\ressources\Promotions"
set "archivesDir=L:\Scripts\ressources\Archives"
set "logFile=%archivesDir%\log_archivage.txt"
set "csvFile=L:\Scripts\ressources"

:: === Création du dossier d'archives si nécessaire ===
if not exist "%archivesDir%" mkdir "%archivesDir%"

:: === Réinitialisation du fichier log ===
echo ===== Journal d'archivage - %date% %time% =====> "%logFile%"

:: === Vérification de l'existence du fichier CSV ===
if not exist "%csvFile%" (
    echo ❌ Le fichier promotions_terminees.csv est introuvable.
    echo ❌ Fichier CSV introuvable >> "%logFile%"
    pause
    exit /b
)

:: === Boucle sur chaque ligne du CSV (hors entête) ===
for /f "skip=1 usebackq delims=" %%A in ("%csvFile%") do (
    set "promo=%%A"
    set "promo=!promo:"=!"  :: supprime les éventuels guillemets

    echo.
    echo 📁 Traitement de : !promo!
    echo 📁 Traitement de : !promo! >> "%logFile%"

    set "promoTrouve=0"

    :: Parcours de tous les dossiers de groupe
    for /d %%G in ("%promotionsDir%\*") do (
        set "groupe=%%~nxG"
        set "promoDir=%%G\!promo!"
        set "zipFile=%archivesDir%\!promo!.zip"

        if exist "!promoDir!" (
            set "promoTrouve=1"
            echo 🔄 Archivage de !promo! depuis le groupe !groupe!...
            echo 🔄 Archivage de !promo! depuis le groupe !groupe! >> "%logFile%"

            powershell -NoProfile -Command ^
            "Compress-Archive -Path '!promoDir!\*' -DestinationPath '!zipFile!' -Force"

            if exist "!zipFile!" (
                echo ✅ Archive créée : !zipFile!
                echo ✅ Archivé avec succès depuis !groupe! >> "%logFile%"
                echo 🔥 Suppression de !promoDir!...
                rmdir /s /q "!promoDir!"
            ) else (
                echo ❌ Échec de l'archivage pour : !promo!
                echo ❌ Échec de l'archivage depuis !groupe! >> "%logFile%"
            )
        )
    )

    :: Si aucun dossier trouvé pour cette promo
    if !promoTrouve! EQU 0 (
        echo ⚠️ Aucun dossier trouvé pour : !promo!
        echo ⚠️ Dossier introuvable pour : !promo! >> "%logFile%"
    )
)

echo.
echo 🗃️ Archivage terminé. Consultez le fichier de log : %logFile%
pause
