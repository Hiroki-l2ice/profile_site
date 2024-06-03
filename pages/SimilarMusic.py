import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import romkan


st.sidebar.page_link("app.py", label="プロフィール")
st.sidebar.write('# 制作物一覧')
st.sidebar.page_link("pages/una.py", label="ペット健康管理アプリ \"una\"")
st.sidebar.page_link("pages/StockPrice.py", label="株価可視化アプリ")
st.sidebar.page_link("pages/ObjectDetection.py", label="物体検出アプリ")
st.sidebar.page_link("pages/SimilarMusic.py", label="類義曲検索アプリ")


# Spotify APIの認証情報を設定する関数
def load_credentials():
    client_id = st.secrets["spotify"]["client_id"]
    client_secret = st.secrets["spotify"]["client_secret"]
    return client_id, client_secret

# 類似楽曲を取得する関数
def get_similar_tracks(artist_name):
    client_id, client_secret = load_credentials()
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # アーティスト名をローマ字に変換して検索
    romanized_name = romkan.to_roma(artist_name)
    results = sp.search(q=romanized_name, type='artist')

    # 検索結果からアーティストIDを取得
    if len(results['artists']['items']) == 0:
        return []  # アーティストが見つからない場合は空のリストを返す

    artist_id = results['artists']['items'][0]['id']
    top_tracks = sp.artist_top_tracks(artist_id)

    # トップトラックのSpotify IDを取得し、特徴を分析
    track_ids = [track['id'] for track in top_tracks['tracks']]
    if not track_ids:
        return []  # トラックIDが見つからない場合は空のリストを返す

    tracks_features = sp.audio_features(track_ids)

    # 特徴の平均値を計算
    averages = {}
    for features in tracks_features:
        for key, value in features.items():
            try:
                value = float(value)
                averages[key] = averages.get(key, 0) + value
            except (ValueError, TypeError):
                pass

    if not averages:
        return []  # 特徴が見つからない場合は空のリストを返す

    # 特徴の平均値を使って類似する楽曲を検索
    for key in averages:
        averages[key] /= len(tracks_features)

    similar_tracks = sp.recommendations(seed_artists=[artist_id],
                                        target_danceability=averages.get('danceability'),
                                        target_energy=averages.get('energy'),
                                        target_loudness=averages.get('loudness'),
                                        target_speechiness=averages.get('speechiness'),
                                        target_acousticness=averages.get('acousticness'),
                                        target_instrumentalness=averages.get('instrumentalness'),
                                        target_liveness=averages.get('liveness'),
                                        target_valence=averages.get('valence'),
                                        target_tempo=averages.get('tempo'))

    # 検索結果からトラック情報を取得して返却
    return [{
        'name': track['name'],
        'url': track['external_urls']['spotify'],
        'artist': track['artists'][0]['name'],
        'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
    } for track in similar_tracks['tracks']]

# StreamlitアプリのUI
st.header('アーティストの特徴に類似する楽曲を検索', divider='grey')
artist_name = st.text_input('アーティスト名を入力してください')

if st.button('検索'):
    if artist_name:
        with st.spinner('検索中...'):
            similar_tracks = get_similar_tracks(artist_name)
            if similar_tracks:
                st.success('類似楽曲が見つかりました！')
                for i in range(0, len(similar_tracks), 2):
                    cols = st.columns(2)
                    for col, track in zip(cols, similar_tracks[i:i+2]):
                        with col:
                            st.write(f"### {track['name']}")
                            st.write(f"アーティスト: {track['artist']}")
                            st.write(f"[Spotifyで聴く]({track['url']})")
                            if track['image_url']:
                                st.image(track['image_url'], width=200)
                    if i + 2 < len(similar_tracks):
                        st.divider()
            else:
                st.error('類似楽曲が見つかりませんでした。')
    else:
        st.error('アーティスト名を入力してください。')

st.write('')
st.write('*Spotify Web APIを利用*')