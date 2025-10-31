# Maritime Color Vision Test - Ishihara + Lantern + ECDIS Implementation
# Copyright © Toni Mandušić 2025

import streamlit as st
import pandas as pd
import os
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
    # ... (ostali plateovi - ostavi postojeće)
}

# Lantern test colors (IMO standard)
LANTERN_COLORS = {
    'red': {'name': 'Red', 'hex': '#FF0000', 'description': 'Signal red'},
    'green': {'name': 'Green', 'hex': '#00FF00', 'description': 'Signal green'}, 
    'yellow': {'name': 'Yellow', 'hex': '#FFD200', 'description': 'Navigation yellow'},
    'white': {'name': 'White', 'hex': '#FFFFFF', 'description': 'Neutral white'}
}

# Lantern test sequences
LANTERN_SEQUENCES = [
    ('red', 'green'), ('red', 'white'), ('green', 'white'),
    ('yellow', 'yellow'), ('red', 'red'), ('green', 'green'),
    ('white', 'white'), ('red', 'yellow'), ('green', 'yellow')
]

# ECDIS Color Palettes (IHO S-52 Standard)
ECDIS_PALETTES = {
    'day': {
        'sea': '#AEE9FF',
        'land': '#E5D8A6', 
        'depth_contours': '#0076BF',
        'text': '#000000',
        'danger': '#FF4444',
        'safe': '#44FF44',
        'navigation_aids': '#FFAA00'
    },
    'dusk': {
        'sea': '#3E6079',
        'land': '#927A48',
        'depth_contours': '#4E9ED9',
        'text': '#FFFFFF',
        'danger': '#FF6666',
        'safe': '#66FF66',
        'navigation_aids': '#FFBB44'
    },
    'night': {
        'sea': '#000A1A',
        'land': '#4A2E00',
        'depth_contours': '#1E3C66',
        'text': '#FFFFA8',
        'danger': '#FF8888',
        'safe': '#88FF88',
        'navigation_aids': '#FFCC66'
    }
}

# ECDIS Test Questions
ECDIS_QUESTIONS = [
    {
        'question': 'Identify the DANGER zone on the chart',
        'correct_color': 'danger',
        'description': 'Danger areas are marked in red tones'
    },
    {
        'question': 'Identify the SAFE navigation channel',
        'correct_color': 'safe', 
        'description': 'Safe channels are marked in green tones'
    },
    {
        'question': 'Find the LAND area on the chart',
        'correct_color': 'land',
        'description': 'Land is typically shown in beige/brown tones'
    },
    {
        'question': 'Locate the DEPTH CONTOURS',
        'correct_color': 'depth_contours',
        'description': 'Depth contours show water depth in blue tones'
    },
    {
        'question': 'Identify NAVIGATION AIDS (buoys, markers)',
        'correct_color': 'navigation_aids',
        'description': 'Navigation aids are shown in yellow/orange tones'
    },
    {
        'question': 'Find the SEA area on the chart',
        'correct_color': 'sea',
        'description': 'Sea areas are shown in blue tones'
    }
]

def ishihara_test():
    # ... (ostavi postojeću ishihara_test funkciju) ...
    pass

def lantern_test():
    # ... (ostavi postojeću lantern_test funkciju) ...
    pass

