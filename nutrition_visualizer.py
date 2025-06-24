# -*- coding: utf-8 -*-
import json
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")  # Tkinterと互換性のあるバックエンドを使用
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class NutritionVisualizer:
    """
    レシピの栄養情報を可視化するクラス
    """
    def __init__(self, master=None, recipe=None):
        self.master = master
        self.recipe = recipe
        self.frame = None
        
    def create_visualization(self, frame):
        """
        栄養情報の可視化を作成する
        """
        self.frame = frame
        
        if not self.recipe or "nutrition" not in self.recipe:
            label = ttk.Label(frame, text="このレシピには栄養情報がありません。")
            label.pack(pady=10)
            return
        
        nutrition = self.recipe["nutrition"]
        
        # 栄養素の基本情報を表示
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        # カロリー情報
        calories_label = ttk.Label(info_frame, text=f"カロリー: {nutrition.get('calories', 0)} kcal", font=("Yu Gothic", 10, "bold"))
        calories_label.pack(side=tk.LEFT, padx=10)
        
        # PFCバランスのグラフを作成
        self.create_pfc_chart(frame, nutrition)
        
        # ビタミン・ミネラル情報
        self.create_vitamin_mineral_info(frame, nutrition)
    
    def create_pfc_chart(self, parent_frame, nutrition):
        """
        PFC（タンパク質、脂質、炭水化物）バランスの円グラフを作成
        """
        # グラフ用のフレーム
        chart_frame = ttk.Frame(parent_frame)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # PFCの値を取得
        protein = nutrition.get("protein", 0)
        fat = nutrition.get("fat", 0)
        carbs = nutrition.get("carbs", 0)
        
        # 合計を計算
        total = protein + fat + carbs
        if total == 0:  # ゼロ除算を防ぐ
            total = 1
        
        # パーセンテージを計算
        protein_pct = round(protein / total * 100)
        fat_pct = round(fat / total * 100)
        carbs_pct = round(carbs / total * 100)
        
        # グラフを作成
        fig, ax = plt.subplots(figsize=(4, 3))
        labels = ['タンパク質', '脂質', '炭水化物']
        sizes = [protein, fat, carbs]
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        explode = (0.1, 0, 0)  # タンパク質を少し強調
        
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax.axis('equal')  # 円グラフを円形に
        plt.title('PFCバランス')
        
        # グラフをTkinterウィンドウに埋め込む
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 数値情報も表示
        pfc_info_frame = ttk.Frame(parent_frame)
        pfc_info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(pfc_info_frame, text=f"タンパク質: {protein}g ({protein_pct}%)", foreground="#ff9999").pack(side=tk.LEFT, padx=10)
        ttk.Label(pfc_info_frame, text=f"脂質: {fat}g ({fat_pct}%)", foreground="#66b3ff").pack(side=tk.LEFT, padx=10)
        ttk.Label(pfc_info_frame, text=f"炭水化物: {carbs}g ({carbs_pct}%)", foreground="#99ff99").pack(side=tk.LEFT, padx=10)
    
    def create_vitamin_mineral_info(self, parent_frame, nutrition):
        """
        ビタミンとミネラルの情報を表示
        """
        # フレーム作成
        vm_frame = ttk.LabelFrame(parent_frame, text="ビタミン・ミネラル")
        vm_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # ビタミン情報
        vitamins = nutrition.get("vitamins", [])
        if vitamins:
            vitamin_label = ttk.Label(vm_frame, text="ビタミン: " + ", ".join(vitamins))
            vitamin_label.pack(anchor=tk.W, padx=10, pady=5)
        else:
            vitamin_label = ttk.Label(vm_frame, text="ビタミン情報なし")
            vitamin_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # ミネラル情報
        minerals = nutrition.get("minerals", [])
        if minerals:
            mineral_label = ttk.Label(vm_frame, text="ミネラル: " + ", ".join(minerals))
            mineral_label.pack(anchor=tk.W, padx=10, pady=5)
        else:
            mineral_label = ttk.Label(vm_frame, text="ミネラル情報なし")
            mineral_label.pack(anchor=tk.W, padx=10, pady=5)

def create_weekly_nutrition_chart(meal_plan):
    """
    週間献立の栄養バランスチャートを作成する
    
    Parameters:
    - meal_plan: 週間献立プラン
    
    Returns:
    - matplotlib Figureオブジェクト
    """
    if not meal_plan:
        return None
    
    # 日ごとの栄養素データを収集
    days = []
    calories = []
    proteins = []
    fats = []
    carbs = []
    
    for day, meals in meal_plan.items():
        days.append(day)
        daily_calories = 0
        daily_protein = 0
        daily_fat = 0
        daily_carbs = 0
        
        for meal_type, recipe in meals.items():
            if recipe and "nutrition" in recipe:
                nutrition = recipe["nutrition"]
                daily_calories += nutrition.get("calories", 0)
                daily_protein += nutrition.get("protein", 0)
                daily_fat += nutrition.get("fat", 0)
                daily_carbs += nutrition.get("carbs", 0)
        
        calories.append(daily_calories)
        proteins.append(daily_protein)
        fats.append(daily_fat)
        carbs.append(daily_carbs)
    
    # グラフを作成
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # カロリーグラフ
    ax1.bar(days, calories, color='#ff9999')
    ax1.set_ylabel('カロリー (kcal)')
    ax1.set_title('1週間のカロリー摂取量')
    ax1.axhline(y=2000, color='r', linestyle='--', alpha=0.7)  # 目安のライン
    
    # PFCグラフ
    x = np.arange(len(days))
    width = 0.25
    
    ax2.bar(x - width, proteins, width, label='タンパク質', color='#ff9999')
    ax2.bar(x, fats, width, label='脂質', color='#66b3ff')
    ax2.bar(x + width, carbs, width, label='炭水化物', color='#99ff99')
    
    ax2.set_ylabel('グラム (g)')
    ax2.set_title('1週間のPFCバランス')
    ax2.set_xticks(x)
    ax2.set_xticklabels(days)
    ax2.legend()
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    # テスト用コード
    root = tk.Tk()
    root.title("栄養情報ビジュアライザー")
    root.geometry("600x500")
    
    # サンプルレシピ
    sample_recipe = {
        "name": "テストレシピ",
        "nutrition": {
            "calories": 450,
            "protein": 25,
            "fat": 15,
            "carbs": 60,
            "vitamins": ["ビタミンA", "ビタミンC", "ビタミンE"],
            "minerals": ["カルシウム", "鉄分", "亜鉛"]
        }
    }
    
    visualizer = NutritionVisualizer(root, sample_recipe)
    visualizer.create_visualization(root)
    
    root.mainloop()