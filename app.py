# Maritime Color Vision Test - Professional Suite
# Copyright © Toni Mandusic 2025

import streamlit as st
import pandas as pd
import os
import random
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Maritime Color Vision Test",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional maritime design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0a2a5a 0%, #1a3d7c 100%);
        padding: 2rem 2rem;
        border-radius: 0 0 0 0;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-bottom: 4px solid #ffd700;
    }
    .test-card {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        background: white;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .test-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border-color: #1a3d7c;
    }
    .footer {
        background-color: #0a2a5a;
        padding: 1.5rem;
        text-align: center;
        margin-top: 3rem;
        border-top: 1px solid #1a3d7c;
        font-size: 0.9rem;
        color: #e5e7eb;
    }
    .user-info-panel {
        background: linear-gradient(135deg, #f0f4f8 0%, #e1e8f0 100%);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #1a3d7c;
        font-weight: 500;
    }
    .timer-warning {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 6px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        color: #856404;
    }
    .results-card {
        background: white;
        border-radius: 8px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #28a745;
    }
    .nav-button {
        margin: 0.5rem;
    }
    .lantern-display {
        background-color: #000000;
        padding: 50px 20px;
        border-radius: 8px;
        text-align: center;
        margin: 20px 0;
        border: 2px solid #333;
    }
    .test-title {
        color: #1a3d7c;
        border-bottom: 2px solid #ffd700;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
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
    ['#44FF44', '#3CE03C', '#33C633', '#2AAD2A', '#229322', '#197A19', '#106110', '#084808'],
    # Olive greens (new)
    ['#808000', '#767A00', '#6D7400', '#636E00', '#596800', '#4F6200', '#455C00', '#3B5600'],
    # Dark purples (new)
    ['#4B0082', '#45007A', '#3F0072', '#39006A', '#330062', '#2D005A', '#270052', '#21004A']
]

def render_header():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div style='padding: 1rem 0;'>
            <h1 style='margin: 0; color: white; font-size: 2.5rem; font-weight: 700;'>MARITIME COLOR VISION TEST</h1>
            <p style='margin: 0; color: #e5e7eb; font-size: 1.2rem;'>
                Professional color vision assessment for maritime personnel
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(
            '<div style="text-align: right; padding-top: 0.5rem;"><img src="https://i.postimg.cc/L8cW5X4H/phant-logo.png" width="150"></div>',
            unsafe_allow_html=True
        )

def user_information():
    st.markdown("### PERSONAL INFORMATION")
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

def show_user_panel():
    if st.session_state.get('user_name'):
        st.markdown(f"""
        <div class="user-info-panel">
            <strong>Candidate:</strong> {st.session_state.user_name} | 
            <strong>ID:</strong> {st.session_state.user_id} | 
            <strong>Position:</strong> {st.session_state.user_position}
        </div>
        """, unsafe_allow_html=True)

def home_page():
    render_header()
    
    if not st.session_state.get('user_name') or not st.session_state.get('user_id'):
        user_information()
        st.markdown("---")
    
    show_user_panel()
    
    st.markdown("### SELECT TEST")
    st.markdown("Choose a test to begin your color vision assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="test-card">
            <h3>LANTERN TEST</h3>
            <p>Navigation light recognition under low-light conditions</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Lantern Test", key="lantern_home", use_container_width=True, type="primary"):
            if validate_user_info():
                st.session_state.current_page = "lantern"
                initialize_lantern_test()
                st.rerun()
    
    with col2:
        st.markdown("""
        <div class="test-card">
            <h3>ISHIHARA TEST</h3>
            <p>Red-green color deficiency screening</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Ishihara Test", key="ishihara_home", use_container_width=True, type="primary"):
            if validate_user_info():
                st.session_state.current_page = "ishihara"
                st.rerun()
    
    with col3:
        st.markdown("""
        <div class="test-card">
            <h3>ECDIS HUE TEST</h3>
            <p>Navigation color discrimination ability</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start ECDIS Test", key="ecdis_home", use_container_width=True, type="primary"):
            if validate_user_info():
                st.session_state.current_page = "ecdiscfm"
                st.rerun()
    
    # Quick navigation between tests if already started
    if any(key in st.session_state for key in ['lantern_answers', 'user_answers', 'ecdis_scores']):
        st.markdown("---")
        st.markdown("### CONTINUE TESTING")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.session_state.get('lantern_answers'):
                if st.button("Continue Lantern Test", use_container_width=True):
                    st.session_state.current_page = "lantern"
                    st.rerun()
        
        with col2:
            if st.session_state.get('user_answers'):
                if st.button("Continue Ishihara Test", use_container_width=True):
                    st.session_state.current_page = "ishihara"
                    st.rerun()
        
        with col3:
            if st.session_state.get('ecdis_scores'):
                if st.button("Continue ECDIS Test", use_container_width=True):
                    st.session_state.current_page = "ecdiscfm"
                    st.rerun()
    
    render_footer()

def validate_user_info():
    if not st.session_state.get('user_name') or not st.session_state.get('user_id'):
        st.error("❌ Please complete personal information before starting tests")
        return False
    return True

def initialize_lantern_test():
    if 'lantern_start_time' not in st.session_state:
        st.session_state.lantern_start_time = time.time()
    if 'lantern_current_pair' not in st.session_state:
        st.session_state.lantern_current_pair = 0
        st.session_state.lantern_answers = {}
        st.session_state.lantern_sequence = random.sample(LANTERN_SEQUENCES, len(LANTERN_SEQUENCES))

def lantern_test():
    render_header()
    show_user_panel()
    st.markdown("### LANTERN TEST")
    
    initialize_lantern_test()
    
    current_pair = st.session_state.lantern_current_pair
    sequence = st.session_state.lantern_sequence
    
    if current_pair >= len(sequence):
        show_lantern_results()
        return
    
    # Timer logic
    elapsed_time = time.time() - st.session_state.lantern_start_time
    time_per_pair = 5  # 5 seconds per pair
    time_remaining = max(0, time_per_pair - (elapsed_time % time_per_pair))
    
    if time_remaining < 2:
        st.markdown(f'<div class="timer-warning">⏰ Time almost up! {time_remaining:.1f}s remaining</div>', unsafe_allow_html=True)
    
    color1, color2 = sequence[current_pair]
    color1_data = LANTERN_COLORS[color1]
    color2_data = LANTERN_COLORS[color2]
    
    st.markdown(f"**Light Pair {current_pair + 1} of {len(sequence)}**")
    st.progress((current_pair + 1) / len(sequence))
    
    # Lantern display - FIXED: Proper black background
    st.markdown('<div class="lantern-display">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f'<div style="width: 120px; height: 120px; border-radius: 50%; background-color: {color1_data["hex"]}; margin: 0 auto; box-shadow: 0 0 50px {color1_data["hex"]}80; border: 3px solid #555;"></div>',
            unsafe_allow_html=True
        )
        st.markdown('<div style="color: white; margin-top: 15px; font-size: 16px;">LIGHT 1</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(
            f'<div style="width: 120px; height: 120px; border-radius: 50%; background-color: {color2_data["hex"]}; margin: 0 auto; box-shadow: 0 0 50px {color2_data["hex"]}80; border: 3px solid #555;"></div>',
            unsafe_allow_html=True
        )
        st.markdown('<div style="color: white; margin-top: 15px; font-size: 16px;">LIGHT 2</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-advance timer
    if time_remaining <= 0:
        st.session_state.lantern_current_pair += 1
        st.session_state.lantern_start_time = time.time()
        st.rerun()
    
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
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if current_pair > 0 and st.button("← Previous", use_container_width=True):
            st.session_state.lantern_current_pair -= 1
            st.session_state.lantern_start_time = time.time()
            st.rerun()
    with col2:
        if st.button("Pause", use_container_width=True):
            st.session_state.lantern_start_time = time.time()  # Reset timer
            st.rerun()
    with col3:
        if st.button("Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with col4:
        if st.button("Next →", use_container_width=True, type="primary"):
            st.session_state.lantern_current_pair += 1
            st.session_state.lantern_start_time = time.time()
            st.rerun()

def ishihara_test():
    render_header()
    show_user_panel()
    st.markdown("### ISHIHARA TEST")
    
    if 'current_plate' not in st.session_state:
        st.session_state.current_plate = 1
        st.session_state.user_answers = {}
    
    plate_number = st.session_state.current_plate
    plate_data = ISHIHARA_DATA[plate_number]
    
    st.markdown(f"**Plate {plate_number} of 24**")
    st.progress(plate_number / 24)
    
    # Center the image with reduced size (20% smaller)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        image_path = f"assets/ishihara_plates/plate{plate_number}.png"
        if os.path.exists(image_path):
            st.image(image_path, width=440, use_column_width=True)  # Reduced from 550 to 440
        else:
            st.error(f"❌ Plate image not found: {image_path}")
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
    with col1:
        if st.button("Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with col2:
        if plate_number > 1 and st.button("← Previous", use_container_width=True):
            st.session_state.current_plate -= 1
            st.rerun()
    with col3:
        if st.button("Other Tests", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with col4:
        if plate_number < 24 and st.button("Next →", use_container_width=True, type="primary"):
            st.session_state.current_plate += 1
            st.rerun()
    with col5:
        if plate_number == 24 and st.button("See Results", use_container_width=True, type="primary"):
            st.session_state.current_page = "results"
            st.rerun()

def ecdisfm_test():
    render_header()
    show_user_panel()
    st.markdown("### ECDIS HUE TEST")
    
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
    
    group_names = ["Sea Blues", "Land Browns", "Depth Blues", "Navigation Yellows", 
                   "Navigation Greens", "Olive Greens", "Dark Purples"]
    st.markdown(f"**{group_names[current_group]}** - Arrange from lightest to darkest")
    st.markdown(f"*Group {current_group + 1} of {len(ECDIS_FM_COLORS)}*")
    st.progress((current_group + 1) / len(ECDIS_FM_COLORS))
    
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
                f'<div style="height:70px; background:{color}; border:{border_width} solid {border_color}; border-radius:8px; margin:2px;"></div>',
                unsafe_allow_html=True
            )
            st.markdown(f'<div style="text-align:center; font-size:12px; margin-top:5px;">{i+1}</div>', unsafe_allow_html=True)
    
    if selected_color:
        st.info("**Selected** - Now click target position to move")
    else:
        st.info("**Click any color to select it**, then click target position")
    
    # Navigation
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with col2:
        if st.button("Shuffle", use_container_width=True):
            random.shuffle(st.session_state.ecdis_user_orders[current_group])
            st.session_state.ecdis_selected_color = None
            st.rerun()
    with col3:
        if st.button("Other Tests", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with col4:
        if current_group < len(ECDIS_FM_COLORS) - 1:
            if st.button("Next Group →", use_container_width=True, type="primary"):
                st.session_state.ecdis_current_group += 1
                st.session_state.ecdis_selected_color = None
                st.rerun()
        else:
            if st.button("See Results", use_container_width=True, type="primary"):
                st.session_state.current_page = "results"
                st.rerun()

def move_ecdis_color(selected_color, target_position):
    current_group = st.session_state.ecdis_current_group
    user_order = st.session_state.ecdis_user_orders[current_group]
    current_position = user_order.index(selected_color)
    user_order.pop(current_position)
    user_order.insert(target_position, selected_color)

def show_lantern_results():
    render_header()
    show_user_panel()
    st.markdown("### LANTERN TEST RESULTS")
    
    answers = st.session_state.lantern_answers
    total_pairs = len(LANTERN_SEQUENCES)
    
    if not answers:
        st.warning("No test data available.")
        return
    
    # Calculate scores
    correct_answers = 0
    detailed_results = []
    
    for pair_idx, answer_data in answers.items():
        light1_correct = answer_data['light1'] == answer_data['correct1']
        light2_correct = answer_data['light2'] == answer_data['correct2']
        pair_correct = light1_correct and light2_correct
        
        if pair_correct:
            correct_answers += 1
        
        detailed_results.append({
            'Pair': pair_idx + 1,
            'Light 1': f"{answer_data['light1'].title()} ({'✅' if light1_correct else '❌'})",
            'Light 2': f"{answer_data['light2'].title()} ({'✅' if light2_correct else '❌'})",
            'Correct': f"{answer_data['correct1'].title()}, {answer_data['correct2'].title()}",
            'Status': 'PASS' if pair_correct else 'FAIL'
        })
    
    accuracy = (correct_answers / total_pairs) * 100
    errors = total_pairs - correct_answers
    
    # Display results
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Correct Pairs", f"{correct_answers}/{total_pairs}")
    with col2:
        st.metric("Accuracy", f"{accuracy:.1f}%")
    with col3:
        st.metric("Errors", errors)
    with col4:
        status = "PASS" if errors <= 1 else "FAIL"
        st.metric("Result", status, delta="PASS" if errors <= 1 else "FAIL", 
                 delta_color="normal" if errors <= 1 else "inverse")
    
    # Detailed results
    st.markdown("#### Detailed Results")
    st.dataframe(pd.DataFrame(detailed_results), use_container_width=True)
    
    # Assessment
    st.markdown("#### PROFESSIONAL ASSESSMENT")
    if errors <= 1:
        st.success("""
        **✅ EXCELLENT - Suitable for Maritime Duties**
        
        Your performance meets IMO standards for color vision requirements in navigation and lookout duties. 
        You demonstrate excellent ability to recognize navigation lights under simulated low-light conditions.
        """)
    elif errors <= 2:
        st.warning("""
        **⚠️ BORDERLINE - Further Assessment Recommended**
        
        Your results indicate minor difficulties with color recognition that may affect performance 
        in challenging conditions. Consider retesting or professional evaluation.
        """)
    else:
        st.error("""
        **❌ UNSATISFACTORY - Not Suitable for Color-Critical Duties**
        
        Significant difficulties with navigation light recognition detected. 
        Consult an eye care specialist for comprehensive assessment before undertaking maritime duties.
        """)
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Retest Lantern", use_container_width=True):
            st.session_state.lantern_current_pair = 0
            st.session_state.lantern_answers = {}
            st.session_state.lantern_sequence = random.sample(LANTERN_SEQUENCES, len(LANTERN_SEQUENCES))
            st.session_state.lantern_start_time = time.time()
            st.rerun()
    with col2:
        if st.button("Back to Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with col3:
        if st.button("All Results", use_container_width=True, type="primary"):
            st.session_state.current_page = "results"
            st.rerun()

def show_results():
    render_header()
    show_user_panel()
    st.markdown("### COMPREHENSIVE TEST RESULTS")
    
    # Collect results from all tests
    results_data = {
        'user_name': st.session_state.get('user_name', 'N/A'),
        'user_id': st.session_state.get('user_id', 'N/A'),
        'position': st.session_state.get('user_position', 'N/A'),
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'tests_completed': []
    }
    
    # Lantern test results
    if st.session_state.get('lantern_answers'):
        lantern_answers = st.session_state.lantern_answers
        total_pairs = len(LANTERN_SEQUENCES)
        correct_pairs = sum(1 for answer in lantern_answers.values() 
                          if answer['light1'] == answer['correct1'] and answer['light2'] == answer['correct2'])
        accuracy = (correct_pairs / total_pairs) * 100
        
        results_data['tests_completed'].append({
            'test': 'Lantern Test',
            'score': f"{correct_pairs}/{total_pairs}",
            'accuracy': f"{accuracy:.1f}%",
            'status': 'PASS' if (total_pairs - correct_pairs) <= 1 else 'FAIL',
            'assessment': 'Excellent color recognition' if (total_pairs - correct_pairs) <= 1 else 'Needs improvement'
        })
    
    # Ishihara test results (simplified)
    if st.session_state.get('user_answers'):
        user_answers = st.session_state.user_answers
        plates_answered = len([v for v in user_answers.values() if v.strip()])
        results_data['tests_completed'].append({
            'test': 'Ishihara Test',
            'score': f"{plates_answered}/24",
            'accuracy': 'Analysis required',
            'status': 'IN PROGRESS' if plates_answered < 24 else 'COMPLETED',
            'assessment': f'{plates_answered} plates completed'
        })
    
    # ECDIS test results
    if st.session_state.get('ecdis_scores'):
        ecdis_scores = st.session_state.ecdis_scores
        avg_score = sum(ecdis_scores) / len(ecdis_scores) if ecdis_scores else 0
        max_score = len(ECDIS_FM_COLORS[0]) * 2
        accuracy = (avg_score / max_score) * 100
        
        results_data['tests_completed'].append({
            'test': 'ECDIS Hue Test',
            'score': f"{avg_score:.1f}/{max_score}",
            'accuracy': f"{accuracy:.1f}%",
            'status': 'COMPLETED',
            'assessment': 'Good color discrimination' if accuracy > 70 else 'Needs practice'
        })
    
    # Display results
    if results_data['tests_completed']:
        st.markdown("#### Test Summary")
        results_df = pd.DataFrame(results_data['tests_completed'])
        st.dataframe(results_df, use_container_width=True)
        
        # Overall assessment
        st.markdown("#### OVERALL ASSESSMENT")
        passed_tests = sum(1 for test in results_data['tests_completed'] if test['status'] == 'PASS')
        total_tests = len(results_data['tests_completed'])
        
        if passed_tests == total_tests:
            st.success(f"**OVERALL RESULT: PASS** - {passed_tests}/{total_tests} tests completed successfully")
        else:
            st.warning(f"**OVERALL RESULT: INCOMPLETE** - {passed_tests}/{total_tests} tests passed")
        
        # Certificate generation
        st.markdown("---")
        st.markdown("#### GENERATE CERTIFICATE")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate PDF Certificate", use_container_width=True, type="primary"):
                st.success("Certificate generation feature will be implemented in the next update!")
        
        with col2:
            if st.button("Email Results", use_container_width=True):
                st.info("Email feature will be implemented in the next update!")
    else:
        st.info("No test results available. Complete at least one test to see results.")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with col2:
        if st.button("Start New Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key not in ['user_name', 'user_id', 'user_position']:
                    del st.session_state[key]
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