# Maritime Color Vision Test - Ishihara Implementation
# Copyright © Toni Mandušić 2025

import streamlit as st
import pandas as pd
import requests
from PIL import Image, ImageDraw
import io
import random

# Page configuration
st.set_page_config(
    page_title="Maritime Vision Test",
    page_icon="🚢",
    layout="wide"
)

# Ishihara test data
ISHIHARA_DATA = {
    1: {"normal": "12", "deutan": "12", "protan": "12", "description": "Everyone should see 12"},
    2: {"normal": "8", "deutan": "3", "protan": "3", "description": "Normal: 8, Deficiency: 3"},
    3: {"normal": "6", "deutan": "5", "protan": "5", "description": "Normal: 6, Deficiency: 5"},
    4: {"normal": "29", "deutan": "70", "protan": "70", "description": "Normal: 29, Deficiency: 70"},
    5: {"normal": "57", "deutan": "35", "protan": "35", "description": "Normal: 57, Deficiency: 35"},
    6: {"normal": "5", "deutan": "2", "protan": "2", "description": "Normal: 5, Deficiency: 2"},
    7: {"normal": "3", "deutan": "5", "protan": "5", "description": "Normal: 3, Deficiency: 5"},
    8: {"normal": "15", "deutan": "17", "protan": "17", "description": "Normal: 15, Deficiency: 17"},
    9: {"normal": "74", "deutan": "21", "protan": "21", "description": "Normal: 74, Deficiency: 21"},
    10: {"normal": "2", "deutan": "", "protan": "", "description": "Normal: 2, Deficiency: Nothing"},
    11: {"normal": "6", "deutan": "", "protan": "", "description": "Normal: 6, Deficiency: Nothing"},
    12: {"normal": "97", "deutan": "", "protan": "", "description": "Normal: 97, Deficiency: Nothing"},
    13: {"normal": "45", "deutan": "", "protan": "", "description": "Normal: 45, Deficiency: Nothing"},
    14: {"normal": "5", "deutan": "", "protan": "", "description": "Normal: 5, Deficiency: Nothing"},
    15: {"normal": "7", "deutan": "", "protan": "", "description": "Normal: 7, Deficiency: Nothing"},
    16: {"normal": "16", "deutan": "", "protan": "", "description": "Normal: 16, Deficiency: Nothing"},
    17: {"normal": "73", "deutan": "", "protan": "", "description": "Normal: 73, Deficiency: Nothing"},
    18: {"normal": "", "deutan": "5", "protan": "5", "description": "Normal: Nothing, Deficiency: 5"},
    19: {"normal": "", "deutan": "2", "protan": "2", "description": "Normal: Nothing, Deficiency: 2"},
    20: {"normal": "", "deutan": "45", "protan": "45", "description": "Normal: Nothing, Deficiency: 45"},
    21: {"normal": "", "deutan": "73", "protan": "73", "description": "Normal: Nothing, Deficiency: 73"},
    22: {"normal": "26", "deutan": "2", "protan": "6", "description": "Normal: 26, Protan: 6, Deutan: 2"},
    23: {"normal": "42", "deutan": "4", "protan": "2", "description": "Normal: 42, Protan: 2, Deutan: 4"},
    24: {"normal": "35", "deutan": "3", "protan": "5", "description": "Normal: 35, Protan: 5, Deutan: 3"}
}

def load_wikimedia_plate(plate_number):
    """Load Ishihara plates from Wikimedia Commons"""
    wikimedia_plates = {
        1: "https://upload.wikimedia.org/wikipedia/commons/0/0a/Ishihara_1.png",
        2: "https://upload.wikimedia.org/wikipedia/commons/1/1e/Ishihara_2.png", 
        3: "https://upload.wikimedia.org/wikipedia/commons/3/3c/Ishihara_3.png",
        4: "https://upload.wikimedia.org/wikipedia/commons/4/4f/Ishihara_4.png",
        5: "https://upload.wikimedia.org/wikipedia/commons/5/5a/Ishihara_5.png",
        6: "https://upload.wikimedia.org/wikipedia/commons/6/6d/Ishihara_6.png",
        9: "https://upload.wikimedia.org/wikipedia/commons/9/9a/Ishihara_9.png",
        10: "https://upload.wikimedia.org/wikipedia/commons/b/bf/Ishihara_10.png",
        14: "https://upload.wikimedia.org/wikipedia/commons/e/e9/Ishihara_14.png",
        15: "https://upload.wikimedia.org/wikipedia/commons/f/f3/Ishihara_15.png",
        16: "https://upload.wikimedia.org/wikipedia/commons/7/7d/Ishihara_16.png",
        17: "https://upload.wikimedia.org/wikipedia/commons/8/8c/Ishihara_17.png",
    }
    
    if plate_number in wikimedia_plates:
        try:
            url = wikimedia_plates[plate_number]
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                return image, "Wikimedia Commons"
        except:
            pass
    
    return None, None

