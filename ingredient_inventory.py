# -*- coding: utf-8 -*-
import json
import os
import datetime

class IngredientInventory:
    """食材在庫を管理するクラス"""
    
    def __init__(self, file_path='ingredient_inventory.json'):
        """初期化"""
        self.file_path = file_path
        self.inventory = {}  # 食材在庫 {食材名: {quantity: 数量, unit: 単位, expiry_date: 賞味期限}}
        self.shopping_list = []  # 買い物リスト
        self.load_inventory()
    
    def load_inventory(self):
        """在庫データをファイルから読み込む"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.inventory = data.get('inventory', {})
                    self.shopping_list = data.get('shopping_list', [])
        except Exception as e:
            print(f"在庫データの読み込み中にエラーが発生しました: {e}")
    
    def save_inventory(self):
        """在庫データをファイルに保存する"""
        try:
            data = {
                'inventory': self.inventory,
                'shopping_list': self.shopping_list
            }
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"在庫データの保存中にエラーが発生しました: {e}")
            return False
    
    def add_ingredient(self, name, quantity=None, unit=None, expiry_date=None):
        """食材を在庫に追加する"""
        if not name:
            return False
        
        # 食材名を正規化（小文字に変換）
        name = name.strip()
        
        # 既存の食材の場合は数量を更新
        if name in self.inventory:
            if quantity is not None:
                current_quantity = self.inventory[name].get('quantity', 0)
                self.inventory[name]['quantity'] = current_quantity + quantity
            if unit is not None:
                self.inventory[name]['unit'] = unit
            if expiry_date is not None:
                self.inventory[name]['expiry_date'] = expiry_date
        else:
            # 新しい食材を追加
            self.inventory[name] = {
                'quantity': quantity,
                'unit': unit,
                'expiry_date': expiry_date
            }
        
        return self.save_inventory()
    
    def remove_ingredient(self, name, quantity=None):
        """食材を在庫から削除する"""
        if name not in self.inventory:
            return False
        
        # 数量が指定されている場合は減算
        if quantity is not None:
            current_quantity = self.inventory[name].get('quantity', 0)
            if current_quantity <= quantity:
                # 数量が0以下になる場合は食材を完全に削除
                del self.inventory[name]
            else:
                self.inventory[name]['quantity'] = current_quantity - quantity
        else:
            # 数量が指定されていない場合は食材を完全に削除
            del self.inventory[name]
        
        return self.save_inventory()
    
    def get_inventory(self):
        """在庫リストを取得する"""
        return self.inventory
    
    def get_expiring_soon(self, days=3):
        """賞味期限が近い食材を取得する"""
        expiring_soon = {}
        today = datetime.datetime.now().date()
        
        for name, data in self.inventory.items():
            expiry_date_str = data.get('expiry_date')
            if expiry_date_str:
                try:
                    expiry_date = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
                    days_left = (expiry_date - today).days
                    if 0 <= days_left <= days:
                        expiring_soon[name] = {
                            'days_left': days_left,
                            'quantity': data.get('quantity'),
                            'unit': data.get('unit')
                        }
                except ValueError:
                    # 日付形式が不正な場合はスキップ
                    continue
        
        return expiring_soon
    
    def add_to_shopping_list(self, item):
        """買い物リストに項目を追加する"""
        if item and item not in self.shopping_list:
            self.shopping_list.append(item)
            return self.save_inventory()
        return False
    
    def remove_from_shopping_list(self, item):
        """買い物リストから項目を削除する"""
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            return self.save_inventory()
        return False
    
    def get_shopping_list(self):
        """買い物リストを取得する"""
        return self.shopping_list
    
    def clear_shopping_list(self):
        """買い物リストをクリアする"""
        self.shopping_list = []
        return self.save_inventory()
    
    def generate_shopping_list_from_recipe(self, recipe):
        """レシピから買い物リストを生成する"""
        if not recipe or "ingredients" not in recipe:
            return False
        
        for ingredient_str in recipe["ingredients"]:
            # 材料文字列から食材名を抽出（単純化のため、最初の数字や単位を除去）
            parts = ingredient_str.split()
            if len(parts) >= 2:
                # 数量や単位を除いた部分を食材名とする
                ingredient_name = ' '.join(parts[1:])
                
                # 在庫にない場合のみ買い物リストに追加
                if ingredient_name not in self.inventory:
                    self.add_to_shopping_list(ingredient_str)
        
        return True
        
    def generate_shopping_list_from_recipes(self, recipes):
        """複数のレシピから買い物リストを生成する（数量を合算し、重複を排除）"""
        if not recipes:
            return False
            
        # 食材ごとの数量を集計するための辞書
        ingredients_dict = {}
        
        for recipe in recipes:
            if not recipe or "ingredients" not in recipe:
                continue
                
            for ingredient_str in recipe["ingredients"]:
                # 材料文字列を解析して食材名と数量、単位を抽出
                try:
                    # 例: "豚ロース薄切り 200g" -> 食材名="豚ロース薄切り", 数量=200, 単位="g"
                    parts = ingredient_str.split()
                    if len(parts) >= 2:
                        # 数値部分を抽出
                        quantity = None
                        unit = ""
                        ingredient_name = ""
                        
                        # 数値と単位を抽出
                        for i, part in enumerate(parts):
                            # 数字を含む部分を見つける
                            if any(c.isdigit() for c in part):
                                # 数字部分と単位部分を分離
                                num_part = ''.join(filter(lambda c: c.isdigit() or c == '.', part))
                                if num_part:
                                    try:
                                        quantity = float(num_part)
                                        # 単位部分を抽出
                                        unit_part = ''.join(filter(lambda c: not c.isdigit() and c != '.', part))
                                        if unit_part:
                                            unit = unit_part
                                        # 食材名は残りの部分
                                        ingredient_name = ' '.join(parts[i+1:])
                                        break
                                    except ValueError:
                                        pass
                        
                        # 数値が見つからない場合は、最初の部分を食材名とする
                        if not ingredient_name:
                            ingredient_name = ' '.join(parts)
                        
                        # 食材名をキーとして辞書に追加または更新
                        if ingredient_name in ingredients_dict:
                            # 同じ単位の場合は数量を加算
                            if unit == ingredients_dict[ingredient_name]['unit']:
                                if quantity is not None and ingredients_dict[ingredient_name]['quantity'] is not None:
                                    ingredients_dict[ingredient_name]['quantity'] += quantity
                            else:
                                # 単位が異なる場合は別の項目として追加
                                new_key = f"{ingredient_name} ({unit})"
                                ingredients_dict[new_key] = {'quantity': quantity, 'unit': unit}
                        else:
                            ingredients_dict[ingredient_name] = {'quantity': quantity, 'unit': unit}
                except Exception as e:
                    print(f"食材の解析中にエラーが発生しました: {e}")
                    continue
        
        # 買い物リストをクリア
        self.clear_shopping_list()
        
        # 集計した食材を買い物リストに追加
        for name, data in ingredients_dict.items():
            quantity = data['quantity']
            unit = data['unit']
            
            # 在庫にある場合はスキップ
            if name in self.inventory:
                continue
                
            # 買い物リストに追加
            if quantity is not None:
                item = f"{name} {quantity}{unit}"
            else:
                item = name
                
            self.add_to_shopping_list(item)
        
        return True
    
    def find_recipes_with_available_ingredients(self, recipes, threshold=0.7):
        """在庫にある食材を使ったレシピを見つける"""
        if not recipes:
            return []
        
        matching_recipes = []
        inventory_keys = set(self.inventory.keys())
        
        for recipe in recipes:
            if "ingredients" not in recipe:
                continue
            
            # レシピの材料から食材名を抽出
            recipe_ingredients = []
            for ingredient_str in recipe["ingredients"]:
                parts = ingredient_str.split()
                if len(parts) >= 2:
                    ingredient_name = ' '.join(parts[1:])
                    recipe_ingredients.append(ingredient_name)
            
            if not recipe_ingredients:
                continue
            
            # 在庫にある食材の割合を計算
            recipe_ingredients_set = set(recipe_ingredients)
            common_ingredients = inventory_keys.intersection(recipe_ingredients_set)
            match_ratio = len(common_ingredients) / len(recipe_ingredients_set)
            
            # しきい値以上の一致率があるレシピを追加
            if match_ratio >= threshold:
                recipe_copy = recipe.copy()
                recipe_copy["match_ratio"] = match_ratio
                recipe_copy["available_ingredients"] = list(common_ingredients)
                recipe_copy["missing_ingredients"] = list(recipe_ingredients_set - inventory_keys)
                matching_recipes.append(recipe_copy)
        
        # 一致率でソート（降順）
        matching_recipes.sort(key=lambda x: x["match_ratio"], reverse=True)
        return matching_recipes

if __name__ == "__main__":
    # テスト用コード
    inventory = IngredientInventory()
    
    # 食材を追加
    inventory.add_ingredient("豚肉", 300, "g", "2025-06-15")
    inventory.add_ingredient("玉ねぎ", 2, "個", "2025-06-12")
    inventory.add_ingredient("にんじん", 3, "本", "2025-06-14")
    
    # 在庫を表示
    print("食材在庫:")
    for name, data in inventory.get_inventory().items():
        print(f"{name}: {data.get('quantity')}{data.get('unit')} (賞味期限: {data.get('expiry_date')})")
    
    # 賞味期限が近い食材を表示
    print("\n賞味期限が近い食材:")
    for name, data in inventory.get_expiring_soon().items():
        print(f"{name}: あと{data['days_left']}日 ({data['quantity']}{data['unit']})")