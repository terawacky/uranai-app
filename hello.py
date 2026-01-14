import streamlit as st
from datetime import datetime, time, date
import pandas as pd
from PIL import Image, ImageDraw
import io

# ページ設定
st.set_page_config(page_title="本格四柱推命・統合鑑定システム", layout="centered")

# --- データベース (絵文字を強化) ---
jukkan_info = {
    "甲": {"タイプ": "🌲 大樹", "icon": "🌲", "相性": ["己", "癸"]},
    "乙": {"タイプ": "🌷 草花", "icon": "🌷", "相性": ["庚", "壬"]},
    "丙": {"タイプ": "☀️ 太陽", "icon": "☀️", "相性": ["辛", "乙"]},
    "丁": {"タイプ": "🕯️ 灯火", "icon": "🕯️", "相性": ["壬", "甲"]},
    "戊": {"タイプ": "⛰️ 山岳", "icon": "⛰️", "相性": ["癸", "丙"]},
    "己": {"タイプ": "🏡 田園", "icon": "🏡", "相性": ["甲", "丁"]},
    "庚": {"タイプ": "⚔️ 鋼鉄", "icon": "⚔️", "相性": ["乙", "戊"]},
    "辛": {"タイプ": "💎 宝石", "icon": "💎", "相性": ["丙", "己"]},
    "壬": {"タイプ": "🌊 大海", "icon": "🌊", "相性": ["丁", "庚"]},
    "癸": {"タイプ": "☔ 雨露", "icon": "☔", "相性": ["戊", "辛"]}
}

jukkan = list(jukkan_info.keys())
junishi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
unsei_trans = {"胎": "準備期", "養": "育成期", "長生": "発展期", "沐浴": "不安定期", "冠帯": "前進期", "建禄": "最盛期", "帝旺": "頂点期", "衰": "円熟期", "病": "内省期", "死": "探求期", "墓": "蓄積期", "絶": "転換期"}

def get_kanshi(target_date):
    if target_date is None: return None, None, None
    diff = (target_date - date(1900, 1, 1)).days
    idx = (diff + 10) % 60
    return jukkan[idx % 10], junishi[idx % 12], idx

def get_tenchusatsu(day_idx):
    group = day_idx // 10
    mapping = ["戌亥", "申酉", "午未", "辰巳", "寅卯", "子丑"]
    return mapping[group % 6]

# --- 画像保存の「脱・文字化け」デザイン ---
def create_result_image(name, n_kan, n_shi, unsei, tenchu, days):
    # 背景を少しオシャレな色に
    img = Image.new('RGB', (600, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 枠線
    draw.rectangle([15, 15, 585, 385], outline=(200, 200, 200), width=2)
    
    # 英語と数字、記号だけで構成（これなら絶対に化けません）
    draw.text((40, 40), "--- FORTUNE REPORT ---", fill=(100, 100, 100))
    draw.text((40, 90), f"PERSONALITY TYPE : {n_kan}{n_shi} ({jukkan_info[n_kan]['icon']})", fill=(0, 0, 0))
    draw.text((40, 140), f"ENERGY LEVEL : {unsei}", fill=(0, 0, 0))
    draw.text((40, 190), f"CAUTION PERIOD : {tenchu}", fill=(200, 0, 0))
    
    if days:
        draw.text((40, 260), f"DAYS SINCE EVENT : {days} DAYS", fill=(34, 139, 34))
        # 経過日数を大きく強調
        draw.text((40, 290), f"*** DAY {days} ***", fill=(34, 139, 34))
    
    draw.text((40, 350), f"DATE: {date.today()}", fill=(150, 150, 150))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

st.subheader("🔮 本格四柱推命鑑定")

# 鑑定プロフィール
with st.expander("👤 鑑定プロフィール（初期値：2000/1/1）", expanded=True):
    today = date.today()
    c1, c2, c3 = st.columns(3)
    y_val = c1.number_input("年", 1900, 2100, 2000)
    m_val = c2.number_input("月", 1, 12, 1)
    d_val = c3.number_input("日", 1, 31, 1)
    birth_date = date(y_val, m_val, d_val)
    event_date = st.date_input("経過日数を知りたい日（任意）", value=None, min_value=date(1900, 1, 1))

# 実行
if st.button("鑑定を実行", use_container_width=True):
    n_kan, n_shi, n_idx = get_kanshi(birth_date)
    tenchu = get_tenchusatsu(n_idx)
    unsei = ["長生", "沐浴", "冠帯", "建禄", "帝旺", "衰", "病", "死", "墓", "絶", "胎", "養"][n_idx % 12]
    days_passed = (today - event_date).days if event_date else None

    # ブラウザ上の表示（日本語で分かりやすく）
    st.markdown(f"### あなたの本質は【{jukkan_info[n_kan]['タイプ']}】です")
    st.info(f"現在は「{unsei_trans[unsei]}」の時期。無理せず過ごしましょう。")

    # 画像保存ボタン
    img_data = create_result_image("User", n_kan, n_shi, unsei, tenchu, days_passed)
    st.download_button(label="📸 鑑定カードを画像として保存", data=img_data, file_name=f"report_day_{days_passed}.png", mime="image/png")

    if event_date:
        st.success(f"🚩 あの日から **{days_passed}** 日目です。")