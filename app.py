import streamlit as st

# 業界リスト
industries = [
    "IT・ソフトウェア", "コンサルティング", "金融・銀行・保険",
    "メーカー（製造）", "商社", "広告・メディア",
    "医療・福祉", "公務員・非営利", "小売・サービス", "不動産・建設"
]

# 業界別の重み設定 [E, I, S, N, T, F, J, P]
weights = {
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
    # MBTIを軸ごとに数値化 [E, I, S, N, T, F, J, P]
    e = 1 if mbti[0] == "E" else 0
    i = 1 - e
    s = 1 if mbti[1] == "S" else 0
    n = 1 - s
    t = 1 if mbti[2] == "T" else 0
    f = 1 - t
    j = 1 if mbti[3] == "J" else 0
    p = 1 - j
    vec = [e, i, s, n, t, f, j, p]

    result = {}
    for industry, w in weights.items():
        result[industry] = sum(v * wt for v, wt in zip(vec, w))
    return result

# --- UI ---
st.title("就活MBTIマッチング診断")
st.write("あなたのMBTIタイプを選んで、業界との相性を確認しましょう。")

mbti_types = [
    "ENFJ", "ENFP", "ENTJ", "ENTP",
    "ESFJ", "ESFP", "ESTJ", "ESTP",
    "INFJ", "INFP", "INTJ", "INTP",
    "ISFJ", "ISFP", "ISTJ", "ISTP"
]

mbti = st.selectbox("あなたのMBTIタイプは？", mbti_types)

if st.button("診断する"):
    scores = calc_scores(mbti)
    sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

    st.subheader(f"{mbti} の業界相性ランキング")
    st.bar_chart(sorted_scores)

    st.subheader("スコア一覧")
    for i, (industry, score) in enumerate(sorted_scores.items(), 1):
        st.write(f"{i}位　{industry}：{score}点")