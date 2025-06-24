@echo off
echo 今日の最適ごはん提案アプリを起動しています...
cd /d "%~dp0"

if exist "dist\MealRecommender.exe" (
    start "" "dist\MealRecommender.exe"
) else (
    echo エラー: アプリケーションが見つかりません。
    echo アプリケーションをビルドしてから再試行してください。
    pause
)