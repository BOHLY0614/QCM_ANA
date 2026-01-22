@echo on
:: @echo on permet de voir toutes les commandes s'exécuter

echo ========================================================
echo      MODE DEBUG - DIAGNOSTIC
echo ========================================================

:: 1. Vérification de Git
echo Etape 1 : Verification de Git...
git --version
if %errorlevel% neq 0 (
    echo ERREUR CRITIQUE : Git n'est pas installe ou pas trouve !
    pause
    exit /b
)
pause

:: 2. Sauvegarde locale
echo Etape 2 : Tentative de sauvegarde (Stash)...
git stash push -u -m "Sauvegarde Debug"
if %errorlevel% neq 0 (
    echo AVERTISSEMENT : Echec du stash (peut-etre rien a sauvegarder ?)
)
pause

:: 3. Téléchargement
echo Etape 3 : Telechargement (Pull)...
git pull origin main
if %errorlevel% neq 0 (
    echo ERREUR : Impossible de telecharger les mises a jour.
    echo Verifiez votre connexion internet ou les conflits.
)
pause

:: 4. Restauration
echo Etape 4 : Restauration des modifs (Stash Pop)...
git stash pop
:: Pas de pause ici, on enchaine sur le lancement

:: 5. Lancement Python
echo ========================================================
echo      LANCEMENT DE PYTHON
echo ========================================================

python --version
python QCM.py

echo.
echo ========================================================
echo      LE PROGRAMME S'EST ARRETE. LISEZ LES ERREURS CI-DESSUS.
echo ========================================================
pause