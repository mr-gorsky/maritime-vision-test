# Maritime Color Vision Test - Complete Suite
# Copyright © Toni Mandušić 2025

import streamlit as st
import pandas as pd
import os
import random
import numpy as np
from streamlit_drag_and_drop import DragAndDrop

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
    # ... (ostali plateovi)
}

# Lantern test colors
LANTERN_COLORS = {
    'red': {'name': 'Red', 'hex': '#FF0000', 'description': 'Signal red'},
    'green': {'name': 'Green', 'hex': '#00FF00', 'description': 'Signal green'}, 
    'yellow': {'name': 'Yellow', 'hex': '#FFD200', 'description': 'Navigation yellow'},
    'white': {'name': 'White', 'hex': '#FFFFFF', 'description': 'Neutral white'}
}

LANTERN_SEQUENCES = [
    ('red', 'green'), ('red', 'white'), ('green', 'white'),
    ('yellow', 'yellow'), ('red', 'red'), ('green', 'green'),
    ('white', 'white'), ('red', 'yellow'), ('green', 'yellow')
]

# ECDIS Color Palettes
ECDIS_PALETTES = {
    'day': {
        'sea': '#AEE9FF', 'land': '#E5D8A6', 'depth_contours': '#0076BF',
        'text': '#000000', 'danger': '#FF4444', 'safe': '#44FF44', 'navigation_aids': '#FFAA00'
    },
    'dusk': {
        'sea': '#3E6079', 'land': '#927A48', 'depth_contours': '#4E9ED9',
        'text': '#FFFFFF', 'danger': '#FF6666', 'safe': '#66FF66', 'navigation_aids': '#FFBB44'
    },
    'night': {
        'sea': '#000A1A', 'land': '#4A2E00', 'depth_contours': '#1E3C66',
        'text': '#FFFFA8', 'danger': '#FF8888', 'safe': '#88FF88', 'navigation_aids': '#FFCC66'
    }
}

ECDIS_QUESTIONS = [
    {'question': 'Identify the DANGER zone', 'correct_color': 'danger', 'description': 'Red tones'},
    {'question': 'Identify the SAFE channel', 'correct_color': 'safe', 'description': 'Green tones'},
    {'question': 'Find the LAND area', 'correct_color': 'land', 'description': 'Beige/brown tones'},
    {'question': 'Locate DEPTH CONTOURS', 'correct_color': 'depth_contours', 'description': 'Blue tones'},
    {'question': 'Identify NAVIGATION AIDS', 'correct_color': 'navigation_aids', 'description': 'Yellow/orange tones'},
    {'question': 'Find the SEA area', 'correct_color': 'sea', 'description': 'Blue tones'}
]

# FM100 Hue Test Colors (standardne FM100 nijanse)
FM100_COLORS = [
    '#FF0000', '#FF2A00', '#FF5500', '#FF8000', '#FFAA00',
    '#FFD500', '#FFFF00', '#D4FF00', '#AAFF00', '#80FF00',
    '#55FF00', '#2AFF00', '#00FF00', '#00FF2A', '#00FF55',
    '#00FF80', '#00FFAA', '#00FFD5', '#00FFFF', '#00D4FF',
    '#00AAFF', '#0080FF', '#0055FF', '#002AFF', '#0000FF',
    '#2A00FF', '#5500FF', '#8000FF', '#AA00FF', '#D400FF',
    '#FF00FF', '#FF00D4', '#FF00AA', '#FF0080', '#FF0055',
    '#FF002A'
]

def ishihara_test():
    # ... (ostavi postojeću implementaciju) ...
    pass

def lantern_test():
    # ... (ostavi postojeću implementaciju) ...
    pass

def ecdis_test():
    # ... (ostavi postojeću implementaciju) ...
    pass

