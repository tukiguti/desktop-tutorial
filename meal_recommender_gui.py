# -*- coding: utf-8 -*-
import sys
import random
import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
import requests
import threading
import time

# Ensure stdout is using UTF-8 encoding for Japanese text
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

# レシピデータベースをJSONファイルから読み込む
def load_recipes():
    """
    JSONファイルからレシピデータを読み込む
    """
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
    """
    デフォルトのレシピデータを返す
    """
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
        "comment": "ビタミンB1が豊富で疲労回復に効果的です！"
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
        "comment": "高タンパク低カロリーで、胃腸に優しい一品です。"
    },
    {
        "id": 3,
        "name": "ほうれん草と卵のスープ",
        "ingredients": [
            "ほうれん草 1束", 
            "卵 2個", 
            "鶏がらスープの素 小さじ2", 
            "水 600ml", 
            "塩 少々", 
            "こしょう 少々", 
            "ごま油 小さじ1"
        ],
        "steps": [
            "1. ほうれん草はさっと茹でて3cm幅に切る。",
            "2. 鍋に水と鶏がらスープの素を入れて沸騰させる。",
            "3. 溶き卵を回し入れる。",
            "4. 卵が固まったらほうれん草を加え、塩こしょうで味を調える。",
            "5. 最後にごま油を垂らして完成。"
        ],
        "tags_mood": ["落ち込んでいる", "リラックスしたい"],
        "tags_condition": ["風邪気味", "喉が痛い"],
        "comment": "ビタミン豊富で消化も良く、体調が優れない時にぴったりです。"
    },
    {
        "id": 4,
        "name": "さばの味噌煮",
        "ingredients": [
            "さば 2切れ", 
            "生姜 1かけ", 
            "水 200ml", 
            "みりん 大さじ2", 
            "酒 大さじ2", 
            "砂糖 大さじ1", 
            "味噌 大さじ2"
        ],
        "steps": [
            "1. さばは両面に塩をふり、10分ほど置いてから水で洗い流す。",
            "2. 生姜は薄切りにする。",
            "3. 鍋にさばと生姜を入れ、水、みりん、酒を加えて中火にかける。",
            "4. 煮立ったらアクを取り除き、砂糖を加える。",
            "5. 5分ほど煮たら味噌を溶き入れ、さらに5分ほど煮る。",
            "6. 味噌が煮詰まったら完成。"
        ],
        "tags_mood": ["元気を出したい", "集中したい"],
        "tags_condition": ["疲れている", "貧血気味"],
        "comment": "DHAやEPAが豊富で、脳の働きを活性化します。鉄分も豊富で貧血予防にも。"
    },
    {
        "id": 5,
        "name": "トマトとモッツァレラのカプレーゼ",
        "ingredients": [
            "トマト 2個", 
            "モッツァレラチーズ 1個", 
            "バジル 適量", 
            "オリーブオイル 大さじ1", 
            "バルサミコ酢 小さじ2", 
            "塩 少々", 
            "こしょう 少々"
        ],
        "steps": [
            "1. トマトとモッツァレラチーズを1cm厚さの輪切りにする。",
            "2. お皿にトマトとチーズを交互に並べる。",
            "3. バジルの葉を散らす。",
            "4. オリーブオイルとバルサミコ酢をかけ、塩こしょうをふる。"
        ],
        "tags_mood": ["リラックスしたい", "気分転換したい"],
        "tags_condition": ["特に問題なし", "暑さで食欲がない"],
        "comment": "さっぱりとした味わいで、暑い日でも食べやすいです。"
    },
    {
        "id": 6,
        "name": "キノコの炊き込みご飯",
        "ingredients": [
            "米 2合", 
            "しめじ 1パック", 
            "まいたけ 1パック", 
            "油揚げ 1枚", 
            "醤油 大さじ2", 
            "みりん 大さじ1", 
            "酒 大さじ1", 
            "昆布 5cm角"
        ],
        "steps": [
            "1. 米は洗ってザルにあげておく。",
            "2. キノコ類は石づきを取り、ほぐす。油揚げは細切りにする。",
            "3. 炊飯器に米、調味料、水を入れ、その上にキノコと油揚げ、昆布をのせる。",
            "4. 通常モードで炊く。",
            "5. 炊き上がったら昆布を取り出し、全体を混ぜる。"
        ],
        "tags_mood": ["落ち着きたい", "ほっとしたい"],
        "tags_condition": ["疲れている", "胃腸を整えたい"],
        "comment": "食物繊維が豊富で腸内環境を整えます。"
    },
    {
        "id": 7,
        "name": "レモンと蜂蜜のホットドリンク",
        "ingredients": [
            "レモン 1/2個", 
            "はちみつ 大さじ1", 
            "お湯 200ml", 
            "ジンジャーパウダー 少々（あれば）"
        ],
        "steps": [
            "1. レモンを絞る。",
            "2. マグカップにレモン汁とはちみつを入れる。",
            "3. お湯を注ぎ、よくかき混ぜる。",
            "4. お好みでジンジャーパウダーを加える。"
        ],
        "tags_mood": ["リラックスしたい", "落ち着きたい"],
        "tags_condition": ["風邪気味", "喉が痛い", "疲れている"],
        "comment": "ビタミンCが豊富で、免疫力アップに。はちみつの抗菌作用も◎"
    },
    {
        "id": 8,
        "name": "アボカドとサーモンの丼",
        "ingredients": [
            "ご飯 茶碗1杯", 
            "アボカド 1個", 
            "スモークサーモン 50g", 
            "醤油 小さじ1", 
            "わさび 少々", 
            "白ごま 少々"
        ],
        "steps": [
            "1. アボカドは皮と種を取り除き、1cm角に切る。",
            "2. スモークサーモンは食べやすい大きさに切る。",
            "3. 丼にご飯を盛り、アボカドとサーモンをのせる。",
            "4. 醤油とわさびを混ぜたものをかけ、白ごまを散らす。"
        ],
        "tags_mood": ["元気を出したい", "集中したい"],
        "tags_condition": ["特に問題なし", "栄養補給したい"],
        "comment": "良質な脂質と高タンパクで、脳の働きを活性化します。"
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
    """
    現在の月から季節を判定する
    """
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
    """
    オンラインからレシピを検索する
    """
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
        
        # APIリクエストを送信（実際の実装ではコメントを外す）
        # response = requests.get("https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426", params=params)
        # data = response.json()
        
        # デモ用のダミーレスポンス
        # 実際の実装では上記のAPIリクエストを使用
        data = {
            "result": [
                {
                    "recipeId": 1001,
                    "recipeTitle": f"{query}に最適な健康レシピ",
                    "recipeDescription": f"{query}の状態に合わせた栄養バランスの良いレシピです。",
                    "foodImageUrl": "",
                    "recipeMaterial": ["玉ねぎ", "にんじん", "豚肉", "醤油", "みりん", "砂糖"],
                    "recipeIndication": "約30分",
                    "recipeCost": "300円前後"
                },
                {
                    "recipeId": 1002,
                    "recipeTitle": f"簡単！{query}向けの15分クッキング",
                    "recipeDescription": "忙しい日でも手軽に作れる栄養満点レシピ。",
                    "foodImageUrl": "",
                    "recipeMaterial": ["卵", "ほうれん草", "ベーコン", "塩", "こしょう"],
                    "recipeIndication": "約15分",
                    "recipeCost": "200円前後"
                },
                {
                    "recipeId": 1003,
                    "recipeTitle": f"{query}に効果的な薬膳風レシピ",
                    "recipeDescription": "東洋医学の知恵を取り入れた体に優しいレシピです。",
                    "foodImageUrl": "",
                    "recipeMaterial": ["生姜", "鶏肉", "白菜", "しいたけ", "ねぎ", "醤油", "酒"],
                    "recipeIndication": "約40分",
                    "recipeCost": "400円前後"
                }
            ]
        }
        
        # APIレスポンスをレシピ形式に変換
        online_recipes = []
        for item in data["result"]:
            recipe = {
                "id": item["recipeId"],
                "name": item["recipeTitle"],
                "ingredients": item["recipeMaterial"],
                "steps": [f"1. {item['recipeDescription']}",
                          f"2. 調理時間: {item['recipeIndication']}",
                          f"3. 予算: {item['recipeCost']}"],
                "tags_mood": [query],
                "tags_condition": [query],
                "comment": item["recipeDescription"],
                "source": "オンラインレシピ"
            }
            online_recipes.append(recipe)
        
        return online_recipes
    
    except Exception as e:
        print(f"オンラインレシピの検索中にエラーが発生しました: {e}")
        return []

def find_recipes(selected_mood, selected_condition, selected_season=None, include_online=True):
    """
    選択された気分と体調、季節に基づいてレシピを検索する
    オンラインレシピも含める場合はinclude_online=Trueを指定
    """
    matching_recipes = []
    
    # 季節が選択されていない場合は現在の季節を使用
    if not selected_season:
        selected_season = get_current_season()
    
    # ローカルレシピから検索
    for recipe in recipes:
        mood_match = selected_mood in recipe["tags_mood"]
        condition_match = selected_condition in recipe["tags_condition"]
        
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
        self.root.geometry("800x600")
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
        self.style.configure("TButton", font=self.normal_font, background=self.accent_color, foreground="#ffffff")
        self.style.map("TButton",
            background=[("active", self.current_theme["accent"]), ("disabled", "#bdc3c7")],
            foreground=[("active", "#ffffff"), ("disabled", "#95a5a6")]
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
        
        # 選択フレーム
        selection_frame = ttk.Frame(self.scrollable_frame, style="TFrame")
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
        
        # 季節ごとのフレームスタイル
        season_frame_styles = {
            "春": f"春.TLabelframe",
            "夏": f"夏.TLabelframe",
            "秋": f"秋.TLabelframe",
            "冬": f"冬.TLabelframe"
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
            # 気分ごとのフレームに背景色を設定
            mood_frame_item = ttk.Frame(mood_frame)
            mood_frame_item.pack(fill=tk.X, pady=3)
            
            # カスタムフレームの背景色を設定
            mood_bg = tk.Frame(mood_frame_item, bg=self.mood_colors[mood], width=5)
            mood_bg.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
            
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
        condition_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
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
            # 体調ごとのフレームに背景色を設定
            condition_frame_item = ttk.Frame(condition_frame)
            condition_frame_item.pack(fill=tk.X, pady=3)
            
            # カスタムフレームの背景色を設定
            condition_bg = tk.Frame(condition_frame_item, bg=self.condition_colors[condition], width=5)
            condition_bg.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
            
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
        button_frame = ttk.Frame(self.scrollable_frame, style="TFrame")
        button_frame.pack(pady=20)
        
        # 検索ボタン
        # 検索ボタンをカスタマイズ
        search_button_style = f"Search.TButton"
        self.style.configure(search_button_style, font=self.header_font, background=self.current_theme["accent"])
        self.style.map(search_button_style,
            background=[("active", self.highlight_color), ("disabled", "#bdc3c7")],
            foreground=[("active", "#ffffff"), ("disabled", "#95a5a6")]
        )
        
        self.search_button = ttk.Button(
            button_frame,
            text="🔍 おすすめごはんを探す",
            command=self.search_recipes,
            state=tk.DISABLED,
            style=search_button_style,
            width=25
        )
        self.search_button.pack(pady=5)
        
        # レシピ表示フレーム
        self.recipe_frame = ttk.Frame(self.scrollable_frame, style="TFrame")
        self.recipe_frame.pack(fill=tk.BOTH, expand=True)
        
        # レシピヘッダーフレーム
        recipe_header_frame = ttk.Frame(self.recipe_frame, style="TFrame")
        recipe_header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # レシピ名ラベル
        self.recipe_name_label = ttk.Label(
            recipe_header_frame,
            text="",
            font=self.header_font,
            style="Header.TLabel"
        )
        self.recipe_name_label.pack(pady=(0, 5))
        
        # 季節タグ表示ラベル
        self.recipe_season_label = ttk.Label(
            recipe_header_frame,
            text="",
            font=self.normal_font
        )
        self.recipe_season_label.pack(pady=(0, 5))
        
        # レシピコメントフレーム
        # レシピコメントフレームをカスタマイズ
        recipe_comment_frame = tk.Frame(self.recipe_frame, padx=10, pady=10, bg=self.current_theme["bg"], relief="groove", borderwidth=1)
        recipe_comment_frame.pack(fill=tk.X, pady=(0, 10))
        
        # レシピコメントラベル
        self.recipe_comment_label = ttk.Label(
            recipe_comment_frame,
            text="",
            font=self.normal_font,
            wraplength=700,
            style=f"{self.season_var.get()}.TLabel"
        )
        self.recipe_comment_label.pack(pady=5)
        
        # レシピ詳細フレーム
        self.recipe_details_frame = ttk.Frame(self.recipe_frame)
        self.recipe_details_frame.pack(fill=tk.BOTH, expand=True)
        
        # 材料フレーム
        self.ingredients_frame = ttk.LabelFrame(
            self.recipe_details_frame, 
            text="材料", 
            padding=10
        )
        self.ingredients_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 材料リスト
        self.ingredients_text = tk.Text(
            self.ingredients_frame,
            height=10,
            width=30,
            font=self.normal_font,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#ffffff",
            fg=self.text_color,
            relief="flat",
            padx=5,
            pady=5
        )
        self.ingredients_text.pack(fill=tk.BOTH, expand=True)
        
        # 作り方フレーム
        self.steps_frame = ttk.LabelFrame(
            self.recipe_details_frame, 
            text="作り方", 
            padding=10
        )
        self.steps_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # 作り方リスト
        self.steps_text = tk.Text(
            self.steps_frame,
            height=10,
            width=40,
            font=self.normal_font,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#ffffff",
            fg=self.text_color,
            relief="flat",
            padx=5,
            pady=5
        )
        self.steps_text.pack(fill=tk.BOTH, expand=True)
        
        # ナビゲーションフレーム
        self.nav_frame = ttk.Frame(self.scrollable_frame)
        self.nav_frame.pack(fill=tk.X, pady=10)
        
        # 前のレシピボタン
        self.prev_button = ttk.Button(
            self.nav_frame, 
            text="前のレシピ", 
            command=self.show_prev_recipe,
            state=tk.DISABLED
        )
        self.prev_button.pack(side=tk.LEFT)
        
        # レシピカウンターラベル
        self.counter_label = ttk.Label(
            self.nav_frame, 
            text="", 
            font=self.normal_font
        )
        self.counter_label.pack(side=tk.LEFT, padx=20)
        
        # 次のレシピボタン
        self.next_button = ttk.Button(
            self.nav_frame, 
            text="次のレシピ", 
            command=self.show_next_recipe,
            state=tk.DISABLED
        )
        self.next_button.pack(side=tk.LEFT)
        
        # 再検索ボタン
        self.restart_button = ttk.Button(
            self.nav_frame, 
            text="もう一度探す", 
            command=self.restart_search
        )
        self.restart_button.pack(side=tk.RIGHT)
        
        # 初期状態ではレシピ表示部分を隠す
        self.recipe_frame.pack_forget()
        self.nav_frame.pack_forget()
    
    def check_selection(self):
        """選択状態をチェックしてボタンの有効/無効を切り替える"""
        if self.mood_var.get() and self.condition_var.get():
            self.search_button.config(state=tk.NORMAL)
        else:
            self.search_button.config(state=tk.DISABLED)
    
    def search_recipes(self):
        """レシピを検索して表示する"""
        selected_mood = self.mood_var.get()
        selected_condition = self.condition_var.get()
        selected_season = self.season_var.get()
        
        # 選択された季節に基づいてテーマカラーを更新
        self.current_theme = self.season_colors[selected_season]
        
        # 季節に基づいてUIの色を更新
        self.update_ui_colors(selected_season)
        
        # 検索中の表示
        self.search_button.config(state=tk.DISABLED, text="🔍 検索中...")
        self.root.update()
        
        # 別スレッドでオンライン検索を実行
        def search_thread():
            # ローカルレシピを検索
            local_recipes = find_recipes(selected_mood, selected_condition, selected_season, include_online=False)
            
            # 結果を表示（ローカルのみ）
            self.matching_recipes = local_recipes
            self.current_recipe_index = 0
            
            # UIを更新
            self.root.after(0, self.update_ui_after_search)
            
            # オンラインレシピを検索
            try:
                # 検索クエリを作成
                query = f"{selected_mood} {selected_condition} {selected_season}"
                online_recipes = search_online_recipes(query)
                
                # 結果を更新（ローカル + オンライン）
                if online_recipes:
                    self.matching_recipes = local_recipes + online_recipes
                    
                    # UIを更新
                    self.root.after(0, self.update_ui_after_search)
            except Exception as e:
                print(f"オンラインレシピの検索中にエラーが発生しました: {e}")
        
        # 検索スレッドを開始
        threading.Thread(target=search_thread, daemon=True).start()
    
    def update_ui_after_search(self):
        """検索完了後にUIを更新する"""
        # 検索ボタンを元に戻す
        self.search_button.config(state=tk.NORMAL, text="🔍 おすすめごはんを探す")
        
        if not self.matching_recipes:
            messagebox.showinfo("検索結果", "条件に合うレシピが見つかりませんでした。")
            return
        
        # レシピ表示部分を表示
        self.recipe_frame.pack(fill=tk.BOTH, expand=True)
        self.nav_frame.pack(fill=tk.X, pady=10)
        
        # レシピを表示
        self.display_current_recipe()
        
        # ナビゲーションボタンの状態を更新
        self.update_navigation_buttons()
    
    def update_ui_colors(self, season):
        """季節に基づいてUIの色を更新する"""
        # レシピコメントフレームの背景色を更新
        for widget in self.recipe_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children() and isinstance(widget.winfo_children()[0], ttk.Label):
                widget.configure(bg=self.season_colors[season]["bg"])
        
        # レシピコメントラベルのスタイルを更新
        self.recipe_comment_label.configure(style=f"{season}.TLabel")
        
        # ボタンのスタイルを更新
        self.style.map("TButton",
            background=[("active", self.season_colors[season]["accent"]), ("disabled", "#bdc3c7")],
            foreground=[("active", "#ffffff"), ("disabled", "#95a5a6")]
        )
    
    def display_current_recipe(self):
        """現在のレシピを表示する"""
        if not self.matching_recipes:
            return
        
        recipe = self.matching_recipes[self.current_recipe_index]
        selected_season = self.season_var.get()
        
        # レシピ名
        self.recipe_name_label.config(text=f"--- レシピ: {recipe['name']} ---")
        
        # 季節タグがあれば表示
        if "tags_season" in recipe:
            season_icons = {
                "春": "🌸",
                "夏": "☀️",
                "秋": "🍁",
                "冬": "❄️"
            }
            seasons_text = ", ".join([f"{season_icons.get(s, '')} {s}" for s in recipe["tags_season"]])
            self.recipe_season_label.config(text=f"季節: {seasons_text}")
        else:
            self.recipe_season_label.config(text="")
        
        # レシピコメント
        self.recipe_comment_label.config(
            text=f"[ポイント: {recipe['comment']}]",
            style=f"{selected_season}.TLabel"
        )
        
        # 材料リスト
        self.ingredients_text.config(state=tk.NORMAL)
        self.ingredients_text.delete(1.0, tk.END)
        for ingredient in recipe["ingredients"]:
            self.ingredients_text.insert(tk.END, f"- {ingredient}\n", "ingredient")
        
        # テキストタグを設定
        self.ingredients_text.tag_configure("ingredient", foreground=self.current_theme["text"])
        self.ingredients_text.config(state=tk.DISABLED)
        
        # 作り方リスト
        self.steps_text.config(state=tk.NORMAL)
        self.steps_text.delete(1.0, tk.END)
        for i, step in enumerate(recipe["steps"]):
            # ステップ番号の部分を強調表示
            if step.startswith(f"{i+1}."):
                prefix, rest = step.split(".", 1)
                self.steps_text.insert(tk.END, f"{prefix}.", "step_number")
                self.steps_text.insert(tk.END, f"{rest}\n", "step_text")
            else:
                self.steps_text.insert(tk.END, f"{step}\n", "step_text")
        
        # テキストタグを設定
        self.steps_text.tag_configure("step_number", foreground=self.current_theme["accent"], font=font.Font(family="Yu Gothic", size=10, weight="bold"))
        self.steps_text.tag_configure("step_text", foreground=self.text_color)
        self.steps_text.config(state=tk.DISABLED)
        
        # カウンターラベル
        self.counter_label.config(
            text=f"{self.current_recipe_index + 1} / {len(self.matching_recipes)}"
        )
    
    def show_prev_recipe(self):
        """前のレシピを表示する"""
        if self.current_recipe_index > 0:
            self.current_recipe_index -= 1
            self.display_current_recipe()
            self.update_navigation_buttons()
    
    def show_next_recipe(self):
        """次のレシピを表示する"""
        if self.current_recipe_index < len(self.matching_recipes) - 1:
            self.current_recipe_index += 1
            self.display_current_recipe()
            self.update_navigation_buttons()
    
    def update_navigation_buttons(self):
        """ナビゲーションボタンの状態を更新する"""
        # 前のレシピボタン
        if self.current_recipe_index > 0:
            self.prev_button.config(state=tk.NORMAL)
        else:
            self.prev_button.config(state=tk.DISABLED)
        
        # 次のレシピボタン
        if self.current_recipe_index < len(self.matching_recipes) - 1:
            self.next_button.config(state=tk.NORMAL)
        else:
            self.next_button.config(state=tk.DISABLED)
    
    def restart_search(self):
        """検索をリセットする"""
        # 選択をクリア
        self.mood_var.set("")
        self.condition_var.set("")
        
        # ボタンを無効化
        self.search_button.config(state=tk.DISABLED)
        
        # レシピ表示部分を隠す
        self.recipe_frame.pack_forget()
        self.nav_frame.pack_forget()
        
        # レシピリストをクリア
        self.matching_recipes = []
        self.current_recipe_index = 0
    
    def on_frame_configure(self, event):
        """スクロール可能な領域のサイズを設定"""
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """キャンバスのサイズ変更時にフレームの幅を調整"""
        self.main_canvas.itemconfig(self.scrollable_frame_window, width=event.width)
    
    def on_mousewheel(self, event):
        """マウスホイールでスクロール"""
        # Windows
        if sys.platform.startswith('win'):
            self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # macOS
        elif sys.platform == 'darwin':
            self.main_canvas.yview_scroll(int(-1 * event.delta), "units")
        # Linux
        else:
            if event.num == 4:
                self.main_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.main_canvas.yview_scroll(1, "units")

def main():
    root = tk.Tk()
    app = MealRecommenderApp(root)
    
    # スクロール領域の設定
    app.scrollable_frame.bind("<Configure>", app.on_frame_configure)
    app.main_canvas.bind("<Configure>", app.on_canvas_configure)
    
    # マウスホイールでスクロール
    # Windows
    app.root.bind_all("<MouseWheel>", app.on_mousewheel)
    # Linux
    app.root.bind_all("<Button-4>", app.on_mousewheel)
    app.root.bind_all("<Button-5>", app.on_mousewheel)
    # macOS
    app.root.bind_all("<MouseWheel>", app.on_mousewheel)
    
    root.mainloop()

if __name__ == "__main__":
    main()