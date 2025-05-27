# -*- coding: utf-8 -*-
import sys
import random
import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os

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

def find_recipes(selected_mood, selected_condition):
    """
    選択された気分と体調に基づいてレシピを検索する
    """
    matching_recipes = []
    
    for recipe in recipes:
        mood_match = selected_mood in recipe["tags_mood"]
        condition_match = selected_condition in recipe["tags_condition"]
        
        # 気分と体調の両方に一致するレシピを優先
        if mood_match and condition_match:
            matching_recipes.append((recipe, 2))  # スコア2（最高）
        # 気分だけ一致
        elif mood_match:
            matching_recipes.append((recipe, 1))  # スコア1
        # 体調だけ一致
        elif condition_match:
            matching_recipes.append((recipe, 1))  # スコア1
    
    # マッチするレシピがない場合はランダムに1つ選ぶ
    if not matching_recipes:
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
        self.current_recipe_index = 0
        self.matching_recipes = []
        
        # メインフレーム
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # タイトル
        title_label = ttk.Label(
            self.main_frame, 
            text="今日の最適ごはん提案アプリ\n（こころとからだのごはんサポーター）", 
            font=self.title_font
        )
        title_label.pack(pady=(0, 10))
        
        # レシピ数表示
        self.recipe_count_label = ttk.Label(
            self.main_frame,
            text=f"現在のレシピ数: {len(recipes)}種類",
            font=self.normal_font
        )
        self.recipe_count_label.pack(pady=(0, 10))
        
        # 選択フレーム
        selection_frame = ttk.Frame(self.main_frame)
        selection_frame.pack(fill=tk.X, pady=10)
        
        # 気分選択
        mood_frame = ttk.LabelFrame(selection_frame, text="今日の気分", padding=10)
        mood_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        for mood in moods:
            rb = ttk.Radiobutton(
                mood_frame, 
                text=mood, 
                value=mood, 
                variable=self.mood_var,
                command=self.check_selection
            )
            rb.pack(anchor=tk.W, pady=2)
        
        # 体調選択
        condition_frame = ttk.LabelFrame(selection_frame, text="今日の体調", padding=10)
        condition_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        for condition in conditions:
            rb = ttk.Radiobutton(
                condition_frame, 
                text=condition, 
                value=condition, 
                variable=self.condition_var,
                command=self.check_selection
            )
            rb.pack(anchor=tk.W, pady=2)
        
        # 検索ボタン
        self.search_button = ttk.Button(
            self.main_frame, 
            text="おすすめごはんを探す", 
            command=self.search_recipes,
            state=tk.DISABLED
        )
        self.search_button.pack(pady=20)
        
        # レシピ表示フレーム
        self.recipe_frame = ttk.Frame(self.main_frame)
        self.recipe_frame.pack(fill=tk.BOTH, expand=True)
        
        # レシピ名ラベル
        self.recipe_name_label = ttk.Label(
            self.recipe_frame, 
            text="", 
            font=self.header_font
        )
        self.recipe_name_label.pack(pady=(0, 5))
        
        # レシピコメントラベル
        self.recipe_comment_label = ttk.Label(
            self.recipe_frame, 
            text="", 
            font=self.normal_font,
            wraplength=700
        )
        self.recipe_comment_label.pack(pady=(0, 10))
        
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
            state=tk.DISABLED
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
            state=tk.DISABLED
        )
        self.steps_text.pack(fill=tk.BOTH, expand=True)
        
        # ナビゲーションフレーム
        self.nav_frame = ttk.Frame(self.main_frame)
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
        
        self.matching_recipes = find_recipes(selected_mood, selected_condition)
        self.current_recipe_index = 0
        
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
    
    def display_current_recipe(self):
        """現在のレシピを表示する"""
        if not self.matching_recipes:
            return
        
        recipe = self.matching_recipes[self.current_recipe_index]
        
        # レシピ名
        self.recipe_name_label.config(text=f"--- レシピ: {recipe['name']} ---")
        
        # レシピコメント
        self.recipe_comment_label.config(text=f"[ポイント: {recipe['comment']}]")
        
        # 材料リスト
        self.ingredients_text.config(state=tk.NORMAL)
        self.ingredients_text.delete(1.0, tk.END)
        for ingredient in recipe["ingredients"]:
            self.ingredients_text.insert(tk.END, f"- {ingredient}\n")
        self.ingredients_text.config(state=tk.DISABLED)
        
        # 作り方リスト
        self.steps_text.config(state=tk.NORMAL)
        self.steps_text.delete(1.0, tk.END)
        for step in recipe["steps"]:
            self.steps_text.insert(tk.END, f"{step}\n")
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

def main():
    root = tk.Tk()
    app = MealRecommenderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()