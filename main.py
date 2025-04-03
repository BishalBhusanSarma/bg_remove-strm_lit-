import streamlit as st
from rembg import remove
from PIL import Image
import io

st.title("🖼️ Background Remover")

# Upload Image
uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

# Color Picker for Background
bg_color = st.color_picker("Pick a Background Color", "#ffffff")

# Remove BG Button
remove_bg = st.button("Remove Background")

if uploaded_file and remove_bg:
    # Open Image
    image = Image.open(uploaded_file).convert("RGBA")
    
    # Remove Background
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    output_bytes = remove(img_bytes.read())
    output_img = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
    
    # Create New Background
    width, height = output_img.size
    new_bg = Image.new("RGBA", (width, height), bg_color + "ff")
    new_bg.paste(output_img, (0, 0), mask=output_img.split()[3])
    
    # Display Images Side by Side
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Original Image", use_container_width=True)
    with col2:
        st.image(new_bg, caption="Background Removed", use_container_width=True)
    
    # Download Processed Image
    img_bytes = io.BytesIO()
    new_bg.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    st.download_button("Download Image", img_bytes, file_name="processed_image.png", mime="image/png")
