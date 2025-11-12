import os
import shutil

import streamlit as st
from googledriver import download_folder
from pathlib import Path



st.logo(
    image="logo_images/BattleBotsLogo.png",size="large")
st.title("Video Showcase")
st.header("A collection of videos demonstrating battlebots in action")
st.subheader("Battlebots in Action")


def get_videos():
    shutil.rmtree("videos")
    os.mkdir("videos")
    url="https://drive.google.com/drive/folders/19TbxZzjPXCdcKN0xqeAwcpheUwLP9ghg?usp=drive_link"
    download_folder(url,save_path="videos")


def clean_folders():
    root=Path(__file__).resolve().parent.parent
    video_path=root.joinpath("videos")
    if len(list(video_path.iterdir()))>0:
        for folder in video_path.iterdir():
            if folder.is_dir():
                for num,file in enumerate(folder.iterdir()):
                    if file.suffix==".jpg" or file.suffix==".HEIC" or file.suffix==".JPG":
                        print("HIT")
                        file.unlink()
                for num, file_2 in enumerate(folder.iterdir()):
                        new_path=video_path /folder/ f"movie_{num+1}{file_2.suffix}"
                        print("new_path:",new_path)
                        file_2.rename(new_path)

        return "Success"
    else:
        return "Empty folder"


video_choice=st.selectbox("Select a video to watch", options=["","Kilobots 57"])

get_latest_video_button=st.button("Get latest video")
if get_latest_video_button:
    with st.spinner("Getting latest video",show_time=True):
        get_videos()

    message=clean_folders()
    if message=='Empty folder':
        st.warning("Empty folder")
    if message=="Success":
        st.success("Success")






if video_choice=="Kilobots 57":
    st.write(
        """
        Here are some of our current robots that participated in Kilobots 57:
        - **Ice licker**: an Antweight custom 1LB Vert robot.
        - **Patrix**: A custom 3LB Horizontal spinner robot. 
        - **Fedykin**: 

        """)

    with st.expander("Kilobots video showcase",expanded=True):
        st.video("https://www.youtube.com/watch?v=NKSgKOJAA-k",loop=True)

    with st.expander("Sonic vs. Ice Licker [Antweight Rookies] - Kilobots 57",expanded=True):
        st.video("https://www.youtube.com/watch?v=I12RkV1gQY4")

    with st.expander("Sans Peur vs. Coyfish IV [Antweight Rookies] - Kilobots 57",expanded=True):
        st.video("https://www.youtube.com/watch?v=XAEOURtccmY&list=PLlgiP7VyG_iApBsKy3jeU7_2itf4vvcK3&index=25")

    with st.expander("Ice Licker vs. Mr. Cardboard [Antweight Rookies] - Kilobots 57",expanded=True):
        st.video("https://www.youtube.com/watch?v=4GALpdL2Mgo&list=PLlgiP7VyG_iApBsKy3jeU7_2itf4vvcK3&index=30")

