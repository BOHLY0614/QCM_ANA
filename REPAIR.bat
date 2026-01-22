@echo off
echo ========================================================
echo      REPARATION DES FICHIERS CORROMPUS
echo      (Cela va ecraser vos modifications locales pour remettre a neuf)
echo ========================================================

git fetch --all
git reset --hard origin/main

echo.
echo ========================================================
echo      REPARATION TERMINEE. VOUS POUVEZ RELANCER LE QCM.
echo ========================================================
pause