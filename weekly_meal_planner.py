# -*- coding: utf-8 -*-
import json
import random
from collections import defaultdict

def load_recipes(file_path='recipes_enhanced.json'):
    """
    JSONファイルからレシピデータを読み込む
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"レシピファイルの読み込みエラー: {e}")
        return []

def save_meal_plan(meal_plan, file_path='meal_plan.json'):
    """
    生成された献立プランをJSONファイルに保存する
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(meal_plan, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"献立プランの保存エラー: {e}")
        return False

def generate_weekly_meal_plan(mood=None, condition=None, season=None, balanced_nutrition=True):
    """
    1週間の献立プランを生成する
    
    Parameters:
    - mood: 気分タグ（例: "元気を出したい"）
    - condition: 体調タグ（例: "胃腸の調子が悪い"）
    - season: 季節タグ（例: "夏"）
    - balanced_nutrition: 栄養バランスを考慮するかどうか
    
    Returns:
    - 1週間の献立プラン（朝食、昼食、夕食）
    """
    recipes = load_recipes()
    if not recipes:
        return None
    
    # 条件に合うレシピをフィルタリング
    filtered_recipes = recipes
    if mood:
        filtered_recipes = [r for r in filtered_recipes if mood in r.get("tags_mood", [])]
    if condition:
        filtered_recipes = [r for r in filtered_recipes if condition in r.get("tags_condition", [])]
    if season:
        filtered_recipes = [r for r in filtered_recipes if season in r.get("tags_season", [])]
    
    # フィルタリングの結果、レシピが少なすぎる場合は全レシピから選択
    if len(filtered_recipes) < 10:
        filtered_recipes = recipes
    
    # 栄養バランスを考慮する場合
    if balanced_nutrition:
        # 栄養素ごとにレシピを分類
        protein_rich = []
        vitamin_rich = []
        balanced = []
        
        for recipe in filtered_recipes:
            nutrition = recipe.get("nutrition", {})
            if nutrition:
                if nutrition.get("protein", 0) > 20:
                    protein_rich.append(recipe)
                if len(nutrition.get("vitamins", [])) >= 2:
                    vitamin_rich.append(recipe)
                if 15 <= nutrition.get("protein", 0) <= 30 and 10 <= nutrition.get("fat", 0) <= 25:
                    balanced.append(recipe)
    
    # 1週間の献立プラン
    days = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
    meal_plan = {}
    
    # 使用済みレシピIDを追跡
    used_recipe_ids = set()
    
    for day in days:
        # 各日の献立
        daily_meals = {
            "朝食": None,
            "昼食": None,
            "夕食": None
        }
        
        # 朝食（軽めの食事）
        breakfast_candidates = [r for r in filtered_recipes if r["id"] not in used_recipe_ids and 
                               (r.get("nutrition", {}).get("calories", 500) < 300)]
        if not breakfast_candidates:
            breakfast_candidates = [r for r in filtered_recipes if r["id"] not in used_recipe_ids]
        if breakfast_candidates:
            breakfast = random.choice(breakfast_candidates)
            daily_meals["朝食"] = breakfast
            used_recipe_ids.add(breakfast["id"])
        
        # 昼食（バランスの良い食事）
        if balanced and any(r["id"] not in used_recipe_ids for r in balanced):
            lunch_candidates = [r for r in balanced if r["id"] not in used_recipe_ids]
            lunch = random.choice(lunch_candidates)
        else:
            lunch_candidates = [r for r in filtered_recipes if r["id"] not in used_recipe_ids]
            if lunch_candidates:
                lunch = random.choice(lunch_candidates)
                used_recipe_ids.add(lunch["id"])
                daily_meals["昼食"] = lunch
        
        # 夕食（タンパク質豊富な食事）
        if protein_rich and any(r["id"] not in used_recipe_ids for r in protein_rich):
            dinner_candidates = [r for r in protein_rich if r["id"] not in used_recipe_ids]
            dinner = random.choice(dinner_candidates)
        else:
            dinner_candidates = [r for r in filtered_recipes if r["id"] not in used_recipe_ids]
            if dinner_candidates:
                dinner = random.choice(dinner_candidates)
                used_recipe_ids.add(dinner["id"])
                daily_meals["夕食"] = dinner
        
        meal_plan[day] = daily_meals
    
    return meal_plan

def get_nutrition_summary(meal_plan):
    """
    献立プランの栄養素サマリーを計算する
    """
    if not meal_plan:
        return None
    
    daily_nutrition = {}
    
    for day, meals in meal_plan.items():
        total_calories = 0
        total_protein = 0
        total_fat = 0
        total_carbs = 0
        vitamins = set()
        minerals = set()
        
        for meal_type, recipe in meals.items():
            if recipe and "nutrition" in recipe:
                nutrition = recipe["nutrition"]
                total_calories += nutrition.get("calories", 0)
                total_protein += nutrition.get("protein", 0)
                total_fat += nutrition.get("fat", 0)
                total_carbs += nutrition.get("carbs", 0)
                vitamins.update(nutrition.get("vitamins", []))
                minerals.update(nutrition.get("minerals", []))
        
        daily_nutrition[day] = {
            "calories": total_calories,
            "protein": total_protein,
            "fat": total_fat,
            "carbs": total_carbs,
            "vitamins": list(vitamins),
            "minerals": list(minerals)
        }
    
    return daily_nutrition

if __name__ == "__main__":
    # テスト用コード
    condition = "胃腸の調子が悪い"
    print(f"{condition}の場合の1週間の献立プラン:")
    meal_plan = generate_weekly_meal_plan(condition=condition)
    
    if meal_plan:
        for day, meals in meal_plan.items():
            print(f"\n{day}:")
            for meal_type, recipe in meals.items():
                if recipe:
                    print(f"  {meal_type}: {recipe['name']}")
                else:
                    print(f"  {meal_type}: レシピなし")
        
        # 栄養素サマリー
        nutrition_summary = get_nutrition_summary(meal_plan)
        if nutrition_summary:
            print("\n栄養素サマリー:")
            for day, nutrition in nutrition_summary.items():
                print(f"\n{day}:")
                print(f"  カロリー: {nutrition['calories']}kcal")
                print(f"  タンパク質: {nutrition['protein']}g")
                print(f"  脂質: {nutrition['fat']}g")
                print(f"  炭水化物: {nutrition['carbs']}g")
    else:
        print("献立プランの生成に失敗しました。")