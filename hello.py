import streamlit as st
from datetime import datetime, time, date
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

# ページ設定
st.set_page_config(page_title="本格四柱推命・統合鑑定システム", layout="centered")

# --- データベース ---
jukkan_info = {
    "甲": {"タイプ": "🌲 大樹", "意味": "真っ直ぐ伸びる正義感", "相性": ["己", "癸"]},
    "乙": {"タイプ": "🌷 草花", "意味": "柔軟で粘り強い和の精神", "相性": ["庚", "壬"]},
    "丙": {"タイプ": "☀️ 太陽", "意味": "明るく情熱的なカリスマ", "相性": ["辛", "乙"]},
    "丁": {"タイプ": "🕯️ 灯火", "意味": "洞察力の鋭い知性派", "相性": ["壬", "甲"]},
    "戊": {"タイプ": "⛰️ 山岳", "意味": "包容力のある安定感", "相性": ["癸", "丙"]},
    "己": {"タイプ": "🏡 田園", "意味": "愛情深く人を育てるのが上手", "相性": ["甲", "丁"]},
    "庚": {"タイプ": "⚔️ 鋼鉄", "意味": "意志が強く決断力がある", "相性": ["乙", "戊"]},
    "辛": {"タイプ": "💎 宝石", "意味": "繊細で美意識が高い", "相性": ["丙", "己"]},
    "壬": {"タイプ": "🌊 大海", "意味": "自由で知性的なロマン派", "相性": ["丁", "庚"]},
    "癸": {"タイプ": "☔ 雨露", "意味": "勤勉で慈愛に満ちた知恵者", "相性": ["戊", "辛"]}
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

# --- 画像生成関数 ---
def create_result_image(name, n_kan, n_shi, unsei, tenchu, days):
    img = Image.new('RGB', (600, 400), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)
    # 簡易的な描画（フォント設定は環境に依存するため標準フォントを使用）
    draw.rectangle([20, 20, 580, 380], outline=(100, 100, 100), width=2)
    draw.text((40, 40), f"【四柱推命 鑑定書】 {name} 様", fill=(0, 0, 0))
    draw.text((40, 80), f"本質：{jukkan_info[n_kan]['タイプ']} ({n_kan}{n_shi})", fill=(0, 0, 0))
    draw.text((40, 120), f"今の勢い：{unsei} ({unsei_trans[unsei]})", fill=(0, 0, 0))
    draw.text((40, 160), f"注意どき：{tenchu}空亡", fill=(200, 0, 0))
    if days: draw.text((40, 200), f"経過記録：{days}日目", fill=(0, 100, 0))
    draw.text((40, 340), f"鑑定日: {date.today()}", fill=(150, 150, 150))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

st.subheader("🔮 四柱推命・精密鑑定（画像保存機能付）")

# 1. 入力
with st.expander("👤 鑑定プロフィール", expanded=True):
    today = date.today()
    c1, c2, c3 = st.columns(3)
    y_val = c1.number_input("年", 1900, 2100, 1957)
    m_val = c2.number_input("月", 1, 12, 11)
    d_val = c3.number_input("日", 1, 31, 20)
    birth_date = date(y_val, m_val, d_val)
    event_date = st.date_input("経過を知りたい起算日（任意）", value=date(2025, 4, 16))

# 2. 相性
st.markdown("---")
partner_name = st.text_input("お相手のお名前", value="かみさん")
partner_date = st.date_input("お相手の生年月日", value=date(1957, 9, 10), min_value=date(1900, 1, 1))

# 3. 実行
if st.button("鑑定を実行", use_container_width=True):
    n_kan, n_shi, n_idx = get_kanshi(birth_date)
    tenchu = get_tenchusatsu(n_idx)
    unsei = ["長生", "沐浴", "冠帯", "建禄", "帝旺", "衰", "病", "死", "墓", "絶", "胎", "養"][n_idx % 12]
    days_passed = (today - event_date).days if event_date else None

    # 結果表示
    st.success(f"あなたの本質：{jukkan_info[n_kan]['タイプ']}")
    st.write(f"現在は「{unsei_trans[unsei]}」の時期です。")
    
    # 画像生成とダウンロードボタン
    img_data = create_result_image("あなた", n_kan, n_shi, unsei, tenchu, days_passed)
    st.download_button(label="📸 鑑定結果を画像として保存", data=img_data, file_name=f"uranai_{today}.png", mime="image/png")

    # 相性
    if partner_date:
        p_kan, _, _ = get_kanshi(partner_date)
        st.info(f"🤝 {partner_name}さんは【{jukkan_info[p_kan]['タイプ']}】です。相性ばっちり！")