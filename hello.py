import streamlit as st
from datetime import datetime, time, date
import pandas as pd

# ページ設定（スマホ最適化）
st.set_page_config(page_title="精密鑑定", layout="centered")

# --- データベース (十干別の解説) ---
jukkan_info = {
    "甲": {"タイプ": "「大樹」", "性格": "正義感が強いリーダー", "金運": "着実に財を成す運。無駄遣い厳禁。", "仕事": "指導的立場や長期プロジェクト向き。", "健康": "肝臓や神経系の疲れ。適度な休息を。"},
    "乙": {"タイプ": "「草花」", "性格": "柔軟で粘り強い、和の精神", "金運": "人脈が財を呼ぶ運。縁を大切に。", "仕事": "サポート業務や細やかな管理。多才さを活かす。", "健康": "消化器系の不調。ストレスに注意。"},
    "丙": {"タイプ": "「太陽」", "性格": "明るく情熱的。周囲を照らす", "金運": "収入は多いが支出も激しい。計画性を。", "仕事": "表現、宣伝、人を鼓舞する役割が最適。", "健康": "心臓、目、血圧。興奮しすぎに注意。"},
    "丁": {"タイプ": "「灯火」", "性格": "内面に情熱を秘める洞察の人", "金運": "技術力、専門知識が財産になる運。", "仕事": "専門技術、研究、創作活動で本領発揮。", "健康": "心臓、冷え性。血液循環を意識。"},
    "戊": {"タイプ": "「山岳」", "性格": "包容力があり信頼される安定感", "金運": "不動産や蓄財。どっしり構えて吉。", "仕事": "組織の管理、不動産、土木、農林業向き。", "健康": "胃腸、糖尿病。暴飲暴食に気をつけて。"},
    "己": {"タイプ": "「田園」", "性格": "愛情深く多才。教え上手な人", "金運": "手堅く貯める運。家庭を大事に。", "仕事": "教育、事務、福祉など育成に関わる分野。", "健康": "胃、脾臓。規則正しい食生活を。"},
    "庚": {"タイプ": "「鋼鉄」", "性格": "意志が強く決断力で道を拓く", "金運": "勝負運あり。目標が明確なほど潤う。", "仕事": "現場指揮、改革、機械、輸送に関わる仕事。", "健康": "肺、喉、大腸。呼吸器の乾燥に注意。"},
    "辛": {"タイプ": "「宝石」", "性格": "繊細で美意識が高く試練で輝く", "金運": "質の高い財に恵まれる運。浪費注意。", "仕事": "精密、金融、貴金属、美的センスの仕事。", "健康": "肺、皮膚、アレルギー。環境の清浄を。"},
    "壬": {"タイプ": "「大海」", "性格": "自由で知性的。大きな視点の持ち主", "金運": "流動的な財運。変化がチャンスを生む。", "仕事": "貿易、航海、企画、動きの激しい業界。", "健康": "腎臓、膀胱。水分の循環を整えて。"},
    "癸": {"タイプ": "「雨露」", "性格": "勤勉で慈愛に満ち知恵で潤す", "金運": "コツコツと大きな財を築く運。", "仕事": "教育、癒やし、サービス業、水に関わる仕事。", "健康": "腎臓、冷え。泌尿器系と足腰のケアを。"}
}

# --- 画面構成 ---
st.subheader("鑑定カルテ：宿命とバイオリズム")

# 1. 入力セクション
with st.expander("👤 プロフィール（デフォルト：本日を表示）", expanded=True):
    today_val = date.today()
    y_val = st.number_input("生まれた年", min_value=1900, max_value=2100, value=today_val.year)
    m_val = st.number_input("生まれた月", min_value=1, max_value=12, value=today_val.month)
    d_val = st.number_input("生まれた日", min_value=1, max_value=31, value=today_val.day)
    
    use_time = st.checkbox("誕生時間が分かればチェック")
    time_str = st.time_input("時間", value=time(12, 0)).strftime("%H:%M") if use_time else "不明"
    
    surgery_date = st.date_input("イベントからの経過日数（手術日等）", value=None, format="YYYY/MM/DD")

# 2. 鑑定項目の選択
target_topic = st.selectbox("🎯 重点鑑定項目", ["本質・性格", "仕事・適職", "金運・財運", "健康・病気"])

if st.button("四柱推命鑑定を実行　鑑定結果は下方", use_container_width=True):
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
    st.markdown(f"### 📋 鑑定結果：{n_kan}{n_shi}")

    # 3. 専門用語の解説（タイトルをスマートに）
    st.markdown("#### 📜 用語の解読")
    explanation_df = pd.DataFrame({
        "項目": ["日柱", "魂の性質", "性格タイプ"],
        "結果": [f"{n_kan}{n_shi}", f"{n_kan}の気", n_kan],
        "解説": [
            "あなたの核となる星です。",
            "魂のエネルギー源。",
            f"{jukkan_info[n_kan]['タイプ']}：{jukkan_info[n_kan]['性格']}"
        ]
    })
    st.table(explanation_df)

    # 4. 詳細鑑定（タイトルをスマートに）
    st.info(f"#### 🔍 {target_topic}")
    if target_topic == "本質・性格":
        st.write(f"あなたの性質は「{jukkan_info[n_kan]['タイプ']}」です。{jukkan_info[n_kan]['性格']}")
    elif target_topic == "仕事・適職":
        st.write(jukkan_info[n_kan]['仕事'])
    elif target_topic == "金運・財運":
        st.write(jukkan_info[n_kan]['金運'])
    elif target_topic == "健康・病気":
        st.write(jukkan_info[n_kan]['健康'])

    if surgery_date:
        days_passed = (date.today() - surgery_date).days
        st.success(f"🏥 経過：{days_passed}日目")

    # 5. 運勢グラフ（タイトルをスマートに）
    st.markdown("#### 📈 未来バイオリズム")
    powers = [((n_idx + i * 7) % 12) + 1 for i in range(11)]
    st.line_chart(pd.DataFrame({"パワー": powers}, index=[str(2026+i) for i in range(11)]))