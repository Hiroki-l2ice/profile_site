import streamlit as st
import pandas as pd
import numpy as np
import datetime
import altair as alt

st.set_page_config(page_title='大沢広貴 una', page_icon='🐕')

st.sidebar.page_link("app.py", label="プロフィール")
st.sidebar.write('# 制作物一覧')
st.sidebar.page_link("pages/una.py", label="ペット健康管理アプリ \"una\"")
st.sidebar.page_link("pages/StockPrice.py", label="株価可視化アプリ")
st.sidebar.page_link("pages/ObjectDetection.py", label="物体検出アプリ")
st.sidebar.page_link("pages/SimilarMusic.py", label="類義曲検索アプリ")

st.sidebar.write('')
st.sidebar.page_link('pages/una.py', label='**アルバム一覧に戻る**')

if 'demo_album' not in st.session_state:
    st.session_state.demo_album = 'unagi'

if st.session_state.demo_album == 'unagi':
    st.sidebar.page_link('pages/una_album.py', label='うなぎのアルバムに戻る')
elif st.session_state.demo_album == 'kuu':
    st.sidebar.page_link('pages/una_album.py', label='くうちゃんのアルバムに戻る')
else:
    album_name = st.session_state.album_name
    st.sidebar.page_link('pages/una_album.py', label=f'{album_name}のアルバムに戻る')

if st.session_state.demo_album == 'unagi':
    st.header('うなぎ の今までの記録')
elif st.session_state.demo_album == 'kuu':
    st.header('くうちゃん の今までの記録')
else:
    st.header(f'{album_name} の今までの記録')

choice = st.selectbox('表示する項目を選択', ['体重', '体温'])

end_date = pd.Timestamp(datetime.date.today())
start_date = end_date - pd.DateOffset(months=12)

dates = pd.date_range(start=start_date, end=end_date, freq='D')

weights = []

if st.session_state.demo_album == 'unagi':
    for date in dates:
        days_diff = (end_date - date).days
        if days_diff <= 90: 
            weight = round(np.random.normal(41, 0.4), 1)
        elif 90 < days_diff <= 180:
            weight = round(np.random.normal(40, 0.4), 1)
        elif 180 < days_diff <= 270:
            weight = round(np.random.normal(39, 0.4), 1)
        else:
            weight = round(np.random.normal(38, 0.4), 1)
        weights.append(weight)
elif st.session_state.demo_album == 'kuu':
    for date in dates:
        days_diff = (end_date - date).days
        if days_diff <= 90: 
            weight = round(np.random.normal(36, 0.4), 1)
        elif 90 < days_diff <= 180:
            weight = round(np.random.normal(35, 0.4), 1)
        elif 180 < days_diff <= 270:
            weight = round(np.random.normal(34, 0.4), 1)
        else:
            weight = round(np.random.normal(33, 0.4), 1)
        weights.append(weight)
else:
    #エラー回避用デモデータ
    for date in dates:
        days_diff = (end_date - date).days
        if days_diff <= 90: 
            weight = round(np.random.normal(41, 0.4), 1)
        elif 90 < days_diff <= 180:
            weight = round(np.random.normal(40, 0.4), 1)
        elif 180 < days_diff <= 270:
            weight = round(np.random.normal(39, 0.4), 1)
        else:
            weight = round(np.random.normal(38, 0.4), 1)
        weights.append(weight)


df = pd.DataFrame({'Date': dates, 'Weight': weights})
df.set_index('Date', inplace=True)

months = [f"{i}ヶ月" for i in range(1, 13)]
selected_month_label = st.selectbox("表示期間を選択", months, index=5)
selected_months = int(selected_month_label.replace("ヶ月", ""))

start_date_selected = end_date - pd.DateOffset(months=selected_months)

filtered_df = df.loc[start_date_selected:end_date]


if choice == '体重' and st.session_state.demo_album != 'other':
    y_min, y_max = st.slider(
        "表示範囲を選択（グラム）",
        min_value=0,
        max_value=100,
        value=(20, 60)
    )

    chart = alt.Chart(filtered_df.reset_index()).mark_line().encode(
        x='Date:T',
        y=alt.Y('Weight:Q', scale=alt.Scale(domain=(y_min, y_max)))
    ).properties(
        width=800,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.write('記録がありません')