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

@st.experimental_dialog("確認")
def check(contents):
    if contents == 'image':
        st.warning('（注意）画像がアップロードされていません')
        st.write('画像は毎日アップロードすることを推奨しています')
        choice = st.radio('このまま保存しますか？', ['いいえ', 'はい'])
        if st.button('決定'):
            if choice == 'はい':
                st.switch_page('pages/una_album.py')
            else:
                st.rerun()
    if contents == 'diary':
        st.warning('（注意）文章が入力されていません')
        st.write('思い出は毎日記入しましょう！')
        if st.button('了解しました'):
            st.rerun()

st.header('今日の記録')
uploaded_file = st.file_uploader("**今日の画像をアップロードしてください**", type=["jpg", "jpeg", "png"])
st.write('')

col1, col2 = st.columns((2, 3))
with col1:
    if uploaded_file is not None:
        diary_image = Image.open(uploaded_file)
        st.image(diary_image , use_column_width=True)
    else:
        st.warning(':arrow_up: 画像が選択されていません')
with col2:
    st.slider('元気度', 1, 5, 3)
    st.selectbox('体調', ['問題なし', '異常あり', '病気がち'])
    st.number_input('体重(グラム)')
st.write('')
diary = st.text_area('今日の思い出を書きましょう！')
if st.button('保存'):
    if diary == '':
        check('diary')
    elif uploaded_file == None:
        check('image')
    else:
        st.switch_page('pages/una_album.py')

st.caption('デモサイトでは内容は保存されません')