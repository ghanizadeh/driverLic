import streamlit as st
import json
import os

# Set custom layout parameters
st.set_page_config(
    page_title="Alberta Driving Test Dashboard",
    page_icon="🚗",
    layout="centered"
)

# Custom responsive CSS injection for UI optimization
st.markdown("""
    <style>
    .category-header {
        color: #E63946;
        font-weight: 700;
        font-size: 1.4rem;
        margin-bottom: 1rem;
    }
    .flashcard-box {
        background-color: #F8F9FA;
        border-radius: 12px;
        padding: 25px;
        border-left: 6px solid #1D3557;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .question-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1D3557;
        margin-bottom: 15px;
    }
    .answer-box {
        background-color: #E8F5E9;
        border-left: 6px solid #2E7D32;
        padding: 15px;
        border-radius: 6px;
        margin-top: 15px;
        font-weight: 600;
        color: #1B5E20;
    }
    </style>
""", unsafe_allow_html=True)

# Natively parse dataset with graceful exception containment fallback
@st.cache_data
def load_deck():
    json_path = "flashcards.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        st.error("🚨 Missing 'flashcards.json' dependency layout data profile in system paths.")
        return {}

FLASHCARD_DECK = load_deck()

# Document Page Layout Framework
st.title("🇨🇦 Alberta Class 5 Knowledge Test Simulator")
st.caption("Structured Modular Refinement Assessment Environment")
st.write("---")

if FLASHCARD_DECK:
    # Sidebar control options mapping parameters logic loops
    st.sidebar.header("🕹️ Session Controls")
    selected_category = st.sidebar.selectbox("Choose Study Section:", list(FLASHCARD_DECK.keys()))
    current_pool = FLASHCARD_DECK[selected_category]

    # Initialize isolated unique parameters state machine counters per specific grouping
    if f"idx_{selected_category}" not in st.session_state:
        st.session_state[f"idx_{selected_category}"] = 0
    if f"score_{selected_category}" not in st.session_state:
        st.session_state[f"score_{selected_category}"] = 0
    if f"answered_{selected_category}" not in st.session_state:
        st.session_state[f"answered_{selected_category}"] = set()

    current_idx = st.session_state[f"idx_{selected_category}"]
    total_questions = len(current_pool)

    # Layout Header Progress bars
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f"<div class='category-header'>{selected_category}</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"**Progress:** {current_idx + 1} / {total_questions}")

    if current_idx < total_questions:
        card = current_pool[current_idx]
        
        # Render clean question box layout elements container
        st.markdown(f"""
            <div class="flashcard-box">
                <div class="question-text">Question {card['id']}:</div>
                <div>{card['q']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Radio context configuration fields options metrics mapping
        user_choice = st.radio(
            "Choose your matching option below:", 
            options=card["opts"], 
            index=None, 
            key=f"radio_{selected_category}_{card['id']}_{current_idx}"
        )
        
        if user_choice:
            q_uid = f"{selected_category}_{card['id']}"
            
            if user_choice == card["a"]:
                st.success("🎯 Correct Selection!")
                if q_uid not in st.session_state[f"answered_{selected_category}"]:
                    st.session_state[f"score_{selected_category}"] += 1
                    st.session_state[f"answered_{selected_category}"].add(q_uid)
            else:
                st.error("❌ Incorrect choice. Flip card parameters map down below to check facts.")
                
            with st.expander("🔄 Flip Card to View Official Answer Key"):
                st.markdown(f"""
                    <div class="answer-box">
                        💡 Correct Answer Key:<br>➔ {card['a']}
                    </div>
                """, unsafe_allow_html=True)
                
        st.write("---")
        
        # Navigation element metrics configurations
        nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
        
        with nav_col1:
            if st.button("⬅️ Previous") and current_idx > 0:
                st.session_state[f"idx_{selected_category}"] -= 1
                st.rerun()
                
        with nav_col2:
            st.metric(
                label="Current Section Score", 
                value=f"{st.session_state[f'score_{selected_category}']} / {total_questions}"
            )
            
        with nav_col3:
            if st.button("Next ➡️"):
                if current_idx < total_questions - 1:
                    st.session_state[f"idx_{selected_category}"] += 1
                else:
                    st.session_state[f"idx_{selected_category}"] = 0
                st.rerun()

    if st.sidebar.button("♻️ Clear Progress Flags"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()