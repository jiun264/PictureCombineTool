import streamlit as st
from PIL import Image
import io

st.title("Image Merger Tool")

# Upload multiple images
uploaded_files = st.file_uploader("Select images", type=['jpg', 'jpeg', 'png', 'gif', 'bmp'], accept_multiple_files=True)

# Choose merge direction
merge_direction = st.radio("Merge direction", ("Vertical", "Horizontal"))

def merge_images(images, direction):
    if direction == "Vertical":
        # Vertical merge (top to bottom)
        widths, heights = zip(*(i.size for i in images))
        max_width = max(widths)
        total_height = sum(heights)

        new_img = Image.new('RGB', (max_width, total_height))

        y_offset = 0
        for img in images:
            new_img.paste(img, (0, y_offset))
            y_offset += img.size[1]

    else:
        # Horizontal merge (left to right)
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
        st.error(f"Failed to open image: {e}")

    if len(images) < 2:
        st.warning("You need at least two images to merge.")
    else:
        if st.button("Merge Images"):
            merged_image = merge_images(images, merge_direction)
            st.image(merged_image, caption="Merged Image", use_column_width=True)

            # Allow user to download the merged image
            buf = io.BytesIO()
            merged_image.save(buf, format="JPEG")
            byte_im = buf.getvalue()
            st.download_button(
                label="Download Merged Image",
                data=byte_im,
                file_name="merged_image.jpg",
                mime="image/jpeg"
            )
