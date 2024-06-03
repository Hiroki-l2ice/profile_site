import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st
from datetime import datetime, timedelta


st.sidebar.page_link("app.py", label="**プロフィールに戻る**")
st.sidebar.write('# 制作物一覧')
st.sidebar.page_link("pages/una.py", label="ペット健康管理アプリ \"una\"")
st.sidebar.page_link("pages/ObjectDetection.py", label="物体検出アプリ")
st.sidebar.page_link("pages/StockPrice.py", label="株価可視化アプリ")
st.sidebar.write('○○○アプリ')
st.sidebar.write('○○○アプリ')
st.sidebar.write('○○○アプリ')

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 2, 500, 200)

st.write(f"""
### 過去 **{days}日間** のGAFA株価
""")

@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(start=start_date, end=end_date)
        hist.index = hist.index.strftime('%Y-%m-%d')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try: 
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 1000.0, (0.0, 700.0)
    )

    tickers = {
        'apple': 'AAPL',
        'meta': 'META',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN'
    }
    df = get_data(days, tickers)
    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['google', 'amazon', 'meta', 'apple']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価 (USD)", data.sort_index())
        data = data.T.reset_index().rename(columns={'index': 'Date'})
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except Exception as e:
    st.error(
        "おっと！なにかエラーが起きているようです。"
    )

st.write('*yfinence APIを利用*')
