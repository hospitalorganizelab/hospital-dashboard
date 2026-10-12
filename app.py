
import streamlit as st

st.title("病院経営管理アプリ")

st.header("病床管理")

beds = st.number_input(
    "稼働可能病床数", min_value=1, value=40
)
patients = st.number_input(
    "在院患者数", min_value=0, value=34
)
admissions = st.number_input(
    "本日の入院数", min_value=0, value=5
)
emergency = st.number_input(
    "緊急入院数", min_value=0, value=3
)
discharges = st.number_input(
    "本日の退院数", min_value=0, value=4
)

occupancy = patients / beds * 100

col1, col2 = st.columns(2)
col1.metric("病床稼働率", f"{occupancy:.1f}%")
col2.metric("空床数", max(0, beds - patients))

col3, col4, col5 = st.columns(3)
col3.metric("緊急入院", emergency)
col4.metric("本日の退院", discharges)
col5.metric("入退院差引", admissions - discharges)

st.divider()
st.header("個室管理・収益")

private_rooms = st.number_input(
    "個室総数", min_value=0, value=8
)
occupied_rooms = st.number_input(
    "使用中の個室数",
    min_value=0,
    max_value=int(private_rooms),
    value=min(6, int(private_rooms))
)
room_fee = st.number_input(
    "個室料（1室・1日あたり／円）",
    min_value=0,
    value=6000,
    step=500
)
charge_days = st.number_input(
    "料金発生日数", min_value=0, value=1
)

room_occupancy = (
    occupied_rooms / private_rooms * 100
    if private_rooms > 0 else 0
)
vacant_rooms = private_rooms - occupied_rooms
daily_revenue = occupied_rooms * room_fee
period_revenue = daily_revenue * charge_days

col1, col2 = st.columns(2)
col1.metric("個室稼働率", f"{room_occupancy:.1f}%")
col2.metric("個室空室数", int(vacant_rooms))

col3, col4 = st.columns(2)
col3.metric("1日あたりの個室料収益",
            f"{daily_revenue:,.0f}円")
col4.metric("期間内の個室料収益",
            f"{period_revenue:,.0f}円")

st.caption(
    "試作版：入力値に基づく概算です。"
    "実際の請求額や会計上の収益とは一致しない場合があります。"
)