def fm100_test():
    st.header("🌈 FM100 Hue Test")
    st.write("**Color Discrimination Ability**")
    
    # Initialize session state
    if 'fm100_colors' not in st.session_state:
        st.session_state.fm100_colors = FM100_COLORS.copy()
        random.shuffle(st.session_state.fm100_colors)
        st.session_state.fm100_original_order = FM100_COLORS.copy()
        st.session_state.fm100_user_order = []
        st.session_state.fm100_test_started = False
        st.session_state.fm100_test_completed = False
    
    if not st.session_state.fm100_test_started:
        st.info("""
        **FM100 Hue Test Instructions:**
        - Arrange the color caps in natural color order
        - Drag and drop colors to create a smooth gradient
        - Start from red, through green, blue, and back to red
        - Take your time - there's no time limit
        - Your arrangement will be scored for accuracy
        """)
        
        if st.button("Start FM100 Test", type="primary"):
            st.session_state.fm100_test_started = True
            st.session_state.fm100_user_order = st.session_state.fm100_colors.copy()
            st.rerun()
        return
    
    if st.session_state.fm100_test_completed:
        show_fm100_results()
        return
    
    st.subheader("Arrange Colors in Hue Order")
    
    # Display current arrangement
    st.write("**Your current arrangement:**")
    
    # Create a grid of draggable color boxes
    cols = st.columns(6)
    user_order = st.session_state.fm100_user_order
    
    for i, color in enumerate(user_order):
        col_idx = i % 6
        with cols[col_idx]:
            st.markdown(
                f"""
                <div style='
                    background-color: {color};
                    height: 60px;
                    border: 2px solid #333;
                    border-radius: 8px;
                    margin: 5px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: grab;
                '>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Simple drag and drop simulation using selectboxes
    st.write("**Rearrange colors:**")
    st.info("Select two colors to swap their positions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        color1_idx = st.selectbox(
            "Select first color:",
            range(len(user_order)),
            format_func=lambda x: f"Color {x+1}",
            key="fm100_color1"
        )
    
    with col2:
        color2_idx = st.selectbox(
            "Select second color:",
            range(len(user_order)),
            format_func=lambda x: f"Color {x+1}",
            key="fm100_color2"
        )
    
    if st.button("Swap Colors"):
        if color1_idx != color2_idx:
            user_order[color1_idx], user_order[color2_idx] = user_order[color2_idx], user_order[color1_idx]
            st.session_state.fm100_user_order = user_order
            st.rerun()
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔀 Shuffle Colors"):
            random.shuffle(st.session_state.fm100_user_order)
            st.rerun()
    
    with col2:
        if st.button("🏠 Finish Test"):
            st.session_state.current_page = "home"
            st.session_state.fm100_test_started = False
            st.rerun()
    
    with col3:
        if st.button("📊 Complete Test", type="primary"):
            st.session_state.fm100_test_completed = True
            st.rerun()
    
    # Reference gradient
    st.write("**Reference gradient (correct order):**")
    ref_cols = st.columns(36)
    for i, color in enumerate(st.session_state.fm100_original_order):
        with ref_cols[i]:
            st.markdown(
                f"<div style='background-color: {color}; height: 20px; border: 1px solid #333;'></div>",
                unsafe_allow_html=True
            )

def show_fm100_results():
    st.header("📊 FM100 Hue Test Results")
    
    user_order = st.session_state.fm100_user_order
    correct_order = st.session_state.fm100_original_order
    
    # Calculate Total Error Score (TES)
    error_score = calculate_fm100_score(user_order, correct_order)
    
    st.subheader("Your Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Error Score", f"{error_score}")
    
    with col2:
        max_score = 200  # Maximum possible error score
        accuracy = max(0, 100 - (error_score / max_score * 100))
        st.metric("Accuracy", f"{accuracy:.1f}%")
    
    with col3:
        if error_score <= 20:
            performance = "Excellent"
        elif error_score <= 40:
            performance = "Good"
        elif error_score <= 60:
            performance = "Fair"
        else:
            performance = "Needs Improvement"
        st.metric("Performance", performance)
    
    # Display comparison
    st.subheader("Color Arrangement Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Your arrangement:**")
        cols = st.columns(6)
        for i, color in enumerate(user_order):
            col_idx = i % 6
            with cols[col_idx]:
                st.markdown(
                    f"<div style='background-color: {color}; height: 40px; border: 1px solid #333; margin: 2px;'></div>",
                    unsafe_allow_html=True
                )
    
    with col2:
        st.write("**Correct arrangement:**")
        cols = st.columns(6)
        for i, color in enumerate(correct_order):
            col_idx = i % 6
            with cols[col_idx]:
                st.markdown(
                    f"<div style='background-color: {color}; height: 40px; border: 1px solid #333; margin: 2px;'></div>",
                    unsafe_allow_html=True
                )
    
    # Error analysis
    st.subheader("Error Analysis")
    
    if error_score <= 20:
        st.success("""
        ✅ **EXCELLENT COLOR DISCRIMINATION**
        
        Your results indicate excellent color discrimination ability.
        You can distinguish subtle hue differences very well.
        """)
    elif error_score <= 40:
        st.info("""
        🔷 **GOOD COLOR DISCRIMINATION**
        
        Your color discrimination is good for most tasks.
        Minor difficulties with very subtle hue variations.
        """)
    elif error_score <= 60:
        st.warning("""
        ⚠️ **FAIR COLOR DISCRIMINATION**
        
        You may experience some difficulties with color matching tasks.
        Consider practice with color discrimination exercises.
        """)
    else:
        st.error("""
        ❌ **COLOR DISCRIMINATION DIFFICULTIES**
        
        Significant difficulties with hue discrimination detected.
        Consult eye care professional for comprehensive assessment.
        """)
    
    if st.button("🔄 Take FM100 Test Again"):
        st.session_state.fm100_test_started = False
        st.session_state.fm100_test_completed = False
        random.shuffle(st.session_state.fm100_colors)
        st.session_state.fm100_user_order = st.session_state.fm100_colors.copy()
        st.rerun()

def calculate_fm100_score(user_order, correct_order):
    """Calculate FM100 Total Error Score"""
    score = 0
    
    # Find positions in correct order
    user_positions = []
    for color in user_order:
        user_positions.append(correct_order.index(color))
    
    # Calculate sum of absolute differences between adjacent colors
    for i in range(len(user_positions) - 1):
        score += abs(user_positions[i] - user_positions[i + 1])
    
    return score

def show_ishihara_results():
    # ... (ostavi postojeću implementaciju) ...
    pass

def show_lantern_results():
    # ... (ostavi postojeću implementaciju) ...
    pass

def show_ecdis_results():
    # ... (ostavi postojeću implementaciju) ...
    pass

def main():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    
    st.title("🚢 Maritime Color Vision Test")
    
    if st.session_state.current_page == "home":
        st.subheader("Professional Color Vision Testing Suite")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("👁️ Ishihara Test", use_container_width=True):
                st.session_state.current_page = "ishihara"
                st.rerun()
        
        with col2:
            if st.button("🎯 Lantern Test", use_container_width=True):
                st.session_state.current_page = "lantern"
                st.rerun()
        
        with col3:
            if st.button("🗺️ ECDIS Test", use_container_width=True):
                st.session_state.current_page = "ecdis"
                st.rerun()
        
        with col4:
            if st.button("🌈 FM100 Test", use_container_width=True):
                st.session_state.current_page = "fm100"
                st.rerun()
        
        st.divider()
        st.markdown("**Copyright © Toni Mandušić 2025**")
    
    elif st.session_state.current_page == "ishihara":
        ishihara_test()
    
    elif st.session_state.current_page == "lantern":
        lantern_test()
    
    elif st.session_state.current_page == "ecdis":
        ecdis_test()
    
    elif st.session_state.current_page == "fm100":
        fm100_test()
    
    elif st.session_state.current_page == "results":
        show_ishihara_results()

if __name__ == "__main__":
    main()