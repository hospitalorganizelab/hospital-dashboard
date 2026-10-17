
import streamlit as st
from supabase import create_client
from datetime import date

st.set_page_config(
    page_title="病院経営管理アプリ",
    page_icon="🐢",
    layout="wide"
)

# ===== デザイン =====
st.markdown("""
<style>
.stApp {
    background: #F2F8FC;
    color: #24465A;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 150px;
    max-width: 1200px;
}
h1, h2, h3 {
    color: #225D7A !important;
}
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #D8EAF4;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 3px 12px #B6D8E522;
}
[data-testid="stMetricLabel"] {
    color: #54819A;
}
[data-testid="stMetricValue"] {
    color: #176F98;
}
.stButton > button {
    border-radius: 12px;
    border: 1px solid #A8D5E9;
    background: #DDF2FA;
    color: #205D7A;
    font-weight: 600;
}
.stButton > button:hover {
    background: #C2E8F5;
    border-color: #70BBD8;
}
div[data-baseweb="input"],
div[data-baseweb="select"] {
    border-radius: 10px;
}
hr {
    border-color: #D4E8F2;
}

/* 海のフッター */
.ocean {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100px;
    z-index: 999;
    pointer-events: none;
    overflow: hidden;
    background: linear-gradient(
        180deg, #DDF5FC00 0%, #B9EAF5CC 45%, #78CDE5EE 100%
    );
}
.wave {
    position: absolute;
    width: 200%;
    height: 36px;
    left: 0;
    top: 14px;
    border-radius: 45% 45% 0 0;
    background: #9ADDED88;
    animation: wave-move 8s linear infinite;
}
.wave.second {
    top: 29px;
    background: #63C2E355;
    animation-duration: 12s;
}
@keyframes wave-move {
    from { transform: translateX(0); }
    to { transform: translateX(-50%); }
}

/* ウミガメ本体 */
.turtle {
    position: absolute;
    bottom: 14px;
    left: -150px;
    width: 125px;
    height: 76px;
    animation: swim 22s linear infinite;
}
@keyframes swim {
    0% { left: -150px; }
    100% { left: calc(100% + 150px); }
}
.flipper {
    transform-box: fill-box;
    transform-origin: center;
}
.front-left {
    animation: paddle 0.9s ease-in-out infinite alternate;
}
.front-right {
    animation: paddle 0.9s ease-in-out infinite alternate-reverse;
}
.back-left {
    animation: paddle 0.75s ease-in-out infinite alternate-reverse;
}
.back-right {
    animation: paddle 0.75s ease-in-out infinite alternate;
}
@keyframes paddle {
    from { transform: rotate(-17deg) translateY(-2px); }
    to { transform: rotate(19deg) translateY(3px); }
}
@media (prefers-reduced-motion: reduce) {
    .wave, .turtle, .flipper {
        animation: none !important;
    }
}
</style>

<div class="ocean">
  <div class="wave"></div>
  <div class="wave second"></div>
  <div class="turtle">
    <svg viewBox="0 0 160 100"
         width="125" height="76"
         xmlns="http://www.w3.org/2000/svg">
      <!-- 後ろのひれ -->
      <g fill="#62B9D0" stroke="#287E9E" stroke-width="1.7">
        <path class="flipper back-left"
          d="M48 56 Q24 63 23 77 Q25 84 43 72 L57 62Z"/>
        <path class="flipper back-right"
          d="M91 58 Q110 64 111 77 Q108 84 94 71 L84 63Z"/>
      </g>
      <!-- 前ひれ -->
      <g fill="#70C8DC" stroke="#287E9E" stroke-width="1.8">
        <path class="flipper front-left"
          d="M57 51 Q35 35 21 43 Q12 50 28 61 L53 64Z"/>
        <path class="flipper front-right"
          d="M95 51 Q116 34 131 42 Q141 50 124 62 L99 64Z"/>
      </g>
      <!-- 甲羅 -->
      <path d="M43 47 Q44 22 76 21 Q105 21 116 46
        Q114 65 82 70 Q52 68 43 47Z"
        fill="#168EB7" stroke="#155C7C" stroke-width="3"/>
      <!-- 甲羅の模様 -->
      <g fill="none" stroke="#A9E5EE" stroke-width="2">
        <path d="M49 39 L65 31 L78 42 L67 61"/>
        <path d="M65 31 L89 29 L99 43 L90 64"/>
        <path d="M78 42 L99 43 L111 48"/>
        <path d="M67 61 L90 64"/>
      </g>
      <!-- 頭 -->
      <path d="M108 39 Q119 25 135 31
        Q148 37 141 49 Q135 57 119 51 L108 49Z"
        fill="#B4E3E7" stroke="#287E9E" stroke-width="2"/>
      <!-- 自然な大きさの目 -->
      <ellipse cx="134" cy="37" rx="2.7" ry="3.3" fill="#24485A"/>
      <circle cx="135" cy="36" r="0.9" fill="white"/>
      <path d="M138 48 Q142 49 144 46"
        fill="none" stroke="#287E9E" stroke-width="1.4"
        stroke-linecap="round"/>
    </svg>
  </div>
</div>
""", unsafe_allow_html=True)

