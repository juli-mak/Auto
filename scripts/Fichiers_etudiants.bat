@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: === PARAMÈTRES ===

::Déclarer le fichier de log
set "log=%~dp0log.txt"
echo === Début du classement [%DATE% %TIME%] === >> "%log%"

:: Dossier source des fichiers à classer
set "source=C:\MesFichiers"

:: Dossier de base où sont les dossiers étudiants
set "baseDir=L:\Scripts\ressources\Apprenants"

:: Fichier CSV contenant les étudiants (colonne unique : nomprenom)
set "listeEtudiants=L:\Scripts\ressources\Etudiants.csv"

:: Fichier temporaire pour stocker les noms concaténés
set "tmpList=%temp%\etudiants_list.txt"

:: Extensions de fichiers à traiter
set "exts=pdf doc docx jpg jpeg png zip rar"

:: === VÉRIFICATION DU CSV ===
if not exist "%listeEtudiants%" (
    echo  Fichier CSV introuvable : "%listeEtudiants%"
    pause
    exit /b
)

:: Activation de delayed expansion si pas déjà fait
setlocal EnableDelayedExpansion

:: Nettoyage de la liste temporaire au début
if exist "%tmpList%" del "%tmpList%"

:: === PRÉPARATION DE LA LISTE TEMPORAIRE ===
for /f "skip=1 usebackq tokens=1,2 delims=;" %%N in ("%listeEtudiants%") do (
    call :ajouter "%%N" "%%O"
)

goto :affichage

:ajouter
set "nom=%~1"
set "prenom=%~2"
set "nomprenom=%nom% %prenom%"
>>"%tmpList%" echo %nomprenom%
exit /b

:affichage
:: (optionnel) Affichage
echo --- Liste temporaire generee ---
type "%tmpList%"
echo --------------------------------
pause

echo  Demarrage du classement...

:: === TRAITEMENT DES FICHIERS ===
for %%E in (%exts%) do (
    for /r "%source%" %%F in (*.%%E) do (
        call :classer "%%~nxF" "%%~fF"
    )
)

echo  Classement termine.
pause
exit /b

:: === SOUS-PROGRAMME : CLASSER ===
:classer
set "file=%~1"
set "full=%~2"
set "etudiant="
set "rubrique="
set "reste="
set "suite="

:: Recherche de l'étudiant correspondant
for /f "usebackq delims=" %%N in ("%tmpList%") do (
    set "line=%%N"
    for /f "tokens=* delims= " %%A in ("!line!") do set "line=%%A"
    set "nomCherche=!line!_"
    set "prefix=!file:~0,100!"

    :: Affichage pour débogage
    echo - Comparaison :
    echo   Depuis CSV  : "[!nomCherche!]"
    echo   Dans nom de fichier : "[!prefix!]"
    
    call set "test=%%prefix:!nomCherche!=%%"
    
    if not "!test!"=="!prefix!" (
        set "etudiant=!line!"
        goto :found
    )
)


echo [ERREUR] Etudiant non reconnu pour : "!file!" >> "%log%"
echo  Etudiant non reconnu pour : "!file!"

exit /b

:found
:: Extraire la partie après "NomPrenom_"
set "reste=!file:%etudiant%_=!"

:: Retirer l'extension
set "ext=!reste:~-4!"
if /i "!ext!"==".jpg"  set "reste=!reste:~0,-4!"
if /i "!ext!"==".png"  set "reste=!reste:~0,-4!"
if /i "!ext!"==".zip"  set "reste=!reste:~0,-4!"
if /i "!ext!"==".rar"  set "reste=!reste:~0,-4!"
if /i "!ext!"==".jpeg" set "reste=!reste:~0,-5!"

echo   Partie apres le nomprenom : "!reste!"

:: Extraire la rubrique principale et la suite
for /f "tokens=1,* delims=_" %%R in ("!reste!") do (
    set "rubrique=%%R"
    set "suite=%%S"
)

:: Traitement spécial pour PEDAGOGIE_...
if /i "!rubrique!"=="PEDAGOGIE" (
    if defined suite (
        for /f "tokens=1,* delims=_" %%A in ("!suite!") do (
            set "rubrique=PEDAGOGIE\%%A"
        )
    ) else (
        set "rubrique=PEDAGOGIE"
    )
)

echo     Rubrique detectee : !rubrique!

set "dest=%baseDir%\!etudiant!\!rubrique!"

if exist "!dest!" (
    echo [OK] !file! → !dest! >> "%log%"
echo  Copie de "!file!" vers "!dest!"

    copy /Y "!full!" "!dest!\" >nul
) else (
    echo [ERREUR] Rubrique non trouvée : "!rubrique!" pour "!file!" >> "%log%"
echo  [ERREUR] Rubrique non trouvée : "!rubrique!" pour "!file!"

)
echo === Fin du classement [%DATE% %TIME%] === >> "%log%"
echo  Un journal a été enregistré dans : "%log%"

exit /b