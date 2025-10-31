# Maritime Color Vision Test - Professional Suite
# Copyright © Toni Mandusic 2025

import streamlit as st
import pandas as pd
import os
import random

# Page configuration
st.set_page_config(
    page_title="Maritime Color Vision Test",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 0 0 15px 15px;
        margin-bottom: 2rem;
        color: white;
    }
    .test-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: transform 0.2s;
        background: white;
    }
    .test-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .footer {
        background-color: #f8f9fa;
        padding: 1rem;
        text-align: center;
        margin-top: 3rem;
        border-top: 1px solid #e0e0e0;
        font-size: 0.9rem;
        color: #6c757d;
    }
    .ishihara-image {
        display: block;
        margin: 0 auto;
        max-width: 600px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .user-info {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .logo-container {
        text-align: right;
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Test data
ISHIHARA_DATA = {
    1: {"normal": "12", "deutan": "12", "protan": "12"},
    2: {"normal": "8", "deutan": "3", "protan": "3"},
    3: {"normal": "6", "deutan": "5", "protan": "5"},
    4: {"normal": "29", "deutan": "70", "protan": "70"},
    5: {"normal": "57", "deutan": "35", "protan": "35"},
    6: {"normal": "5", "deutan": "2", "protan": "2"},
    7: {"normal": "3", "deutan": "5", "protan": "5"},
    8: {"normal": "15", "deutan": "17", "protan": "17"},
    9: {"normal": "74", "deutan": "21", "protan": "21"},
    10: {"normal": "2", "deutan": "", "protan": ""},
    11: {"normal": "6", "deutan": "", "protan": ""},
    12: {"normal": "97", "deutan": "", "protan": ""},
    13: {"normal": "45", "deutan": "", "protan": ""},
    14: {"normal": "5", "deutan": "", "protan": ""},
    15: {"normal": "7", "deutan": "", "protan": ""},
    16: {"normal": "16", "deutan": "", "protan": ""},
    17: {"normal": "73", "deutan": "", "protan": ""},
    18: {"normal": "", "deutan": "5", "protan": "5"},
    19: {"normal": "", "deutan": "2", "protan": "2"},
    20: {"normal": "", "deutan": "45", "protan": "45"},
    21: {"normal": "", "deutan": "73", "protan": "73"},
    22: {"normal": "26", "deutan": "2", "protan": "6"},
    23: {"normal": "42", "deutan": "4", "protan": "2"},
    24: {"normal": "35", "deutan": "3", "protan": "5"}
}

LANTERN_COLORS = {
    'red': {'name': 'Red', 'hex': '#FF0000'},
    'green': {'name': 'Green', 'hex': '#00FF00'}, 
    'yellow': {'name': 'Yellow', 'hex': '#FFD200'},
    'white': {'name': 'White', 'hex': '#FFFFFF'}
}

LANTERN_SEQUENCES = [
    ('red', 'green'), ('red', 'white'), ('green', 'white'),
    ('yellow', 'yellow'), ('red', 'red'), ('green', 'green'),
    ('white', 'white'), ('red', 'yellow'), ('green', 'yellow')
]

ECDIS_FM_COLORS = [
    # Sea blues
    ['#AEE9FF', '#9BDDF5', '#88D1EB', '#75C5E1', '#62B9D7', '#4FADCD', '#3CA1C3', '#2995B9'],
    # Land browns
    ['#E5D8A6', '#D4C895', '#C3B884', '#B2A873', '#A19862', '#908851', '#7F7840', '#6E682F'],
    # Depth blues
    ['#0076BF', '#006BAC', '#005F99', '#005386', '#004773', '#003B60', '#002F4D', '#00233A'],
    # Navigation yellows
    ['#FFAA00', '#E69900', '#CC8800', '#B37700', '#996600', '#805500', '#664400', '#4D3300'],
    # Navigation greens
    ['#44FF44', '#3CE03C', '#33C633', '#2AAD2A', '#229322', '#197A19', '#106110', '#084808']
]

def render_header():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div style='padding: 1rem 0;'>
            <h1 style='margin: 0; color: #1e3c72;'>Maritime Color Vision Test</h1>
            <p style='margin: 0; color: #6c757d; font-size: 1.1rem;'>
                Professional color vision assessment for maritime personnel
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(
            '<div class="logo-container"><img src="https://i.postimg.cc/L8cW5X4H/phant-logo.png" width="120"></div>',
            unsafe_allow_html=True
        )

def user_information():
    st.markdown("### Personal Information")
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.user_name = st.text_input("Full Name", placeholder="Enter your full name")
        with col2:
            st.session_state.user_id = st.text_input("ID Number", placeholder="ID or passport number")
        with col3:
            st.session_state.user_position = st.selectbox(
                "Position",
                ["Select position", "Deck Officer", "Engine Officer", "Lookout", "Pilot", "Other"]
            )

def home_page():
    render_header()
    user_information()
    
    st.markdown("---")
    st.markdown("### Select Test")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            '<div style="text-align: center;"><img src="https://i.postimg.cc/HLgBVDzm/Gemini-Generated-Image-2uib402uib402uib.png" width="80"></div>',
            unsafe_allow_html=True
        )
        st.markdown("### 🎯 Lantern Test")
        st.markdown("Navigation light recognition under low-light conditions")
        if st.button("Start Lantern Test", key="lantern_home", use_container_width=True):
            if validate_user_info():
                st.session_state.current_page = "lantern"
                st.rerun()
    
    with col2:
        st.markdown(
            '<div style="text-align: center;"><img src="https://i.postimg.cc/vZ6N4vdv/Gemini-Generated-Image-5xg9ca5xg9ca5xg9.png" width="80"></div>',
            unsafe_allow_html=True
        )
        st.markdown("### 👁️ Ishihara Test")
        st.markdown("Red-green color deficiency screening")
        if st.button("Start Ishihara Test", key="ishihara_home", use_container_width=True):
            if validate_user_info():
                st.session_state.current_page = "ishihara"
                st.rerun()
    
    with col3:
        st.markdown(
            '<div style="text-align: center;"><img src="https://i.postimg.cc/mDhMr806/Gemini-Generated-Image-7a116v7a116v7a11.png" width="80"></div>',
            unsafe_allow_html=True
        )
        st.markdown("### 🌈 ECDIS Hue Test")
        st.markdown("Navigation color discrimination ability")
        if st.button("Start ECDIS Test", key="ecdis_home", use_container_width=True):
            if validate_user_info():
                st.session_state.current_page = "ecdiscfm"
                st.rerun()
    
    render_footer()

def validate_user_info():
    if not st.session_state.get('user_name') or not st.session_state.get('user_id'):
        st.error("Please complete personal information before starting tests")
        return False
    return True

def lantern_test():
    render_header()
    st.markdown("### 🎯 Lantern Test")
    
    if 'lantern_current_pair' not in st.session_state:
        st.session_state.lantern_current_pair = 0
        st.session_state.lantern_answers = {}
        st.session_state.lantern_sequence = random.sample(LANTERN_SEQUENCES, len(LANTERN_SEQUENCES))
    
    current_pair = st.session_state.lantern_current_pair
    sequence = st.session_state.lantern_sequence
    
    if current_pair >= len(sequence):
        show_lantern_results()
        return
    
    color1, color2 = sequence[current_pair]
    color1_data = LANTERN_COLORS[color1]
    color2_data = LANTERN_COLORS[color2]
    
    st.markdown(f"**Light Pair {current_pair + 1} of {len(sequence)}**")
    
    # Lantern display
    st.markdown('<div style="background-color: #000000; padding: 40px; border-radius: 15px; text-align: center; margin: 20px 0;">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f'<div style="width: 80px; height: 80px; border-radius: 50%; background-color: {color1_data["hex"]}; margin: 0 auto; box-shadow: 0 0 30px {color1_data["hex"]}80; border: 3px solid #333;"></div>',
            unsafe_allow_html=True
        )
        st.markdown('<div style="color: white; margin-top: 10px;">Light 1</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(
            f'<div style="width: 80px; height: 80px; border-radius: 50%; background-color: {color2_data["hex"]}; margin: 0 auto; box-shadow: 0 0 30px {color2_data["hex"]}80; border: 3px solid #333;"></div>',
            unsafe_allow_html=True
        )
        st.markdown('<div style="color: white; margin-top: 10px;">Light 2</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Answer section
    col1, col2 = st.columns(2)
    with col1:
        light1_answer = st.selectbox("Light 1 Color:", ["Select color", "Red", "Green", "Yellow", "White"], key=f"lantern_1_{current_pair}")
    with col2:
        light2_answer = st.selectbox("Light 2 Color:", ["Select color", "Red", "Green", "Yellow", "White"], key=f"lantern_2_{current_pair}")
    
    if light1_answer != "Select color" and light2_answer != "Select color":
        st.session_state.lantern_answers[current_pair] = {
            'light1': light1_answer.lower(), 'light2': light2_answer.lower(),
            'correct1': color1_data['name'].lower(), 'correct2': color2_data['name'].lower()
        }
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if current_pair > 0 and st.button("← Previous"):
            st.session_state.lantern_current_pair -= 1
            st.rerun()
    with col2:
        if st.button("🏠 Home"):
            st.session_state.current_page = "home"
            st.rerun()
    with col3:
        if st.button("Next →"):
            st.session_state.lantern_current_pair += 1
            st.rerun()
    
    st.progress((current_pair + 1) / len(sequence))

def ishihara_test():
    render_header()
    st.markdown("### 👁️ Ishihara Test")
    
    if 'current_plate' not in st.session_state:
        st.session_state.current_plate = 1
        st.session_state.user_answers = {}
    
    plate_number = st.session_state.current_plate
    plate_data = ISHIHARA_DATA[plate_number]
    
    st.markdown(f"**Plate {plate_number} of 24**")
    
    # Center the image with increased size
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        image_path = f"assets/ishihara_plates/plate{plate_number}.png"
        if os.path.exists(image_path):
            st.image(image_path, width=500, use_column_width=True)
        else:
            st.error(f"Plate image not found: {image_path}")
            return
    
    # User input centered
    with col2:
        user_answer = st.text_input(
            "What number do you see? (Leave blank if none)",
            value=st.session_state.user_answers.get(plate_number, ""),
            key=f"plate_{plate_number}"
        )
        st.session_state.user_answers[plate_number] = user_answer.strip()
    
    # Navigation
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        if plate_number > 1 and st.button("← Previous"):
            st.session_state.current_plate -= 1
            st.rerun()
    with col3:
        if st.button("🏠 Home"):
            st.session_state.current_page = "home"
            st.rerun()
    with col4:
        if plate_number < 24 and st.button("Next →"):
            st.session_state.current_plate += 1
            st.rerun()
        elif plate_number == 24 and st.button("See Results"):
            st.session_state.current_page = "results"
            st.rerun()
    
    st.progress(plate_number / 24)

def ecdisfm_test():
    render_header()
    st.markdown("### 🌈 ECDIS Hue Test")
    
    if 'ecdis_current_group' not in st.session_state:
        st.session_state.ecdis_current_group = 0
        st.session_state.ecdis_scores = [0] * len(ECDIS_FM_COLORS)
        st.session_state.ecdis_user_orders = []
        for group in ECDIS_FM_COLORS:
            shuffled = group.copy()
            random.shuffle(shuffled)
            st.session_state.ecdis_user_orders.append(shuffled)
        st.session_state.ecdis_selected_color = None
    
    current_group = st.session_state.ecdis_current_group
    user_order = st.session_state.ecdis_user_orders[current_group]
    selected_color = st.session_state.ecdis_selected_color
    
    group_names = ["Sea Blues", "Land Browns", "Depth Blues", "Navigation Yellows", "Navigation Greens"]
    st.markdown(f"**{group_names[current_group]}** - Arrange from lightest to darkest")
    st.markdown(f"*Group {current_group + 1} of {len(ECDIS_FM_COLORS)}*")
    
    # Color grid
    cols = st.columns(8)
    for i, color in enumerate(user_order):
        with cols[i]:
            border_color = "#FF0000" if color == selected_color else "#333333"
            border_width = "3px" if color == selected_color else "1px"
            
            if st.button("", key=f"ecdis_color_{i}"):
                if selected_color is None:
                    st.session_state.ecdis_selected_color = color
                else:
                    move_ecdis_color(selected_color, i)
                    st.session_state.ecdis_selected_color = None
                st.rerun()
            
            st.markdown(
                f'<div style="height:60px; background:{color}; border:{border_width} solid {border_color}; border-radius:5px; margin:2px;"></div>',
                unsafe_allow_html=True
            )
            st.markdown(f'<div style="text-align:center; font-size:10px;">{i+1}</div>', unsafe_allow_html=True)
    
    if selected_color:
        st.info("Selected - click target position")
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔀 Shuffle"):
            random.shuffle(st.session_state.ecdis_user_orders[current_group])
            st.session_state.ecdis_selected_color = None
            st.rerun()
    with col2:
        if st.button("🏠 Home"):
            st.session_state.current_page = "home"
            st.rerun()
    with col3:
        if current_group < len(ECDIS_FM_COLORS) - 1:
            if st.button("Next Group →"):
                st.session_state.ecdis_current_group += 1
                st.session_state.ecdis_selected_color = None
                st.rerun()
        else:
            if st.button("See Results"):
                st.session_state.current_page = "results"
                st.rerun()
    
    st.progress((current_group + 1) / len(ECDIS_FM_COLORS))

def move_ecdis_color(selected_color, target_position):
    current_group = st.session_state.ecdis_current_group
    user_order = st.session_state.ecdis_user_orders[current_group]
    current_position = user_order.index(selected_color)
    user_order.pop(current_position)
    user_order.insert(target_position, selected_color)

def show_lantern_results():
    render_header()
    st.markdown("### 📊 Lantern Test Results")
    
    answers = st.session_state.lantern_answers
    total_pairs = len(LANTERN_SEQUENCES)
    
    if not answers:
        st.warning("No test data available.")
        return
    
    # Calculate scores
    correct_answers = 0
    for answer_data in answers.values():
        if (answer_data['light1'] == answer_data['correct1'] and 
            answer_data['light2'] == answer_data['correct2']):
            correct_answers += 1
    
    # Display results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Correct Pairs", f"{correct_answers}/{total_pairs}")
    with col2:
        accuracy = (correct_answers / total_pairs) * 100
        st.metric("Accuracy", f"{accuracy:.1f}%")
    with col3:
        errors = total_pairs - correct_answers
        st.metric("Errors", errors)
    
    # Assessment
    if errors <= 1:
        st.success("✅ **PASS** - Suitable for maritime duties")
    else:
        st.error("❌ **FAIL** - Further assessment recommended")
    
    if st.button("🏠 Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()

def show_results():
    render_header()
    st.markdown("### 📊 Test Results")
    
    st.info("Results dashboard and certificate generation will be implemented in the next phase")
    
    if st.button("🏠 Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()

def render_footer():
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>Medical Disclaimer:</strong> This test is for screening purposes only and is not a substitute for professional medical examination. Consult a qualified eye care specialist for official diagnosis.</p>
        <p>Copyright © Toni Mandusic 2025. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    
    # Initialize user info
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = ""
    if 'user_position' not in st.session_state:
        st.session_state.user_position = "Select position"
    
    # Page routing
    if st.session_state.current_page == "home":
        home_page()
    elif st.session_state.current_page == "lantern":
        lantern_test()
    elif st.session_state.current_page == "ishihara":
        ishihara_test()
    elif st.session_state.current_page == "ecdiscfm":
        ecdisfm_test()
    elif st.session_state.current_page == "results":
        show_results()

if __name__ == "__main__":
    main()