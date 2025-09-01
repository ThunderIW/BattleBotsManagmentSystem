import streamlit as st




st.title("Video Showcase")
st.header("A collection of videos demonstrating battlebots in action")
st.subheader("Battlebots in Action")

video_choice=st.selectbox("Select a video to watch", options=["","Kilobots 57"])

if video_choice=="Kilobots 57":
    with st.expander("Kilobots video showcase",expanded=True):
        st.video("https://www.youtube.com/watch?v=NKSgKOJAA-k",loop=True)

    with st.expander("Sonic vs. Ice Licker [Antweight Rookies] - Kilobots 57",expanded=True):
        st.video("https://www.youtube.com/watch?v=I12RkV1gQY4")

    with st.expander("Sans Peur vs. Coyfish IV [Antweight Rookies] - Kilobots 57",expanded=True):
        st.video("https://www.youtube.com/watch?v=XAEOURtccmY&list=PLlgiP7VyG_iApBsKy3jeU7_2itf4vvcK3&index=25")

    with st.expander("Ice Licker vs. Mr. Cardboard [Antweight Rookies] - Kilobots 57",expanded=True):
        st.video("https://www.youtube.com/watch?v=4GALpdL2Mgo&list=PLlgiP7VyG_iApBsKy3jeU7_2itf4vvcK3&index=30")

