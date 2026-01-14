import streamlit as st
from datetime import datetime, time, date
import pandas as pd

# ページ設定
st.set_page_config(page_title="本格四柱推命・精密鑑定", layout="centered")

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

unsei_trans = {"胎": "準備期", "養": "育成期", "長生": "発展期", "沐浴": "不安定期", "冠帯": "前進期", "建禄": "最盛期", "帝旺": "頂点期", "衰": "円熟期", "病": "内省期", "死": "探求期", "墓": "蓄積期", "絶": "転換期"}

def get_kanshi(target_date):
    if target_date is None: return None, None, None
    jukkan = list(jukkan_info.keys())
    junishi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    diff = (target_date - date(1900, 1, 1)).days
    idx = (diff + 10) % 60
    return jukkan[idx % 10], junishi[idx % 12], idx

def get_tenchusatsu(day_idx):
    group = day_idx // 10
    mapping = ["戌亥", "申酉", "午未", "辰巳", "寅卯", "子丑"]
    return mapping[group % 6]

# 表の色付け用関数
def color_rows(row):
    color = 'background-color: transparent'
    if "本質" in row['鑑定項目']: color = 'background-color: #e3f2fd' # 水色
    elif "注意時期" in row['鑑定項目']: color = 'background-color: #ffebee' # 薄赤
    elif "現在の勢い" in row['鑑定項目']: color = 'background-color: #f1f8e9' # 薄緑
    elif "経過日数" in row['鑑定項目']: color = 'background-color: #fff3e0' # 薄オレンジ
    elif "相性" in row['鑑定項目']: color = 'background-color: #f3e5f5' # 薄紫
    return [color] * len(row)

st.subheader("🔮 本格四柱推命・精密鑑定カルテ")

with st.expander("👤 鑑定プロフィールを入力", expanded=True):
    today = date.today()
    c1, c2, c3 = st.columns(3)
    y_val = c1.number_input("生まれた年", 1900, 2100, 2000)
    m_val = c2.number_input("生まれた月", 1, 12, 1)
    d_val = c3.number_input("生まれた日", 1, 31, 1)
    birth_date = date(y_val, m_val, d_val)
    event_date = st.date_input("経過を知りたい日（任意）", value=None, min_value=date(1900, 1, 1))

st.markdown("---")
st.markdown("##### 🤝 相性鑑定（ご家族・友人）")
col_a, col_b = st.columns(2)
partner_name = col_a.text_input("お相手のお名前", placeholder="例：かみさん")
partner_date = col_b.date_input("お相手の生年月日", value=None, min_value=date(1900, 1, 1))

if st.button("精密鑑定を実行", use_container_width=True):
    n_kan, n_shi, n_idx = get_kanshi(birth_date)
    tenchu = get_tenchusatsu(n_idx)
    unsei = ["長生", "沐浴", "冠帯", "建禄", "帝旺", "衰", "病", "死", "墓", "絶", "胎", "養"][n_idx % 12]
    
    items, results, details = [], [], []
    items.extend(["本質（魂のタイプ）", "注意時期（天中殺）", "現在の勢い（運勢）"])
    results.extend([f"{jukkan_info[n_kan]['タイプ']} ({n_kan}{n_shi})", f"{tenchu}空亡", f"{unsei_trans[unsei]} ({unsei})"])
    details.extend([f"{jukkan_info[n_kan]['意味']}", "無理を控え、体調を整える時期です。", "現在のエネルギー状態です。"])

    if event_date:
        items.append("イベント経過日数")
        results.append(f"{(today - event_date).days} 日目")
        details.append("指定された起算日からの通算日数です。")

    if partner_date:
        p_kan, p_shi, _ = get_kanshi(partner_date)
        items.append(f"{partner_name if partner_name else 'お相手'}との相性")
        results.append(f"{jukkan_info[p_kan]['タイプ']} ({p_kan}{p_shi})")
        details.append("🌟 最高！" if p_kan in jukkan_info[n_kan]['相性'] else "🍵 落ち着いた相性")

    st.markdown("---")
    st.markdown("### 📜 鑑定結果一覧")
    
    # カラーリングを適用した表を表示
    df_result = pd.DataFrame({"鑑定項目": items, "診断結果": results, "詳細メッセージ": details})
    st.table(df_result.style.apply(color_rows, axis=1))

    st.markdown("#### 📈 未来バイオリズム")
    powers = [((n_idx + i * 7) % 12) + 1 for i in range(10)]
    st.line_chart(pd.DataFrame({"パワー": powers}, index=[str(today.year + i) for i in range(10)]))