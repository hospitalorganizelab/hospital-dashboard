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
