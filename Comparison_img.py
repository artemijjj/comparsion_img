# For start this app, run on terminal:
# streamlit run E:\proj\Comparison_image\Comparison_img.py --server.port 4180


from PIL import Image, ImageChops
import numpy as np
import streamlit as st
import os


def comparison_img(before, after):
    compar = ImageChops.difference(before.convert('RGB'), after.convert('RGB'))
    compare = ImageChops.invert(compar)
    pix_map = compare.load()
    for i in range(compare.size[0]):
        for j in range(compare.size[1]):
            if pix_map[i, j] != (255, 255, 255):
                pix_map[i, j] = (255, 0, 0)
    mask = ImageChops.invert(compare.convert('L'))
    background = before.convert('1').convert('RGB')
    background.paste(compare, (0,0), mask=mask)
    st.title('Разница изображений')
    st.image(compare, use_column_width=True)
    st.title('Результат наложения изображений')
    st.image(background, use_column_width=True)


# Upload image and convert to opencv
def uploaded_file(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)

    return image


# This main body streamlit app
# Open u logo:
logo = Image.open("LOGO.png")
logo = logo.resize((600, 300))

st.sidebar.image(logo)
st.sidebar.title('Сравнение изображений')
# Load u image
uploaded_file_one = st.sidebar.file_uploader("Выберите первое изображение", type=["jpg","png","JPEG"])
uploaded_file_two = st.sidebar.file_uploader("Выберите второе изображение", type=["jpg","png","JPEG"])

if uploaded_file_one:
    st.title('Первое изображение')
    before = uploaded_file(uploaded_file_one)

if uploaded_file_two:
    st.title('Второе изображение')
    after = uploaded_file(uploaded_file_two)

    if before and after:
        comp_img = comparison_img(after, before)

# Create thread for modification image
# Due to the fact that it is a server and performs constant reading (loop),
# this design excludes the creation of a thread before the images are loaded
# (there may be a more elegant solution, but I don’t know it yet)
# try:
#     thread = ThreadWithReturnValue(target=comparison_img, args=(before, after))
#     add_report_ctx(thread)
#     thread.start()
#     thread.join()
# except:
#     pass
