import streamlit as st


st.sidebar.page_link("app.py", label="プロフィール")
st.sidebar.write('# 制作物一覧')
st.sidebar.page_link("pages/una.py", label="ペット健康管理アプリ \"una\"")
st.sidebar.page_link("pages/ObjectDetection.py", label="物体検出アプリ")
st.sidebar.page_link("pages/StockPrice.py", label="株価可視化アプリ")
st.sidebar.write('○○○アプリ')
st.sidebar.write('○○○アプリ')
st.sidebar.write('○○○アプリ')

st.header('プロフィール', divider='grey')

col1, col2 = st.columns((4, 7))
with col1:
    st.image('images/shoumeishashin.jpg')
with col2:
    st.write("""
    ### 大沢 広貴（Hiroki Osawa）
    """)
    st.write('')
    st.page_link('https://www.dhw.ac.jp/', label='**デジタルハリウッド大学**')
    st.write('''
    デジタルコミュニケーション学部  
    デジタルコンテンツ学科
    ''')

with open("resume.pdf", "rb") as f:
    pdf_content = f.read()
st.download_button(
    label="履歴書をダウンロード（PDFファイル）",
    data=pdf_content,
    file_name='大沢広貴.pdf',
    mime="application/pdf"
)

st.write('e-mail: osawa.digital@gmail.com')

st.write('>**技術**')
st.write('**Python, Java, JavaScript, HTML, CSS, SQL**')

st.write(yf.__version__)
