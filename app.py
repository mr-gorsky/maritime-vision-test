# Maritime Color Vision Test - Ishihara Implementation
# Copyright © Toni Mandušić 2025

import streamlit as st
import pandas as pd

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
    
    # Display plate description
    st.write(f"*{plate_data['description']}*")
    
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
    st.subheader("Scores")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Normal Vision", f"{normal_score}/24")
    with col2:
        st.metric("Deutan Indicators", f"{deutan_score}/24")
    with col3:
        st.metric("Protan Indicators", f"{protan_score}/24")
    
    # Diagnosis
    max_score = max(normal_score, deutan_score, protan_score)
    
    if normal_score == max_score:
        diagnosis = "✅ Likely Normal Color Vision"
        st.success(diagnosis)
    elif deutan_score == max_score:
        diagnosis = "⚠️ Possible Deuteranopia (Green Deficiency)"
        st.warning(diagnosis)
    elif protan_score == max_score:
        diagnosis = "⚠️ Possible Protanopia (Red Deficiency)"
        st.warning(diagnosis)
    else:
        diagnosis = "❓ Inconclusive - Consult Professional"
        st.error(diagnosis)
    
    # Answer review
    st.subheader("Answer Review")
    review_data = []
    for plate_num in range(1, 25):
        plate_data = ISHIHARA_DATA[plate_num]
        user_answer = st.session_state.user_answers.get(plate_num, "No answer")
        
        review_data.append({
            "Plate": plate_num,
            "Your Answer": user_answer,
            "Expected Normal": plate_data["normal"],
            "Expected Deutan": plate_data["deutan"],
            "Expected Protan": plate_data["protan"]
        })
    
    st.dataframe(pd.DataFrame(review_data), use_container_width=True)
    
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
    
    if st.session_state.current_page == "home":
        st.subheader("Professional Color Vision Testing Suite")
        
        st.success("✅ Select a test to begin")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("👁️ Ishihara Test", use_container_width=True):
                st.session_state.current_page = "ishihara"
                st.rerun()
        
        with col2:
            st.button("🎯 Lantern Test", use_container_width=True, disabled=True)
            st.caption("Coming Soon")
        
        with col3:
            st.button("🌈 FM15 Test", use_container_width=True, disabled=True)
            st.caption("Coming Soon")
        
        with col4:
            st.button("🗺️ ECDIS Test", use_container_width=True, disabled=True)
            st.caption("Coming Soon")
        
        st.divider()
        st.markdown("**Copyright © Toni Mandušić 2025**")
    
    elif st.session_state.current_page == "ishihara":
        ishihara_test()
    
    elif st.session_state.current_page == "results":
        show_results()

if __name__ == "__main__":
    main())