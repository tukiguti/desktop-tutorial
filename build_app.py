import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_executable():
    """PyInstallerを使用してアプリケーションをビルドする"""
    print("アプリケーションのビルドを開始します...")
    
    # ビルドコマンドを構築
    build_cmd = [
        "pyinstaller",
        "--onefile",  # 単一の実行可能ファイルを作成
        "--windowed",  # コンソールウィンドウを表示しない
        "--icon=meal_recommender_icon.ico",  # アイコンファイルを指定
        "--name=MealRecommender",  # 出力ファイル名
        "--clean",  # ビルド前にキャッシュをクリア
        # データファイルを追加
        "--add-data=recipes.json;.",
        "--add-data=recipes_enhanced.json;.",
        "meal_recommender_gui_enhanced.py"  # メインスクリプト
    ]
    
    # Windowsでない場合はパス区切り文字を変更
    if not sys.platform.startswith('win'):
        build_cmd[6] = "--add-data=recipes.json:."
        build_cmd[7] = "--add-data=recipes_enhanced.json:."
    
    # コマンドを実行
    result = subprocess.run(build_cmd, capture_output=True, text=True)
    
    # 結果を表示
    if result.returncode == 0:
        print("ビルドが成功しました！")
        print(f"実行可能ファイルは 'dist/MealRecommender.exe' に作成されました。")
        return True
    else:
        print("ビルドに失敗しました。")
        print("エラー出力:")
        print(result.stderr)
        return False

def create_desktop_shortcut():
    """デスクトップにショートカットを作成する"""
    print("デスクトップにショートカットを作成します...")
    
    # 実行可能ファイルのパスを取得
    exe_path = os.path.abspath("dist/MealRecommender.exe")
    
    if not os.path.exists(exe_path):
        print(f"エラー: {exe_path} が見つかりません。")
        return False
    
    # デスクトップのパスを取得
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # バッチファイルを作成
    batch_path = os.path.join(os.getcwd(), "create_shortcut.bat")
    with open(batch_path, "w") as f:
        f.write(f'@echo off\n')
        f.write(f'echo Creating shortcut on desktop...\n')
        f.write(f'powershell "$ws = New-Object -ComObject WScript.Shell; ')
        f.write(f'$s = $ws.CreateShortcut(\'{desktop_path}\\今日の最適ごはん提案アプリ.lnk\'); ')
        f.write(f'$s.TargetPath = \'{exe_path}\'; ')
        f.write(f'$s.IconLocation = \'{exe_path},0\'; ')
        f.write(f'$s.Description = \'今日の最適ごはん提案アプリ\'; ')
        f.write(f'$s.WorkingDirectory = \'{os.path.dirname(exe_path)}\'; ')
        f.write(f'$s.Save()"\n')
        f.write(f'echo Shortcut created successfully!\n')
        f.write(f'pause\n')
    
    print(f"ショートカット作成用のバッチファイルを作成しました: {batch_path}")
    print("このバッチファイルを実行して、デスクトップにショートカットを作成してください。")
    return True

if __name__ == "__main__":
    if build_executable():
        create_desktop_shortcut()
    print("完了しました。")