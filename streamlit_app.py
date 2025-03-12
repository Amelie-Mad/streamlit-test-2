import streamlit as st
import cv2
import numpy as np
from PIL import Image

def analyze_home_image(image):
    # Convert image to grayscale for basic analysis
    # I am adding this random comment, does the branch thing work?
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    
    # Basic estimation: count edges to approximate complexity
    complexity = np.sum(edges > 0)
    estimated_size = min(max(complexity // 50000, 5000), 60000)  # Rough BTU estimation
    
    return estimated_size

def calculate_heat_pump(size, insulation, climate):
    base_btu = size * 20  # Base BTU estimate per sq. ft.
    
    # Adjust for insulation
    if insulation == 'Poor':
        base_btu *= 1.3
    elif insulation == 'Good':
        base_btu *= 0.9
    
    # Adjust for climate
    if climate == 'Cold':
        base_btu *= 1.2
    elif climate == 'Hot':
        base_btu *= 1.1
    
    return round(base_btu, -2)

st.title("🏡 Heat Pump Size Recommender")
st.write("Upload a picture of your home, and we'll estimate the ideal heat pump size!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Home Image', use_column_width=True)
    
    estimated_size = analyze_home_image(image)
    
    st.write("### Additional Details")
    user_size = st.number_input("Estimated home size (sq. ft.)", min_value=500, max_value=10000, value=estimated_size)
    insulation = st.selectbox("Insulation quality", ["Poor", "Average", "Good"])
    climate = st.selectbox("Climate zone", ["Cold", "Temperate", "Hot"])
    
    if st.button("Calculate Heat Pump Size"):
        recommended_btu = calculate_heat_pump(user_size, insulation, climate)
        st.success(f"✅ Recommended Heat Pump Size: {recommended_btu} BTU")
