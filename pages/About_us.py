import streamlit as st
from PIL import Image

# Example team images (replace with your own image paths or URLs)
# You can also skip images if not needed
team_members = [
    {
        "name": "Immanuel Wiessler",
        "role": "Lead Software Developer",
        "bio": "Hi there I am Immanuel, A 4th year Computer Science student at UBCO.I am passionate about robotics and AI and love working on making personal projects in my free time. "
               "In addition I am also learning **circuitPython** and **embedded systems**. ",
        "image": "Japan_trip_image.jpg"
    },
    {
        "name": "Jane Doe",
        "role": "Technical Designer",
        "bio": "Jane creates clean and engaging designs with a focus on user experience.",
        "image": "https://via.placeholder.com/150"
    }
]

st.set_page_config(page_title="About Us", page_icon="🌐", layout="centered")


st.logo(
    image="logo_images/BattleBotsLogo.png",size="large")
st.title("🌐 About Us")
st.markdown(
    """
    We are  **UBCO Battlebots**!, a passionate team of students at the University of [British Columbia Okanagan (UBCO)](https://ok.ubc.ca/).
    dedicated to designing, building, and competing with custom robots or kit robots
    

    
    """
)

st.header("👥 Meet the Team")

cols = st.columns(len(team_members))
for i, member in enumerate(team_members):
    with cols[i]:
        st.image(member["image"])
        st.subheader(member["name"])
        st.caption(member["role"])
        st.write(member["bio"])


st.header("🤖 Battlebot showcase ")
st.write(
    """
    Here are some of our current robots:
    - **Ice licker**: SAMPLE TEXT
    - **Robot 2**: A heavy-duty robot built for power and durability.
    - **Robot 3**: A versatile robot capable of adapting to various combat scenarios.
    
    """)


st.header("📩 Contact Us")
st.write(
    """
    Ready to get involved ?  
    Email us at: **contact@example.com**
    """
)

st.markdown("---")
st.write("© 2025 Our Project. All rights reserved.")
