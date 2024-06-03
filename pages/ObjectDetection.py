from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

import json
import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont


st.sidebar.page_link("app.py", label="プロフィール")
st.sidebar.write('# 制作物一覧')
st.sidebar.page_link("pages/una.py", label="ペット健康管理アプリ \"una\"")
st.sidebar.page_link("pages/StockPrice.py", label="株価可視化アプリ")
st.sidebar.page_link("pages/ObjectDetection.py", label="物体検出アプリ")
st.sidebar.page_link("pages/SimilarMusic.py", label="類義曲検索アプリ")


KEY = st.secrets["KEY"]
ENDPOINT = st.secrets['ENDPOINT']

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_tags(filepath):
    with open(filepath, "rb") as local_image:
        tags_result = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result.tags
    tags_name = [tag.name for tag in tags]
    return tags_name

def detect_objects(filepath):
    with open(filepath, "rb") as local_image:
        detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results.objects
    return objects

st.header('物体検出アプリ', divider='grey')

if 'uploaded' not in st.session_state:
    st.session_state.uploaded = False
if 'use_demo_image' not in st.session_state:
    st.session_state.use_demo_image = False

uploaded_file = st.file_uploader('画像をアップロード、またはデモ画像を選択してください', type=['jpg', 'png'])

if uploaded_file is not None:
    st.session_state.uploaded = True
    st.session_state.use_demo_image = False

if uploaded_file is None and st.session_state.uploaded:
    st.session_state.uploaded = False

if not st.session_state.uploaded:
    st.session_state.use_demo_image = st.checkbox('デモ画像を使用する')

if st.session_state.uploaded and uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'temp_{uploaded_file.name}'
    img.save(img_path)
elif st.session_state.use_demo_image:
    img_path = 'images/demo.jpg'
    img = Image.open(img_path)
else:
    st.write('*Azure Vision Studioを利用*')
    st.stop()

objects = detect_objects(img_path)

draw = ImageDraw.Draw(img)
font = ImageFont.truetype(font='./Helvetica 400.ttf', size=20)

for object in objects:
    x = object.rectangle.x
    y = object.rectangle.y
    w = object.rectangle.w
    h = object.rectangle.h
    caption = object.object_property

    left, top, right, bottom = draw.textbbox((0, 0), caption, font=font)
    text_w = right - left
    text_h = bottom - top

    draw.rectangle([(x, y), (x+w, y+h)], fill=None, outline='green', width=5)
    draw.rectangle([(x, y - text_h), (x + text_w, y)], fill='green')
    draw.text((x, y - text_h), caption, fill='white', font=font)

st.image(img)

tags_name = get_tags(img_path)
tags_name = ', '.join(tags_name)
st.markdown('**認識されたコンテンツタグ**')
st.markdown(f'> {tags_name}')

if uploaded_file is not None:
    os.remove(img_path)

st.write('*Azure Vision Studioを利用*')