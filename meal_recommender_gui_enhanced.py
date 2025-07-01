# -*- coding: utf-8 -*-
import sys
import random
import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import json
import os
# import requests  # オンライン機能を無効化
import threading
import time
import datetime
# from PIL import Image, ImageTk  # 使用していないため無効化
# import matplotlib  # 栄養可視化機能を無効化
# matplotlib.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 新機能のインポート
from weekly_meal_planner import generate_weekly_meal_plan, get_nutrition_summary
# from nutrition_visualizer import NutritionVisualizer, create_weekly_nutrition_chart  # matplotlib依存のため無効化
from user_reports import UserReportManager, UserReportViewer
from user_preferences import UserPreferences
from ingredient_inventory import IngredientInventory

# Ensure stdout is using UTF-8 encoding for Japanese text
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

# レシピデータベースをJSONファイルから読み込む
def load_recipes(file_path='recipes_enhanced.json'):
    """JSONファイルからレシピデータを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("拡張レシピファイルが見つかりません。通常のレシピファイルを使用します。")
        try:
            with open('recipes.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("レシピファイルが見つかりません。デフォルトのレシピを使用します。")
            return default_recipes()
    except json.JSONDecodeError:
        print("レシピファイルの形式が正しくありません。デフォルトのレシピを使用します。")
        return default_recipes()

# デフォルトのレシピデータ（JSONファイルが読み込めない場合に使用）
def default_recipes():
    """デフォルトのレシピデータを返す"""
    return [
    {
        "id": 1,
        "name": "豚の生姜焼き",
        "ingredients": [
            "豚ロース薄切り 200g", 
            "玉ねぎ 1/2個", 
            "生姜 1かけ", 
            "醤油 大さじ2", 
            "みりん 大さじ2", 
            "酒 大さじ1", 
            "砂糖 小さじ1"
        ],
        "steps": [
            "1. 玉ねぎは薄切り、生姜はすりおろす。",
            "2. 豚肉に塩こしょうを軽くふる。",
            "3. フライパンに油を熱し、豚肉を中火で焼く。",
            "4. 肉の色が変わったら玉ねぎを加えて炒める。",
            "5. 玉ねぎがしんなりしたら、調味料と生姜を加えて絡める。",
            "6. 全体に味がなじんだら完成。"
        ],
        "tags_mood": ["元気を出したい", "やる気アップ"],
        "tags_condition": ["疲れている", "スタミナ不足"],
        "comment": "ビタミンB1が豊富で疲労回復に効果的です！",
        "nutrition": {
            "calories": 450,
            "protein": 25,
            "fat": 30,
            "carbs": 15,
            "vitamins": ["ビタミンB1", "ビタミンB6"],
            "minerals": ["亜鉛", "鉄分"]
        }
    },
    {
        "id": 2,
        "name": "鶏むね肉とブロッコリーの蒸し物",
        "ingredients": [
            "鶏むね肉 1枚", 
            "ブロッコリー 1/2個", 
            "塩 少々", 
            "こしょう 少々", 
            "オリーブオイル 小さじ1", 
            "レモン汁 小さじ1"
        ],
        "steps": [
            "1. 鶏むね肉は一口大に切り、塩こしょうをふる。",
            "2. ブロッコリーは小房に分ける。",
            "3. 耐熱容器に鶏肉とブロッコリーを入れ、オリーブオイルを回しかける。",
            "4. ラップをして600Wの電子レンジで4分加熱する。",
            "5. 取り出してレモン汁をかけたら完成。"
        ],
        "tags_mood": ["リラックスしたい", "穏やかな気分になりたい"],
        "tags_condition": ["胃腸の調子が悪い", "ヘルシーに食べたい"],
        "comment": "高タンパク低カロリーで、胃腸に優しい一品です。",
        "nutrition": {
            "calories": 250,
            "protein": 30,
            "fat": 10,
            "carbs": 8,
            "vitamins": ["ビタミンC", "ビタミンK", "ビタミンB6"],
            "minerals": ["カリウム", "マグネシウム"]
        }
    }
    ]

# レシピデータを読み込む
recipes = load_recipes()

# 気分の選択肢
moods = [
    "元気を出したい",
    "リラックスしたい",
    "落ち込んでいる",
    "集中したい",
    "気分転換したい",
    "ほっとしたい"
]

# 体調の選択肢
conditions = [
    "疲れている",
    "胃腸の調子が悪い",
    "風邪気味",
    "特に問題なし",
    "喉が痛い",
    "貧血気味",
    "暑さで食欲がない",
    "栄養補給したい"
]

# 季節の選択肢
seasons = [
    "春",
    "夏",
    "秋",
    "冬"
]

# 現在の季節を取得する関数
def get_current_season():
    """現在の月から季節を判定する"""
    import datetime
    month = datetime.datetime.now().month
    
    if 3 <= month <= 5:
        return "春"
    elif 6 <= month <= 8:
        return "夏"
    elif 9 <= month <= 11:
        return "秋"
    else:  # 12, 1, 2月
        return "冬"

# オンラインからレシピを検索する関数
def search_online_recipes(query, limit=5):
    """オンラインからレシピを検索する"""
    try:
        # 楽天レシピAPIのエンドポイント (実際のAPIキーが必要)
        # 注: これは例示用です。実際の実装では適切なAPIキーが必要です
        api_key = "dummy_api_key"  # 実際のAPIキーに置き換える必要があります
        
        # 検索クエリを作成
        params = {
            "applicationId": api_key,
            "keyword": query,
            "format": "json",
            "hits": limit
        }
        
        # オンライン機能は無効化 - ダミーデータを返す
        print("オンライン機能は無効化されています。ダミーデータを使用します。")
        return generate_dummy_recipes(query, limit)
    
    except Exception as e:
        print(f"オンラインレシピの検索中にエラーが発生しました: {e}")
        return []

# ダミーレシピデータを生成する関数
def generate_dummy_recipes(query, limit=3):
    """ダミーのレシピデータを生成する（APIが使用できない場合のフォールバック）"""
    dummy_recipes = []
    
    recipe_templates = [
        {
            "title": f"{query}に最適な健康レシピ",
            "description": f"{query}の状態に合わせた栄養バランスの良いレシピです。",
            "materials": ["玉ねぎ", "にんじん", "豚肉", "醤油", "みりん", "砂糖"],
            "time": "約30分",
            "cost": "300円前後"
        },
        {
            "title": f"簡単！{query}向けの15分クッキング",
            "description": "忙しい日でも手軽に作れる栄養満点レシピ。",
            "materials": ["卵", "ほうれん草", "ベーコン", "塩", "こしょう"],
            "time": "約15分",
            "cost": "200円前後"
        },
        {
            "title": f"{query}に効果的な薬膳風レシピ",
            "description": "東洋医学の知恵を取り入れた体に優しいレシピです。",
            "materials": ["生姜", "鶏肉", "白菜", "しいたけ", "ねぎ", "醤油", "酒"],
            "time": "約40分",
            "cost": "400円前後"
        }
    ]
    
    # 必要な数のレシピを生成
    for i in range(min(limit, len(recipe_templates))):
        template = recipe_templates[i]
        recipe = {
            "id": 1000 + i,
            "name": template["title"],
            "ingredients": template["materials"],
            "steps": [
                f"1. {template['description']}",
                f"2. 調理時間: {template['time']}",
                f"3. 予算: {template['cost']}"
            ],
            "tags_mood": [query],
            "tags_condition": [query],
            "comment": template["description"],
            "source": "オンラインレシピ",
            "nutrition": {
                "calories": random.randint(200, 500),
                "protein": random.randint(10, 30),
                "fat": random.randint(5, 25),
                "carbs": random.randint(10, 50),
                "vitamins": ["ビタミンA", "ビタミンC"],
                "minerals": ["カルシウム", "鉄分"]
            }
        }
        dummy_recipes.append(recipe)
    
    return dummy_recipes

def find_recipes(selected_mood, selected_condition, selected_season=None, include_online=True, user_preferences=None):
    """
    選択された気分と体調、季節に基づいてレシピを検索する
    オンラインレシピも含める場合はinclude_online=Trueを指定
    アレルギーや嫌いな食材を除外する場合はuser_preferencesを指定
    """
    matching_recipes = []
    
    # 季節が選択されていない場合は現在の季節を使用
    if not selected_season:
        selected_season = get_current_season()
    
    # ローカルレシピから検索
    for recipe in recipes:
        # アレルギーや嫌いな食材をチェック
        if user_preferences:
            is_compatible, _ = user_preferences.check_recipe_compatibility(recipe)
            if not is_compatible:
                continue  # アレルギーや嫌いな食材を含む場合はスキップ
        
        mood_match = selected_mood in recipe.get("tags_mood", [])
        condition_match = selected_condition in recipe.get("tags_condition", [])
        
        # 季節タグがある場合は季節も考慮
        if "tags_season" in recipe:
            season_match = selected_season in recipe["tags_season"]
        else:
            # 季節タグがない場合は季節に関係なくマッチ
            season_match = True
        
        # 気分、体調、季節の全てに一致するレシピを最優先
        if mood_match and condition_match and season_match:
            matching_recipes.append((recipe, 3))  # スコア3（最高）
        # 気分と体調に一致するレシピを次に優先
        elif mood_match and condition_match:
            matching_recipes.append((recipe, 2))  # スコア2
        # 気分と季節、または体調と季節に一致するレシピ
        elif (mood_match and season_match) or (condition_match and season_match):
            matching_recipes.append((recipe, 1.5))  # スコア1.5
        # 気分だけ、または体調だけに一致するレシピ
        elif mood_match or condition_match:
            matching_recipes.append((recipe, 1))  # スコア1
        # 季節だけに一致するレシピ
        elif season_match:
            matching_recipes.append((recipe, 0.5))  # スコア0.5
    
    # オンラインレシピを検索
    if include_online:
        # 検索クエリを作成
        query = f"{selected_mood} {selected_condition} {selected_season}"
        online_recipes = search_online_recipes(query)
        
        # オンラインレシピにスコア2を付与（ローカルの最優先レシピの次に表示）
        for recipe in online_recipes:
            matching_recipes.append((recipe, 2.5))
    
    # マッチするレシピがない場合はランダムに1つ選ぶ
    if not matching_recipes:
        if include_online:
            # オンラインから一般的なレシピを検索
            online_recipes = search_online_recipes("健康 レシピ")
            if online_recipes:
                return online_recipes
        
        # それでもなければローカルからランダムに選択
        return [random.choice(recipes)]
    
    # スコアでソート（降順）
    matching_recipes.sort(key=lambda x: x[1], reverse=True)
    
    # レシピのみを返す（スコアは除く）
    return [recipe for recipe, score in matching_recipes]

class MealRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("今日の最適ごはん提案アプリ")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # レシピ数を表示するためのラベル
        self.recipe_count_label = None
        
        # フォント設定
        self.title_font = font.Font(family="Yu Gothic", size=16, weight="bold")
        self.header_font = font.Font(family="Yu Gothic", size=12, weight="bold")
        self.normal_font = font.Font(family="Yu Gothic", size=10)
        
        # 変数の初期化
        self.mood_var = tk.StringVar()
        self.condition_var = tk.StringVar()
        self.season_var = tk.StringVar(value=get_current_season())  # 現在の季節をデフォルト値に設定
        self.current_recipe_index = 0
        self.matching_recipes = []
        self.current_step = 1  # 現在の選択ステップ（1: 季節, 2: 気分, 3: 体調）
        
        # 週間献立プラン
        self.weekly_meal_plan = None
        
        # ユーザーレポートマネージャー
        self.report_manager = UserReportManager()
        
        # ユーザー設定
        self.user_preferences = UserPreferences()
        
        # 食材在庫管理
        self.ingredient_inventory = IngredientInventory()
        
        # カラーテーマ設定
        self.base_bg_color = "#f0f8ff"  # 薄い青色の背景
        self.accent_color = "#3498db"    # アクセントカラー
        self.text_color = "#2c3e50"      # テキストカラー
        self.highlight_color = "#e74c3c" # ハイライトカラー
        
        # 季節ごとの色設定
        self.season_colors = {
            "春": {"bg": "#f8e5ff", "accent": "#e056fd", "text": "#6c5ce7"},  # 春: 薄紫
            "夏": {"bg": "#e3f9ff", "accent": "#0abde3", "text": "#0652DD"},  # 夏: 水色
            "秋": {"bg": "#fff5e5", "accent": "#fa8231", "text": "#cc8e35"},  # 秋: オレンジ
            "冬": {"bg": "#f1f2f6", "accent": "#a5b1c2", "text": "#4b6584"}   # 冬: グレー
        }
        
        # 気分ごとの色設定
        self.mood_colors = {
            "元気を出したい": "#ff7979",      # 赤
            "リラックスしたい": "#badc58",    # 緑
            "落ち込んでいる": "#7ed6df",      # 水色
            "集中したい": "#e056fd",          # 紫
            "気分転換したい": "#f9ca24",      # 黄色
            "ほっとしたい": "#f0932b"         # オレンジ
        }
        
        # 体調ごとの色設定
        self.condition_colors = {
            "疲れている": "#eb4d4b",          # 赤
            "胃腸の調子が悪い": "#6ab04c",    # 緑
            "風邪気味": "#22a6b3",            # 青緑
            "特に問題なし": "#4834d4",        # 青紫
            "喉が痛い": "#be2edd",            # 紫
            "貧血気味": "#f0932b",            # オレンジ
            "暑さで食欲がない": "#ffbe76",    # 薄いオレンジ
            "栄養補給したい": "#7ed6df"       # 水色
        }
        
        # 現在の季節に基づいて基本色を設定
        current_season = get_current_season()
        self.current_theme = self.season_colors[current_season]
        
        # スタイル設定
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.base_bg_color)
        self.style.configure("TLabelframe", background=self.base_bg_color)
        self.style.configure("TLabelframe.Label", font=self.header_font, background=self.base_bg_color, foreground=self.text_color)
        self.style.configure("TLabel", background=self.base_bg_color, foreground=self.text_color)
        # ボタンスタイルの設定（macOS対応）
        self.style.configure("TButton", 
            font=self.normal_font, 
            background=self.accent_color, 
            foreground="#ffffff",
            borderwidth=1,
            focuscolor="none",
            relief="solid"
        )
        self.style.map("TButton",
            background=[("active", self.current_theme["accent"]), ("pressed", "#2980b9"), ("disabled", "#bdc3c7"), ("!disabled", self.accent_color)],
            foreground=[("active", "#ffffff"), ("pressed", "#ffffff"), ("disabled", "#95a5a6"), ("!disabled", "#ffffff")],
            relief=[("active", "solid"), ("pressed", "sunken"), ("!disabled", "solid")]
        )
        self.style.configure("Header.TLabel", font=self.header_font, background=self.base_bg_color, foreground=self.current_theme["text"])
        self.style.configure("Title.TLabel", font=self.title_font, background=self.base_bg_color, foreground=self.current_theme["text"])
        
        # 季節ごとのスタイル
        for season, colors in self.season_colors.items():
            self.style.configure(f"{season}.TFrame", background=colors["bg"])
            self.style.configure(f"{season}.TLabel", background=colors["bg"], foreground=colors["text"])
            self.style.configure(f"{season}.TLabelframe", background=colors["bg"])
            self.style.configure(f"{season}.TLabelframe.Label", background=colors["bg"], foreground=colors["text"])
        
        # メインフレーム
        self.main_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # スクロールバー
        self.main_scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical")
        self.main_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # メインキャンバス
        self.main_canvas = tk.Canvas(self.main_frame, background=self.base_bg_color, highlightthickness=0)
        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # キャンバスとスクロールバーを連動
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)
        self.main_scrollbar.configure(command=self.main_canvas.yview)
        
        # スクロール可能なフレーム
        self.scrollable_frame = ttk.Frame(self.main_canvas, style="TFrame")
        self.scrollable_frame_window = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # ヘッダーフレーム
        header_frame = ttk.Frame(self.scrollable_frame, style="TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # タイトル
        title_label = ttk.Label(
            header_frame,
            text="今日の最適ごはん提案アプリ",
            font=self.title_font,
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(
            header_frame,
            text="こころとからだのごはんサポーター",
            font=self.header_font,
            style="Header.TLabel"
        )
        subtitle_label.pack(pady=(0, 10))
        
        # レシピ数表示
        self.recipe_count_label = ttk.Label(
            header_frame,
            text=f"現在のレシピ数: {len(recipes)}種類",
            font=self.normal_font,
            style="TLabel"
        )
        self.recipe_count_label.pack(pady=(0, 5))
        
        # タブコントロール
        self.tab_control = ttk.Notebook(self.scrollable_frame)
        self.tab_control.pack(fill=tk.BOTH, expand=True)
        
        # 単品レシピ検索タブ
        self.single_recipe_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.single_recipe_tab, text="単品レシピ検索")
        
        # 週間献立プランタブ
        self.weekly_plan_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.weekly_plan_tab, text="週間献立プラン")
        
        # 設定タブ
        self.preferences_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.preferences_tab, text="設定")
        
        # 食材在庫タブ
        self.inventory_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.inventory_tab, text="食材在庫")
        
        # 単品レシピ検索タブの内容を作成
        self.create_single_recipe_tab()
        
        # 週間献立プランタブの内容を作成
        self.create_weekly_plan_tab()
        
        # 設定タブの内容を作成
        self.create_preferences_tab()
        
        # 食材在庫タブの内容を作成
        self.create_inventory_tab()
        
        # 選択したレシピのリスト（買い物リスト生成用）
        self.selected_recipes = []
        
        # キャンバスのサイズ調整
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.main_canvas.bind("<Configure>", self.on_canvas_configure)
        
        # マウスホイールでスクロール
        self.main_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
    def create_single_recipe_tab(self):
        """単品レシピ検索タブの内容を作成"""
        # 選択フレーム
        selection_frame = ttk.Frame(self.single_recipe_tab, style="TFrame")
        selection_frame.pack(fill=tk.X, pady=10)
        
        # 季節選択
        season_frame = ttk.LabelFrame(selection_frame, text="季節", padding=15)
        season_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 季節アイコンと色の設定
        season_icons = {
            "春": "🌸",
            "夏": "☀️",
            "秋": "🍁",
            "冬": "❄️"
        }
        
        for season in seasons:
            season_frame_item = ttk.Frame(season_frame, style=f"{season}.TFrame")
            season_frame_item.pack(fill=tk.X, pady=3)
            
            icon_label = ttk.Label(
                season_frame_item,
                text=season_icons[season],
                font=font.Font(family="Yu Gothic", size=12),
                style=f"{season}.TLabel"
            )
            icon_label.pack(side=tk.LEFT, padx=(0, 5))
            
            rb = ttk.Radiobutton(
                season_frame_item,
                text=season,
                value=season,
                variable=self.season_var,
                command=self.check_selection
            )
            rb.pack(side=tk.LEFT)
        
        # 気分選択
        mood_frame = ttk.LabelFrame(selection_frame, text="今日の気分", padding=15)
        mood_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 5))
        
        # 気分アイコンの設定
        mood_icons = {
            "元気を出したい": "💪",
            "リラックスしたい": "😌",
            "落ち込んでいる": "😔",
            "集中したい": "🧠",
            "気分転換したい": "🔄",
            "ほっとしたい": "☕"
        }
        
        for mood in moods:
            mood_frame_item = ttk.Frame(mood_frame)
            mood_frame_item.pack(fill=tk.X, pady=3)
            
            icon_label = ttk.Label(
                mood_frame_item,
                text=mood_icons[mood],
                font=font.Font(family="Yu Gothic", size=12)
            )
            icon_label.pack(side=tk.LEFT, padx=(0, 5))
            
            rb = ttk.Radiobutton(
                mood_frame_item,
                text=mood,
                value=mood,
                variable=self.mood_var,
                command=self.check_selection
            )
            rb.pack(side=tk.LEFT)
        
        # 体調選択
        condition_frame = ttk.LabelFrame(selection_frame, text="今日の体調", padding=15)
        condition_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # 体調アイコンの設定
        condition_icons = {
            "疲れている": "😫",
            "胃腸の調子が悪い": "🤢",
            "風邪気味": "🤧",
            "特に問題なし": "😊",
            "喉が痛い": "😷",
            "貧血気味": "😵",
            "暑さで食欲がない": "🥵",
            "栄養補給したい": "💪"
        }
        
        for condition in conditions:
            condition_frame_item = ttk.Frame(condition_frame)
            condition_frame_item.pack(fill=tk.X, pady=3)
            
            icon_label = ttk.Label(
                condition_frame_item,
                text=condition_icons[condition],
                font=font.Font(family="Yu Gothic", size=12)
            )
            icon_label.pack(side=tk.LEFT, padx=(0, 5))
            
            rb = ttk.Radiobutton(
                condition_frame_item,
                text=condition,
                value=condition,
                variable=self.condition_var,
                command=self.check_selection
            )
            rb.pack(side=tk.LEFT)
        
        # 検索ボタンフレーム
        button_frame = ttk.Frame(self.single_recipe_tab)
        button_frame.pack(fill=tk.X, pady=20)
        
        # 検索ボタン（標準tkinter.Buttonで色を明示的に指定）
        self.search_button = tk.Button(
            button_frame,
            text="レシピを検索",
            command=self.search_recipes,
            state="disabled",
            font=self.normal_font,
            bg="#3498db",  # 青色背景
            fg="white",    # 白色文字
            relief="raised",
            borderwidth=2,
            padx=20,
            pady=5
        )
        self.search_button.pack(side=tk.RIGHT)
        
        # レシピ表示フレーム
        self.recipe_frame = ttk.Frame(self.single_recipe_tab)
        self.recipe_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 初期メッセージ
        ttk.Label(
            self.recipe_frame,
            text="気分と体調を選択して、レシピを検索してください。",
            font=self.normal_font
        ).pack(pady=50)
    
    def create_weekly_plan_tab(self):
        """週間献立プランタブの内容を作成"""
        # 設定フレーム
        settings_frame = ttk.Frame(self.weekly_plan_tab)
        settings_frame.pack(fill=tk.X, pady=10)
        
        # 説明ラベル
        description_label = ttk.Label(
            settings_frame,
            text="あなたの状態に合わせた1週間の献立プランを生成します。",
            font=self.header_font
        )
        description_label.pack(pady=(0, 10))
        
        # 条件選択フレーム
        condition_frame = ttk.Frame(settings_frame)
        condition_frame.pack(fill=tk.X, pady=5)
        
        # 体調選択
        ttk.Label(condition_frame, text="体調:", font=self.normal_font).pack(side=tk.LEFT, padx=(0, 5))
        
        self.weekly_condition_var = tk.StringVar()
        condition_combo = ttk.Combobox(condition_frame, textvariable=self.weekly_condition_var, values=conditions, width=15)
        condition_combo.pack(side=tk.LEFT, padx=(0, 20))
        condition_combo.current(0)
        
        # 栄養バランス考慮
        self.balance_var = tk.BooleanVar(value=True)
        balance_check = ttk.Checkbutton(condition_frame, text="栄養バランスを考慮", variable=self.balance_var)
        balance_check.pack(side=tk.LEFT)
        
        # 生成ボタン（標準tkinter.Buttonで色を明示的に指定）
        generate_button = tk.Button(
            settings_frame, 
            text="献立プランを生成", 
            command=self.generate_weekly_plan,
            font=self.normal_font,
            bg="#27ae60",  # 緑色背景
            fg="white",    # 白色文字
            relief="raised",
            borderwidth=2,
            padx=20,
            pady=5
        )
        generate_button.pack(pady=10)
        
        # 結果表示フレーム
        self.weekly_result_frame = ttk.Frame(self.weekly_plan_tab)
        self.weekly_result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 初期メッセージ
        ttk.Label(
            self.weekly_result_frame,
            text="「献立プランを生成」ボタンをクリックして、1週間の献立プランを作成してください。",
            font=self.normal_font,
            wraplength=600
        ).pack(pady=50)
    
    def check_selection(self):
        """選択状態をチェックし、検索ボタンの有効/無効を切り替える"""
        if self.mood_var.get() and self.condition_var.get():
            self.search_button.config(state="normal")
        else:
            self.search_button.config(state="disabled")
    
    def create_inventory_tab(self):
        """食材在庫管理タブの内容を作成"""
        # メインフレーム
        main_frame = ttk.Frame(self.inventory_tab, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左側フレーム（在庫リスト）
        left_frame = ttk.LabelFrame(main_frame, text="食材在庫", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 在庫リスト
        inventory_frame = ttk.Frame(left_frame)
        inventory_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # スクロールバー付きリストボックス
        self.inventory_listbox_frame = ttk.Frame(inventory_frame)
        self.inventory_listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.inventory_listbox = tk.Listbox(
            self.inventory_listbox_frame,
            font=self.normal_font,
            selectmode=tk.SINGLE,
            height=15
        )
        self.inventory_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        inventory_scrollbar = ttk.Scrollbar(self.inventory_listbox_frame, orient=tk.VERTICAL, command=self.inventory_listbox.yview)
        inventory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.inventory_listbox.config(yscrollcommand=inventory_scrollbar.set)
        
        # 在庫追加フレーム
        add_inventory_frame = ttk.Frame(left_frame)
        add_inventory_frame.pack(fill=tk.X, pady=5)
        
        # 食材名入力
        ttk.Label(add_inventory_frame, text="食材名:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ingredient_name_var = tk.StringVar()
        ingredient_name_entry = ttk.Entry(add_inventory_frame, textvariable=self.ingredient_name_var, width=15)
        ingredient_name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 数量入力
        ttk.Label(add_inventory_frame, text="数量:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.ingredient_quantity_var = tk.StringVar()
        ingredient_quantity_entry = ttk.Entry(add_inventory_frame, textvariable=self.ingredient_quantity_var, width=5)
        ingredient_quantity_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # 単位入力
        ttk.Label(add_inventory_frame, text="単位:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.ingredient_unit_var = tk.StringVar()
        ingredient_unit_combo = ttk.Combobox(add_inventory_frame, textvariable=self.ingredient_unit_var, width=5)
        ingredient_unit_combo['values'] = ('g', 'kg', '個', '本', '袋', 'ml', 'L', '枚', '束')
        ingredient_unit_combo.grid(row=0, column=5, sticky=tk.W, padx=5, pady=5)
        
        # 賞味期限入力
        ttk.Label(add_inventory_frame, text="賞味期限:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.ingredient_expiry_var = tk.StringVar()
        ingredient_expiry_entry = ttk.Entry(add_inventory_frame, textvariable=self.ingredient_expiry_var, width=15)
        ingredient_expiry_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(add_inventory_frame, text="(YYYY-MM-DD)").grid(row=1, column=3, columnspan=3, sticky=tk.W, padx=5, pady=5)
        
        # ボタンフレーム
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        # 追加ボタン
        add_button = ttk.Button(button_frame, text="追加", command=self.add_ingredient)
        add_button.pack(side=tk.LEFT, padx=5)
        
        # 削除ボタン
        remove_button = ttk.Button(button_frame, text="削除", command=self.remove_ingredient)
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # 更新ボタン
        refresh_button = ttk.Button(button_frame, text="更新", command=self.refresh_inventory)
        refresh_button.pack(side=tk.RIGHT, padx=5)
        
        # 右側フレーム（買い物リスト）
        right_frame = ttk.LabelFrame(main_frame, text="買い物リスト", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # 買い物リスト
        shopping_frame = ttk.Frame(right_frame)
        shopping_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # スクロールバー付きリストボックス
        self.shopping_listbox_frame = ttk.Frame(shopping_frame)
        self.shopping_listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.shopping_listbox = tk.Listbox(
            self.shopping_listbox_frame,
            font=self.normal_font,
            selectmode=tk.SINGLE,
            height=15
        )
        self.shopping_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        shopping_scrollbar = ttk.Scrollbar(self.shopping_listbox_frame, orient=tk.VERTICAL, command=self.shopping_listbox.yview)
        shopping_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.shopping_listbox.config(yscrollcommand=shopping_scrollbar.set)
        
        # 買い物リスト追加フレーム
        add_shopping_frame = ttk.Frame(right_frame)
        add_shopping_frame.pack(fill=tk.X, pady=5)
        
        # 項目入力
        ttk.Label(add_shopping_frame, text="項目:").pack(side=tk.LEFT, padx=5)
        self.shopping_item_var = tk.StringVar()
        shopping_item_entry = ttk.Entry(add_shopping_frame, textvariable=self.shopping_item_var, width=30)
        shopping_item_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # ボタンフレーム
        shopping_button_frame = ttk.Frame(right_frame)
        shopping_button_frame.pack(fill=tk.X, pady=5)
        
        # 追加ボタン
        add_shopping_button = ttk.Button(shopping_button_frame, text="追加", command=self.add_shopping_item)
        add_shopping_button.pack(side=tk.LEFT, padx=5)
        
        # 削除ボタン
        remove_shopping_button = ttk.Button(shopping_button_frame, text="削除", command=self.remove_shopping_item)
        remove_shopping_button.pack(side=tk.LEFT, padx=5)
        
        # クリアボタン
        clear_shopping_button = ttk.Button(shopping_button_frame, text="クリア", command=self.clear_shopping_list)
        clear_shopping_button.pack(side=tk.RIGHT, padx=5)
        
        # 選択したレシピから買い物リスト生成ボタン
        generate_shopping_frame = ttk.Frame(right_frame)
        generate_shopping_frame.pack(fill=tk.X, pady=10)
        
        generate_shopping_button = ttk.Button(
            generate_shopping_frame,
            text="選択したレシピから買い物リスト生成",
            command=self.generate_shopping_list_from_selected_recipes
        )
        generate_shopping_button.pack(fill=tk.X)
        
        # レシピ検索フレーム
        recipe_search_frame = ttk.LabelFrame(main_frame, text="在庫食材からレシピ検索", padding=10)
        recipe_search_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # 説明ラベル
        ttk.Label(
            recipe_search_frame,
            text="在庫にある食材を使ったレシピを検索します。",
            font=self.normal_font
        ).pack(pady=(0, 10))
        
        # 検索ボタン
        search_inventory_button = ttk.Button(
            recipe_search_frame,
            text="在庫食材でレシピ検索",
            command=self.search_recipes_by_inventory
        )
        search_inventory_button.pack(pady=5)
        
        # 初期表示
        self.refresh_inventory()
        self.refresh_shopping_list()
    
    def add_ingredient(self):
        """食材を在庫に追加する"""
        name = self.ingredient_name_var.get().strip()
        if not name:
            messagebox.showwarning("入力エラー", "食材名を入力してください。")
            return
        
        # 数量を取得（数値に変換）
        quantity_str = self.ingredient_quantity_var.get().strip()
        quantity = None
        if quantity_str:
            try:
                quantity = float(quantity_str)
            except ValueError:
                messagebox.showwarning("入力エラー", "数量は数値で入力してください。")
                return
        
        unit = self.ingredient_unit_var.get().strip()
        expiry_date = self.ingredient_expiry_var.get().strip()
        
        # 在庫に追加
        success = self.ingredient_inventory.add_ingredient(name, quantity, unit, expiry_date)
        
        if success:
            messagebox.showinfo("成功", f"{name}を在庫に追加しました。")
            # 入力フィールドをクリア
            self.ingredient_name_var.set("")
            self.ingredient_quantity_var.set("")
            self.ingredient_unit_var.set("")
            self.ingredient_expiry_var.set("")
            # 在庫リストを更新
            self.refresh_inventory()
        else:
            messagebox.showerror("エラー", "在庫の追加に失敗しました。")
    
    def remove_ingredient(self):
        """選択された食材を在庫から削除する"""
        selection = self.inventory_listbox.curselection()
        if not selection:
            messagebox.showwarning("選択エラー", "削除する食材を選択してください。")
            return
        
        # 選択された項目のテキストから食材名を抽出
        item_text = self.inventory_listbox.get(selection[0])
        name = item_text.split(":")[0].strip()
        
        # 確認ダイアログ
        if messagebox.askyesno("確認", f"{name}を在庫から削除しますか？"):
            success = self.ingredient_inventory.remove_ingredient(name)
            
            if success:
                messagebox.showinfo("成功", f"{name}を在庫から削除しました。")
                # 在庫リストを更新
                self.refresh_inventory()
            else:
                messagebox.showerror("エラー", "在庫の削除に失敗しました。")
    
    def refresh_inventory(self):
        """在庫リストを更新する"""
        # リストボックスをクリア
        self.inventory_listbox.delete(0, tk.END)
        
        # 在庫データを取得
        inventory = self.ingredient_inventory.get_inventory()
        
        # 在庫リストに追加
        for name, data in inventory.items():
            quantity = data.get('quantity', '')
            unit = data.get('unit', '')
            expiry_date = data.get('expiry_date', '')
            
            display_text = f"{name}: {quantity} {unit}"
            if expiry_date:
                display_text += f" (期限: {expiry_date})"
            
            self.inventory_listbox.insert(tk.END, display_text)
    
    def add_shopping_item(self):
        """買い物リストに項目を追加する"""
        item = self.shopping_item_var.get().strip()
        if not item:
            messagebox.showwarning("入力エラー", "買い物リストの項目を入力してください。")
            return
        
        success = self.ingredient_inventory.add_to_shopping_list(item)
        
        if success:
            # 入力フィールドをクリア
            self.shopping_item_var.set("")
            # 買い物リストを更新
            self.refresh_shopping_list()
        else:
            messagebox.showerror("エラー", "買い物リストの追加に失敗しました。")
    
    def remove_shopping_item(self):
        """選択された項目を買い物リストから削除する"""
        selection = self.shopping_listbox.curselection()
        if not selection:
            messagebox.showwarning("選択エラー", "削除する項目を選択してください。")
            return
        
        # 選択された項目のテキスト
        item = self.shopping_listbox.get(selection[0])
        
        success = self.ingredient_inventory.remove_from_shopping_list(item)
        
        if success:
            # 買い物リストを更新
            self.refresh_shopping_list()
        else:
            messagebox.showerror("エラー", "買い物リストの削除に失敗しました。")
    
    def clear_shopping_list(self):
        """買い物リストをクリアする"""
        if messagebox.askyesno("確認", "買い物リストをクリアしますか？"):
            success = self.ingredient_inventory.clear_shopping_list()
            
            if success:
                # 買い物リストを更新
                self.refresh_shopping_list()
            else:
                messagebox.showerror("エラー", "買い物リストのクリアに失敗しました。")
    
    def refresh_shopping_list(self):
        """買い物リストを更新する"""
        # リストボックスをクリア
        self.shopping_listbox.delete(0, tk.END)
        
        # 買い物リストを取得
        shopping_list = self.ingredient_inventory.get_shopping_list()
        
        # 買い物リストに追加
        for item in shopping_list:
            self.shopping_listbox.insert(tk.END, item)
    
    def search_recipes_by_inventory(self):
        """在庫にある食材を使ったレシピを検索する"""
        # 検索中メッセージを表示
        searching_window = tk.Toplevel(self.root)
        searching_window.title("検索中")
        searching_window.geometry("300x100")
        searching_window.transient(self.root)
        searching_window.grab_set()
        
        ttk.Label(
            searching_window,
            text="在庫食材を使ったレシピを検索中...",
            font=self.normal_font
        ).pack(pady=20)
        
        # 検索処理を別スレッドで実行
        def search_thread():
            try:
                # 在庫食材を使ったレシピを検索
                matching_recipes = self.ingredient_inventory.find_recipes_with_available_ingredients(recipes)
                
                # 検索結果を表示するウィンドウを作成
                self.root.after(100, lambda: self.show_inventory_recipe_results(matching_recipes))
                
                # 検索中ウィンドウを閉じる
                self.root.after(100, searching_window.destroy)
            except Exception as e:
                print(f"レシピ検索中にエラーが発生しました: {e}")
                messagebox.showerror("エラー", f"レシピ検索中にエラーが発生しました: {e}")
                searching_window.destroy()
        
        threading.Thread(target=search_thread).start()
    
    def show_inventory_recipe_results(self, matching_recipes):
        """在庫食材を使ったレシピの検索結果を表示する"""
        if not matching_recipes:
            messagebox.showinfo("検索結果", "在庫食材を使ったレシピが見つかりませんでした。")
            return
        
        # 結果ウィンドウを作成
        result_window = tk.Toplevel(self.root)
        result_window.title("在庫食材レシピ検索結果")
        result_window.geometry("800x600")
        result_window.transient(self.root)
        
        # メインフレーム
        main_frame = ttk.Frame(result_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # タイトル
        ttk.Label(
            main_frame,
            text="在庫食材を使ったレシピ",
            font=self.title_font
        ).pack(pady=(0, 20))
        
        # 検索結果数
        ttk.Label(
            main_frame,
            text=f"{len(matching_recipes)}件のレシピが見つかりました",
            font=self.normal_font
        ).pack(pady=(0, 10))
        
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
        
        # レシピを表示
        for i, recipe in enumerate(matching_recipes):
            recipe_frame = ttk.Frame(scrollable_frame, padding=10)
            recipe_frame.pack(fill=tk.X, pady=10)
            
            # 区切り線（最初のレシピ以外）
            if i > 0:
                separator = ttk.Separator(recipe_frame, orient="horizontal")
                separator.pack(fill=tk.X, pady=(0, 10))
            
            # レシピ名
            name_frame = ttk.Frame(recipe_frame)
            name_frame.pack(fill=tk.X)
            
            ttk.Label(
                name_frame,
                text=recipe["name"],
                font=self.header_font
            ).pack(side=tk.LEFT)
            
            # 一致率
            match_ratio = recipe.get("match_ratio", 0) * 100
            ttk.Label(
                name_frame,
                text=f"一致率: {match_ratio:.1f}%",
                font=self.normal_font
            ).pack(side=tk.RIGHT)
            
            # 利用可能な食材
            available_frame = ttk.LabelFrame(recipe_frame, text="在庫にある食材", padding=5)
            available_frame.pack(fill=tk.X, pady=5)
            
            available_text = ", ".join(recipe.get("available_ingredients", []))
            ttk.Label(
                available_frame,
                text=available_text or "なし",
                font=self.normal_font,
                wraplength=700
            ).pack(anchor=tk.W)
            
            # 不足している食材
            missing_frame = ttk.LabelFrame(recipe_frame, text="不足している食材", padding=5)
            missing_frame.pack(fill=tk.X, pady=5)
            
            missing_text = ", ".join(recipe.get("missing_ingredients", []))
            ttk.Label(
                missing_frame,
                text=missing_text or "なし",
                font=self.normal_font,
                wraplength=700
            ).pack(anchor=tk.W)
            
            # 買い物リストに追加ボタン
            if recipe.get("missing_ingredients"):
                add_button = ttk.Button(
                    recipe_frame,
                    text="不足食材を買い物リストに追加",
                    command=lambda r=recipe: self.add_missing_to_shopping_list(r)
                )
                add_button.pack(anchor=tk.E, pady=5)
            
            # レシピ詳細ボタン
            detail_button = ttk.Button(
                recipe_frame,
                text="レシピ詳細",
                command=lambda r=recipe: self.show_recipe_detail(r)
            )
            detail_button.pack(anchor=tk.E, pady=5)
    
    def add_missing_to_shopping_list(self, recipe):
        """不足している食材を買い物リストに追加する"""
        missing_ingredients = recipe.get("missing_ingredients", [])
        if not missing_ingredients:
            return
        
        # 買い物リストに追加
        added_count = 0
        for ingredient in missing_ingredients:
            success = self.ingredient_inventory.add_to_shopping_list(ingredient)
            if success:
                added_count += 1
        
        if added_count > 0:
            messagebox.showinfo("成功", f"{added_count}個の食材を買い物リストに追加しました。")
            # 買い物リストを更新
            self.refresh_shopping_list()
        else:
            messagebox.showinfo("情報", "買い物リストに追加する食材がありませんでした。")
    
    def search_recipes(self):
        """レシピを検索して表示する"""
        selected_mood = self.mood_var.get()
        selected_condition = self.condition_var.get()
        selected_season = self.season_var.get()
        user_preferences = self.user_preferences
        
        # 検索中メッセージを表示
        for widget in self.recipe_frame.winfo_children():
            widget.destroy()
        
        searching_label = ttk.Label(
            self.recipe_frame,
            text="レシピを検索中...",
            font=self.header_font
        )
        searching_label.pack(pady=20)
        self.root.update()
        
        # 別スレッドで検索を実行
        def search_thread():
            # 常にオンラインレシピを含めて検索
            try:
                # オンラインレシピを検索
                query = f"{selected_mood} {selected_condition} {selected_season}"
                online_recipes = search_online_recipes(query)
                
                # ローカルレシピも検索（アレルギーや嫌いな食材を除外）
                local_recipes = find_recipes(selected_mood, selected_condition, selected_season, include_online=False, user_preferences=user_preferences)
                
                # オンラインレシピとローカルレシピを結合
                all_recipes = online_recipes + local_recipes
                
                # 重複を除去（IDが同じレシピを除去）
                unique_recipes = []
                recipe_ids = set()
                
                for recipe in all_recipes:
                    if recipe["id"] not in recipe_ids:
                        unique_recipes.append(recipe)
                        recipe_ids.add(recipe["id"])
                
                self.matching_recipes = unique_recipes
                self.current_recipe_index = 0
                
                # 在庫食材を考慮したレシピのスコアリング
                # 在庫にある食材を多く使うレシピを優先
                inventory = self.ingredient_inventory.get_inventory()
                if inventory:
                    inventory_keys = set(inventory.keys())
                    for recipe in self.matching_recipes:
                        if "ingredients" in recipe:
                            recipe_ingredients = []
                            for ingredient_str in recipe["ingredients"]:
                                parts = ingredient_str.split()
                                if len(parts) >= 2:
                                    ingredient_name = ' '.join(parts[1:])
                                    recipe_ingredients.append(ingredient_name)
                            
                            if recipe_ingredients:
                                recipe_ingredients_set = set(recipe_ingredients)
                                common_ingredients = inventory_keys.intersection(recipe_ingredients_set)
                                match_ratio = len(common_ingredients) / len(recipe_ingredients_set)
                                
                                # 既存のスコアに在庫一致率を加味
                                recipe["inventory_match"] = match_ratio
                                recipe["available_ingredients"] = list(common_ingredients)
                                recipe["missing_ingredients"] = list(recipe_ingredients_set - inventory_keys)
                
                # レシピ数を更新
                self.recipe_count_label.config(text=f"現在のレシピ数: {len(recipes) + len(online_recipes)}種類")
                
                # UIを更新
                self.root.after(0, self.update_ui_after_search)
            except Exception as e:
                print(f"レシピ検索中にエラーが発生しました: {e}")
                # エラー時はローカルレシピのみを表示（アレルギーや嫌いな食材を除外）
                local_recipes = find_recipes(selected_mood, selected_condition, selected_season, include_online=False, user_preferences=user_preferences)
                self.matching_recipes = local_recipes
                self.current_recipe_index = 0
                self.root.after(0, self.update_ui_after_search)
        
        # 検索スレッドを開始
        threading.Thread(target=search_thread, daemon=True).start()
    
    def update_ui_after_search(self):
        """検索結果に基づいてUIを更新する"""
        # 季節に基づいてUIカラーを更新
        self.update_ui_colors(self.season_var.get())
        
        # 現在のレシピを表示
        self.display_current_recipe()
    
    def update_ui_colors(self, season):
        """季節に基づいてUIカラーを更新する"""
        if season in self.season_colors:
            self.current_theme = self.season_colors[season]
            
            # スタイルを更新
            self.style.configure("Title.TLabel", foreground=self.current_theme["text"])
            self.style.configure("Header.TLabel", foreground=self.current_theme["text"])
            self.style.map("TButton",
                background=[("active", self.current_theme["accent"]), ("disabled", "#bdc3c7")]
            )
            
            # キャンバスの背景色を更新
            self.main_canvas.configure(background=self.current_theme["bg"])
            
            # スクロール可能なフレームの背景色を更新
            self.scrollable_frame.configure(style=f"{season}.TFrame")
    
    def display_current_recipe(self):
        """現在のレシピを表示する"""
        # レシピフレームをクリア
        for widget in self.recipe_frame.winfo_children():
            widget.destroy()
        
        if not self.matching_recipes:
            # レシピが見つからない場合
            no_recipe_label = ttk.Label(
                self.recipe_frame,
                text="条件に合うレシピが見つかりませんでした。",
                font=self.header_font
            )
            no_recipe_label.pack(pady=20)
            return
        
        # 現在のレシピを取得
        recipe = self.matching_recipes[self.current_recipe_index]
        
        # アレルギーや嫌いな食材をチェック
        is_compatible, incompatible_items = self.user_preferences.check_recipe_compatibility(recipe)
        
        # レシピ表示フレーム
        recipe_display_frame = ttk.Frame(self.recipe_frame)
        recipe_display_frame.pack(fill=tk.BOTH, expand=True)
        
        # レシピ名
        recipe_name_frame = ttk.Frame(recipe_display_frame)
        recipe_name_frame.pack(fill=tk.X, pady=(0, 10))
        
        recipe_name_label = ttk.Label(
            recipe_name_frame,
            text=recipe["name"],
            font=self.title_font
        )
        recipe_name_label.pack(side=tk.LEFT)
        
        # 買い物リストに追加ボタン
        add_to_shopping_button = ttk.Button(
            recipe_name_frame,
            text="買い物リストに追加",
            command=lambda: self.toggle_recipe_for_shopping_list(recipe)
        )
        add_to_shopping_button.pack(side=tk.RIGHT)
        
        # 在庫食材の一致情報（あれば表示）
        if "inventory_match" in recipe:
            match_frame = ttk.Frame(recipe_display_frame)
            match_frame.pack(fill=tk.X, pady=(0, 10))
            
            match_ratio = recipe["inventory_match"] * 100
            match_label = ttk.Label(
                match_frame,
                text=f"在庫食材一致率: {match_ratio:.1f}%",
                font=self.normal_font
            )
            match_label.pack(side=tk.LEFT)
            
            # 買い物リストに追加ボタン（不足食材がある場合）
            if recipe.get("missing_ingredients"):
                add_button = ttk.Button(
                    match_frame,
                    text="不足食材を買い物リストに追加",
                    command=lambda: self.add_missing_to_shopping_list(recipe)
                )
                add_button.pack(side=tk.RIGHT)
        
        # オンラインレシピの場合はソースを表示
        if "source" in recipe and recipe["source"] == "オンラインレシピ":
            source_label = ttk.Label(
                recipe_name_frame,
                text="[オンラインレシピ]",
                font=self.normal_font,
                foreground="#0652DD"
            )
            source_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 専門家監修の場合は表示
        if "expert_supervision" in recipe and recipe["expert_supervision"]["supervised"]:
            expert_label = ttk.Label(
                recipe_name_frame,
                text=f"[監修: {recipe['expert_supervision']['expert_name']}]",
                font=self.normal_font,
                foreground="#6ab04c"
            )
            expert_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # コメント
        if "comment" in recipe:
            comment_frame = ttk.LabelFrame(recipe_display_frame, text="ポイント")
            comment_frame.pack(fill=tk.X, pady=5)
            
            comment_label = ttk.Label(
                comment_frame,
                text=recipe["comment"],
                font=self.normal_font,
                wraplength=600
            )
            comment_label.pack(pady=5, padx=5, anchor=tk.W)
        
        # アレルギーや嫌いな食材の警告
        if not is_compatible:
            warning_frame = ttk.LabelFrame(recipe_display_frame, text="⚠️ 注意", padding=5)
            warning_frame.pack(fill=tk.X, pady=5)
            
            warning_text = "このレシピには以下の食材が含まれています：\n"
            for item in incompatible_items:
                warning_text += f"• {item['item']} ({item['type']})\n"
            
            warning_label = ttk.Label(
                warning_frame,
                text=warning_text,
                font=self.normal_font,
                foreground="#e74c3c",
                wraplength=600
            )
            warning_label.pack(pady=5, padx=5, anchor=tk.W)
        
        # タブコントロール（レシピ詳細用）
        recipe_tabs = ttk.Notebook(recipe_display_frame)
        recipe_tabs.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 材料タブ
        ingredients_tab = ttk.Frame(recipe_tabs)
        recipe_tabs.add(ingredients_tab, text="材料")
        
        # 作り方タブ
        steps_tab = ttk.Frame(recipe_tabs)
        recipe_tabs.add(steps_tab, text="作り方")
        
        # 栄養情報タブ
        nutrition_tab = ttk.Frame(recipe_tabs)
        recipe_tabs.add(nutrition_tab, text="栄養情報")
        
        # つくったよレポートタブ
        reports_tab = ttk.Frame(recipe_tabs)
        recipe_tabs.add(reports_tab, text="つくったよレポート")
        
        # 材料タブの内容
        ingredients_frame = ttk.Frame(ingredients_tab, padding=10)
        ingredients_frame.pack(fill=tk.BOTH, expand=True)
        
        for ingredient in recipe["ingredients"]:
            ingredient_frame = ttk.Frame(ingredients_frame)
            ingredient_frame.pack(fill=tk.X, pady=2)
            
            bullet_label = ttk.Label(ingredient_frame, text="•", font=self.normal_font)
            bullet_label.pack(side=tk.LEFT, padx=(0, 5))
            
            ingredient_label = ttk.Label(ingredient_frame, text=ingredient, font=self.normal_font)
            ingredient_label.pack(side=tk.LEFT)
        
        # 代替食材があれば表示
        if "alternatives" in recipe and recipe["alternatives"]:
            alt_frame = ttk.LabelFrame(ingredients_tab, text="代替食材", padding=10)
            alt_frame.pack(fill=tk.X, pady=10, padx=10)
            
            for alt in recipe["alternatives"]:
                alt_item_frame = ttk.Frame(alt_frame)
                alt_item_frame.pack(fill=tk.X, pady=2)
                
                alt_label = ttk.Label(
                    alt_item_frame,
                    text=f"{alt['ingredient']} → {alt['alternative']}",
                    font=self.normal_font
                )
                alt_label.pack(side=tk.LEFT)
                
                if "note" in alt:
                    note_label = ttk.Label(
                        alt_item_frame,
                        text=f"（{alt['note']}）",
                        font=self.normal_font,
                        foreground="#7f8c8d"
                    )
                    note_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 作り方タブの内容
        steps_frame = ttk.Frame(steps_tab, padding=10)
        steps_frame.pack(fill=tk.BOTH, expand=True)
        
        # 調理モード（キッチンモード）ボタン
        kitchen_mode_frame = ttk.Frame(steps_frame)
        kitchen_mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        kitchen_mode_button = tk.Button(
            kitchen_mode_frame,
            text="調理モードで開く",
            command=lambda: self.open_kitchen_mode(recipe),
            font=self.normal_font,
            bg="#e67e22",  # オレンジ背景
            fg="white",    # 白色文字
            relief="raised",
            borderwidth=1,
            padx=15,
            pady=3
        )
        kitchen_mode_button.pack(side=tk.RIGHT)
        
        # 手順を表示
        for step in recipe["steps"]:
            step_label = ttk.Label(steps_frame, text=step, font=self.normal_font, wraplength=600)
            step_label.pack(anchor=tk.W, pady=5)
        
        # 栄養情報タブの内容（栄養可視化機能は無効化）
        if "nutrition" in recipe:
            # 栄養情報をテキストで表示
            nutrition_info = recipe["nutrition"]
            nutrition_text = f"カロリー: {nutrition_info.get('calories', 'N/A')} kcal\n"
            nutrition_text += f"タンパク質: {nutrition_info.get('protein', 'N/A')} g\n"
            nutrition_text += f"脂質: {nutrition_info.get('fat', 'N/A')} g\n"
            nutrition_text += f"炭水化物: {nutrition_info.get('carbs', 'N/A')} g\n"
            if 'vitamins' in nutrition_info:
                nutrition_text += f"ビタミン: {', '.join(nutrition_info['vitamins'])}\n"
            if 'minerals' in nutrition_info:
                nutrition_text += f"ミネラル: {', '.join(nutrition_info['minerals'])}"
            
            ttk.Label(
                nutrition_tab,
                text=nutrition_text,
                font=self.normal_font,
                justify=tk.LEFT
            ).pack(pady=20, padx=20, anchor=tk.W)
        else:
            ttk.Label(
                nutrition_tab,
                text="このレシピには栄養情報がありません。",
                font=self.normal_font
            ).pack(pady=20)
        
        # つくったよレポートタブの内容
        report_viewer = UserReportViewer(reports_tab, recipe, self.report_manager)
        report_viewer.create_viewer(reports_tab)
        
        # ナビゲーションボタン
        nav_frame = ttk.Frame(recipe_display_frame)
        nav_frame.pack(fill=tk.X, pady=10)
        
        self.prev_button = tk.Button(
            nav_frame,
            text="前のレシピ",
            command=self.show_prev_recipe,
            font=self.normal_font,
            bg="#95a5a6",  # グレー背景
            fg="white",    # 白色文字
            relief="raised",
            borderwidth=1,
            padx=15,
            pady=3
        )
        self.prev_button.pack(side=tk.LEFT)
        
        self.next_button = tk.Button(
            nav_frame,
            text="次のレシピ",
            command=self.show_next_recipe,
            font=self.normal_font,
            bg="#95a5a6",  # グレー背景
            fg="white",    # 白色文字
            relief="raised",
            borderwidth=1,
            padx=15,
            pady=3
        )
        self.next_button.pack(side=tk.RIGHT)
        
        # 再検索ボタン
        restart_button = tk.Button(
            nav_frame,
            text="条件を変えて再検索",
            command=self.restart_search,
            font=self.normal_font,
            bg="#f39c12",  # オレンジ背景
            fg="white",    # 白色文字
            relief="raised",
            borderwidth=1,
            padx=15,
            pady=3
        )
        restart_button.pack(side=tk.TOP, pady=(10, 0))
            
    def open_kitchen_mode(self, recipe):
        """調理モード（キッチンモード）を開く"""
        if not recipe or "steps" not in recipe:
            messagebox.showerror("エラー", "レシピの手順が見つかりません。")
            return
            
        # キッチンモードウィンドウを作成
        kitchen_window = tk.Toplevel(self.root)
        kitchen_window.title(f"調理モード: {recipe['name']}")
        kitchen_window.geometry("800x600")
        kitchen_window.protocol("WM_DELETE_WINDOW", lambda: self.close_kitchen_mode(kitchen_window))
        
        # スクリーンセーバーを無効化（スリープ防止）
        if sys.platform.startswith('win'):
            # Windowsの場合
            kitchen_window.attributes('-topmost', True)  # 常に最前面に表示
            # スリープ防止のためのコード（実際の実装では適切なライブラリを使用）
            try:
                import ctypes
                ES_CONTINUOUS = 0x80000000
                ES_SYSTEM_REQUIRED = 0x00000001
                ES_DISPLAY_REQUIRED = 0x00000002
                ctypes.windll.kernel32.SetThreadExecutionState(
                    ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
            except Exception as e:
                print(f"スリープ防止の設定中にエラーが発生しました: {e}")
        elif sys.platform.startswith('darwin'):
            # macOSの場合
            kitchen_window.attributes('-topmost', True)  # 常に最前面に表示
            # macOSでのスリープ防止は別途実装が必要
        
        # メインフレーム
        main_frame = ttk.Frame(kitchen_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # タイトル
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text=recipe["name"],
            font=font.Font(family="Yu Gothic", size=24, weight="bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # 閉じるボタン
        close_button = ttk.Button(
            title_frame,
            text="調理モードを終了",
            command=lambda: self.close_kitchen_mode(kitchen_window)
        )
        close_button.pack(side=tk.RIGHT)
        
        # 材料フレーム
        ingredients_frame = ttk.LabelFrame(main_frame, text="材料", padding=10)
        ingredients_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 材料を2列で表示
        ingredients_grid = ttk.Frame(ingredients_frame)
        ingredients_grid.pack(fill=tk.X, padx=5, pady=5)
        
        ingredients = recipe["ingredients"]
        half_length = (len(ingredients) + 1) // 2
        
        for i, ingredient in enumerate(ingredients):
            row = i % half_length
            col = i // half_length
            
            ingredient_frame = ttk.Frame(ingredients_grid)
            ingredient_frame.grid(row=row, column=col, sticky="w", padx=10, pady=2)
            
            bullet_label = ttk.Label(
                ingredient_frame,
                text="•",
                font=font.Font(family="Yu Gothic", size=14)
            )
            bullet_label.pack(side=tk.LEFT, padx=(0, 5))
            
            ingredient_label = ttk.Label(
                ingredient_frame,
                text=ingredient,
                font=font.Font(family="Yu Gothic", size=14)
            )
            ingredient_label.pack(side=tk.LEFT)
        
        # 代替食材があれば表示
        if "alternatives" in recipe and recipe["alternatives"]:
            alt_frame = ttk.LabelFrame(main_frame, text="代替食材", padding=10)
            alt_frame.pack(fill=tk.X, pady=(0, 20))
            
            for alt in recipe["alternatives"]:
                alt_item_frame = ttk.Frame(alt_frame)
                alt_item_frame.pack(fill=tk.X, pady=2)
                
                alt_label = ttk.Label(
                    alt_item_frame,
                    text=f"{alt['ingredient']} → {alt['alternative']}",
                    font=font.Font(family="Yu Gothic", size=14)
                )
                alt_label.pack(side=tk.LEFT)
                
                if "note" in alt:
                    note_label = ttk.Label(
                        alt_item_frame,
                        text=f"（{alt['note']}）",
                        font=font.Font(family="Yu Gothic", size=14),
                        foreground="#7f8c8d"
                    )
                    note_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 手順フレーム
        steps_frame = ttk.LabelFrame(main_frame, text="調理手順", padding=10)
        steps_frame.pack(fill=tk.BOTH, expand=True)
        
        # スクロール可能なキャンバス
        canvas = tk.Canvas(steps_frame)
        scrollbar = ttk.Scrollbar(steps_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 手順を大きなフォントで表示
        for i, step in enumerate(recipe["steps"]):
            step_frame = ttk.Frame(scrollable_frame, padding=10)
            step_frame.pack(fill=tk.X, pady=5)
            
            # 手順番号
            step_num = i + 1
            step_num_label = ttk.Label(
                step_frame,
                text=f"手順 {step_num}",
                font=font.Font(family="Yu Gothic", size=16, weight="bold")
            )
            step_num_label.pack(anchor=tk.W)
            
            # 手順内容
            step_content = step
            if step.startswith(f"{step_num}."):
                # 番号が既に含まれている場合は除去
                step_content = step[step.find(".")+1:].strip()
            
            step_label = ttk.Label(
                step_frame,
                text=step_content,
                font=font.Font(family="Yu Gothic", size=16),
                wraplength=700,
                justify=tk.LEFT
            )
            step_label.pack(anchor=tk.W, pady=(5, 0))
            
            # タイマーボタン（時間が含まれる場合）
            time_patterns = [
                r'(\d+)分', r'(\d+)秒',
                r'(\d+)時間', r'(\d+)時',
                r'(\d+)min', r'(\d+)sec',
                r'(\d+)hour', r'(\d+)hr'
            ]
            
            import re
            time_found = False
            for pattern in time_patterns:
                match = re.search(pattern, step_content)
                if match:
                    time_found = True
                    time_value = int(match.group(1))
                    time_unit = match.group(0)[len(match.group(1)):]
                    
                    # 時間を秒に変換
                    seconds = time_value
                    if '分' in time_unit or 'min' in time_unit:
                        seconds = time_value * 60
                    elif '時間' in time_unit or '時' in time_unit or 'hour' in time_unit or 'hr' in time_unit:
                        seconds = time_value * 3600
                    
                    timer_button = ttk.Button(
                        step_frame,
                        text=f"タイマーをセット ({match.group(0)})",
                        command=lambda s=seconds: self.set_timer(s, kitchen_window)
                    )
                    timer_button.pack(anchor=tk.E, pady=(5, 0))
                    break
            
            # 区切り線
            if i < len(recipe["steps"]) - 1:
                separator = ttk.Separator(scrollable_frame, orient="horizontal")
                separator.pack(fill=tk.X, pady=10)
        
        # タイマーフレーム（初期状態では非表示）
        self.timer_frame = ttk.Frame(main_frame)
        self.timer_frame.pack_forget()
        
        self.timer_label = ttk.Label(
            self.timer_frame,
            text="00:00",
            font=font.Font(family="Yu Gothic", size=24, weight="bold")
        )
        self.timer_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.timer_stop_button = ttk.Button(
            self.timer_frame,
            text="タイマー停止",
            command=self.stop_timer
        )
        self.timer_stop_button.pack(side=tk.LEFT)
        
        # タイマー変数
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_after_id = None
        
        # キッチンモードウィンドウを中央に配置
        kitchen_window.update_idletasks()
        width = kitchen_window.winfo_width()
        height = kitchen_window.winfo_height()
        x = (kitchen_window.winfo_screenwidth() // 2) - (width // 2)
        y = (kitchen_window.winfo_screenheight() // 2) - (height // 2)
        kitchen_window.geometry(f'{width}x{height}+{x}+{y}')
    
    def set_timer(self, seconds, parent_window):
        """タイマーをセットする"""
        # 既存のタイマーを停止
        self.stop_timer()
        
        # タイマー変数を設定
        self.timer_running = True
        self.timer_seconds = seconds
        
        # タイマーフレームを表示
        self.timer_frame.pack(fill=tk.X, pady=10)
        
        # タイマーを更新
        self.update_timer(parent_window)
    
    def update_timer(self, parent_window):
        """タイマーを更新する"""
        if not self.timer_running:
            return
            
        # 残り時間を計算
        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        
        # タイマーラベルを更新
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        
        # タイマーが終了したらアラートを表示
        if self.timer_seconds <= 0:
            self.timer_running = False
            messagebox.showinfo("タイマー", "時間になりました！", parent=parent_window)
            # アラート音を鳴らす（実際の実装では適切なライブラリを使用）
            parent_window.bell()
            return
            
        # 1秒減らす
        self.timer_seconds -= 1
        
        # 1秒後に再度更新
        self.timer_after_id = parent_window.after(1000, lambda: self.update_timer(parent_window))
    
    def stop_timer(self):
        """タイマーを停止する"""
        if self.timer_after_id:
            try:
                self.root.after_cancel(self.timer_after_id)
            except Exception:
                pass
            self.timer_after_id = None
        
        self.timer_running = False
        self.timer_frame.pack_forget()
    
    def close_kitchen_mode(self, kitchen_window):
        """キッチンモードを閉じる"""
        # タイマーを停止
        self.stop_timer()
        
        # スリープ防止を解除
        if sys.platform.startswith('win'):
            try:
                import ctypes
                ES_CONTINUOUS = 0x80000000
                ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            except Exception as e:
                print(f"スリープ防止の解除中にエラーが発生しました: {e}")
        
        # ウィンドウを閉じる
        kitchen_window.destroy()
        
    def toggle_recipe_for_shopping_list(self, recipe):
        """買い物リスト生成用にレシピを選択/解除する"""
        if not recipe:
            return
            
        # レシピIDを取得
        recipe_id = recipe.get("id")
        if not recipe_id:
            return
            
        # 既に選択されているか確認
        for i, selected_recipe in enumerate(self.selected_recipes):
            if selected_recipe.get("id") == recipe_id:
                # 既に選択されている場合は解除
                self.selected_recipes.pop(i)
                messagebox.showinfo("買い物リスト", f"{recipe['name']}を買い物リスト生成から除外しました。")
                return
                
        # 選択されていない場合は追加
        self.selected_recipes.append(recipe)
        
        # 選択したレシピの数を表示
        messagebox.showinfo(
            "買い物リスト",
            f"{recipe['name']}を買い物リスト生成に追加しました。\n"
            f"現在{len(self.selected_recipes)}個のレシピが選択されています。\n"
            f"食材在庫タブで「選択したレシピから買い物リスト生成」ボタンを押すと、"
            f"必要な材料をまとめた買い物リストが生成されます。"
        )
        
    def generate_shopping_list_from_selected_recipes(self):
        """選択したレシピから買い物リストを生成する"""
        if not self.selected_recipes:
            messagebox.showinfo("買い物リスト", "レシピが選択されていません。\n"
                               "レシピ表示画面で「買い物リストに追加」ボタンを押して、"
                               "レシピを選択してください。")
            return
            
        # 買い物リストを生成
        success = self.ingredient_inventory.generate_shopping_list_from_recipes(self.selected_recipes)
        
        if success:
            # 買い物リストを更新
            self.refresh_shopping_list()
            
            # 選択したレシピの数をメッセージで表示
            recipe_names = [recipe.get("name", "不明なレシピ") for recipe in self.selected_recipes]
            message = "以下のレシピから買い物リストを生成しました：\n\n"
            for name in recipe_names:
                message += f"• {name}\n"
                
            messagebox.showinfo("買い物リスト生成完了", message)
            
            # 選択したレシピをクリア
            self.selected_recipes = []
        else:
            messagebox.showerror("エラー", "買い物リストの生成に失敗しました。")
    
    def show_prev_recipe(self):
        """前のレシピを表示する"""
        if self.current_recipe_index > 0:
            self.current_recipe_index -= 1
            self.display_current_recipe()
    
    def show_next_recipe(self):
        """次のレシピを表示する"""
        if self.current_recipe_index < len(self.matching_recipes) - 1:
            self.current_recipe_index += 1
            self.display_current_recipe()
    
    def update_navigation_buttons(self):
        """ナビゲーションボタンの状態を更新する"""
        if self.current_recipe_index <= 0:
            self.prev_button.config(state="disabled")
        else:
            self.prev_button.config(state="normal")
        
        if self.current_recipe_index >= len(self.matching_recipes) - 1:
            self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="normal")
    
    def restart_search(self):
        """検索をリセットする"""
        # レシピフレームをクリア
        for widget in self.recipe_frame.winfo_children():
            widget.destroy()
        
        # 選択をリセット
        self.mood_var.set("")
        self.condition_var.set("")
        
        # 検索ボタンを無効化
        self.search_button.config(state="disabled")
        
        # 初期メッセージを表示
        ttk.Label(
            self.recipe_frame,
            text="気分と体調を選択して、レシピを検索してください。",
            font=self.normal_font
        ).pack(pady=50)
    
    def generate_weekly_plan(self):
        """週間献立プランを生成する"""
        # 選択された条件を取得
        condition = self.weekly_condition_var.get()
        balanced = self.balance_var.get()
        season = self.season_var.get()
        
        # 生成中メッセージを表示
        for widget in self.weekly_result_frame.winfo_children():
            widget.destroy()
        
        generating_label = ttk.Label(
            self.weekly_result_frame,
            text="献立プランを生成中...",
            font=self.header_font
        )
        generating_label.pack(pady=20)
        self.root.update()
        
        # 別スレッドで生成を実行
        def generate_thread():
            try:
                # 週間献立プランを生成
                meal_plan = generate_weekly_meal_plan(
                    condition=condition,
                    season=season,
                    balanced_nutrition=balanced
                )
                
                self.weekly_meal_plan = meal_plan
                
                # UIを更新
                self.root.after(0, self.display_weekly_plan)
            except Exception as e:
                print(f"献立プラン生成中にエラーが発生しました: {e}")
                self.root.after(0, lambda: self.show_weekly_plan_error(str(e)))
        
        # 生成スレッドを開始
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def display_weekly_plan(self):
        """週間献立プランを表示する"""
        # 結果フレームをクリア
        for widget in self.weekly_result_frame.winfo_children():
            widget.destroy()
        
        if not self.weekly_meal_plan:
            ttk.Label(
                self.weekly_result_frame,
                text="献立プランの生成に失敗しました。",
                font=self.header_font
            ).pack(pady=20)
            return
        
        # タブコントロール（週間プラン用）
        plan_tabs = ttk.Notebook(self.weekly_result_frame)
        plan_tabs.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 献立表タブ
        schedule_tab = ttk.Frame(plan_tabs)
        plan_tabs.add(schedule_tab, text="献立表")
        
        # 栄養バランスタブ
        nutrition_tab = ttk.Frame(plan_tabs)
        plan_tabs.add(nutrition_tab, text="栄養バランス")
        
        # 献立表タブの内容
        schedule_frame = ttk.Frame(schedule_tab, padding=10)
        schedule_frame.pack(fill=tk.BOTH, expand=True)
        
        # 曜日ごとの献立を表示
        for day, meals in self.weekly_meal_plan.items():
            day_frame = ttk.LabelFrame(schedule_frame, text=day, padding=10)
            day_frame.pack(fill=tk.X, pady=5)
            
            for meal_type, recipe in meals.items():
                if recipe:
                    meal_frame = ttk.Frame(day_frame)
                    meal_frame.pack(fill=tk.X, pady=2)
                    
                    meal_label = ttk.Label(
                        meal_frame,
                        text=f"{meal_type}: {recipe['name']}",
                        font=self.normal_font
                    )
                    meal_label.pack(side=tk.LEFT)
                    
                    # レシピ詳細ボタン
                    detail_button = ttk.Button(
                        meal_frame,
                        text="詳細",
                        command=lambda r=recipe: self.show_recipe_detail(r)
                    )
                    detail_button.pack(side=tk.RIGHT)
        
        # 栄養バランスタブの内容
        nutrition_frame = ttk.Frame(nutrition_tab, padding=10)
        nutrition_frame.pack(fill=tk.BOTH, expand=True)
        
        # 栄養サマリーを取得
        nutrition_summary = get_nutrition_summary(self.weekly_meal_plan)
        
        if nutrition_summary:
            # 栄養情報をテキストで表示（グラフ機能は無効化）
            nutrition_text = "週間栄養情報:\n\n"
            for day, summary in nutrition_summary.items():
                nutrition_text += f"{day}:\n"
                nutrition_text += f"  カロリー: {summary.get('calories', 'N/A')} kcal\n"
                nutrition_text += f"  タンパク質: {summary.get('protein', 'N/A')} g\n"
                nutrition_text += f"  脂質: {summary.get('fat', 'N/A')} g\n"
                nutrition_text += f"  炭水化物: {summary.get('carbs', 'N/A')} g\n\n"
            
            nutrition_label = tk.Text(
                nutrition_frame,
                height=15,
                font=self.normal_font,
                wrap=tk.WORD,
                state=tk.DISABLED
            )
            nutrition_label.config(state=tk.NORMAL)
            nutrition_label.insert(tk.END, nutrition_text)
            nutrition_label.config(state=tk.DISABLED)
            nutrition_label.pack(fill=tk.BOTH, expand=True, pady=10)
        else:
            ttk.Label(
                nutrition_frame,
                text="栄養情報を表示できません。",
                font=self.normal_font
            ).pack(pady=20)
        
        # 保存ボタン
        save_button = tk.Button(
            self.weekly_result_frame,
            text="献立プランを保存",
            command=self.save_weekly_plan,
            font=self.normal_font,
            bg="#9b59b6",  # 紫色背景
            fg="white",    # 白色文字
            relief="raised",
            borderwidth=1,
            padx=15,
            pady=5
        )
        save_button.pack(pady=10)
    
    def show_recipe_detail(self, recipe):
        """レシピ詳細ダイアログを表示する"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"レシピ詳細: {recipe['name']}")
        detail_window.geometry("600x500")
        detail_window.transient(self.root)
        detail_window.grab_set()
        
        # レシピ詳細を表示
        detail_frame = ttk.Frame(detail_window, padding=20)
        detail_frame.pack(fill=tk.BOTH, expand=True)
        
        # レシピ名
        ttk.Label(
            detail_frame,
            text=recipe["name"],
            font=self.title_font
        ).pack(pady=(0, 10))
        
        # タブコントロール
        tabs = ttk.Notebook(detail_frame)
        tabs.pack(fill=tk.BOTH, expand=True)
        
        # 材料タブ
        ingredients_tab = ttk.Frame(tabs)
        tabs.add(ingredients_tab, text="材料")
        
        # 作り方タブ
        steps_tab = ttk.Frame(tabs)
        tabs.add(steps_tab, text="作り方")
        
        # 栄養情報タブ
        nutrition_tab = ttk.Frame(tabs)
        tabs.add(nutrition_tab, text="栄養情報")
        
        # 材料タブの内容
        for ingredient in recipe["ingredients"]:
            ttk.Label(
                ingredients_tab,
                text=f"• {ingredient}",
                font=self.normal_font
            ).pack(anchor=tk.W, pady=2, padx=10)
        
        # 作り方タブの内容
        for step in recipe["steps"]:
            ttk.Label(
                steps_tab,
                text=step,
                font=self.normal_font,
                wraplength=500
            ).pack(anchor=tk.W, pady=5, padx=10)
        
        # 栄養情報タブの内容（栄養可視化機能は無効化）
        if "nutrition" in recipe:
            # 栄養情報をテキストで表示
            nutrition_info = recipe["nutrition"]
            nutrition_text = f"カロリー: {nutrition_info.get('calories', 'N/A')} kcal\n"
            nutrition_text += f"タンパク質: {nutrition_info.get('protein', 'N/A')} g\n"
            nutrition_text += f"脂質: {nutrition_info.get('fat', 'N/A')} g\n"
            nutrition_text += f"炭水化物: {nutrition_info.get('carbs', 'N/A')} g\n"
            if 'vitamins' in nutrition_info:
                nutrition_text += f"ビタミン: {', '.join(nutrition_info['vitamins'])}\n"
            if 'minerals' in nutrition_info:
                nutrition_text += f"ミネラル: {', '.join(nutrition_info['minerals'])}"
            
            ttk.Label(
                nutrition_tab,
                text=nutrition_text,
                font=self.normal_font,
                justify=tk.LEFT
            ).pack(pady=20, padx=20, anchor=tk.W)
        else:
            ttk.Label(
                nutrition_tab,
                text="このレシピには栄養情報がありません。",
                font=self.normal_font
            ).pack(pady=20)
        
        # 閉じるボタン
        ttk.Button(
            detail_frame,
            text="閉じる",
            command=detail_window.destroy
        ).pack(pady=10)
    
    def save_weekly_plan(self):
        """週間献立プランをJSONファイルに保存する"""
        if not self.weekly_meal_plan:
            messagebox.showerror("エラー", "保存する献立プランがありません。")
            return
        
        # 保存先を選択
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSONファイル", "*.json"), ("すべてのファイル", "*.*")],
            title="献立プランを保存"
        )
        
        if not file_path:
            return
        
        try:
            # 保存用のデータを作成（レシピの詳細情報を削除）
            simplified_plan = {}
            
            for day, meals in self.weekly_meal_plan.items():
                simplified_plan[day] = {}
                
                for meal_type, recipe in meals.items():
                    if recipe:
                        simplified_plan[day][meal_type] = {
                            "id": recipe["id"],
                            "name": recipe["name"]
                        }
                    else:
                        simplified_plan[day][meal_type] = None
            
            # JSONファイルに保存
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(simplified_plan, file, ensure_ascii=False, indent=4)
            
            messagebox.showinfo("成功", "献立プランを保存しました。")
        
        except Exception as e:
            messagebox.showerror("エラー", f"保存中にエラーが発生しました: {e}")
    
    def show_weekly_plan_error(self, error_message):
        """週間献立プラン生成エラーを表示する"""
        # 結果フレームをクリア
        for widget in self.weekly_result_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(
            self.weekly_result_frame,
            text="献立プランの生成に失敗しました。",
            font=self.header_font
        ).pack(pady=20)
        
        ttk.Label(
            self.weekly_result_frame,
            text=f"エラー: {error_message}",
            font=self.normal_font,
            foreground="#e74c3c"
        ).pack(pady=5)
    
    def on_frame_configure(self, event):
        """スクロール可能なフレームのサイズが変更されたときに呼ばれる"""
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """キャンバスのサイズが変更されたときに呼ばれる"""
        # スクロール可能なフレームの幅をキャンバスの幅に合わせる
        self.main_canvas.itemconfig(self.scrollable_frame_window, width=event.width)
    
    def on_mousewheel(self, event):
        """マウスホイールでスクロールする"""
        self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_preferences_tab(self):
        """設定タブの内容を作成"""
        # メインフレーム
        main_frame = ttk.Frame(self.preferences_tab, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # タイトル
        ttk.Label(
            main_frame,
            text="食材の設定",
            font=self.header_font
        ).pack(pady=(0, 20))
        
        # アレルギー設定フレーム
        allergy_frame = ttk.LabelFrame(main_frame, text="アレルギー食材", padding=10)
        allergy_frame.pack(fill=tk.X, pady=(0, 10))
        
        # アレルギー食材入力
        allergy_input_frame = ttk.Frame(allergy_frame)
        allergy_input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            allergy_input_frame,
            text="アレルギー食材:"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.allergy_entry = ttk.Entry(allergy_input_frame, width=20)
        self.allergy_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        add_allergy_button = ttk.Button(
            allergy_input_frame,
            text="追加",
            command=self.add_allergy
        )
        add_allergy_button.pack(side=tk.LEFT)
        
        # アレルギー食材リスト
        self.allergy_listbox_frame = ttk.Frame(allergy_frame)
        self.allergy_listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.allergy_listbox = tk.Listbox(
            self.allergy_listbox_frame,
            height=5,
            selectmode=tk.SINGLE,
            font=self.normal_font
        )
        self.allergy_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        allergy_scrollbar = ttk.Scrollbar(self.allergy_listbox_frame, orient=tk.VERTICAL, command=self.allergy_listbox.yview)
        allergy_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.allergy_listbox.config(yscrollcommand=allergy_scrollbar.set)
        
        # アレルギー食材削除ボタン
        remove_allergy_button = ttk.Button(
            allergy_frame,
            text="選択した食材を削除",
            command=self.remove_allergy
        )
        remove_allergy_button.pack(pady=5)
        
        # 嫌いな食材設定フレーム
        dislike_frame = ttk.LabelFrame(main_frame, text="嫌いな食材", padding=10)
        dislike_frame.pack(fill=tk.X, pady=10)
        
        # 嫌いな食材入力
        dislike_input_frame = ttk.Frame(dislike_frame)
        dislike_input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            dislike_input_frame,
            text="嫌いな食材:"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.dislike_entry = ttk.Entry(dislike_input_frame, width=20)
        self.dislike_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        add_dislike_button = ttk.Button(
            dislike_input_frame,
            text="追加",
            command=self.add_dislike
        )
        add_dislike_button.pack(side=tk.LEFT)
        
        # 嫌いな食材リスト
        self.dislike_listbox_frame = ttk.Frame(dislike_frame)
        self.dislike_listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.dislike_listbox = tk.Listbox(
            self.dislike_listbox_frame,
            height=5,
            selectmode=tk.SINGLE,
            font=self.normal_font
        )
        self.dislike_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        dislike_scrollbar = ttk.Scrollbar(self.dislike_listbox_frame, orient=tk.VERTICAL, command=self.dislike_listbox.yview)
        dislike_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.dislike_listbox.config(yscrollcommand=dislike_scrollbar.set)
        
        # 嫌いな食材削除ボタン
        remove_dislike_button = ttk.Button(
            dislike_frame,
            text="選択した食材を削除",
            command=self.remove_dislike
        )
        remove_dislike_button.pack(pady=5)
        
        # 設定保存ボタン
        save_button = ttk.Button(
            main_frame,
            text="設定を保存",
            command=self.save_preferences
        )
        save_button.pack(pady=20)
        
        # 現在の設定を表示
        self.update_preferences_display()
    
    def update_preferences_display(self):
        """設定画面の表示を更新"""
        # アレルギーリストをクリア
        self.allergy_listbox.delete(0, tk.END)
        
        # アレルギー食材を表示
        for allergy in self.user_preferences.allergies:
            self.allergy_listbox.insert(tk.END, allergy)
        
        # 嫌いな食材リストをクリア
        self.dislike_listbox.delete(0, tk.END)
        
        # 嫌いな食材を表示
        for dislike in self.user_preferences.dislikes:
            self.dislike_listbox.insert(tk.END, dislike)
    
    def add_allergy(self):
        """アレルギー食材を追加"""
        allergy = self.allergy_entry.get().strip()
        if allergy:
            if self.user_preferences.add_allergy(allergy):
                self.allergy_listbox.insert(tk.END, allergy)
                self.allergy_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("情報", "この食材は既にリストに追加されています。")
    
    def remove_allergy(self):
        """選択したアレルギー食材を削除"""
        selected = self.allergy_listbox.curselection()
        if selected:
            allergy = self.allergy_listbox.get(selected[0])
            if self.user_preferences.remove_allergy(allergy):
                self.allergy_listbox.delete(selected[0])
    
    def add_dislike(self):
        """嫌いな食材を追加"""
        dislike = self.dislike_entry.get().strip()
        if dislike:
            if self.user_preferences.add_dislike(dislike):
                self.dislike_listbox.insert(tk.END, dislike)
                self.dislike_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("情報", "この食材は既にリストに追加されています。")
    
    def remove_dislike(self):
        """選択した嫌いな食材を削除"""
        selected = self.dislike_listbox.curselection()
        if selected:
            dislike = self.dislike_listbox.get(selected[0])
            if self.user_preferences.remove_dislike(dislike):
                self.dislike_listbox.delete(selected[0])
    
    def save_preferences(self):
        """設定を保存"""
        if self.user_preferences.save_preferences():
            messagebox.showinfo("成功", "設定を保存しました。")
        else:
            messagebox.showerror("エラー", "設定の保存に失敗しました。")

def main():
    """メイン関数"""
    root = tk.Tk()
    app = MealRecommenderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()