# -*- coding: utf-8 -*-
import sys
import random
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

def display_recipe(recipe):
    """
    レシピを表示する
    """
    print("\n" + "=" * 50)
    print(f"--- レシピ: {recipe['name']} ---")
    print(f"[ポイント: {recipe['comment']}]")
    
    print("\n[材料]")
    for ingredient in recipe["ingredients"]:
        print(f"- {ingredient}")
    
    print("\n[作り方]")
    for step in recipe["steps"]:
        print(step)
    
    print("=" * 50)

def main():
    """
    メインプログラム
    """
    print("ようこそ！今日の最適ごはん提案アプリへ")
    print("（こころとからだのごはんサポーター）")
    print(f"現在のレシピ数: {len(recipes)}種類")
    
    while True:
        # 気分の選択
        print("\n今日の気分を選んでください:")
        for i, mood in enumerate(moods, 1):
            print(f"{i}: {mood}")
        
        try:
            mood_choice = int(input("選択 (番号): "))
            if mood_choice < 1 or mood_choice > len(moods):
                print("無効な選択です。もう一度お試しください。")
                continue
            selected_mood = moods[mood_choice - 1]
        except ValueError:
            print("数字を入力してください。")
            continue
        
        # 体調の選択
        print("\n今日の体調を選んでください:")
        for i, condition in enumerate(conditions, 1):
            print(f"{i}: {condition}")
        
        try:
            condition_choice = int(input("選択 (番号): "))
            if condition_choice < 1 or condition_choice > len(conditions):
                print("無効な選択です。もう一度お試しください。")
                continue
            selected_condition = conditions[condition_choice - 1]
        except ValueError:
            print("数字を入力してください。")
            continue
        
        # レシピ検索
        matching_recipes = find_recipes(selected_mood, selected_condition)
        
        if not matching_recipes:
            print("\n申し訳ありません。条件に合うレシピが見つかりませんでした。")
        else:
            print("\nあなたへのおすすめごはんはこちらです！")
            
            # 最初のレシピを表示
            display_recipe(matching_recipes[0])
            
            # 他のレシピがある場合は選択肢を提供
            if len(matching_recipes) > 1:
                print(f"\n他に {len(matching_recipes) - 1} 件のおすすめレシピがあります。")
                see_more = input("他のレシピも見ますか？ (y/n): ")
                
                if see_more.lower() == 'y':
                    for i, recipe in enumerate(matching_recipes[1:], 1):
                        print(f"\n--- 別のおすすめ {i} ---")
                        display_recipe(recipe)
                        
                        if i < len(matching_recipes) - 1:
                            continue_viewing = input("次のレシピを見ますか？ (y/n): ")
                            if continue_viewing.lower() != 'y':
                                break
        
        # 再検索するか終了するか
        retry = input("\nもう一度探しますか？ (y/n): ")
        if retry.lower() != 'y':
            print("アプリを終了します。良い食事時間をお過ごしください！")
            break

if __name__ == "__main__":
    main()