def create_color_pattern(plate_number):
    """Create a colored dot pattern as placeholder"""
    img = Image.new('RGB', (400, 400), color='#F0F8FF')  # Light blue background
    draw = ImageDraw.Draw(img)
    
    # Different color sets for variety
    color_sets = [
        ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],  # Bright colors
        ['#6A0572', '#AB83A1', '#5F4B8B', '#E69A8D', '#F0C987'],  # Muted colors
        ['#2A9D8F', '#E9C46A', '#F4A261', '#E76F51', '#264653'],  # Nature colors
    ]
    
    colors = color_sets[plate_number % len(color_sets)]
    
    # Draw background dots
    for i in range(200):
        x = random.randint(20, 380)
        y = random.randint(20, 380)
        radius = random.randint(5, 15)
        color = colors[random.randint(0, len(colors)-1)]
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    
    return img

def ishihara_test():
    st.header("👁️ Ishihara Color Vision Test")
    
    # Initialize session state
    if 'current_plate' not in st.session_state:
        st.session_state.current_plate = 1
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    
    plate_number = st.session_state.current_plate
    plate_data = ISHIHARA_DATA[plate_number]
    
    # Display current plate
    st.subheader(f"Plate {plate_number}")
    
    # Try to load from Wikimedia first
    with st.spinner("Loading test plate..."):
        plate_image, source = load_wikimedia_plate(plate_number)
    
    if plate_image:
        st.image(plate_image, width=400, caption=f"Plate {plate_number}")
        st.success(f"✅ Real Ishihara plate (Source: {source})")
    else:
        # Create color pattern as fallback
        pattern_image = create_color_pattern(plate_number)
        st.image(pattern_image, width=400, caption=f"Color Pattern {plate_number}")
        st.info("🎨 Using color pattern simulation")
        
        # Show what should be visible
        st.write(f"**This plate should show:** {plate_data['description']}")
        
        with st.expander("ℹ️ About this test"):
            st.write("""
            **Note about online testing:**
            - Real Ishihara plates are copyright protected
            - This simulation helps understand the test format
            - For accurate diagnosis, use official Ishihara books
            - Consult eye care professional for medical assessment
            """)
    
    # User input
    user_answer = st.text_input(
        "What number do you see? (Leave blank if you don't see anything)",
        value=st.session_state.user_answers.get(plate_number, ""),
        key=f"plate_{plate_number}"
    )
    
    # Store answer
    st.session_state.user_answers[plate_number] = user_answer.strip()
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if plate_number > 1:
            if st.button("← Previous Plate", use_container_width=True):
                st.session_state.current_plate -= 1
                st.rerun()
    
    with col2:
        if st.button("🏠 Finish Test", use_container_width=True):
            st.session_state.current_page = "home"
            st.session_state.current_plate = 1
            st.rerun()
    
    with col3:
        if plate_number < 24:
            if st.button("Next Plate →", use_container_width=True):
                st.session_state.current_plate += 1
                st.rerun()
        else:
            if st.button("📊 See Results", use_container_width=True):
                st.session_state.current_page = "results"
                st.rerun()
    
    # Progress
    progress = plate_number / 24
    st.progress(progress)
    st.write(f"Progress: {plate_number} of 24 plates")
    
    # Instructions
    with st.expander("📋 Test Instructions"):
        st.write("""
        - Look at each plate and type the number you see
        - If you don't see any number, leave the field blank
        - Complete all 24 plates for accurate results
        - Sit about 75cm from the screen
        - Ensure normal room lighting
        - This test screens for red-green color vision deficiencies
        """)

