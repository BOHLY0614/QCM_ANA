@echo off
echo ========================================================
echo      MISE A JOUR DU QCM ET RECUPERATION DES FICHIERS
echo ========================================================

:: 1. On configure git pour éviter les problèmes de fin de ligne
git config core.autocrlf true

:: 2. Sauvegarde TOUT (y compris les nouveaux fichiers non suivis avec -u)
echo Sauvegarde des modifications locales...
git stash push -u -m "Sauvegarde auto avant update"

:: 3. On s'assure d'être sur la branche principale (main ou master)
git checkout main
:: (Si ton git utilise 'master' au lieu de 'main', change le mot ci-dessus)

:: 4. On force la récupération des nouveautés
echo Telechargement des mises a jour...
git pull origin main

:: 5. On ré-applique les modifications de l'utilisateur
echo Restauration des modifications locales...
git stash pop

:: Si "git stash pop" échoue (conflit), on ne veut pas que ça bloque le lancement
if %errorlevel% neq 0 (
    echo Attention : Certains conflits ont ete detectes ou rien a restaurer.
)

echo ========================================================
echo      LANCEMENT DU QCM
echo ========================================================

py QCM.py

pause