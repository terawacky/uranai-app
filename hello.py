import streamlit as st
from datetime import datetime, time, date
import pandas as pd

# ページ設定
st.set_page_config(page_title="本格四柱推命・精密鑑定", layout="wide")

# --- データベース ---
jukkan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
junishi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

st.title("🔮 本格四柱推命：精密鑑定システム")

# --- サイドバー設定 ---
st.sidebar.header("プロフィール入力")

# 本日の日付を取得
today_val = date.today()

# 改善ポイント：min_valueを1900年に設定し、valueをtodayにすることで本日を起点に過去へ戻れるようにします
st.sidebar.write("① 生年月日を選択（1900年〜対応）")
birth_date = st.sidebar.date_input(
    "カレンダーをクリックして年を選んでください", 
    value=today_val,           # 初期表示は本日
    min_value=date(1900, 1, 1), # 1900年まで遡れるように拡大
    max_value=date(2100, 12, 31),
    format="YYYY/MM/DD"
)

# 補助：数字で直接「年」を入力してジャンプする機能（1957などと打つと早いです）
y_jump = st.sidebar.number_input("年を直接入力して移動", min_value=1900, max_value=2100, value=birth_date.year)
if y_jump != birth_date.year:
    # 数字入力が変更されたらカレンダー側も更新されるようにします
    birth_date = date(y_jump, birth_date.month, birth_date.day)

birth_time = st.sidebar.time_input("誕生時間（任意）", value=time(12, 0))

# 手術経過（任意入力）
surgery_date = st.sidebar.date_input("手術経過を確認（任意）", value=None, min_value=date(1900, 1, 1), format="YYYY/MM/DD")

if st.sidebar.button("鑑定を実行"):
    # 本日 2026年1月11日
    today = date.today()
    
    # 計算ロジック
    base_date = date(1900, 1, 1)
    diff_days = (birth_date - base_date).days
    n_idx = (diff_days + 10) % 60
    n_kan = jukkan[n_idx % 10]
    n_shi = junishi[n_idx % 12]

    # 鑑定結果の表示
    st.header(f"✨ 鑑定結果：{n_kan}{n_shi}")
    
    # 手術日（2025年4月16日）を基準にした経過表示
    if surgery_date:
        days_passed = (today - surgery_date).days
        st.success(f"🏥 手術から **{days_passed}日目** です。")

    t1, t2 = st.tabs(["📊 宿命の解説", "📈 10年バイオリズム"])

    with t1:
        st.subheader("💡 鑑定結果の意味")
        st.table(pd.DataFrame({
            "項目": ["日柱 (自分自身)", "中心五行"],
            "結果": [f"{n_kan}{n_shi}", f"{n_kan}の気"]
        }))

    with t2:
        st.subheader("2026年からの10年運勢バイオリズム")
        years = [str(2026 + i) for i in range(11)]
        powers = [((n_idx + i * 7) % 12) + 1 for i in range(11)]
        st.line_chart(pd.DataFrame({"年": years, "パワー": powers}).set_index("年"))