# -*- coding: utf-8 -*-
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import datetime
import uuid
import shutil

class UserReportManager:
    """
    ユーザーレポート（つくったよレポート）を管理するクラス
    """
    def __init__(self, recipes_file='recipes_enhanced.json', reports_dir='user_reports'):
        self.recipes_file = recipes_file
        self.reports_dir = reports_dir
        self.recipes = self.load_recipes()
        
        # レポート保存用ディレクトリの作成
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        # 画像保存用ディレクトリの作成
        self.images_dir = os.path.join(reports_dir, 'images')
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
    
    def load_recipes(self):
        """
        レシピデータを読み込む
        """
        try:
            with open(self.recipes_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"レシピファイルの読み込みエラー: {e}")
            return []
    
    def save_recipes(self):
        """
        レシピデータを保存する
        """
        try:
            with open(self.recipes_file, 'w', encoding='utf-8') as file:
                json.dump(self.recipes, file, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"レシピファイルの保存エラー: {e}")
            return False
    
    def add_report(self, recipe_id, user_name, comment, rating, image_path=None):
        """
        レシピにユーザーレポートを追加する
        
        Parameters:
        - recipe_id: レシピID
        - user_name: ユーザー名
        - comment: コメント
        - rating: 評価（1-5）
        - image_path: 画像ファイルのパス（オプション）
        
        Returns:
        - 成功した場合はTrue、失敗した場合はFalse
        """
        # レシピを検索
        recipe = None
        for r in self.recipes:
            if r["id"] == recipe_id:
                recipe = r
                break
        
        if not recipe:
            print(f"レシピID {recipe_id} が見つかりません。")
            return False
        
        # 画像の処理
        image_filename = None
        if image_path and os.path.exists(image_path):
            # 一意のファイル名を生成
            image_filename = f"{uuid.uuid4()}{os.path.splitext(image_path)[1]}"
            destination = os.path.join(self.images_dir, image_filename)
            
            try:
                # 画像をコピー
                shutil.copy2(image_path, destination)
            except Exception as e:
                print(f"画像のコピーエラー: {e}")
                return False
        
        # レポートの作成
        report = {
            "id": str(uuid.uuid4()),
            "user_name": user_name,
            "comment": comment,
            "rating": rating,
            "image": image_filename,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # レシピにレポートを追加
        if "user_reports" not in recipe:
            recipe["user_reports"] = []
        
        recipe["user_reports"].append(report)
        
        # レシピデータを保存
        return self.save_recipes()
    
    def get_reports_for_recipe(self, recipe_id):
        """
        特定のレシピのユーザーレポートを取得する
        """
        for recipe in self.recipes:
            if recipe["id"] == recipe_id:
                return recipe.get("user_reports", [])
        
        return []
    
    def get_image_path(self, image_filename):
        """
        画像ファイルの完全パスを取得する
        """
        if not image_filename:
            return None
        
        return os.path.join(self.images_dir, image_filename)

class UserReportDialog:
    """
    ユーザーレポート投稿用ダイアログ
    """
    def __init__(self, parent, recipe):
        self.parent = parent
        self.recipe = recipe
        self.image_path = None
        self.result = None
        
        # ダイアログウィンドウの作成
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"つくったよレポート - {recipe['name']}")
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # フォント設定
        self.title_font = ("Yu Gothic", 14, "bold")
        self.header_font = ("Yu Gothic", 12, "bold")
        self.normal_font = ("Yu Gothic", 10)
        
        self.create_widgets()
    
    def create_widgets(self):
        """
        ウィジェットを作成する
        """
        # メインフレーム
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # タイトル
        title_label = ttk.Label(main_frame, text=f"{self.recipe['name']}を作りました！", font=self.title_font)
        title_label.pack(pady=(0, 20))
        
        # ユーザー名入力
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=5)
        
        name_label = ttk.Label(name_frame, text="ニックネーム:", font=self.normal_font)
        name_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, width=30)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 評価入力
        rating_frame = ttk.Frame(main_frame)
        rating_frame.pack(fill=tk.X, pady=10)
        
        rating_label = ttk.Label(rating_frame, text="評価:", font=self.normal_font)
        rating_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.rating_var = tk.IntVar(value=5)
        for i in range(1, 6):
            rb = ttk.Radiobutton(rating_frame, text=str(i), variable=self.rating_var, value=i)
            rb.pack(side=tk.LEFT, padx=5)
        
        # コメント入力
        comment_frame = ttk.LabelFrame(main_frame, text="コメント", padding=10)
        comment_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.comment_text = tk.Text(comment_frame, wrap=tk.WORD, height=5, font=self.normal_font)
        self.comment_text.pack(fill=tk.BOTH, expand=True)
        
        # 画像アップロード
        image_frame = ttk.LabelFrame(main_frame, text="写真", padding=10)
        image_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.image_preview = ttk.Label(image_frame, text="画像がありません")
        self.image_preview.pack(fill=tk.BOTH, expand=True, pady=5)
        
        image_button_frame = ttk.Frame(image_frame)
        image_button_frame.pack(fill=tk.X)
        
        upload_button = ttk.Button(image_button_frame, text="画像を選択", command=self.select_image)
        upload_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(image_button_frame, text="クリア", command=self.clear_image)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # ボタン
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        cancel_button = ttk.Button(button_frame, text="キャンセル", command=self.cancel)
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        submit_button = ttk.Button(button_frame, text="投稿する", command=self.submit)
        submit_button.pack(side=tk.RIGHT, padx=5)
    
    def select_image(self):
        """
        画像ファイルを選択する
        """
        file_types = [
            ("画像ファイル", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("すべてのファイル", "*.*")
        ]
        
        image_path = filedialog.askopenfilename(
            parent=self.dialog,
            title="画像を選択",
            filetypes=file_types
        )
        
        if image_path:
            try:
                # 画像をプレビュー表示
                image = Image.open(image_path)
                image = image.resize((300, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                self.image_preview.config(image=photo, text="")
                self.image_preview.image = photo  # 参照を保持
                
                self.image_path = image_path
            except Exception as e:
                messagebox.showerror("エラー", f"画像の読み込みに失敗しました: {e}")
    
    def clear_image(self):
        """
        画像をクリアする
        """
        self.image_preview.config(image="", text="画像がありません")
        self.image_path = None
    
    def submit(self):
        """
        レポートを投稿する
        """
        # 入力チェック
        user_name = self.name_var.get().strip()
        if not user_name:
            messagebox.showwarning("入力エラー", "ニックネームを入力してください。")
            return
        
        comment = self.comment_text.get("1.0", tk.END).strip()
        if not comment:
            messagebox.showwarning("入力エラー", "コメントを入力してください。")
            return
        
        rating = self.rating_var.get()
        
        # 結果を設定
        self.result = {
            "user_name": user_name,
            "comment": comment,
            "rating": rating,
            "image_path": self.image_path
        }
        
        # ダイアログを閉じる
        self.dialog.destroy()
    
    def cancel(self):
        """
        キャンセルする
        """
        self.dialog.destroy()

class UserReportViewer:
    """
    ユーザーレポート表示用クラス
    """
    def __init__(self, parent, recipe, report_manager):
        self.parent = parent
        self.recipe = recipe
        self.report_manager = report_manager
        
        # フォント設定
        self.title_font = ("Yu Gothic", 14, "bold")
        self.header_font = ("Yu Gothic", 12, "bold")
        self.normal_font = ("Yu Gothic", 10)
        
        # レポートを取得
        self.reports = report_manager.get_reports_for_recipe(recipe["id"])
    
    def create_viewer(self, container):
        """
        レポート表示用ウィジェットを作成する
        """
        # メインフレーム
        main_frame = ttk.Frame(container, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # タイトル
        title_label = ttk.Label(main_frame, text=f"{self.recipe['name']}のつくったよレポート", font=self.title_font)
        title_label.pack(pady=(0, 10))
        
        # レポート数
        count_label = ttk.Label(main_frame, text=f"全{len(self.reports)}件のレポート", font=self.normal_font)
        count_label.pack(pady=(0, 10))
        
        # レポート追加ボタン
        add_button = ttk.Button(main_frame, text="レポートを投稿する", command=self.add_report)
        add_button.pack(pady=(0, 20))
        
        # レポート一覧
        if not self.reports:
            no_reports_label = ttk.Label(main_frame, text="まだレポートがありません。最初のレポートを投稿しましょう！", font=self.normal_font)
            no_reports_label.pack(pady=20)
        else:
            # スクロール可能なキャンバス
            canvas = tk.Canvas(main_frame)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # レポートを表示
            for i, report in enumerate(self.reports):
                self.create_report_widget(scrollable_frame, report, i)
    
    def create_report_widget(self, parent, report, index):
        """
        個別のレポートウィジェットを作成する
        """
        # レポートフレーム
        report_frame = ttk.Frame(parent, padding=10)
        report_frame.pack(fill=tk.X, pady=10)
        
        # 区切り線（最初のレポート以外）
        if index > 0:
            separator = ttk.Separator(report_frame, orient="horizontal")
            separator.pack(fill=tk.X, pady=(0, 10))
        
        # ヘッダー情報（ユーザー名、日付、評価）
        header_frame = ttk.Frame(report_frame)
        header_frame.pack(fill=tk.X)
        
        user_label = ttk.Label(header_frame, text=report["user_name"], font=self.header_font)
        user_label.pack(side=tk.LEFT)
        
        date_label = ttk.Label(header_frame, text=report["date"], font=self.normal_font)
        date_label.pack(side=tk.RIGHT)
        
        # 評価
        rating_frame = ttk.Frame(report_frame)
        rating_frame.pack(fill=tk.X, pady=5)
        
        rating_label = ttk.Label(rating_frame, text="評価: ", font=self.normal_font)
        rating_label.pack(side=tk.LEFT)
        
        for i in range(1, 6):
            star = "★" if i <= report["rating"] else "☆"
            star_label = ttk.Label(rating_frame, text=star, font=self.normal_font)
            star_label.pack(side=tk.LEFT)
        
        # コメント
        comment_frame = ttk.LabelFrame(report_frame, text="コメント", padding=5)
        comment_frame.pack(fill=tk.X, pady=5)
        
        comment_label = ttk.Label(comment_frame, text=report["comment"], font=self.normal_font, wraplength=400)
        comment_label.pack(anchor=tk.W)
        
        # 画像（あれば）
        if report.get("image"):
            image_path = self.report_manager.get_image_path(report["image"])
            if image_path and os.path.exists(image_path):
                try:
                    image = Image.open(image_path)
                    image = image.resize((300, 200), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    
                    image_label = ttk.Label(report_frame, image=photo)
                    image_label.image = photo  # 参照を保持
                    image_label.pack(pady=10)
                except Exception as e:
                    print(f"画像の読み込みエラー: {e}")
    
    def add_report(self):
        """
        新しいレポートを追加する
        """
        dialog = UserReportDialog(self.parent, self.recipe)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.result:
            # レポートを追加
            success = self.report_manager.add_report(
                self.recipe["id"],
                dialog.result["user_name"],
                dialog.result["comment"],
                dialog.result["rating"],
                dialog.result["image_path"]
            )
            
            if success:
                messagebox.showinfo("成功", "レポートが投稿されました！")
                
                # レポートを再読み込み
                self.reports = self.report_manager.get_reports_for_recipe(self.recipe["id"])
                
                # 表示を更新（ここでは簡易的に親ウィンドウを再描画）
                for widget in self.parent.winfo_children():
                    widget.destroy()
                
                self.create_viewer(self.parent)
            else:
                messagebox.showerror("エラー", "レポートの投稿に失敗しました。")

if __name__ == "__main__":
    # テスト用コード
    root = tk.Tk()
    root.title("つくったよレポート")
    root.geometry("600x800")
    
    # サンプルレシピ
    sample_recipe = {
        "id": 1,
        "name": "豚の生姜焼き",
        "ingredients": ["豚肉", "生姜", "醤油"],
        "steps": ["手順1", "手順2", "手順3"],
        "user_reports": []
    }
    
    # レポートマネージャー
    report_manager = UserReportManager()
    
    # レポートビューアー
    viewer = UserReportViewer(root, sample_recipe, report_manager)
    viewer.create_viewer(root)
    
    root.mainloop()