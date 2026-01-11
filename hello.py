import streamlit as st
from datetime import datetime

# ページ設定
st.set_page_config(page_title="四柱推命・特選鑑定", layout="centered")
st.markdown('<html lang="ja"></html>', unsafe_allow_html=True)

# 鑑定データ（すべての干に 'desc' を含む全項目を揃えました）
master_data = {
    "甲": {"star": "比肩", "fortune": "着実な蓄財が吉。", "health": "肝臓・目に注意。", "color": "深緑", "bike": "慎重な運転が吉。一本気な性格が運転に出やすいので余裕を。", "desc": "大樹のように正義感が強く、リーダーの資質があります。"},
    "乙": {"star": "劫財", "fortune": "人との繋がりが財を生みます。", "health": "肩こり・自律神経に注意。", "color": "薄緑", "bike": "柔軟な対応ができる日。景色を楽しむツーリングが最適。", "desc": "草花のように柔軟で粘り強く、周囲と協力する力があります。"},
    "丙": {"star": "食神", "fortune": "生涯食べることには困りません。", "health": "心臓・血圧に注意。", "color": "赤", "bike": "開放的になりすぎて速度超過に注意。明るい走りを。", "desc": "太陽のように明るく、陽気で表現力豊かな社交家です。"},
    "丁": {"star": "傷官", "fortune": "才能が財に直結します。", "health": "視力・睡眠不足に注意。", "color": "オレンジ", "bike": "感受性が鋭い日。夜のツーリングや細かな整備にツキあり。", "desc": "灯火のように繊細で、鋭い感受性と知性を持っています。"},
    "戊": {"star": "偏財", "fortune": "大きな財を動かす運勢。", "health": "胃腸の不調に注意。", "color": "黄", "bike": "どっしり安定した運転ができる日。ロングツーリングに最適。", "desc": "堂々とした山のように、包容力があり周囲から頼られます。"},
    "己": {"star": "正財", "fortune": "堅実で安定した蓄財運。", "health": "脾臓・胃痛に注意。", "color": "茶", "bike": "基本に忠実な運転ができる日。日常の点検をしっかり行うと吉。", "desc": "実り豊かな大地のように、誠実で教養があり努力家です。"},
    "庚": {"star": "偏官", "fortune": "勝負運があり一気に築く運。", "health": "呼吸器系に注意。", "color": "シルバー", "bike": "決断力が冴える日。力強い加速を楽しめますが強引な運転は禁物。", "desc": "鍛えられた刀のように、決断力と行動力に溢れています。"},
    "辛": {"star": "正官", "fortune": "品位を保つと財運アップ。", "health": "皮膚・喉に注意。", "color": "パールホワイト", "bike": "気品ある運転ができる日。愛車を磨いてから出発すると吉。", "desc": "気品ある宝石のように、完璧主義で美意識が高い人です。"},
    "壬": {"star": "偏印", "fortune": "アイデアを形にすると吉。", "health": "腎臓・耳に注意。", "color": "紺", "bike": "自由を求める日。行き先を決めない放浪ツーリングに発見あり。", "desc": "大海原のようにダイナミックで、自由を愛する冒険家です。"},
    "癸": {"star": "印綬", "fortune": "知恵と学びが財を生みます。", "health": "冷え・泌尿器に注意。", "color": "水色", "bike": "思慮深い日。事前の準備と地図の確認を徹底すると吉。", "desc": "恵みの雨のように、優しく思慮深い癒やし系です。"}
}

st.title("🔮 四柱推命・特選鑑定")

# 入力セクション
col1, col2 = st.columns(2)
with col1:
    birth_date = st.date_input("生年月日を選択", value=datetime(1957, 11, 20), format="YYYY/MM/DD")
with col2:
    birth_time = st.time_input("生まれた時間（任意）", value=None)

st.subheader("📋 占いたい項目を選んでください")
target_item = st.selectbox(
    "鑑定メニュー",
    ["総合鑑定（すべて表示）", "金運・仕事運", "健康運・ラッキーカラー", "バイク・安全運転鑑定"]
)

if st.button("鑑定実行"):
    jukkan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    junishi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    base_date = datetime(1900, 1, 1).date()
    diff_days = (birth_date - base_date).days
    eto_index = (diff_days + 10) % 60
    nichi_kan = jukkan[eto_index % 10]
    nichi_shi = junishi[eto_index % 12]
    
    res = master_data.get(nichi_kan)

    st.markdown("---")
    st.header(f"鑑定結果：{nichi_kan}{nichi_shi}")

    if target_item == "総合鑑定（すべて表示）" or target_item == "金運・仕事運":
        st.success(f"**💰 金運・仕事:** {res['fortune']}")

    if target_item == "総合鑑定（すべて表示）" or target_item == "健康運・ラッキーカラー":
        st.warning(f"**🏥 健康運:** {res['health']}")
        st.info(f"**🎨 ラッキーカラー:** {res['color']}")

    if target_item == "総合鑑定（すべて表示）" or target_item == "バイク・安全運転鑑定":
        st.error(f"**🏍 バイク・運転のアドバイス:**\n\n{res['bike']}")

    if target_item == "総合鑑定（すべて表示）":
        with st.expander("あなたの本質的な性格（詳しく見る）"):
            st.write(res['desc'])