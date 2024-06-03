import time
import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image, ImageDraw
import numpy as np

st.set_page_config(page_title='大沢広貴 una', page_icon='🐕')

st.sidebar.page_link("app.py", label="プロフィール")
st.sidebar.write('# 制作物一覧')
st.sidebar.page_link("pages/una.py", label="ペット健康管理アプリ \"una\"")
st.sidebar.page_link("pages/StockPrice.py", label="株価可視化アプリ")
st.sidebar.page_link("pages/ObjectDetection.py", label="物体検出アプリ")
st.sidebar.page_link("pages/SimilarMusic.py", label="類義曲検索アプリ")

st.sidebar.write('')
st.sidebar.page_link('pages/una.py', label='**アルバム一覧に戻る**')

st.write('## 新規アルバムを作成')

def cropper(uploaded_file):
    try:
        img = Image.open(uploaded_file)
        cropped_img = st_cropper(img, aspect_ratio=(1, 1), box_color='#FF6000')
        return cropped_img
    except Exception as e:
        st.error(f"画像のトリミング中にエラーが発生しました: {e}")
        return None
    
def make_circle_image(image):
    np_image = np.array(image)
    h, w = np_image.shape[:2]
    size = min(h, w)
    left = (w - size) // 2
    top = (h - size) // 2
    right = (w + size) // 2
    bottom = (h + size) // 2
    np_image = np_image[top:bottom, left:right]

    square_image = Image.fromarray(np_image).convert("RGBA")

    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    result = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    result.paste(square_image, (0, 0), mask=mask)
    return result

if 'edit' not in st.session_state:
    st.session_state.edit = True
if 'cropped_img' not in st.session_state:
    st.session_state.cropped_img = None

uploaded_file = st.file_uploader("**ペットの画像ををアップロードし、トリミングをしてください**", type=["jpg", "jpeg", "png"])
 
edit = st.empty()
    
with edit.container():
    if uploaded_file is not None:
        if st.session_state.edit:
            st.write('### 表示範囲を選択')
            cropped_img = cropper(uploaded_file)
            if st.button(":o: 決定"):
                edit.empty()
                st.session_state.edit = False
                st.session_state.cropped_img = cropped_img
    
if uploaded_file is None:
    st.session_state.edit = True
    st.session_state.cropped_img = None
    st.session_state.album_name = None

col1, col2 = st.columns((2, 3))
with col1:
    if st.session_state.cropped_img is not None:
        circular_img = make_circle_image(st.session_state.cropped_img)
        new_width = 500
        new_height = int((st.session_state.cropped_img.height / st.session_state.cropped_img.width) * new_width)
        circular_img = circular_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        st.session_state.circular_img = circular_img

        st.write('')
        st.image(st.session_state.cropped_img , use_column_width=True)
    else:
        st.write('')
        st.warning(':arrow_up: 画像が選択されていません')
        st.session_state.use_demo_album = st.checkbox('デモ画像を使用する')
        if st.session_state.use_demo_album:
            st.session_state.cropped_img = Image.open('images/hamster_demo.jpg')
            st.session_state.circular_img = Image.open('images/hamster_demo.png')
            st.image(st.session_state.cropped_img)

with col2:
    name = st.text_input('**お名前**', placeholder='必須')
    date = st.date_input('**お誕生日、またはお迎えした日**')
    st.write('')
    st.write('**記録したい項目を選択してください**')
    st.session_state.fine = st.checkbox('元気度')
    st.checkbox('体調')
    st.checkbox('体重')
    st.checkbox('体温')
    st.checkbox('今日のご飯')
    # if st.button(':heavy_plus_sign: 項目を追加'):
    #     st.switch_page('pages/.py')

st.write('')
def create_album():
    if name == '' or st.session_state.cropped_img is None:
        st.button(':closed_book: アルバムを作成', help='必要項目が入力されていません', disabled=True)
    if st.session_state.cropped_img is not None and name !='':
        if st.button(':closed_book: アルバムを作成'):
            st.caption('デモサイトの為、作成されたアルバムは保持されません')
            st.balloons()
            time.sleep(2)
            st.session_state.album_name = name
            st.switch_page('pages/una.py')

create_album()
st.caption('デモサイトの為、作成されたアルバムは保持されません')
