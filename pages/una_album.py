import streamlit as st
from PIL import Image

st.sidebar.page_link("app.py", label="プロフィール")
st.sidebar.write('# 制作物一覧')
st.sidebar.page_link("pages/una.py", label="ペット健康管理アプリ \"una\"")
st.sidebar.page_link("pages/StockPrice.py", label="株価可視化アプリ")
st.sidebar.page_link("pages/ObjectDetection.py", label="物体検出アプリ")
st.sidebar.page_link("pages/SimilarMusic.py", label="類義曲検索アプリ")

st.sidebar.write('')
st.sidebar.page_link('pages/una.py', label='**アルバム一覧に戻る**')

@st.experimental_dialog("このアルバムを削除しますか？")
def delite_album():
    st.write('''
             :red[削除したアルバムは元に戻せません。  
             本当によろしいですか？]
             ''')
    choice = st.radio('選択してください', ['いいえ', 'はい'])
    if st.button('決定'):
        if choice == 'はい':
            st.session_state.album_name = None
            st.switch_page('pages/una.py')
        else:
            st.rerun()


if 'album_name' not in st.session_state:
    st.session_state.album_name = None
if 'cropped_img' not in st.session_state:
    st.session_state.cropped_img = None
if 'demo_album' not in st.session_state:
    st.session_state.demo_album = 'unagi'

if st.session_state.demo_album == 'unagi':
    st.header('うなぎ のアルバム')
    st.write('')
    col1, space, col2 = st.columns((10, 2, 9))
    with col1:
        st.image(Image.open('images/hamster.jpg'))
        st.write('''
                   私が飼っていたハムスターの"うなぎ"です。  
                   このアプリを制作するきっかけになってくれました。
                   ''')
    with col2:
        if st.button(':lower_left_crayon: 今日の記録', type="primary"):
            st.switch_page('pages/una_diary.py')
        if st.button(':spiral_calendar_pad: カレンダー', type="primary"):
            st.switch_page('pages/una_calendar.py')
        if st.button(':memo: 記録を編集', type="primary"):
            st.switch_page('pages/una_edit.py')
        if st.button(':chart_with_upwards_trend: 今までの記録', type="primary"):
            st.switch_page('pages/una_data.py')
        st.write('---')
        st.button(':red[アルバムを削除]', disabled=True)
        st.caption('デモアルバムは削除できません')
elif st.session_state.demo_album == 'kuu':
    st.header('くうちゃん のアルバム')
    st.write('')
    col1, space, col2 = st.columns((10, 2, 9))
    with col1:
        st.image(Image.open('images/parakeet.jpg'))
        st.write('''
                   私が飼っていたセキセイインコの"くうちゃん"です。  
                   ''')
    with col2:
        if st.button(':lower_left_crayon: 今日の記録', type="primary"):
            st.switch_page('pages/una_diary.py')
        if st.button(':spiral_calendar_pad: カレンダー', type="primary"):
            st.switch_page('pages/una_calendar.py')
        if st.button(':memo: 記録を編集', type="primary"):
            st.switch_page('pages/una_edit.py')
        if st.button(':chart_with_upwards_trend: 今までの記録', type="primary"):
            st.switch_page('pages/una_data.py')
        st.write('---')
        st.button(':red[アルバムを削除]', disabled=True)
        st.caption('デモアルバムは削除できません')
else:
    st.header(f'{st.session_state.album_name} のアルバム')
    st.write('')
    col1, space, col2 = st.columns((10, 2, 9))
    with col1:
        st.session_state.cropped_img
    with col2:
        if st.button(':lower_left_crayon: 今日の記録', type="primary"):
            st.switch_page('pages/una_diary.py')
        if st.button(':spiral_calendar_pad: カレンダー', type="primary"):
            st.switch_page('pages/una_calendar.py')
        if st.button(':memo: 記録を編集', type="primary"):
            st.switch_page('pages/una_edit.py')
        if st.button(':chart_with_upwards_trend: 今までの記録', type="primary"):
            st.switch_page('pages/una_data.py')
        st.write('---')
        if st.button(':red[アルバムを削除]'):
            delite_album()