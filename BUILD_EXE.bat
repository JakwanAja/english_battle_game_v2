@echo off
echo ============================================
echo   English Battle Pets - Build EXE
echo ============================================
echo.

:: Install dependencies
echo [1/3] Installing dependencies...
pip install pygame pyinstaller --quiet
if %errorlevel% neq 0 (
    echo ERROR: pip install failed. Pastikan Python sudah terinstall.
    pause
    exit /b 1
)

:: Build exe
echo [2/3] Building EXE...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "EnglishBattlePets" ^
    --add-data "assets;assets" ^
    --hidden-import pygame ^
    --hidden-import pygame.mixer ^
    --hidden-import pygame.font ^
    --hidden-import pygame.image ^
    --icon "assets/logo_game.png" ^
    main.py

if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

:: Done
echo.
echo [3/3] SELESAI!
echo File EXE ada di folder: dist\EnglishBattlePets.exe
echo.
pause
