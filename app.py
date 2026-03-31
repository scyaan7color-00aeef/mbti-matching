import streamlit as st

# MBTIカラー設定
MBTI_COLORS = {
    "NT": {"name": "紫", "hex": "#9B59B6", "types": ["INTJ","INTP","ENTJ","ENTP"]},
    "NF": {"name": "緑", "hex": "#27AE60", "types": ["INFJ","INFP","ENFJ","ENFP"]},
    "SJ": {"name": "青", "hex": "#2980B9", "types": ["ISTJ","ISFJ","ESTJ","ESFJ"]},
    "SP": {"name": "黄", "hex": "#F1C40F", "types": ["ISTP","ISFP","ESTP","ESFP"]},
}

def get_color_group(mbti):
    for group, data in MBTI_COLORS.items():
        if mbti in data["types"]:
            return group, data
    return "NT", MBTI_COLORS["NT"]

# 業界スコア計算
WEIGHTS = {
    "IT・ソフトウェア":   [10, 20,  5, 25, 30,  5, 20, 15],
    "コンサルティング":   [25,  5, 10, 20, 25,  5, 20, 10],
    "金融・銀行・保険":   [10, 15, 25, 10, 25, 10, 25,  5],
    "メーカー（製造）":   [10, 15, 25, 10, 20, 15, 25,  5],
    "商社":               [25,  5, 15, 15, 20, 10, 20, 15],
    "広告・メディア":     [25,  5,  5, 30, 10, 20, 10, 20],
    "医療・福祉":         [15, 10, 20, 10,  5, 35, 25,  5],
    "公務員・非営利":     [10, 15, 30,  5, 15, 20, 30,  5],
    "小売・サービス":     [30,  5, 20, 10, 10, 25, 15, 10],
    "不動産・建設":       [20, 10, 20, 10, 15, 15, 25, 10],
}

def calc_scores(mbti):
    e = 1 if mbti[0] == "E" else 0
    i = 1 - e
    s = 1 if mbti[1] == "S" else 0
    n = 1 - s
    t = 1 if mbti[2] == "T" else 0
    f = 1 - t
    j = 1 if mbti[3] == "J" else 0
    p = 1 - j
    vec = [e, i, s, n, t, f, j, p]
    return {ind: sum(v * w for v, w in zip(vec, ws)) for ind, ws in WEIGHTS.items()}

def derive_mbti(e_score, s_score, t_score, j_score):
    e = "E" if e_score >= 3 else "I"
    s = "S" if s_score >= 3 else "N"
    t = "T" if t_score >= 3 else "F"
    j = "J" if j_score >= 3 else "P"
    return e + s + t + j

# --- ページ設定 ---
st.set_page_config(page_title="就活MBTIマッチング", layout="centered")
# カスタムCSS
st.markdown("""
<style>
/* 質問文を大きく */
div[class*="stRadio"] > label p { font-size: 20px !important; font-weight: 600; }
/* 選択肢を少し小さく */
div[class*="stRadio"] label div p { font-size: 14px !important; font-weight: normal; }
/* subheaderを小さく */
h3 { font-size: 18px !important; }
</style>
""", unsafe_allow_html=True)
# =====================
# ページ1：質問
# =====================
if st.session_state.page == "questions":
    st.title("就活 自己分析診断")
    st.write("各質問に正直に答えてください。")
    st.divider()

    options = ["まったくそう思わない", "あまりそう思わない", "どちらでもない", "ややそう思う", "とてもそう思う"]

    def radio_score(key, label):
        answer = st.radio(label, options, index=2, key=key, horizontal=True)
        return options.index(answer) + 1

    st.subheader("① エネルギーの向き")
    q1 = radio_score("q1", "大勢の人といると、エネルギーが湧いてくる")
    q2 = radio_score("q2", "初対面の人とも、すぐに打ち解けられる")
    q3 = radio_score("q3", "一人でいる時間より、誰かといる時間のほうが好きだ")
    st.divider()

    st.subheader("② 情報の受け取り方")
    q4 = radio_score("q4", "新しいアイデアより、実績ある方法を好む")
    q5 = radio_score("q5", "将来の可能性より、今の現実を重視する")
    q6 = radio_score("q6", "細かいデータや事実を丁寧に確認するほうだ")
    st.divider()

    st.subheader("③ 判断の基準")
    q7 = radio_score("q7", "感情より論理・データで決断する")
    q8 = radio_score("q8", "相手に対して率直な意見を言える")
    q9 = radio_score("q9", "公平性やルールを、思いやりより優先することがある")
    st.divider()

    st.subheader("④ 生活スタイル")
    q10 = radio_score("q10", "計画を立ててから行動しないと落ち着かない")
    q11 = radio_score("q11", "締め切りは早めに終わらせる派だ")
    q12 = radio_score("q12", "予定が急に変わると、ストレスを感じる")
    st.divider()

    if st.button("診断する", type="primary", use_container_width=True):
        e_score = (q1 + q2 + q3) / 3
        s_score = (q4 + q5 + q6) / 3
        t_score = (q7 + q8 + q9) / 3
        j_score = (q10 + q11 + q12) / 3
        st.session_state.mbti = derive_mbti(e_score, s_score, t_score, j_score)
        st.session_state.page = "result"
        st.rerun()

# =====================
# ページ2：結果
# =====================
elif st.session_state.page == "result":
    mbti = st.session_state.mbti
    group, color_data = get_color_group(mbti)

    # カラーテーマ背景
    st.markdown(
        f"""
        <div style="
            background-color: {color_data['hex']}22;
            border-left: 6px solid {color_data['hex']};
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <h1 style="color: {color_data['hex']}; margin: 0;">あなたのタイプ：{mbti}</h1>
            <p style="font-size: 18px; margin: 8px 0 0;">
                カラーグループ：<strong>{color_data['name']}（{group}型）</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # スコア計算・表示
    scores = calc_scores(mbti)
    sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

    st.subheader("業界相性ランキング")
    st.bar_chart(sorted_scores, color=color_data["hex"])

    st.subheader("スコア一覧")
    for i, (industry, score) in enumerate(sorted_scores.items(), 1):
        st.write(f"{i}位　{industry}：{score}点")

    st.divider()
    if st.button("もう一度診断する", use_container_width=True):
        st.session_state.page = "questions"
        st.session_state.mbti = None
        st.rerun()
#streamlit run app.py
