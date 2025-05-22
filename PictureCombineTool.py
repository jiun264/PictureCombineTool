import streamlit as st
from PIL import Image
import io

st.title("圖片合併工具")

# 上傳多張圖片
uploaded_files = st.file_uploader("選擇圖片", type=['jpg', 'jpeg', 'png', 'gif', 'bmp'], accept_multiple_files=True)

# 選擇合併方向
merge_direction = st.radio("合併方向", ("上下合併", "左右合併"))

def merge_images(images, direction):
    if direction == "上下合併":
        # 垂直合併 (上下)
        widths, heights = zip(*(i.size for i in images))
        max_width = max(widths)
        total_height = sum(heights)

        new_img = Image.new('RGB', (max_width, total_height))

        y_offset = 0
        for img in images:
            new_img.paste(img, (0, y_offset))
            y_offset += img.size[1]

    else:
        # 水平合併 (左右)
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)

        new_img = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for img in images:
            new_img.paste(img, (x_offset, 0))
            x_offset += img.size[0]

    return new_img

if uploaded_files:
    images = []
    try:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            images.append(image)
    except Exception as e:
        st.error(f"無法開啟圖片: {e}")

    if len(images) < 2:
        st.warning("需要至少兩張圖片才能合併。")
    else:
        if st.button("合併圖片"):
            merged_image = merge_images(images, merge_direction)
            st.image(merged_image, caption="合併後的圖片", use_column_width=True)

            # 讓使用者下載合併後的圖片
            buf = io.BytesIO()
            merged_image.save(buf, format="JPEG")
            byte_im = buf.getvalue()
            st.download_button(
                label="下載合併後的圖片",
                data=byte_im,
                file_name="merged_image.jpg",
                mime="image/jpeg"
            )
