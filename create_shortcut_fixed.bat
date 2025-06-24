@echo off
echo デスクトップにショートカットを作成しています...

set EXE_PATH=%~dp0dist\MealRecommender.exe
set DESKTOP_PATH=%USERPROFILE%\Desktop

if not exist "%EXE_PATH%" (
    echo エラー: %EXE_PATH% が見つかりません。
    pause
    exit /b 1
)

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%DESKTOP_PATH%\今日の最適ごはん提案アプリ.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%EXE_PATH%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%~dp0dist" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "今日の最適ごはん提案アプリ" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%EXE_PATH%, 0" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"
cscript //nologo "%TEMP%\CreateShortcut.vbs"
del "%TEMP%\CreateShortcut.vbs"

if %ERRORLEVEL% EQU 0 (
    echo ショートカットが正常に作成されました！
) else (
    echo ショートカットの作成中にエラーが発生しました。
)

pause