st.title("病院経営管理アプリ")
st.caption("病床管理・個室収益・日次記録")

# ===== Supabase接続 =====
try:
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
except Exception:
    st.error("Supabaseの接続設定を確認してください。")
    st.stop()

# ===== 日次記録 =====
st.header("日次記録")
record_date = st.date_input("記録日", value=date.today())

# ===== 病床管理 =====
st.header("病床管理")
beds = st.number_input(
    "稼働可能病床数", min_value=1, value=40
)
patients = st.number_input(
    "在院患者数", min_value=0,
    max_value=int(beds), value=min(34, int(beds))
)
admissions = st.number_input(
    "本日の入院数", min_value=0, value=5
)
emergency = st.number_input(
    "緊急入院数", min_value=0,
    max_value=int(admissions),
    value=min(3, int(admissions))
)
discharges = st.number_input(
    "本日の退院数", min_value=0, value=4
)

occupancy = patients / beds * 100

col1, col2 = st.columns(2)
col1.metric("病床稼働率", f"{occupancy:.1f}%")
col2.metric("空床数", int(beds - patients))

col1, col2, col3 = st.columns(3)
col1.metric("緊急入院", int(emergency))
col2.metric("本日の退院", int(discharges))
col3.metric("入退院差引", int(admissions - discharges))

# ===== 個室管理・収益 =====
st.divider()
st.header("個室管理・収益")

private_rooms = st.number_input(
    "個室総数", min_value=0, value=8
)
occupied_rooms = st.number_input(
    "使用中の個室数", min_value=0,
    max_value=int(private_rooms),
    value=min(6, int(private_rooms))
)
room_fee = st.number_input(
    "個室料（1室・1日あたり／円）",
    min_value=0, value=6000, step=500
)
charge_days = st.number_input(
    "料金発生日数", min_value=0, value=1
)

room_occupancy = (
    occupied_rooms / private_rooms * 100
    if private_rooms > 0 else 0
)
daily_revenue = occupied_rooms * room_fee
period_revenue = daily_revenue * charge_days

col1, col2 = st.columns(2)
col1.metric("個室稼働率", f"{room_occupancy:.1f}%")
col2.metric("個室空室数", int(private_rooms - occupied_rooms))

col1, col2 = st.columns(2)
col1.metric("1日あたりの個室料収益", f"{daily_revenue:,.0f}円")
col2.metric("期間内の個室料収益", f"{period_revenue:,.0f}円")

# ===== 保存 =====
st.divider()

if st.button("この日の記録を保存", type="primary"):
    try:
        data = {
            "record_date": record_date.isoformat(),
            "total_beds": int(beds),
            "occupied_beds": int(patients),
            "admissions": int(admissions),
            "emergency_admissions": int(emergency),
            "discharges": int(discharges),
            "private_rooms": int(private_rooms),
            "occupied_private_rooms": int(occupied_rooms),
            "room_fee": int(room_fee),
            "charge_days": int(charge_days),
        }

        supabase.table("daily_hospital_stats").upsert(
            data, on_conflict="record_date"
        ).execute()

        st.success("記録を保存しました。")
    except Exception:
        st.error(
            "保存できませんでした。接続設定、テーブル、"
            "アクセス権限を確認してください。"
        )

# ===== 過去の記録 =====
st.divider()
st.header("過去の記録")

if st.button("過去30件を読み込む"):
    try:
        result = (
            supabase.table("daily_hospital_stats")
            .select("*")
            .order("record_date", desc=True)
            .limit(30)
            .execute()
        )
        if result.data:
            st.dataframe(
                result.data, use_container_width=True
            )
        else:
            st.info("まだ保存された記録はありません。")
    except Exception:
        st.error(
            "記録を読み込めませんでした。"
            "アクセス権限を確認してください。"
        )

st.caption(
    "試作版：テストデータ専用。"
    "実際の患者情報は入力しないでください。"
)
