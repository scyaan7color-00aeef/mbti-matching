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

st.set_page_config(page_title="就活MBTIマッチング", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "questions"
if "mbti" not in st.session_state:
    st.session_state.mbti = None

if st.session_state.page == "questions":
    st.title("就活 自己分析診断")
    st.write("各質問に正直に答えてください。")
    st.divider()

    options = ["まったくそう思わない", "あまりそう思わない", "どちらでもない", "ややそう思う", "とてもそう思う"]

    def radio_score(key, label):
        st.markdown(f"<p style='font-size:1.2rem; font-weight:700; margin-bottom:4px;'>{label}</p>", unsafe_allow_html=True)
        answer = st.radio("　", options, index=2, key=key, horizontal=True, label_visibility="collapsed")
        return options.index(answer) + 1

    q1 = radio_score("q1", "大勢の人といると、エネルギーが湧いてくる")
    q2 = radio_score("q2", "初対面の人とも、すぐに打ち解けられる")
    q3 = radio_score("q3", "一人でいる時間より、誰かといる時間のほうが好きだ")
    st.divider()

    q4 = radio_score("q4", "新しいアイデアより、実績ある方法を好む")
    q5 = radio_score("q5", "将来の可能性より、今の現実を重視する")
    q6 = radio_score("q6", "細かいデータや事実を丁寧に確認するほうだ")
    st.divider()

    q7 = radio_score("q7", "感情より論理・データで決断する")
    q8 = radio_score("q8", "相手に対して率直な意見を言える")
    q9 = radio_score("q9", "公平性やルールを、思いやりより優先することがある")
    st.divider()

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

elif st.session_state.page == "result":
    mbti = st.session_state.mbti
    group, color_data = get_color_group(mbti)
# 強み・弱み・克服法
    ANALYSIS = {
        "NT": {
            "strength": "論理的思考と戦略立案を得意とし、複雑な問題を構造的に分解する力があります。知的好奇心が強く、常に改善策を模索する姿勢は、IT・コンサル・研究職などの分野で高く評価されます。データや根拠に基づいた判断ができるため、意思決定の場面で信頼されやすく、チームの羅針盤的な役割を担えます。独立心が強く、自ら課題を設定して深く掘り下げる力は、専門性を要するキャリアで大きな武器になります。",
            "weakness": "感情表現や共感が苦手なため、対人関係でぶつかることがあります。また、完璧主義が強く出ると意思決定が遅れたり、他者の感情的なニーズを見落とすことがあります。チームワークが求められる場面では、自分のペースや論理を押し付けてしまうと評価が下がる場合もあります。",
            "overcome": "自分の強みである「論理性」を活かしながら、相手の立場を意識する習慣をつけることが重要です。例えば提案の際に「相手にとってのメリット」を先に伝える構成にするだけで印象が変わります。また、弱みを認識した上でFタイプの人と意図的に協力する関係を築くことで、自分の盲点を補えます。",
        },
        "NF": {
            "strength": "共感力と人を動かすコミュニケーション力が際立ちます。理想やビジョンを言葉にして周囲を鼓舞できるため、チームのモチベーション維持や人材育成の場面で力を発揮します。クリエイティブな発想と人への深い関心を持ち合わせており、広告・教育・福祉・HR職などで本来の強みを活かせます。価値観に基づいた判断ができるため、ブレない軸を持ったキャリア形成が可能です。",
            "weakness": "批判や否定に対して傷つきやすく、職場での人間関係がストレスになりやすいです。また、感情に引っ張られて客観的な判断が難しくなることがあります。理想が高すぎるあまり、現実とのギャップに疲弊するケースも見られます。",
            "overcome": "「感じたことを言語化して整理する」習慣が有効です。日記や振り返りメモを書くことで感情と事実を分離しやすくなります。また、批判をフィードバックとして受け取る練習として、信頼できる人から小さな指摘を受ける場を意識的に作ることで、メンタルの耐性を育てられます。",
        },
        "SJ": {
            "strength": "責任感と実行力が高く、ルールや手順を守りながら確実に成果を出す力があります。安定志向で計画的に物事を進められるため、金融・公務員・製造業など信頼性が求められる業界で評価されます。チームの秩序を維持しながら、縁の下の力持ちとして組織を支える役割に向いています。",
            "weakness": "変化や新しいやり方への適応が遅く、既存のやり方に固執することがあります。また、マニュアル外の状況で判断力が低下したり、革新的な提案を受け入れにくいと見られることがあります。",
            "overcome": "強みである「安定した実行力」を土台に、小さな変化を意図的に試す習慣をつけることで柔軟性が育まれます。例えば月に一度「新しい方法で業務を試す」チャレンジを設けるだけで、変化への耐性が高まります。チームでNタイプの発想を取り入れることで相互補完関係も生まれます。",
        },
        "SP": {
            "strength": "状況への適応力と即興的な問題解決力が強みです。現場での機転が利き、スピード感を持って動けるため、変化の激しい環境やサービス業・営業職で特に輝きます。行動力があり、リスクを恐れずに挑戦できる姿勢は、スタートアップや新規事業の開拓にも向いています。",
            "weakness": "長期的な計画を立てたり、コツコツと継続することが苦手な傾向があります。締め切り直前まで動き出せなかったり、飽きっぽさから中途半端になるケースもあります。",
            "overcome": "強みの「瞬発力」を活かしながら、短いスパンの目標設定（週単位・日単位）で計画を管理する方法が効果的です。長期目標を細かく分解し、「今日やること」だけに集中することで継続性が生まれます。また、締め切りを自分で前倒しに設定する習慣も有効です。",
        },
    }

    analysis = ANALYSIS[group]
    st.subheader("あなたの強み")
    st.info(analysis["strength"])
    st.subheader("あなたの弱み")
    st.warning(analysis["weakness"])
    st.subheader("弱みの乗り越え方")
    st.success(analysis["overcome"])
    st.markdown(
        f"<div style='"
        f"background-color:{color_data['hex']}22;"
        f"border-left:6px solid {color_data['hex']};"
        f"border-radius:8px;padding:20px;margin-bottom:20px;'>"
        f"<h1 style='color:{color_data['hex']};margin:0;'>あなたのタイプ：{mbti}</h1>"
        f"<p style='font-size:18px;margin:8px 0 0;'>"
        f"カラーグループ：<strong>{color_data['name']}（{group}型）</strong></p>"
        f"</div>",
        unsafe_allow_html=True
    )

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
