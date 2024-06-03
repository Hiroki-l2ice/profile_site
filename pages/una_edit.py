import streamlit as st
from PIL import Image

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

if 'demo_album' not in st.session_state:
    st.session_state.demo_album = 'unagi'

st.header('記録を編集')
date = st.date_input('日付を指定', disabled=True)
st.caption('日付を指定して過去の記録を閲覧できます（デモサイトでは使えません）')
st.header(f'{date}の記録')

if st.session_state.demo_album != 'other':
    uploaded_file = st.file_uploader("**画像を変更する場合はアップロードしてください**", type=["jpg", "jpeg", "png"])

condition_list = ['問題なし', '軽度異常あり', '異常あり', '病気がち']
col1, col2 = st.columns((2, 3))
if st.session_state.demo_album == 'unagi':
    with col1:
        if uploaded_file is not None:
            st.session_state.diary_image = Image.open(uploaded_file)
            st.image(st.session_state.diary_image , use_column_width=True)
        else:
            if st.session_state.demo_album == 'unagi':
                st.image(Image.open('images/hamster_album.jpg'))
    with col2:
        if st.session_state.demo_album == 'unagi':
            if 'contents_unagi' not in st.session_state:
                contents_unagi = {'vitality': 5, 'condition': '軽度異常あり', 'weight': 41.2, 'text': '今日はうなぎの健康のためにレタスをあげた。ちょっと太ってきたように見えるから餌の量に気をつけよう！うんちがちょっと下痢気味で少し心配...'}
                st.session_state.contents_unagi = contents_unagi
            st.session_state.contents_unagi['vitality'] = st.slider('元気度', 1, 5, st.session_state.contents_unagi['vitality'])
            st.session_state.contents_unagi['condition'] = st.selectbox('体調', ['問題なし', '軽度異常あり', '異常あり', '病気がち'], index=condition_list.index(st.session_state.contents_unagi['condition']))
            st.session_state.contents_unagi['weight'] = st.number_input('体重(グラム)' , value=st.session_state.contents_unagi['weight'])
    st.write('')
    st.session_state.contents_unagi['text'] = st.text_area('今日の思い出を書きましょう！', st.session_state.contents_unagi['text'])
    if st.button('確定'):
        st.switch_page('pages/una_calendar.py')
elif st.session_state.demo_album == 'kuu':
    with col1:
        if uploaded_file is not None:
            st.session_state.diary_image = Image.open(uploaded_file)
            st.image(st.session_state.diary_image , use_column_width=True)
        else:
            if st.session_state.demo_album == 'kuu':
                st.image(Image.open('images/parakeet_album.jpg'))
    with col2:
        if st.session_state.demo_album == 'kuu':
            if 'contents_kuu' not in st.session_state:
                contents_kuu = {'condition': '問題なし', 'weight': 35.7, 'text': 'いつも通り体調は問題なさそうだったけど、なぜかいつもより元気がなかった。餌の食いつきも悪くないし一旦様子見かな。'}
                st.session_state.contents_kuu = contents_kuu
            st.session_state.contents_kuu['condition'] = st.selectbox('体調', ['問題なし', '軽度異常あり', '異常あり', '病気がち'], index=condition_list.index(st.session_state.contents_kuu['condition']))
            st.session_state.contents_kuu['weight'] = st.number_input('体重(グラム)' , value=st.session_state.contents_kuu['weight'])
    st.write('')
    st.session_state.contents_kuu['text'] = st.text_area('今日の思い出を書きましょう！', st.session_state.contents_kuu['text'])
    if st.button('確定'):
        st.switch_page('pages/una_calendar.py')

else:
    st.write('記録がありません')