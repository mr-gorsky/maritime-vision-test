# Maritime Color Vision Test - Professional Suite
# Copyright © Toni Mandusic 2025

import streamlit as st
import pandas as pd
import os
import random
import time
from datetime import datetime
from fpdf import FPDF
import base64
from io import BytesIO

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
    .lantern-display-container {
        background-color: #000000;
        padding: 80px 20px;
        border-radius: 8px;
        text-align: center;
        margin: 20px 0;
        border: 2px solid #333;
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .lantern-lights-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 100px;
        width: 100%;
    }
    .lantern-light {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .test-title {
        color: #1a3d7c;
        border-bottom: 2px solid #ffd700;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    /* Fix for selectbox jumping */
    .stSelectbox > div > div {
        transition: none !important;
    }
    /* Prevent layout shifts */
    .element-container {
        transition: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Test data - CORRECTED Ishihara interpretations according to PDF
# Using all plates EXCEPT: 3, 18, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38
ISHIHARA_DATA = {
    # Plate 1: Everyone sees 12
    1: {"normal": "12", "deutan": "12", "protan": "12"},
    
    # Plate 2: Normal vs Red-green deficiency
    2: {"normal": "8", "deutan": "3", "protan": "3"},
    
    # Plate 4-9: Normal vs Red-green deficiency
    4: {"normal": "29", "deutan": "70", "protan": "70"},
    5: {"normal": "57", "deutan": "35", "protan": "35"},
    6: {"normal": "5", "deutan": "2", "protan": "2"},
    7: {"normal": "3", "deutan": "5", "protan": "5"},
    8: {"normal": "15", "deutan": "17", "protan": "17"},
    9: {"normal": "74", "deutan": "21", "protan": "21"},
    
    # Plates 10-17: Normal sees number, colorblind sees nothing/wrong
    10: {"normal": "2", "deutan": "", "protan": ""},
    11: {"normal": "6", "deutan": "", "protan": ""},
    12: {"normal": "97", "deutan": "", "protan": ""},
    13: {"normal": "45", "deutan": "", "protan": ""},
    14: {"normal": "5", "deutan": "", "protan": ""},
    15: {"normal": "7", "deutan": "", "protan": ""},
    16: {"normal": "16", "deutan": "", "protan": ""},
    17: {"normal": "73", "deutan": "", "protan": ""},
    
    # Plates 19-21: Normal sees nothing, colorblind sees number
    19: {"normal": "", "deutan": "2", "protan": "2"},
    20: {"normal": "", "deutan": "45", "protan": "45"},
    21: {"normal": "", "deutan": "73", "protan": "73"},
    
    # Plates 22-25: Different numbers for different types
    22: {"normal": "26", "deutan": "2", "protan": "6"},
    23: {"normal": "42", "deutan": "4", "protan": "2"},
    24: {"normal": "35", "deutan": "3", "protan": "5"},
    25: {"normal": "96", "deutan": "9", "protan": "6"}
}

# List of plates we're actually using (all except excluded ones)
USED_PLATES = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25]
TOTAL_PLATES = len(USED_PLATES)

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

# RADAR COLOR TEST DATA - DODANO
RADAR_COLORS = {
    'critical_pairs': [
        ['#80FF80', '#80FF80'],  # identične
        ['#FF8080', '#FF6060'],  # vrlo slične crvene
        ['#80FF80', '#60FF60'],  # vrlo slične zelene  
        ['#FFD200', '#FFB000'],  # slične žute
        ['#FF8080', '#80FF80'],  # različite (crvena vs zelena)
        ['#FFD200', '#80FF80'],  # različite (žuta vs zelena)
    ],
    'intensity_scale': [
        '#004400', '#006600', '#008800', '#00AA00', '#00CC00', '#00EE00', '#80FF80', '#FFFFFF'
    ],
    'contrast_targets': [
        {'bg': '#000818', 'target': '#80FF80', 'visible': True},
        {'bg': '#000818', 'target': '#404040', 'visible': False},
        {'bg': '#1A3D7C', 'target': '#80FF80', 'visible': True},
        {'bg': '#1A3D7C', 'target': '#606060', 'visible': False},
    ]
}

class CertificatePDF(FPDF):
    def header(self):
        # Logo
        self.image('https://i.postimg.cc/L8cW5X4H/phant-logo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 18)
        self.cell(0, 10, 'MARITIME COLOR VISION CERTIFICATE', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_certificate(user_data, test_results):
    pdf = CertificatePDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 20, 'CERTIFICATE OF COLOR VISION ASSESSMENT', 0, 1, 'C')
    pdf.ln(10)
    
    # Candidate Information
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'CANDIDATE INFORMATION', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    
    # FIX: Encode text to Latin-1 and replace unsupported characters
    def safe_text(text):
        if isinstance(text, str):
            # Replace problematic characters
            text = text.encode('latin-1', 'replace').decode('latin-1')
        return str(text)
    
    pdf.cell(0, 8, f'Name: {safe_text(user_data["name"])}', 0, 1)
    pdf.cell(0, 8, f'ID: {safe_text(user_data["id"])}', 0, 1)
    pdf.cell(0, 8, f'Position: {safe_text(user_data["position"])}', 0, 1)
    pdf.cell(0, 8, f'Date of Assessment: {safe_text(user_data["date"])}', 0, 1)
    pdf.ln(10)
    
    # Test Results
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'TEST RESULTS SUMMARY', 0, 1, 'L')
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(60, 10, 'Test', 1, 0, 'C')
    pdf.cell(40, 10, 'Score', 1, 0, 'C')
    pdf.cell(40, 10, 'Accuracy', 1, 0, 'C')
    pdf.cell(50, 10, 'Status', 1, 1, 'C')
    
    pdf.set_font('Arial', '', 11)
    for test in test_results:
        pdf.cell(60, 10, safe_text(test['test']), 1, 0, 'L')
        pdf.cell(40, 10, safe_text(test['score']), 1, 0, 'C')
        pdf.cell(40, 10, safe_text(test['accuracy']), 1, 0, 'C')
        status_color = (0, 128, 0) if test['status'] == 'PASS' else (255, 0, 0)
        pdf.set_text_color(*status_color)
        pdf.cell(50, 10, safe_text(test['status']), 1, 1, 'C')
        pdf.set_text_color(0, 0, 0)
    
    pdf.ln(10)
    
    # Overall Assessment
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'OVERALL ASSESSMENT', 0, 1, 'L')
    
    passed_tests = sum(1 for test in test_results if test['status'] == 'PASS')
    total_tests = len(test_results)
    
    if passed_tests == total_tests:
        pdf.set_text_color(0, 128, 0)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 12, 'OVERALL RESULT: PASS', 0, 1, 'L')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 8, safe_text('The candidate has demonstrated satisfactory color vision capabilities for maritime duties. Performance meets IMO standards for navigation and lookout responsibilities.'))
    else:
        pdf.set_text_color(255, 0, 0)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 12, 'OVERALL RESULT: FAIL', 0, 1, 'L')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 8, safe_text('The candidate has not met the required standards for color vision in maritime operations. Further professional assessment is recommended.'))
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    
    # Professional Endorsement
    pdf.set_font('Arial', 'I', 10)
    pdf.multi_cell(0, 8, safe_text('This certificate is issued based on computerized color vision assessment. For official medical certification, consult a qualified maritime medical examiner.'))
    
    # Signature area
    pdf.ln(20)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Maritime Color Vision Test System', 0, 1, 'C')
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, 'Copyright © Toni Mandusic 2025', 0, 1, 'C')
    
    return pdf

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
        # Logo povećan za 50% (sa 150 na 225)
        st.markdown(
            '<div style="text-align: right; padding-top: 0.5rem;"><img src="https://i.postimg.cc/L8cW5X4H/phant-logo.png" width="225"></div>',
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
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="test-card">
            <h3>LANTERN TEST</h3>
            <p>Navigation light recognition</p>
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
            <p>Navigation color discrimination</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start ECDIS Test", key="ecdis_home", use_container_width=True, type="primary"):
            if validate_user_info():
                st.session_state.current_page = "ecdiscfm"
                st.rerun()
    
    # DODANO: Radar test card
    with col4:
        st.markdown("""
        <div class="test-card">
            <h3>RADAR COLOR TEST</h3>
            <p>Radar color discrimination</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Radar Test", key="radar_home", use_container_width=True, type="primary"):
            if validate_user_info():
                st.session_state.current_page = "radar_simple"
                st.rerun()
    
    # Quick navigation between tests if already started
    if any(key in st.session_state for key in ['lantern_answers', 'user_answers', 'ecdis_scores', 'radar_scores']):
        st.markdown("---")
        st.markdown("### CONTINUE TESTING")
        col1, col2, col3, col4 = st.columns(4)
        
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
        
        # DODANO: Continue Radar Test
        with col4:
            if st.session_state.get('radar_scores'):
                if st.button("Continue Radar Test", use_container_width=True):
                    st.session_state.current_page = "radar_simple"
                    st.rerun()
    
    render_footer()

def validate_user_info():
    if not st.session_state.get('user_name') or not st.session_state.get('user_id'):
        st.error("❌ Please complete personal information before starting tests")
        return False
    return True

def initialize_lantern_test():
    if 'lantern_pair_start_time' not in st.session_state:
        st.session_state.lantern_pair_start_time = time.time()
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
    
    # FIXED TIMER LOGIC - 10 seconds fixed, no warnings
    if 'lantern_pair_start_time' not in st.session_state:
        st.session_state.lantern_pair_start_time = time.time()
    
    elapsed_time = time.time() - st.session_state.lantern_pair_start_time
    time_remaining = max(0, 10 - elapsed_time)  # 10 seconds fixed
    
    # Display simple countdown timer
    st.markdown(f"**Time remaining: {time_remaining:.1f}s**")
    st.progress(time_remaining / 10)
    
    color1, color2 = sequence[current_pair]
    color1_data = LANTERN_COLORS[color1]
    color2_data = LANTERN_COLORS[color2]
    
    st.markdown(f"**Light Pair {current_pair + 1} of {len(sequence)}**")
    
    # Lantern display
    lantern_html = f"""
    <div class="lantern-display-container">
        <div class="lantern-lights-wrapper">
            <div class="lantern-light">
                <div style="width: 96px; height: 96px; border-radius: 50%; background-color: {color1_data['hex']}; margin: 0 auto; box-shadow: 0 0 40px {color1_data['hex']}80; border: 3px solid #555;"></div>
                <div style="color: white; margin-top: 15px; font-size: 16px;">LIGHT 1</div>
            </div>
            <div class="lantern-light">
                <div style="width: 96px; height: 96px; border-radius: 50%; background-color: {color2_data['hex']}; margin: 0 auto; box-shadow: 0 0 40px {color2_data['hex']}80; border: 3px solid #555;"></div>
                <div style="color: white; margin-top: 15px; font-size: 16px;">LIGHT 2</div>
            </div>
        </div>
    </div>
    """
    st.markdown(lantern_html, unsafe_allow_html=True)
    
    # Auto-advance after 10 seconds
    if time_remaining <= 0:
        st.session_state.lantern_current_pair += 1
        st.session_state.lantern_pair_start_time = time.time()
        st.rerun()
    
    # Answer section
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            light1_answer = st.selectbox("Light 1 Color:", ["Select color", "Red", "Green", "Yellow", "White"], 
                                       key=f"lantern_1_{current_pair}")
        with col2:
            light2_answer = st.selectbox("Light 2 Color:", ["Select color", "Red", "Green", "Yellow", "White"], 
                                       key=f"lantern_2_{current_pair}")
    
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
            st.session_state.lantern_pair_start_time = time.time()
            st.rerun()
    with col2:
        if st.button("Skip", use_container_width=True):
            st.session_state.lantern_current_pair += 1
            st.session_state.lantern_pair_start_time = time.time()
            st.rerun()
    with col3:
        if st.button("Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with col4:
        if st.button("Next →", use_container_width=True, type="primary"):
            st.session_state.lantern_current_pair += 1
            st.session_state.lantern_pair_start_time = time.time()
            st.rerun()

def ishihara_test():
    render_header()
    show_user_panel()
    st.markdown("### ISHIHARA TEST")
    
    # Dodaj custom CSS za kontrolu veličine slika
    st.markdown("""
    <style>
    .ishihara-image img {
        width: 300px !important;
        height: auto !important;
        max-width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if 'current_plate' not in st.session_state:
        st.session_state.current_plate = 0
        st.session_state.user_answers = {}
        st.session_state.ishihara_score = 0
    
    current_index = st.session_state.current_plate
    plate_number = USED_PLATES[current_index]
    plate_data = ISHIHARA_DATA[plate_number]
    
    st.markdown(f"**Plate {current_index + 1} of {TOTAL_PLATES}**")
    st.progress((current_index + 1) / TOTAL_PLATES)
    
    # Center the image with reduced size
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        image_path = f"assets/ishihara_plates/plate{plate_number}.png"
        if os.path.exists(image_path):
            # Koristi st.image s CSS klasom
            st.markdown('<div class="ishihara-image">', unsafe_allow_html=True)
            st.image(image_path, use_column_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
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
    
    # Navigation (ostaje isto kao gore)
    # ... navigation code ...

def calculate_ishihara_score():
    """Calculate Ishihara test score based on correct answers"""
    score = 0
    user_answers = st.session_state.user_answers
    
    for plate_num in USED_PLATES:
        user_answer = user_answers.get(plate_num, "").strip()
        plate_data = ISHIHARA_DATA[plate_num]
        
        # For plates where normal vision sees a number
        if plate_data["normal"] != "":
            if user_answer == plate_data["normal"]:
                score += 1
        # For plates where normal vision sees nothing (plates 19-21)
        else:
            if user_answer == "":
                score += 1
    
    return score

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
                # Calculate score for current group before moving to next
                calculate_ecdis_group_score(current_group)
                st.session_state.ecdis_current_group += 1
                st.session_state.ecdis_selected_color = None
                st.rerun()
        else:
            if st.button("See Results", use_container_width=True, type="primary"):
                # Calculate score for final group
                calculate_ecdis_group_score(current_group)
                st.session_state.current_page = "results"
                st.rerun()

def calculate_ecdis_group_score(group_index):
    """Calculate score for ECDIS group based on correct ordering"""
    user_order = st.session_state.ecdis_user_orders[group_index]
    correct_order = ECDIS_FM_COLORS[group_index]
    
    score = 0
    max_score = len(correct_order)
    
    # Simple scoring: count how many colors are in correct position
    for i, color in enumerate(user_order):
        if color == correct_order[i]:
            score += 1
    
    st.session_state.ecdis_scores[group_index] = score

def move_ecdis_color(selected_color, target_position):
    current_group = st.session_state.ecdis_current_group
    user_order = st.session_state.ecdis_user_orders[current_group]
    current_position = user_order.index(selected_color)
    user_order.pop(current_position)
    user_order.insert(target_position, selected_color)

# DODANO: RADAR SIMPLE TEST FUNCTIONS
def radar_simple_test():
    render_header()
    show_user_panel()
    st.markdown("### RADAR COLOR DISCRIMINATION TEST")
    
    if 'radar_current_test' not in st.session_state:
        st.session_state.radar_current_test = 0
        st.session_state.radar_scores = [0, 0, 0, 0]  # 4 podtesta
        st.session_state.radar_start_time = time.time()
    
    current_test = st.session_state.radar_current_test
    test_types = ["Critical Color Pairs", "Intensity Ordering", "Contrast Detection", "Night Mode"]
    
    st.markdown(f"**{test_types[current_test]}** - Test {current_test + 1} of 4")
    st.progress((current_test + 1) / 4)
    
    if current_test == 0:
        critical_color_pairs_test()
    elif current_test == 1:
        intensity_ordering_test()
    elif current_test == 2:
        contrast_detection_test()
    elif current_test == 3:
        night_mode_test()
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with col2:
        if current_test > 0 and st.button("← Previous", use_container_width=True):
            st.session_state.radar_current_test -= 1
            st.rerun()
    with col3:
        if current_test < 3 and st.button("Next →", use_container_width=True, type="primary"):
            st.session_state.radar_current_test += 1
            st.rerun()
        elif current_test == 3 and st.button("See Results", use_container_width=True, type="primary"):
            st.session_state.current_page = "results"
            st.rerun()

def critical_color_pairs_test():
    st.markdown("**Are these two colors THE SAME or DIFFERENT?**")
    
    if 'radar_pair_index' not in st.session_state:
        st.session_state.radar_pair_index = 0
        st.session_state.radar_pair_answers = []
    
    pair_idx = st.session_state.radar_pair_index
    pairs = RADAR_COLORS['critical_pairs']
    
    if pair_idx >= len(pairs):
        # Calculate score
        correct = sum(st.session_state.radar_pair_answers)
        st.session_state.radar_scores[0] = correct
        st.success(f"Test completed! Score: {correct}/{len(pairs)}")
        return
    
    color1, color2 = pairs[pair_idx]
    is_same = color1 == color2
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div style="height:100px; background:{color1}; border-radius:8px; border:2px solid #333;"></div>', 
                   unsafe_allow_html=True)
        st.markdown("<div style='text-align:center'>Color A</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="height:100px; background:{color2}; border-radius:8px; border:2px solid #333;"></div>', 
                   unsafe_allow_html=True)
        st.markdown("<div style='text-align:center'>Color B</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("SAME COLORS", use_container_width=True, key=f"same_{pair_idx}"):
            st.session_state.radar_pair_answers.append(is_same == True)
            st.session_state.radar_pair_index += 1
            st.rerun()
    with col2:
        if st.button("DIFFERENT COLORS", use_container_width=True, key=f"diff_{pair_idx}"):
            st.session_state.radar_pair_answers.append(is_same == False)
            st.session_state.radar_pair_index += 1
            st.rerun()
    
    st.markdown(f"**Progress: {pair_idx + 1}/{len(pairs)} pairs**")

def intensity_ordering_test():
    st.markdown("**Arrange radar colors from WEAKEST to STRONGEST signal**")
    
    if 'radar_order_user' not in st.session_state:
        colors = RADAR_COLORS['intensity_scale'].copy()
        random.shuffle(colors)
        st.session_state.radar_order_user = colors
        st.session_state.radar_selected_color = None
    
    user_order = st.session_state.radar_order_user
    selected_color = st.session_state.radar_selected_color
    
    # Color grid
    cols = st.columns(8)
    for i, color in enumerate(user_order):
        with cols[i]:
            border_color = "#FF0000" if color == selected_color else "#333333"
            border_width = "3px" if color == selected_color else "1px"
            
            if st.button("", key=f"radar_color_{i}"):
                if selected_color is None:
                    st.session_state.radar_selected_color = color
                else:
                    # Move color
                    current_idx = user_order.index(selected_color)
                    user_order.pop(current_idx)
                    user_order.insert(i, selected_color)
                    st.session_state.radar_selected_color = None
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
    
    # Check order button
    if st.button("Check Order", type="primary", key="radar_check_order"):
        correct_order = RADAR_COLORS['intensity_scale']
        score = 0
        for i, color in enumerate(user_order):
            if color == correct_order[i]:
                score += 1
        st.session_state.radar_scores[1] = score
        st.success(f"Ordering score: {score}/8 correct positions")

def contrast_detection_test():
    st.markdown("**Can you detect the target in different background conditions?**")
    
    if 'radar_contrast_index' not in st.session_state:
        st.session_state.radar_contrast_index = 0
        st.session_state.radar_contrast_answers = []
    
    contrast_idx = st.session_state.radar_contrast_index
    contrasts = RADAR_COLORS['contrast_targets']
    
    if contrast_idx >= len(contrasts):
        correct = sum(st.session_state.radar_contrast_answers)
        st.session_state.radar_scores[2] = correct
        st.success(f"Contrast test completed! Score: {correct}/{len(contrasts)}")
        return
    
    contrast = contrasts[contrast_idx]
    
    # Display radar background with potential target
    st.markdown(f'<div style="height:200px; background:{contrast["bg"]}; border-radius:8px; border:2px solid #333; position:relative;">'
                f'<div style="width:40px; height:40px; background:{contrast["target"]}; border-radius:50%; position:absolute; top:80px; left:170px;"></div>'
                f'</div>', unsafe_allow_html=True)
    
    st.markdown("**Is there a visible target in the radar display?**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("YES, I see it", use_container_width=True, key=f"yes_{contrast_idx}"):
            st.session_state.radar_contrast_answers.append(contrast["visible"] == True)
            st.session_state.radar_contrast_index += 1
            st.rerun()
    with col2:
        if st.button("NO, not visible", use_container_width=True, key=f"no_{contrast_idx}"):
            st.session_state.radar_contrast_answers.append(contrast["visible"] == False)
            st.session_state.radar_contrast_index += 1
            st.rerun()
    
    st.markdown(f"**Progress: {contrast_idx + 1}/{len(contrasts)} scenarios**")

def night_mode_test():
    st.markdown("**Night Mode Detection**")
    st.markdown("Count how many targets you can see in this night radar display:")
    
    # FIXED: Spremi originalni broj meta prije nego što se prikaže rezultat
    if 'radar_night_original_targets' not in st.session_state:
        st.session_state.radar_night_original_targets = random.randint(1, 5)
        st.session_state.radar_night_start = time.time()
        st.session_state.radar_night_positions = []
        
        # Generate and store positions
        for i in range(st.session_state.radar_night_original_targets):
            x = random.randint(50, 350)
            y = random.randint(50, 250)
            st.session_state.radar_night_positions.append((x, y))
    
    num_targets = st.session_state.radar_night_original_targets
    positions = st.session_state.radar_night_positions
    
    # Create night radar display
    radar_html = '<div style="height:300px; background:#000818; border-radius:8px; border:2px solid #333; position:relative; margin:20px 0;">'
    
    # Add stored targets
    for x, y in positions:
        radar_html += f'<div style="width:12px; height:12px; background:#80FF80; border-radius:50%; position:absolute; top:{y}px; left:{x}px; box-shadow: 0 0 10px #80FF80;"></div>'
    
    radar_html += '</div>'
    st.markdown(radar_html, unsafe_allow_html=True)
    
    # User input
    user_guess = st.number_input("How many targets do you see?", min_value=0, max_value=10, value=0, key="radar_night_guess")
    
    if st.button("Submit Answer", type="primary", key="radar_night_submit"):
        reaction_time = time.time() - st.session_state.radar_night_start
        score = 5 - abs(user_guess - num_targets)  # 5 points minus difference
        score = max(0, score)
        st.session_state.radar_scores[3] = score
        
        # FIXED: Prikaži ispravne rezultate
        st.success(f"**Correct answer: {num_targets} targets** | **Your answer: {user_guess}**")
        st.info(f"Reaction time: {reaction_time:.1f}s | Score: {score}/5")
        
        # Clear for next test
        if 'radar_night_original_targets' in st.session_state:
            del st.session_state.radar_night_original_targets
        if 'radar_night_positions' in st.session_state:
            del st.session_state.radar_night_positions

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
        st.success("""**✅ EXCELLENT - Suitable for Maritime Duties**
        
Your performance meets IMO standards for color vision requirements in navigation and lookout duties. 
You demonstrate excellent ability to recognize navigation lights under simulated low-light conditions.""")
    elif errors <= 2:
        st.warning("""**⚠️ BORDERLINE - Further Assessment Recommended**
        
Your results indicate minor difficulties with color recognition that may affect performance 
in challenging conditions. Consider retesting or professional evaluation.""")
    else:
        st.error("""**❌ UNSATISFACTORY - Not Suitable for Color-Critical Duties**
        
Significant difficulties with navigation light recognition detected. 
Consult an eye care specialist for comprehensive assessment before undertaking maritime duties.""")
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Retest Lantern", use_container_width=True):
            st.session_state.lantern_current_pair = 0
            st.session_state.lantern_answers = {}
            st.session_state.lantern_sequence = random.sample(LANTERN_SEQUENCES, len(LANTERN_SEQUENCES))
            st.session_state.lantern_pair_start_time = time.time()
            st.rerun()
    with col2:
        if st.button("Back to Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with col3:
        if st.button("All Results", use_container_width=True, type="primary"):
            st.session_state.current_page = "results"
            st.rerun()

def create_download_link(pdf_output, filename):
    """Generate a download link for PDF"""
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download Certificate</a>'
    return href

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
    
    # Ishihara test results
    if st.session_state.get('user_answers'):
        ishihara_score = st.session_state.get('ishihara_score', 0)
        total_plates = TOTAL_PLATES
        
        # Determine Ishihara status (simplified logic)
        if ishihara_score >= 18:  # Normal color vision typically scores high
            ishihara_status = 'PASS'
            assessment = 'Normal color vision'
        else:
            ishihara_status = 'FAIL' 
            assessment = 'Possible color deficiency'
        
        results_data['tests_completed'].append({
            'test': 'Ishihara Test',
            'score': f"{ishihara_score}/{total_plates}",
            'accuracy': f"{(ishihara_score/total_plates)*100:.1f}%",
            'status': ishihara_status,
            'assessment': assessment
        })
    
    # ECDIS test results - FIXED scoring
    if st.session_state.get('ecdis_scores'):
        ecdis_scores = st.session_state.ecdis_scores
        total_score = sum(ecdis_scores)
        max_possible_score = len(ECDIS_FM_COLORS) * len(ECDIS_FM_COLORS[0])  # 7 groups * 8 colors
        accuracy = (total_score / max_possible_score) * 100
        
        # Determine ECDIS status
        if accuracy >= 80:  # 80% accuracy required for pass
            ecdis_status = 'PASS'
            assessment = 'Good color discrimination'
        else:
            ecdis_status = 'FAIL'
            assessment = 'Needs practice'
        
        results_data['tests_completed'].append({
            'test': 'ECDIS Hue Test',
            'score': f"{total_score}/{max_possible_score}",
            'accuracy': f"{accuracy:.1f}%",
            'status': ecdis_status,
            'assessment': assessment
        })
    
    # DODANO: Radar test results
    if st.session_state.get('radar_scores'):
        radar_total = sum(st.session_state.radar_scores)
        radar_max = 6 + 8 + 4 + 5  # Max scores from each subtest
        accuracy = (radar_total / radar_max) * 100
        
        # Determine Radar status
        if accuracy >= 80:  # 80% accuracy required for pass
            radar_status = 'PASS'
            assessment = 'Good radar color discrimination'
        else:
            radar_status = 'FAIL'
            assessment = 'Needs improvement'
        
        results_data['tests_completed'].append({
            'test': 'Radar Color Test',
            'score': f"{radar_total}/{radar_max}",
            'accuracy': f"{accuracy:.1f}%",
            'status': radar_status,
            'assessment': assessment
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
        
        # Check if all tests are PASS for certificate generation
        all_passed = all(test['status'] == 'PASS' for test in results_data['tests_completed'])
        
        if all_passed:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Generate PDF Certificate", use_container_width=True, type="primary"):
                    try:
                        # Prepare data for certificate
                        user_data = {
                            'name': results_data['user_name'],
                            'id': results_data['user_id'],
                            'position': results_data['position'],
                            'date': results_data['date']
                        }
                        
                        # Generate PDF
                        pdf = generate_certificate(user_data, results_data['tests_completed'])
                        
                        # Save to bytes buffer
                        pdf_bytes = pdf.output(dest='S').encode('latin1')
                        
                        # Create download link
                        st.markdown(create_download_link(pdf_bytes, 
                            f"Color_Vision_Certificate_{results_data['user_name'].replace(' ', '_')}.pdf"), 
                            unsafe_allow_html=True)
                        st.success("✅ Certificate generated successfully! Click the download link above.")
                    except Exception as e:
                        st.error(f"❌ Error generating certificate: {str(e)}")
                        st.info("Please try again with simpler text (avoid special characters)")
            
            with col2:
                if st.button("Email Results", use_container_width=True):
                    st.info("Email feature will be implemented in the next update!")
        else:
            st.warning("Certificate is only available when all tests are passed. Complete all tests with PASS status to generate your certificate.")
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
    elif st.session_state.current_page == "radar_simple":  # DODANO
        radar_simple_test()
    elif st.session_state.current_page == "results":
        show_results()

if __name__ == "__main__":
    main()