def ecdis_test():
    st.header("🗺️ ECDIS Color Recognition Test")
    st.write("**Electronic Chart Display Information System**")
    
    # Initialize session state for ECDIS test
    if 'ecdis_current_mode' not in st.session_state:
        st.session_state.ecdis_current_mode = 'day'
        st.session_state.ecdis_current_question = 0
        st.session_state.ecdis_answers = {}
        st.session_state.ecdis_question_order = random.sample(ECDIS_QUESTIONS, len(ECDIS_QUESTIONS))
    
    current_mode = st.session_state.ecdis_current_mode
    current_question_idx = st.session_state.ecdis_current_question
    question_order = st.session_state.ecdis_question_order
    
    if current_question_idx >= len(question_order):
        # Test completed
        show_ecdis_results()
        return
    
    current_question = question_order[current_question_idx]
    palette = ECDIS_PALETTES[current_mode]
    
    st.subheader(f"ECDIS {current_mode.title()} Mode - Question {current_question_idx + 1} of {len(question_order)}")
    
    # Display ECDIS simulation
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # ECDIS Chart Simulation
        st.markdown(
            f"""
            <div style='
                background-color: {palette['sea']};
                padding: 30px;
                border-radius: 10px;
                border: 2px solid #333;
                min-height: 400px;
                position: relative;
            '>
                <!-- Land Area -->
                <div style='
                    position: absolute;
                    top: 50px;
                    left: 50px;
                    width: 120px;
                    height: 80px;
                    background-color: {palette['land']};
                    border-radius: 5px;
                    border: 1px solid #666;
                '></div>
                
                <!-- Safe Channel -->
                <div style='
                    position: absolute;
                    top: 150px;
                    left: 200px;
                    width: 180px;
                    height: 30px;
                    background-color: {palette['safe']};
                    border: 2px dashed #333;
                '></div>
                
                <!-- Danger Zone -->
                <div style='
                    position: absolute;
                    top: 250px;
                    left: 100px;
                    width: 100px;
                    height: 100px;
                    background-color: {palette['danger']};
                    border: 2px solid #333;
                    border-radius: 50%;
                    opacity: 0.7;
                '></div>
                
                <!-- Depth Contours -->
                <div style='
                    position: absolute;
                    top: 100px;
                    left: 300px;
                    width: 200px;
                    height: 150px;
                    background: repeating-linear-gradient(
                        45deg,
                        transparent,
                        transparent 10px,
                        {palette['depth_contours']} 10px,
                        {palette['depth_contours']} 20px
                    );
                    border: 1px solid {palette['depth_contours']};
                '></div>
                
                <!-- Navigation Aids -->
                <div style='
                    position: absolute;
                    top: 300px;
                    left: 350px;
                    width: 40px;
                    height: 40px;
                    background-color: {palette['navigation_aids']};
                    border: 2px solid #333;
                    border-radius: 50%;
                '></div>
                
                <!-- Text Labels -->
                <div style='
                    position: absolute;
                    top: 20px;
                    left: 20px;
                    color: {palette['text']};
                    font-family: Arial, sans-serif;
                    font-weight: bold;
                '>
                    ECDIS Chart - {current_mode.title()} Mode
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.write("**Chart Elements:**")
        
        # Display color legend
        for color_name, color_hex in palette.items():
            if color_name != 'text':  # Don't show text color in legend
                st.markdown(
                    f"<div style='display: flex; align-items: center; margin: 5px 0;'>"
                    f"<div style='width: 20px; height: 20px; background-color: {color_hex}; border: 1px solid #333; margin-right: 10px;'></div>"
                    f"<span>{color_name.replace('_', ' ').title()}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
    
    # Question and answer section
    st.write(f"**{current_question['question']}**")
    st.write(f"*{current_question['description']}*")
    
    # Answer options
    color_options = list(palette.keys())
    color_options.remove('text')  # Remove text color from options
    
    user_answer = st.selectbox(
        "Select the corresponding chart element:",
        ["Select element"] + [opt.replace('_', ' ').title() for opt in color_options],
        key=f"ecdis_question_{current_question_idx}"
    )
    
    # Store answer
    if user_answer != "Select element":
        st.session_state.ecdis_answers[current_question_idx] = {
            'user_answer': user_answer.lower().replace(' ', '_'),
            'correct_answer': current_question['correct_color'],
            'mode': current_mode
        }
    
    # Navigation
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if current_question_idx > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.ecdis_current_question -= 1
                st.rerun()
    
    with col2:
        if st.button("🏠 Finish Test", use_container_width=True):
            st.session_state.current_page = "home"
            st.session_state.ecdis_current_question = 0
            st.rerun()
    
    with col3:
        # Mode selector
        new_mode = st.selectbox(
            "Chart Mode:",
            ["day", "dusk", "night"],
            index=["day", "dusk", "night"].index(current_mode),
            key="ecdis_mode_selector"
        )
        if new_mode != current_mode:
            st.session_state.ecdis_current_mode = new_mode
            st.rerun()
    
    with col4:
        if st.button("Next Question →", use_container_width=True):
            st.session_state.ecdis_current_question += 1
            st.rerun()
    
    # Instructions
    with st.expander("📋 ECDIS Test Instructions"):
        st.write("""
        **ECDIS Color Recognition Test:**
        - Identify chart elements in different display modes
        - Three modes: Day, Dusk, Night
        - Tests ability to recognize navigation colors under different conditions
        - Based on IHO S-52 standard color palettes
        
        **Chart Elements:**
        - Sea: Water areas
        - Land: Coastal and land areas  
        - Depth Contours: Water depth lines
        - Danger: Hazardous areas
        - Safe: Navigable channels
        - Navigation Aids: Buoys, markers, beacons
        """)

def show_ecdis_results():
    st.header("📊 ECDIS Test Results")
    
    answers = st.session_state.ecdis_answers
    total_questions = len(ECDIS_QUESTIONS)
    
    if not answers:
        st.warning("No test data available.")
        return
    
    # Calculate scores
    correct_answers = 0
    results_data = []
    
    for question_idx, answer_data in answers.items():
        is_correct = answer_data['user_answer'] == answer_data['correct_answer']
        
        if is_correct:
            correct_answers += 1
        
        results_data.append({
            'Question': question_idx + 1,
            'Mode': answer_data['mode'].title(),
            'Your Answer': answer_data['user_answer'].replace('_', ' ').title(),
            'Correct Answer': answer_data['correct_answer'].replace('_', ' ').title(),
            'Status': '✅ Correct' if is_correct else '❌ Incorrect'
        })
    
    # Display results
    st.subheader("Performance Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Correct Answers", f"{correct_answers}/{total_questions}")
    
    with col2:
        accuracy = (correct_answers / total_questions) * 100
        st.metric("Accuracy", f"{accuracy:.1f}%")
    
    with col3:
        errors = total_questions - correct_answers
        st.metric("Errors", errors)
    
    # Assessment
    st.subheader("Assessment")
    if accuracy >= 85:
        st.success("""
        ✅ **EXCELLENT - Strong ECDIS Color Recognition**
        
        You demonstrate excellent ability to recognize navigation colors
        across different ECDIS display modes.
        """)
    elif accuracy >= 70:
        st.warning("""
        ⚠️ **GOOD - Adequate ECDIS Color Recognition**
        
        Your color recognition skills are adequate for most ECDIS operations.
        Consider additional practice with night mode displays.
        """)
    else:
        st.error("""
        ❌ **NEEDS IMPROVEMENT - ECDIS Color Recognition Difficulties**
        
        You may experience difficulties distinguishing critical navigation colors
        on electronic chart displays. Additional training recommended.
        """)
    
    # Detailed results
    st.subheader("Detailed Results")
    st.dataframe(pd.DataFrame(results_data), use_container_width=True)
    
    # Mode-specific performance
    st.subheader("Performance by Display Mode")
    mode_performance = {}
    for answer in answers.values():
        mode = answer['mode']
        is_correct = answer['user_answer'] == answer['correct_answer']
        if mode not in mode_performance:
            mode_performance[mode] = {'correct': 0, 'total': 0}
        mode_performance[mode]['total'] += 1
        if is_correct:
            mode_performance[mode]['correct'] += 1
    
    for mode, stats in mode_performance.items():
        accuracy = (stats['correct'] / stats['total']) * 100
        st.write(f"**{mode.title()} Mode:** {stats['correct']}/{stats['total']} correct ({accuracy:.1f}%)")
    
    if st.button("🔄 Take ECDIS Test Again"):
        st.session_state.ecdis_current_question = 0
        st.session_state.ecdis_answers = {}
        st.session_state.ecdis_question_order = random.sample(ECDIS_QUESTIONS, len(ECDIS_QUESTIONS))
        st.rerun()

def show_ishihara_results():
    # ... (ostavi postojeću show_ishihara_results funkciju) ...
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
            st.button("🌈 FM15 Test", use_container_width=True, disabled=True)
            st.caption("Coming Soon")
        
        st.divider()
        st.markdown("**Copyright © Toni Mandušić 2025**")
    
    elif st.session_state.current_page == "ishihara":
        ishihara_test()
    
    elif st.session_state.current_page == "lantern":
        lantern_test()
    
    elif st.session_state.current_page == "ecdis":
        ecdis_test()
    
    elif st.session_state.current_page == "results":
        show_ishihara_results()

if __name__ == "__main__":
    main()