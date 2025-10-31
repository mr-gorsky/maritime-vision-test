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
    st.header("👁️ Ishihara Color Vision Test")
    
    if 'current_plate' not in st.session_state:
        st.session_state.current_plate = 1
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    
    plate_number = st.session_state.current_plate
    plate_data = ISHIHARA_DATA[plate_number]
    
    st.subheader(f"Plate {plate_number}")
    
    # Load local plate image
    image_path = f"assets/ishihara_plates/plate{plate_number}.png"
    
    if os.path.exists(image_path):
        st.image(image_path, width=400, caption=f"Plate {plate_number}")
        st.success("✅ Standard Ishihara Plate")
    else:
        st.error(f"❌ Plate image not found: {image_path}")
        return
    
    st.write(f"*{plate_data['description']}*")
    
    user_answer = st.text_input(
        "What number do you see? (Leave blank if you don't see anything)",
        value=st.session_state.user_answers.get(plate_number, ""),
        key=f"plate_{plate_number}"
    )
    
    st.session_state.user_answers[plate_number] = user_answer.strip()
    
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
    
    progress = plate_number / 24
    st.progress(progress)
    st.write(f"Progress: {plate_number} of 24 plates")

def lantern_test():
    st.header("🎯 Lantern Test")
    st.write("**Navigation Light Recognition Simulation**")
    
    # Initialize session state for lantern test
    if 'lantern_current_pair' not in st.session_state:
        st.session_state.lantern_current_pair = 0
        st.session_state.lantern_answers = {}
        st.session_state.lantern_sequence = random.sample(LANTERN_SEQUENCES, len(LANTERN_SEQUENCES))
    
    current_pair = st.session_state.lantern_current_pair
    sequence = st.session_state.lantern_sequence
    
    if current_pair >= len(sequence):
        # Test completed
        show_lantern_results()
        return
    
    # Get current color pair
    color1, color2 = sequence[current_pair]
    color1_data = LANTERN_COLORS[color1]
    color2_data = LANTERN_COLORS[color2]
    
    st.subheader(f"Light Pair {current_pair + 1} of {len(sequence)}")
    
    # Create lantern display using Streamlit columns
    st.markdown(
        """
        <style>
        .lantern-container {
            background-color: #000000;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            margin: 20px 0;
        }
        .light-label {
            color: white;
            font-size: 12px;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Display the lights using columns with black background
    st.markdown('<div class="lantern-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Light 1 with glow effect
        st.markdown(
            f'<div style="width: 80px; height: 80px; border-radius: 50%; background-color: {color1_data["hex"]}; margin: 0 auto; box-shadow: 0 0 30px {color1_data["hex"]}80; border: 3px solid #333;"></div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="light-label">Light 1</div>', unsafe_allow_html=True)
    
    with col2:
        # Light 2 with glow effect
        st.markdown(
            f'<div style="width: 80px; height: 80px; border-radius: 50%; background-color: {color2_data["hex"]}; margin: 0 auto; box-shadow: 0 0 30px {color2_data["hex"]}80; border: 3px solid #333;"></div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="light-label">Light 2</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("**Identify the colors of both lights:**")
    
    # Color selection for both lights
    col1, col2 = st.columns(2)
    
    with col1:
        light1_answer = st.selectbox(
            "Light 1 Color:",
            ["Select color", "Red", "Green", "Yellow", "White"],
            key=f"lantern_light1_{current_pair}"
        )
    
    with col2:
        light2_answer = st.selectbox(
            "Light 2 Color:",
            ["Select color", "Red", "Green", "Yellow", "White"],
            key=f"lantern_light2_{current_pair}"
        )
    
    # Store answers
    if light1_answer != "Select color" and light2_answer != "Select color":
        st.session_state.lantern_answers[current_pair] = {
            'light1': light1_answer.lower(),
            'light2': light2_answer.lower(),
            'correct1': color1_data['name'].lower(),
            'correct2': color2_data['name'].lower()
        }
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_pair > 0:
            if st.button("← Previous Pair", use_container_width=True):
                st.session_state.lantern_current_pair -= 1
                st.rerun()
    
    with col2:
        if st.button("🏠 Finish Test", use_container_width=True):
            st.session_state.current_page = "home"
            st.session_state.lantern_current_pair = 0
            st.rerun()
    
    with col3:
        if st.button("Next Pair →", use_container_width=True):
            st.session_state.lantern_current_pair += 1
            st.rerun()
    
    # Instructions
    with st.expander("📋 Lantern Test Instructions"):
        st.write("""
        **IMO/ICAO Standard Lantern Test:**
        - Identify the color of each navigation light
        - Colors: Red, Green, Yellow, White
        - Simulates low-light conditions at sea
        - 9 light pairs total
        - **Passing criteria:** ≤1 error for maritime standards
        
        **Common errors:**
        - Red-Green confusion (Protan/Deutan deficiency)
        - Yellow-White confusion (light sensitivity issues)
        """)

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
        show_ecdis_results()
        return
    
    current_question = question_order[current_question_idx]
    palette = ECDIS_PALETTES[current_mode]
    
    st.subheader(f"ECDIS {current_mode.title()} Mode - Question {current_question_idx + 1} of {len(question_order)}")
    
    # Simple ECDIS simulation using Streamlit components
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create a simple chart representation
        st.write("**ECDIS Chart Simulation:**")
        
        # Sea background with chart elements
        st.markdown(f"<div style='background-color: {palette['sea']}; padding: 20px; border-radius: 10px; border: 2px solid #333;'>", unsafe_allow_html=True)
        
        # Create chart elements using columns
        col_a, col_b, col_c = st.columns([1, 2, 1])
        
        with col_a:
            st.markdown(f"<div style='background-color: {palette['land']}; padding: 15px; border-radius: 5px; text-align: center; margin: 5px; font-weight: bold;'>LAND</div>", unsafe_allow_html=True)
        
        with col_b:
            st.markdown(f"<div style='background-color: {palette['safe']}; padding: 10px; border: 2px dashed #333; text-align: center; margin: 5px; font-weight: bold;'>SAFE CHANNEL</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='background: repeating-linear-gradient(45deg, transparent, transparent 5px, {palette['depth_contours']} 5px, {palette['depth_contours']} 10px); padding: 15px; border: 1px solid {palette['depth_contours']}; margin: 5px; text-align: center; font-weight: bold;'>DEPTH</div>", unsafe_allow_html=True)
        
        with col_c:
            st.markdown(f"<div style='background-color: {palette['danger']}; padding: 15px; border-radius: 50%; text-align: center; margin: 5px; font-weight: bold;'>DANGER</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='background-color: {palette['navigation_aids']}; padding: 10px; border-radius: 50%; text-align: center; margin: 5px; font-weight: bold;'>NAV AID</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.write("**Color Legend:**")
        
        # Simple color legend using Streamlit
        for color_name, color_hex in palette.items():
            if color_name != 'text':
                st.markdown(
                    f"<div style='display: flex; align-items: center; margin: 8px 0;'>"
                    f"<div style='width: 25px; height: 25px; background-color: {color_hex}; border: 1px solid #333; margin-right: 10px; border-radius: 3px;'></div>"
                    f"<span style='font-size: 14px;'>{color_name.replace('_', ' ').title()}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
    
    # Question section
    st.write("---")
    st.write(f"**Question:** {current_question['question']}")
    st.write(f"*Hint: {current_question['description']}*")
    
    # Answer options
    color_options = [opt for opt in palette.keys() if opt != 'text']
    
    user_answer = st.selectbox(
        "Select the chart element:",
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
        if st.button("Next →", use_container_width=True):
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

def show_lantern_results():
    st.header("📊 Lantern Test Results")
    
    answers = st.session_state.lantern_answers
    total_pairs = len(LANTERN_SEQUENCES)
    
    if not answers:
        st.warning("No test data available.")
        return
    
    # Calculate scores
    correct_answers = 0
    total_answers = len(answers)
    
    results_data = []
    for pair_idx, answer_data in answers.items():
        light1_correct = answer_data['light1'] == answer_data['correct1']
        light2_correct = answer_data['light2'] == answer_data['correct2']
        pair_correct = light1_correct and light2_correct
        
        if pair_correct:
            correct_answers += 1
        
        results_data.append({
            'Pair': pair_idx + 1,
            'Light 1 Your Answer': answer_data['light1'].title(),
            'Light 1 Correct': answer_data['correct1'].title(),
            'Light 2 Your Answer': answer_data['light2'].title(), 
            'Light 2 Correct': answer_data['correct2'].title(),
            'Status': '✅ Correct' if pair_correct else '❌ Incorrect'
        })
    
    # Display results
    st.subheader("Performance Summary")
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
    st.subheader("Assessment")
    if errors <= 1:
        st.success("""
        ✅ **PASS - Suitable for Maritime Duties**
        
        Your performance meets IMO standards for color vision requirements
        in navigation and lookout duties.
        """)
    else:
        st.error("""
        ❌ **FAIL - Further Assessment Recommended**
        
        Your results indicate potential color vision difficulties that
        may affect navigation light recognition. Consult eye care professional.
        """)
    
    # Detailed results
    st.subheader("Detailed Results")
    st.dataframe(pd.DataFrame(results_data), use_container_width=True)
    
    if st.button("🔄 Take Lantern Test Again"):
        st.session_state.lantern_current_pair = 0
        st.session_state.lantern_answers = {}
        st.session_state.lantern_sequence = random.sample(LANTERN_SEQUENCES, len(LANTERN_SEQUENCES))
        st.rerun()

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
    st.header("📊 Ishihara Test Results")
    
    if not st.session_state.get('user_answers'):
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
    elif deutan_score == max_score:
        st.warning("⚠️ **Possible Deuteranopia (Green Deficiency)**")
    elif protan_score == max_score:
        st.warning("⚠️ **Possible Protanopia (Red Deficiency)**")
    else:
        st.error("❓ **Inconclusive Results**")
    
    if st.button("🔄 Take Ishihara Test Again"):
        st.session_state.current_plate = 1
        st.session_state.user_answers = {}
        st.session_state.current_page = "ishihara"
        st.rerun()

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