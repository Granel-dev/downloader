import streamlit as st
from pytubefix import YouTube
import os
st.write("# YouTube Video Downloader")
if "link" not in st.session_state:
    st.session_state.link = None
url = st.text_input(label="youtube link",placeholder="paste here") 
yt = st.session_state.link
def data():
    try:
        st.session_state.link = YouTube(url) 
        st.write(f"video title: {st.session_state.link.title}")
        st.write(f"views: {st.session_state.link.views}")        
        st.write(f"year posted: {st.session_state.link.publish_date}")
    except Exception:
        st.write("no data found")
       
if st.button("Submit"):
    data()
else:
    st.write("no information found")

def dl_process():
    try:
        if "selected_resolution" not in st.session_state:
            st.session_state.selected_resolution = None
        if "dl" not in st.session_state:
            st.session_state.dl = None
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        
        options = [stream.resolution for stream in streams]
        select = st.selectbox('avialable',list(dict.fromkeys(sorted(options))))
        st.session_state.selected_resolution = select
        st.session_state.dl = st.button("Download")
        if st.session_state.dl:
            st.write("downloading")
            process(yt, st.session_state.selected_resolution)
            st.write("downloaded successfully")
    except Exception:
        pass
def process(yt, resolution):
    download_directory = os.path.expanduser("~/Downloads") 
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    
    stream = yt.streams.filter(res=resolution, progressive=True, file_extension="mp4").order_by("resolution").first()
    if stream:    
        file_path = os.path.join(download_directory, f"{resolution}_video.mp4")
        stream.download(output_path=download_directory, filename=f"{resolution}_video.mp4")
        st.write("downloaded")
    else:
        st.write("failed")
dl_process()
