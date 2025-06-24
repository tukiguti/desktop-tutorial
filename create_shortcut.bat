@echo off
echo デスクトップにショートカットを作成しています...

set EXE_PATH=%~dp0dist\MealRecommender.exe
set DESKTOP_PATH=%USERPROFILE%\Desktop

if not exist "%EXE_PATH%" (
    echo エラー: %EXE_PATH% が見つかりません。
    pause
    exit /b 1
)

powershell "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESKTOP_PATH%\今日の最適ごはん提案アプリ.lnk'); $s.TargetPath = '%EXE_PATH%'; $s.IconLocation = '%EXE_PATH%,0'; $s.Description = '今日の最適ごはん提案アプリ'; $s.WorkingDirectory = '%~dp0dist'; $s.Save()"

if %ERRORLEVEL% EQU 0 (
    echo ショートカットが正常に作成されました！
) else (
    echo ショートカットの作成中にエラーが発生しました。
)

pause