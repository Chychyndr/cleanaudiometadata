@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "TARGET=%~1"

if "%TARGET%"=="" (
    set /p "TARGET=Вставь путь к папке с музыкой: "
)

set "TARGET=%TARGET:"=%"

echo.
echo Папка: %TARGET%
echo.

uv run --with mutagen python "%~dp0clean_audio_metadata.py" "%TARGET%" --recursive

echo.
pause