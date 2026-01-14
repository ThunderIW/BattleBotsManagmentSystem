import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "BotsImages")

st.set_page_config(page_title="Bots Description", layout="centered")
st.title("Our Bots")

# ----------------------------
# bots into accessible array
# ----------------------------
robots = [
    {"name": "Ice Holder", "image": "IceHolderIm.png", "page": "pages/IceHolderDes.py"},
    {"name": "Bullet Ant", "image": "BulletAnt_Im.jpg", "page": "pages/BulletAntDes.py"},
    {"name": "Chrell", "image": "Chrell_Im.jpg", "page": "pages/ChrellDes.py"},
    {"name": "Fruit Ninja", "image": "FruitNinjaIm.png", "page": "pages/FruitNinjaDes.py"},
    {"name": "Ice Licker", "image": "IceLicker_Im.png", "page": "pages/IceLickerDes.py"},
    {"name": "Ice Licker 2", "image": "IceLicker_Im.png", "page": "pages/IceLicker2Des.py"},
    {"name": "Patrik", "image": "Patrik_Im.jpg", "page": "pages/PatrikDes.py"},
    {"name": "Visible Chaos", "image": "VisableChaos_Im.png", "page": "pages/VisibleChaosDes.py"},
]


# ----------------------------
# display robots + buttons
# ----------------------------
for robot in robots:
    st.header(robot["name"])

    image_path = os.path.join(IMAGES_DIR, robot["image"])
    st.image(image_path)

    if st.button("See More", key=f"btn_{robot['name']}"):
        st.switch_page(robot["page"])
