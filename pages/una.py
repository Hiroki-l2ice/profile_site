import streamlit as st
from PIL import Image

st.set_page_config(page_title='大沢広貴 una', page_icon='🐕')

st.sidebar.page_link("app.py", label="プロフィール")
st.sidebar.write('# 制作物一覧')
st.sidebar.page_link("pages/una.py", label="ペット健康管理アプリ \"una\"")
st.sidebar.page_link("pages/StockPrice.py", label="株価可視化アプリ")
st.sidebar.page_link("pages/ObjectDetection.py", label="物体検出アプリ")
st.sidebar.page_link("pages/SimilarMusic.py", label="類義曲検索アプリ")

st.header('ペット健康管理アプリ "una"', divider='grey')

st.header('アルバム一覧')

if 'cropped_img' not in st.session_state:
    st.session_state.cropped_img = None
if 'album_name' not in st.session_state:
    st.session_state.album_name = None

col1, col2 = st.columns((1, 1))
col3, col4 = st.columns((1, 1))
with col1:
        st.write('---')
        col_img, col_name = st.columns((1, 1))
        with col_img:
            st.image(Image.open('images/hamster.png'))
        with col_name:
            st.write('')
            st.write('うなぎ のアルバム')
            if st.button('アルバムを開く', key='unagi'):
                st.session_state.demo_album = 'unagi'
                st.switch_page('pages/una_album.py')

with col2:
        st.write('---')
        col_img, col_name = st.columns((1, 1))
        with col_img:
            st.image(Image.open('images/parakeet.png'))
        with col_name:
            st.write('')
            st.write('くうちゃん のアルバム')
            if st.button('アルバムを開く', key='kuu'):
                st.session_state.demo_album = 'kuu'
                st.switch_page('pages/una_album.py')

if st.session_state.album_name is not None:
    with col3:
        st.write('---')
        col_img2, col_name2 = st.columns((1, 1))
    with col_img2:
        st.session_state.circular_img
    with col_name2:
        st.write('')
        st.write(st.session_state.album_name, ' のアルバム')
        if st.button('アルバムを開く', key=st.session_state.album_name):
            st.session_state.demo_album = 'other'
            st.switch_page('pages/una_album.py')

st.write('---')
if st.button(':closed_book: 新規アルバムを作成'):
    st.switch_page('pages/una_new_album.py')