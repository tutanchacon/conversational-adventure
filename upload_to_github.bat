@echo off
echo ========================================
echo SUBIR REPOSITORIO A GITHUB
echo ========================================
echo.
echo INSTRUCCIONES:
echo 1. Crea un nuevo repositorio en GitHub.com
echo 2. Nombra el repositorio: conversational-adventure
echo 3. NO agregues README, .gitignore o license
echo 4. Copia la URL del repositorio que GitHub te muestre
echo 5. Reemplaza YOUR_USERNAME en el comando siguiente:
echo.
echo COMANDO A EJECUTAR:
echo git remote add origin https://github.com/YOUR_USERNAME/conversational-adventure.git
echo git branch -M main
echo git push -u origin main
echo.
echo ========================================
echo EJEMPLO COMPLETO:
echo ========================================
echo Si tu usuario es "john_doe", ejecuta:
echo.
echo git remote add origin https://github.com/john_doe/conversational-adventure.git
echo git branch -M main  
echo git push -u origin main
echo.
pause
