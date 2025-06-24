# -*- coding: utf-8 -*-
import json
import os

class UserPreferences:
    """ユーザー設定を管理するクラス"""
    
    def __init__(self, file_path='user_preferences.json'):
        """初期化"""
        self.file_path = file_path
        self.allergies = []  # アレルギー食材リスト
        self.dislikes = []   # 嫌いな食材リスト
        self.load_preferences()
    
    def load_preferences(self):
        """設定ファイルから設定を読み込む"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.allergies = data.get('allergies', [])
                    self.dislikes = data.get('dislikes', [])
        except Exception as e:
            print(f"設定ファイルの読み込み中にエラーが発生しました: {e}")
    
    def save_preferences(self):
        """設定をファイルに保存する"""
        try:
            data = {
                'allergies': self.allergies,
                'dislikes': self.dislikes
            }
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"設定ファイルの保存中にエラーが発生しました: {e}")
            return False
    
    def add_allergy(self, item):
        """アレルギー食材を追加"""
        if item and item not in self.allergies:
            self.allergies.append(item)
            return True
        return False
    
    def remove_allergy(self, item):
        """アレルギー食材を削除"""
        if item in self.allergies:
            self.allergies.remove(item)
            return True
        return False
    
    def add_dislike(self, item):
        """嫌いな食材を追加"""
        if item and item not in self.dislikes:
            self.dislikes.append(item)
            return True
        return False
    
    def remove_dislike(self, item):
        """嫌いな食材を削除"""
        if item in self.dislikes:
            self.dislikes.remove(item)
            return True
        return False
    
    def check_recipe_compatibility(self, recipe):
        """レシピがアレルギーや嫌いな食材を含んでいるかチェック"""
        if not recipe or "ingredients" not in recipe:
            return True, []
        
        incompatible_items = []
        
        # 材料リストを文字列に変換して検索しやすくする
        ingredients_text = " ".join(recipe["ingredients"]).lower()
        
        # アレルギー食材をチェック
        for allergy in self.allergies:
            if allergy.lower() in ingredients_text:
                incompatible_items.append({"item": allergy, "type": "アレルギー"})
        
        # 嫌いな食材をチェック
        for dislike in self.dislikes:
            if dislike.lower() in ingredients_text:
                incompatible_items.append({"item": dislike, "type": "嫌いな食材"})
        
        # 互換性があるかどうかと、問題のある食材リストを返す
        return len(incompatible_items) == 0, incompatible_items