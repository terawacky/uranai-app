import streamlit as st
from datetime import datetime, time, date
import pandas as pd

# ページ設定
st.set_page_config(page_title="本格四柱推命・統合鑑定", layout="centered")

# --- データベース ---
jukkan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
junishi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

tenchu_period = {
    "戌亥": "毎年10月・11月", "申酉": "毎年8月・9月", "午未": "毎年6月・7月",
    "辰巳": "毎年4月・5月", "寅卯": "毎年2月・3月", "子丑": "毎年12月・1月"
}

unsei_trans = {
    "胎": "準備期", "養": "育成期", "長生": "発展期", "沐浴": "不安定期",
    "冠帯": "前進期", "建禄": "最盛期", "帝旺": "頂点期", "衰": "円熟期",
    "病": "内省期", "死": "探求期", "墓": "蓄積期", "絶": "転換期"
}

def get_kanshi(target_date):
    diff = (target_date - date(1900, 1, 1)).days
    idx = (diff + 10) % 60
    return jukkan[idx % 10], junishi[idx % 12], idx

def get_tenchusatsu(day_idx):
    group = day_idx // 10
    mapping = ["戌亥", "申酉", "午未", "辰巳", "寅卯", "子丑"]
    return mapping[group % 6]

st.subheader("🔮 統合鑑定カルテ：精密プロフェッショナル版")

# 1. プロフィール入力
with st.expander("👤 鑑定プロフィール（初期値：本日）", expanded=True):
    today = date.today()
    c1, c2, c3 = st.columns(3)
    y_val = c1.number_input("生まれた年", 1900, 2100, today.year)
    m_val = c2.number_input("生まれた月", 1, 12, today.month)
    d_val = c3.number_input("生まれた日", 1, 31, today.day)
    birth_date = date(y_val, m_val, d_val)
    
    # 時間入力
    use_time = st.checkbox("生まれた時間を指定する")
    if use_time:
        birth_time = st.time_input("生まれた時間", value=time(12, 0))
    
    event_date = st.date_input("イベント経過日数（任意：起算日を選択）", value=None)

# 2. 相性鑑定セクション
st.markdown("---")
st.markdown("##### 🤝 相性鑑定（ご家族・友人）")
col_a, col_b = st.columns(2)
partner_name = col_a.text_input("お相手のお名前", placeholder="例：かみさん")
partner_date = col_b.date_input("お相手の生年月日", value=today, key="partner")

# 3. 鑑定実行
if st.button("四柱推命の鑑定を実行", use_container_width=True):
    n_kan, n_shi, n_idx = get_kanshi(birth_date)
    tenchu = get_tenchusatsu(n_idx)
    unsei_list = ["長生", "沐浴", "冠帯", "建禄", "帝旺", "衰", "病", "死", "墓", "絶", "胎", "養"]
    unsei = unsei_list[n_idx % 12]

    st.markdown("---")
    st.markdown("### 📜 あなたの「取り扱い説明書」")
    
    res_df = pd.DataFrame({
        "項目": ["本質（魂の形）", "注意どき（天中殺）", "今の勢い（十二運星）", "持っている才能"],
        "具体的な内容": [f"{n_kan}{n_shi}", f"{tenchu}空亡", f"{unsei}", "技術・ブログ・探求"],
        "いつ？ どうすれば？": [
            "あなたの根っこの性格です。",
            f"具体的には【{tenchu_period[tenchu]}】。この時期は自分を労わって。",
            f"「{unsei_trans[unsei]}」の状態。今の心の持ちようを表します。",
            "専門的なこと（Pythonやブログ運営）を深掘りすると成功します。"
        ]
    })
    st.table(res_df)

    # 相性鑑定の結果表示
    if partner_name:
        p_kan, p_shi, _ = get_kanshi(partner_date)
        st.success(f"🤝 **{partner_name}さんとの相性**：{partner_name}さんは「{p_kan}」の性質をお持ちです。")

    # 経過日数の表示
    if event_date:
        days_passed = (today - event_date).days
        st.info(f"🚩 **イベントから {days_passed} 日目**") # 術後経過（2025/4/16起算）なら本日で271日目

    # 未来バイオリズムの再実装
    st.markdown("#### 📈 未来バイオリズム（2026-2035）")
    years = [str(2026 + i) for i in range(10)]
    powers = [((n_idx + i * 7) % 12) + 1 for i in range(10)]
    st.line_chart(pd.DataFrame({"パワー": powers}, index=years))