import os
from PIL import Image, ImageDraw, ImageFont

# アイコンのサイズ
icon_size = (256, 256)

# アイコンを作成
icon = Image.new('RGBA', icon_size, color=(240, 248, 255, 255))  # 薄い青色の背景
draw = ImageDraw.Draw(icon)

# 円を描画
draw.ellipse((48, 48, 208, 208), fill=(52, 152, 219, 255))  # 青い円

# テキストを描画（フォントがない場合はこの部分をスキップ）
try:
    # フォントが利用可能な場合
    font = ImageFont.truetype("arial.ttf", 120)
    draw.text((128, 128), "M", fill=(255, 255, 255, 255), font=font, anchor="mm")
except IOError:
    # フォントが利用できない場合は簡単な代替手段
    draw.rectangle((96, 96, 160, 160), fill=(255, 255, 255, 255))

# アイコンを保存
icon.save('meal_recommender_icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("アイコンファイルが作成されました: meal_recommender_icon.ico")