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

# --- セッション状態 ---
if "page" not in st.session_state:
    st.session_state.page = "questions"
if "mbti" not in st.session_state:
    st.session_state.mbti = None

# =====================
# ページ1：質問
# =====================
if st.session_state.page == "questions":
    st.title("就活 自己分析診断")
    st.write("各質問に1〜5で答えてください。（1=左に近い、5=右に近い）")
    st.divider()

    st.subheader("① エネルギーの向き")
    q1 = st.slider("大勢といると元気になる", 1, 5, 3, key="q1",
                   help="1=一人が好き ／ 5=大勢が好き")
    q2 = st.slider("初対面でもすぐ打ち解ける", 1, 5, 3, key="q2",
                   help="1=時間がかかる ／ 5=すぐ打ち解ける")
    st.divider()

    st.subheader("② 情報の受け取り方")
    q3 = st.slider("実績ある手順を好む", 1, 5, 3, key="q3",
                   help="1=新しいやり方派 ／ 5=実績ある手順派")
    q4 = st.slider("今の現実を重視する", 1, 5, 3, key="q4",
                   help="1=可能性重視 ／ 5=現実重視")
    st.divider()

    st.subheader("③ 判断の基準")
    q5 = st.slider("論理・データで決断する", 1, 5, 3, key="q5",
                   help="1=感情・人間関係派 ／ 5=論理・データ派")
    q6 = st.slider("率直な批評をする", 1, 5, 3, key="q6",
                   help="1=気持ちを優先する ／ 5=率直に言う")
    st.divider()

    st.subheader("④ 生活スタイル")
    q7 = st.slider("計画を立てないと落ち着かない", 1, 5, 3, key="q7",
                   help="1=行き当たりばったりOK ／ 5=計画必須")
    st.divider()

    if st.button("診断する", type="primary", use_container_width=True):
        e_score = (q1 + q2) / 2
        s_score = (q3 + q4) / 2
        t_score = (q5 + q6) / 2
        j_score = (q7 + q8) / 2
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
```

---

貼り付けたら保存して：
```
streamlit run app.py
