import streamlit as st
import yt_dlp
import tempfile
import os

st.title("JW Player HD Downloader")

url = st.text_input("Enter JW Player Video URL")

if st.button("Fetch Available Qualities") and url:
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            quality_map = {f"{f['format_id']} - {f.get('height', 'NA')}p": f['format_id']
                           for f in formats if f.get("height")}
            st.session_state['qualities'] = quality_map
            st.success("Qualities loaded.")
    except Exception as e:
        st.error(f"Failed to fetch qualities: {e}")

if 'qualities' in st.session_state:
    quality = st.selectbox("Choose Quality", list(st.session_state['qualities'].keys()))
    if st.button("Download"):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                format_id = st.session_state['qualities'][quality]
                options = {
                    'format': format_id,
                    'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s')
                }
                with yt_dlp.YoutubeDL(options) as ydl:
                    ydl.download([url])
                st.success("Download complete.")
        except Exception as e:
            st.error(f"Download failed: {e}")
