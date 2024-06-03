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

if 'demo_album' not in st.session_state:
    st.session_state.demo_album = 'unagi'

if st.session_state.demo_album == 'unagi':
    st.sidebar.page_link('pages/una_album.py', label='うなぎのアルバムに戻る')
elif st.session_state.demo_album == 'kuu':
    st.sidebar.page_link('pages/una_album.py', label='くうちゃんのアルバムに戻る')
else:
    album_name = st.session_state.album_name
    st.sidebar.page_link('pages/una_album.py', label=f'{album_name}のアルバムに戻る')


st.header('カレンダー')
date = st.date_input('日付を指定', disabled=True)
st.caption('日付を指定して過去の記録を閲覧できます（デモサイトでは使えません）')
st.header(f'{date}の記録')
if st.session_state.demo_album == 'unagi':
    if 'contents_unagi' not in st.session_state:
        contents_unagi = {'vitality': 5, 'condition': '軽度異常あり', 'weight': 41.2, 'text': '今日はうなぎの健康のためにレタスをあげた。ちょっと太ってきたように見えるから餌の量に気をつけよう！うんちがちょっと下痢気味で少し心配...'}
        st.session_state.contents_unagi = contents_unagi
    
    col1, col_not, col2 = st.columns((6, 1, 7))
    with col1:
            if 'diary_image' not in st.session_state:
                st.session_state.diary_image = Image.open('images/hamster_album.jpg')
            st.write('')
            st.image(st.session_state.diary_image , use_column_width=True)
    with col2:
        st.write('---')
        if st.session_state.contents_unagi["vitality"] in [1, 2]:
            st.write(f'### 元気度: :orange[{st.session_state.contents_unagi["vitality"]}]')
        else:
            st.write(f'### 元気度: :green[{st.session_state.contents_unagi["vitality"]}]')

        if st.session_state.contents_unagi["condition"] is '問題なし':
            st.write(f'### 体調: :green[{st.session_state.contents_unagi["condition"]}]')
        else:
            st.write(f'### 体調: :orange[{st.session_state.contents_unagi["condition"]}]')
        
        st.write(f'### 体重: {st.session_state.contents_unagi["weight"]} g')
    st.write('')
    st.write(st.session_state.contents_unagi['text'])
    
    st.write('')
    if st.button('内容を編集'):
        st.switch_page('pages/una_edit.py')

elif st.session_state.demo_album == 'kuu':
    if 'contents_kuu' not in st.session_state:
        contents_kuu = {'condition': '問題なし', 'weight': 35.7, 'text': 'いつも通り体調は問題なさそうだったけど、なぜかいつもより元気がなかった。餌の食いつきも悪くないし一旦様子見かな。'}
        st.session_state.contents_kuu = contents_kuu
    
    col1, col_not, col2 = st.columns((6, 1, 7))
    with col1:
            if 'diary_parakeet' not in st.session_state:
                st.session_state.diary_parakeet = Image.open('images/parakeet_album.jpg')
            st.write('')
            st.image(st.session_state.diary_parakeet , use_column_width=True)
    with col2:
        st.write('---')

        if st.session_state.contents_kuu["condition"] == '問題なし':
            st.write(f'### 体調: :green[{st.session_state.contents_kuu["condition"]}]')
        else:
            st.write(f'### 体調: :orange[{st.session_state.contents_kuu["condition"]}]')
        
        st.write(f'### 体重: {st.session_state.contents_kuu["weight"]} g')
    st.write('')
    st.write(st.session_state.contents_kuu['text'])
    
    st.write('')
    if st.button('内容を編集'):
        st.switch_page('pages/una_edit.py')

else:
    st.write('')
    st.write('記録がありません')