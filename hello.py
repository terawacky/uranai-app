import streamlit as st
from datetime import datetime, time, date
import pandas as pd

# ページ設定（スマホ最適化）
st.set_page_config(page_title="精密鑑定", layout="centered")

# --- データベース (十干別の解説) ---
jukkan_info = {
    "甲": {"タイプ": "「大樹」", "性格": "真っ直ぐで正義感が強いリーダー", "金運": "着実に財を成す運。無駄遣いを控えると吉。", "仕事": "人を導く役職や長期プロジェクト向き。", "健康": "肝臓や神経系の疲れに注意。"},
    "乙": {"タイプ": "「草花」", "性格": "柔軟で粘り強く、和を重んじる", "金運": "人との縁から財が入る運。人脈が宝。", "仕事": "サポート役や細やかな気遣いの仕事向き。", "健康": "消化器系の不調、ストレスに注意。"},
    "丙": {"タイプ": "「太陽」", "性格": "明るく情熱的。周囲を照らすカリスマ", "金運": "派手にお金が入るが、出費も多い傾向。", "仕事": "表舞台に立つ仕事や人を励ます役割向き。", "健康": "心臓、目、血圧に注意。熱中しすぎに注意。"},
    "丁": {"タイプ": "「灯火」", "性格": "内面に情熱を秘める、洞察力の鋭い知性派", "金運": "技術や才能がお金に変わる運。", "仕事": "専門職やじっくり取り組む創作活動向き。", "健康": "心臓、冷え性、循環器系に注意。"},
    "戊": {"タイプ": "「山岳」", "性格": "包容力があり、信頼される安定感の持ち主", "金運": "不動産や蓄財に向く運。どっしり構えて吉。", "仕事": "組織の要となる役職や管理業務向き。", "健康": "胃腸の不調に注意。暴飲暴食を控えて。"},
    "己": {"タイプ": "「田園」", "性格": "愛情深く多才。人を育てるのが上手い", "金運": "コツコツ貯めるのが得意な運。", "仕事": "教育、福祉、事務など人の役に立つ仕事向き。", "健康": "脾臓や胃に注意。規則正しい生活を。"},
    "庚": {"タイプ": "「鋼鉄」", "性格": "意志が強く、決断力と行動力で道を拓く", "金運": "勝負運あり。大きな目標が金運を呼ぶ。", "仕事": "現場指揮や変化の激しい環境向き。", "健康": "肺、大腸、喉に注意。深呼吸を。"},
    "辛": {"タイプ": "「宝石」", "性格": "繊細で美意識が高く、試練を越えて輝く", "金運": "質の高いものに恵まれる運。浪費注意。", "仕事": "精密作業や美的センスを活かす仕事向き。", "健康": "肺や皮膚の過敏症、呼吸器に注意。"},
    "壬": {"タイプ": "「大海」", "性格": "自由で知性的。大きな視点を持つロマン派", "金運": "流動的な財運。変化を恐れず動くと吉。", "仕事": "貿易、輸送、企画など動きのある仕事向き。", "健康": "腎臓、膀胱に注意。水分代謝を整えて。"},
    "癸": {"タイプ": "「雨露」", "性格": "勤勉で慈愛に満ち、知恵で周囲を潤す", "金運": "少額から大きな財を築く運。", "仕事": "教育、コンサル、癒やしの仕事向き。", "健康": "腎臓、冷え性、足腰の疲れに注意。"}
}

# --- 画面構成 ---
st.subheader("🔮 精密鑑定システム：人生の鑑定書")

# 入力セクション
with st.expander("📅 プロフィール入力（タップで展開）", expanded=True):
    # 本日の日付を取得してデフォルト値に設定
    today_val = date.today()
    
    y_val = st.number_input("年", min_value=1900, max_value=2100, value=today_val.year)
    m_val = st.number_input("月", min_value=1, max_value=12, value=today_val.month)
    d_val = st.number_input("日", min_value=1, max_value=31, value=today_val.day)
    
    use_time = st.checkbox("誕生時間を指定")
    time_str = st.time_input("時間", value=time(12, 0)).strftime("%H:%M") if use_time else "不明"
    
    surgery_date = st.date_input("手術経過を確認（任意）", value=None, format="YYYY/MM/DD")

# 鑑定項目の選択
target_topic = st.selectbox("🔍 詳しく占いたい項目", ["本質・基本性格", "仕事運・適職", "金運・財運", "健康運・病気"])

if st.button("精密鑑定を実行する", use_container_width=True):
    try:
        birth_date = date(y_val, m_val, d_val)
    except:
        st.error("正しい日付を入力してください")
        st.stop()

    # 四柱推命計算
    jukkan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    junishi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    diff_days = (birth_date - date(1900, 1, 1)).days
    n_idx = (diff_days + 10) % 60
    n_kan, n_shi = jukkan[n_idx % 10], junishi[n_idx % 12]

    st.markdown("---")
    st.header(f"✨ 鑑定結果：{n_kan}{n_shi}")
    st.write(f"（{birth_date.year}年{birth_date.month}月{birth_date.day}日生まれ）")

    # 【解説表】
    st.subheader("📜 鑑定用語の解説")
    explanation_df = pd.DataFrame({
        "項目": ["日柱 (自分自身)", "魂の性質", "性格のタイプ"],
        "結果": [f"{n_kan}{n_shi}", f"{n_kan}の気", n_kan],
        "プロの解説": [
            "あなたの本質。最も重要な星です。",
            "生まれ持った自然のエネルギー。",
            f"{jukkan_info[n_kan]['タイプ']}：{jukkan_info[n_kan]['性格']}"
        ]
    })
    st.table(explanation_df)

    # 項目別詳細
    st.info(f"#### 🔍 {target_topic}の詳細鑑定")
    if target_topic == "本質・基本性格":
        st.write(f"あなたの魂は「{jukkan_info[n_kan]['タイプ']}」の性質を持っています。{jukkan_info[n_kan]['性格']}")
    elif target_topic == "仕事運・適職":
        st.write(jukkan_info[n_kan]['仕事'])
    elif target_topic == "金運・財運":
        st.write(jukkan_info[n_kan]['金運'])
    elif target_topic == "健康運・病気":
        st.write(jukkan_info[n_kan]['健康'])

    if surgery_date:
        days_passed = (date.today() - surgery_date).days
        st.success(f"🏥 手術日から **{days_passed}日目** です。")

    # 運勢グラフ
    st.subheader("📈 2026年からのバイオリズム")
    powers = [((n_idx + i * 7) % 12) + 1 for i in range(11)]
    st.line_chart(pd.DataFrame({"パワー": powers}, index=[str(2026+i) for i in range(11)]))