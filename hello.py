import streamlit as st
from datetime import datetime, time, date
import pandas as pd
from PIL import Image, ImageDraw
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

# --- 画像保存の文字化け対策版 ---
def create_result_image(name, n_kan, n_shi, unsei, tenchu, days):
    img = Image.new('RGB', (600, 450), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 590, 440], outline=(200, 200, 200), width=3)
    
    # サーバー環境でも文字化けしにくいよう、英数字をメインに構成
    draw.text((30, 30), " Fortune Telling Result Card ", fill=(50, 50, 50))
    draw.text((30, 80), f" Target: {name if name else 'User'}", fill=(0, 0, 0))
    draw.text((30, 120), f" Type: {jukkan_info[n_kan]['タイプ']} ({n_kan}{n_shi})", fill=(0, 0, 0))
    draw.text((30, 160), f" Energy: {unsei_trans[unsei]} ({unsei})", fill=(0, 0, 0))
    draw.text((30, 200), f" Caution: {tenchu} period", fill=(200, 0, 0))
    if days: draw.text((30, 240), f" Days Passed: {days} days", fill=(0, 128, 0))
    draw.text((30, 400), f" Date: {date.today()}", fill=(150, 150, 150))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

st.subheader("🔮 本格四柱推命：精密鑑定システム")

# 1. 鑑定プロフィール
with st.expander("👤 鑑定プロフィールを入力", expanded=True):
    today = date.today()
    c1, c2, c3 = st.columns(3)
    # 公開用に標準値を設定
    y_val = c1.number_input("生まれた年", 1900, 2100, 2000)
    m_val = c2.number_input("生まれた月", 1, 12, 1)
    d_val = c3.number_input("生まれた日", 1, 31, 1)
    birth_date = date(y_val, m_val, d_val)
    
    use_time = st.checkbox("生まれた時間を指定する")
    if use_time:
        st.time_input("時間を選択", value=time(12, 0))
    
    # 日付範囲エラーを回避
    event_date = st.date_input("経過日数を知りたい日（任意）", value=None, min_value=date(1900, 1, 1))

# 2. 相性鑑定
st.markdown("---")
st.markdown("##### 🤝 相性鑑定（ご家族・友人）")
col_a, col_b = st.columns(2)
partner_name = col_a.text_input("お相手のお名前", placeholder="例：かみさん")
partner_date = col_b.date_input("お相手の生年月日", value=None, min_value=date(1900, 1, 1), max_value=date(2100, 12, 31))

# 3. 実行
if st.button("四柱推命の鑑定を実行", use_container_width=True):
    n_kan, n_shi, n_idx = get_kanshi(birth_date)
    tenchu = get_tenchusatsu(n_idx)
    unsei_list = ["長生", "沐浴", "冠帯", "建禄", "帝旺", "衰", "病", "死", "墓", "絶", "胎", "養"]
    unsei = unsei_list[n_idx % 12]
    days_passed = (today - event_date).days if event_date else None

    st.markdown("---")
    st.success(f"あなたの本質は【{jukkan_info[n_kan]['タイプ']}】です")
    
    # 鑑定表
    res_df = pd.DataFrame({
        "項目": ["本質", "注意時期", "今の勢い"],
        "鑑定結果": [f"{jukkan_info[n_kan]['タイプ']}", f"{tenchu}空亡", f"{unsei_trans[unsei]}"],
        "解説": [f"{jukkan_info[n_kan]['意味']}", "体調管理に気を配る時期です。", "現在のエネルギー状態です。"]
    })
    st.table(res_df)

    # 画像保存ボタン（文字化け対策版）
    img_data = create_result_image("Result", n_kan, n_shi, unsei, tenchu, days_passed)
    st.download_button(label="📸 鑑定結果を画像として保存", data=img_data, file_name="uranai_card.png", mime="image/png")

    if partner_date:
        p_kan, _, _ = get_kanshi(partner_date)
        st.info(f"🤝 **{partner_name if partner_name else 'お相手'}さんは【{jukkan_info[p_kan]['タイプ']}】です**")

    if event_date:
        st.info(f"🚩 **経過日数：あの日から {days_passed} 日目**") # 2026/1/14で273日目

    # 📈 バイオリズムグラフ
    st.markdown("#### 📈 未来バイオリズム（10年間の波）")
    years = [str(today.year + i) for i in range(10)]
    powers = [((n_idx + i * 7) % 12) + 1 for i in range(10)]
    st.line_chart(pd.DataFrame({"パワー": powers}, index=years))