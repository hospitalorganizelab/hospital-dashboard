import streamlit as st
from supabase import create_client
from datetime import date

st.set_page_config(page_title="病院経営管理アプリ", layout="wide")
st.title("病院経営管理アプリ")

# Supabase接続設定
try:
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
except Exception:
    st.error("Supabaseの接続設定を確認してください。")
    st.stop()

st.header("日次記録")
record_date = st.date_input("記録日", value=date.today())

st.header("病床管理")
beds = st.number_input("稼働可能病床数", min_value=1, value=40)
patients = st.number_input(
    "在院患者数", min_value=0, max_value=int(beds), value=min(34, int(beds))
)
admissions = st.number_input("本日の入院数", min_value=0, value=5)
emergency = st.number_input(
    "緊急入院数", min_value=0, max_value=int(admissions),
    value=min(3, int(admissions))
)
discharges = st.number_input("本日の退院数", min_value=0, value=4)

occupancy = patients / beds * 100
col1, col2 = st.columns(2)
col1.metric("病床稼働率", f"{occupancy:.1f}%")
col2.metric("空床数", int(beds - patients))

col1, col2, col3 = st.columns(3)
col1.metric("緊急入院", int(emergency))
col2.metric("本日の退院", int(discharges))
col3.metric("入退院差引", int(admissions - discharges))

st.divider()
st.header("個室管理・収益")

private_rooms = st.number_input("個室総数", min_value=0, value=8)
occupied_rooms = st.number_input(
    "使用中の個室数", min_value=0,
    max_value=int(private_rooms), value=min(6, int(private_rooms))
)
room_fee = st.number_input(
    "個室料（1室・1日あたり／円）",
    min_value=0, value=6000, step=500
)
charge_days = st.number_input("料金発生日数", min_value=0, value=1)

room_occupancy = (
    occupied_rooms / private_rooms * 100 if private_rooms > 0 else 0
)
daily_revenue = occupied_rooms * room_fee
period_revenue = daily_revenue * charge_days

col1, col2 = st.columns(2)
col1.metric("個室稼働率", f"{room_occupancy:.1f}%")
col2.metric("個室空室数", int(private_rooms - occupied_rooms))

col1, col2 = st.columns(2)
col1.metric("1日あたりの個室料収益", f"{daily_revenue:,.0f}円")
col2.metric("期間内の個室料収益", f"{period_revenue:,.0f}円")

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
            "保存できませんでした。Supabaseの接続設定、"
            "テーブル、アクセス権限を確認してください。"
        )

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
            st.dataframe(result.data, use_container_width=True)
        else:
            st.info("まだ保存された記録はありません。")
    except Exception:
        st.error("記録を読み込めませんでした。アクセス権限を確認してください。")

st.caption("試作版：テストデータ専用。実際の患者情報は入力しないでください。")

# 画面下を泳ぐ青いウミガメ
st.markdown("""
<style>
.sea-turtle {
    position: fixed;
    bottom: 8px;
    left: 0;
    z-index: 999;
    pointer-events: none;
    animation: turtle-swim 24s linear infinite;
}
.sea-turtle svg {
    width: 110px;
    height: 75px;
    overflow: visible;
}
@keyframes turtle-swim {
    0%   { transform: translateX(-130px); }
    100% { transform: translateX(110vw); }
}
@media (prefers-reduced-motion: reduce) {
    .sea-turtle { animation: none; left: 10px; }
}
</style>
<div class="sea-turtle">
<svg viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg">
  <!-- ひれ -->
  <g fill="#36AFCB" stroke="#167B9B" stroke-width="2">
    <path d="M54 53 Q22 35 15 55 Q12 69 49 66 L65 61Z"/>
    <path d="M83 58 Q102 76 92 91 Q80 99 69 66Z"/>
    <path d="M109 54 Q133 42 140 58 Q143 69 111 68Z"/>
  </g>
  <!-- 頭 -->
  <path d="M111 40 Q121 20 141 27 Q158 33 150 48
           Q145 59 126 54 L110 52Z"
        fill="#B9E8E8" stroke="#167B9B" stroke-width="2"/>
  <!-- 目 -->
  <ellipse cx="141" cy="35" rx="3.5" ry="4.5" fill="#183D50"/>
  <circle cx="142" cy="34" r="1.2" fill="white"/>
  <!-- 甲羅 -->
  <path d="M38 49 Q44 22 77 22 Q104 22 119 43
           L111 59 Q79 75 48 61Z"
        fill="#159CC4" stroke="#145A7B" stroke-width="3"/>
  <!-- 甲羅の模様 -->
  <g fill="none" stroke="#C5F3F1" stroke-width="2">
    <path d="M54 29 L69 43 L62 59"/>
    <path d="M72 24 L82 43 L69 64"/>
    <path d="M89 27 L96 43 L87 65"/>
    <path d="M105 36 L108 48 L101 61"/>
    <path d="M43 45 L62 43 L82 43 L105 48"/>
  </g>
  <!-- 口 -->
  <path d="M143 48 Q148 51 151 47"
        fill="none" stroke="#167B9B" stroke-width="1.5"
        stroke-linecap="round"/>
</svg>
</div>
""", unsafe_allow_html=True)