def show_results():
    st.header("📊 Ishihara Test Results")
    
    if not st.session_state.user_answers:
        st.warning("No test data available. Please complete the test first.")
        return
    
    # Calculate scores
    normal_score = 0
    deutan_score = 0
    protan_score = 0
    
    for plate_num, user_answer in st.session_state.user_answers.items():
        plate_data = ISHIHARA_DATA[plate_num]
        
        if user_answer.lower() == plate_data["normal"].lower():
            normal_score += 1
        if user_answer.lower() == plate_data["deutan"].lower():
            deutan_score += 1
        if user_answer.lower() == plate_data["protan"].lower():
            protan_score += 1
    
    # Display results
    st.subheader("Test Scores")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Normal Vision", f"{normal_score}/24")
    with col2:
        st.metric("Deutan Indicators", f"{deutan_score}/24")
    with col3:
        st.metric("Protan Indicators", f"{protan_score}/24")
    
    # Diagnosis
    max_score = max(normal_score, deutan_score, protan_score)
    
    st.subheader("Assessment")
    if normal_score == max_score:
        st.success("✅ **Likely Normal Color Vision**")
        st.write("Your responses are consistent with normal color vision.")
    elif deutan_score == max_score:
        st.warning("⚠️ **Possible Deuteranopia (Green Deficiency)**")
        st.write("Your responses suggest possible difficulty distinguishing green hues.")
    elif protan_score == max_score:
        st.warning("⚠️ **Possible Protanopia (Red Deficiency)**")
        st.write("Your responses suggest possible difficulty distinguishing red hues.")
    else:
        st.error("❓ **Inconclusive Results**")
        st.write("Please consult an eye care professional for comprehensive assessment.")
    
    # Answer review
    st.subheader("Detailed Results")
    review_data = []
    for plate_num in range(1, 25):
        plate_data = ISHIHARA_DATA[plate_num]
        user_answer = st.session_state.user_answers.get(plate_num, "No answer")
        
        # Determine answer status
        if user_answer.lower() == plate_data["normal"].lower():
            status = "✅ Normal"
        elif user_answer.lower() == plate_data["deutan"].lower():
            status = "🟡 Deutan"
        elif user_answer.lower() == plate_data["protan"].lower():
            status = "🟠 Protan"
        else:
            status = "❌ Incorrect"
        
        review_data.append({
            "Plate": plate_num,
            "Your Answer": user_answer,
            "Expected Normal": plate_data["normal"],
            "Status": status
        })
    
    st.dataframe(pd.DataFrame(review_data), use_container_width=True)
    
    # Professional disclaimer
    st.warning("""
    **Professional Disclaimer:** 
    This online test is for educational and screening purposes only. 
    It is not a substitute for professional medical diagnosis. 
    For official color vision assessment, please consult a qualified eye care specialist.
    """)
    
    if st.button("🔄 Take Test Again"):
        st.session_state.current_plate = 1
        st.session_state.user_answers = {}
        st.session_state.current_page = "ishihara"
        st.rerun()

def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    
    # Main navigation
    st.title("🚢 Maritime Color Vision Test")
    st.subheader("Professional Color Vision Testing Suite")
    
    if st.session_state.current_page == "home":
        st.success("✅ Select a test to begin comprehensive color vision assessment")
        
        # Test selection
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("### 👁️ Ishihara Test")
            st.write("Red-green deficiency screening")
            if st.button("Start Ishihara Test", key="ishihara", use_container_width=True):
                st.session_state.current_page = "ishihara"
                st.rerun()
        
        with col2:
            st.markdown("### 🎯 Lantern Test")
            st.write("Navigation light recognition")
            st.button("Coming Soon", use_container_width=True, disabled=True)
        
        with col3:
            st.markdown("### 🌈 FM15 Test") 
            st.write("Color discrimination ability")
            st.button("Coming Soon", use_container_width=True, disabled=True)
        
        with col4:
            st.markdown("### 🗺️ ECDIS Test")
            st.write("Chart display colors")
            st.button("Coming Soon", use_container_width=True, disabled=True)
        
        # About section
        with st.expander("ℹ️ About This Application"):
            st.write("""
            **Maritime Color Vision Testing Suite**
            
            This application provides standardized color vision tests specifically 
            designed for maritime professionals. The tests help identify color 
            vision deficiencies that could affect navigation safety.
            
            **Current tests available:**
            - Ishihara Test: Screens for red-green color deficiencies
            - More tests coming soon...
            
            **Copyright © Toni Mandušić 2025**
            """)
        
        st.divider()
        st.caption("For professional use only - Consult medical professionals for official diagnosis")
    
    elif st.session_state.current_page == "ishihara":
        ishihara_test()
    
    elif st.session_state.current_page == "results":
        show_results()

if __name__ == "__main__":
    main()