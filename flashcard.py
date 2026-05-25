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
    [data-testid="stSidebar"] {
        display: none !important;
    }
    .category-header {
        color: #E63946;
        font-weight: 700;
        font-size: 1.3rem;
        margin-top: 5px;
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
    .rtl-text {
        direction: rtl;
        text-align: right;
        font-family: 'Tahoma', sans-serif;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# UI Strings for Translation
UI_STRINGS = {
    "en": {
        "title": "🇨🇦 Alberta Class 5 Knowledge Test Simulator",
        "caption": "A clean, simple study workspace designed for beginners.",
        "lang_label": "🌐 App Language:",
        "sec_label": "📚 Select Study Topic:",
        "progress": "Question:",
        "q_num": "Question",
        "radio_label": "Select the correct answer:",
        "correct": "🎯 Correct! Excellent job.",
        "incorrect": "❌ Not quite right. Reveal the answer below to see why!",
        "flip_label": "🔄 View Correct Answer Key",
        "ans_key": "💡 Correct Answer:",
        "prev": "⬅️ Previous Question",
        "next": "Next Question ➡️",
        "score_label": "Current Section Score",
        "clear_btn": "♻️ Reset All Progress"
    },
    "fa": {
        "title": "🇨🇦 شبیه‌ساز آزمون آیین‌نامه رانندگی آلبرتا (کلاس ۵)",
        "caption": "یک محیط مطالعه ساده و روان برای کاربران تازه‌کار.",
        "lang_label": "🌐 زبان برنامه:",
        "sec_label": "📚 انتخاب موضوع مطالعه:",
        "progress": "سوال:",
        "q_num": "سوال",
        "radio_label": "گزینه صحیح را انتخاب کنید:",
        "correct": "🎯 درست بود! آفرین.",
        "incorrect": "❌ اشتباه بود. پاسخ صحیح را در پایین نمایان کنید.",
        "flip_label": "🔄 مشاهده پاسخ صحیح",
        "ans_key": "💡 پاسخ صحیح:",
        "prev": "⬅️ سوال قبلی",
        "next": "سوال بعدی ➡️",
        "score_label": "امتیاز این بخش",
        "clear_btn": "♻️ پاک کردن تمام سوابق"
    }
}

@st.cache_data
def load_deck():
    json_path = "flashcards.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        st.error("🚨 Missing 'flashcards.json' data file.")
        return {}

FLASHCARD_DECK = load_deck()

# Header Configurator Layout
top_col1, top_col2 = st.columns([2, 1])
with top_col2:
    lang = st.selectbox("", ["English", "فارسی"], index=0, label_visibility="collapsed")
    lang_code = "en" if lang == "English" else "fa"

is_rtl = lang_code == "fa"

if is_rtl:
    st.markdown(f"<h2 class='rtl-text'>{UI_STRINGS[lang_code]['title']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='rtl-text' style='color:gray;'>{UI_STRINGS[lang_code]['caption']}</p>", unsafe_allow_html=True)
else:
    st.title(UI_STRINGS[lang_code]["title"])
    st.caption(UI_STRINGS[lang_code]["caption"])

st.write("---")

if FLASHCARD_DECK:
    categories = list(FLASHCARD_DECK.keys())
    selected_category = st.selectbox(UI_STRINGS[lang_code]["sec_label"], categories)
    current_pool = FLASHCARD_DECK[selected_category]

    if f"idx_{selected_category}" not in st.session_state:
        st.session_state[f"idx_{selected_category}"] = 0
    if f"score_{selected_category}" not in st.session_state:
        st.session_state[f"score_{selected_category}"] = 0
    if f"answered_{selected_category}" not in st.session_state:
        st.session_state[f"answered_{selected_category}"] = set()

    current_idx = st.session_state[f"idx_{selected_category}"]
    total_questions = len(current_pool)

    st.write("")
    info_col1, info_col2 = st.columns([2, 1])
    with info_col1:
        st.markdown(f"<div class='category-header'>📍 {selected_category}</div>", unsafe_allow_html=True)
    with info_col2:
        st.markdown(f"<div style='text-align: right; font-weight: bold;'>{UI_STRINGS[lang_code]['progress']} {current_idx + 1} / {total_questions}</div>", unsafe_allow_html=True)

    if current_idx < total_questions:
        card = current_pool[current_idx]
        
        q_text = card["q_" + lang_code]
        opts = card["opts_" + lang_code]
        correct_ans = card["a_" + lang_code]
        
        rtl_class = "rtl-text" if is_rtl else ""
        st.markdown(f"""
            <div class="flashcard-box {rtl_class}">
                <div class="question-text">{UI_STRINGS[lang_code]['q_num']} {card['id']}:</div>
                <div>{q_text}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Live web asset ingestion loop
        if "img" in card and card["img"]:
            # Renders directly via the live online URL paths provided in JSON
            st.image(card["img"], width=150)
            st.write("")
        
        user_choice = st.radio(
            UI_STRINGS[lang_code]["radio_label"], 
            options=opts, 
            index=None, 
            key=f"radio_{selected_category}_{card['id']}_{current_idx}_{lang_code}"
        )
        
        if user_choice:
            q_uid = f"{selected_category}_{card['id']}"
            
            if user_choice == correct_ans:
                st.success(UI_STRINGS[lang_code]["correct"])
                if q_uid not in st.session_state[f"answered_{selected_category}"]:
                    st.session_state[f"score_{selected_category}"] += 1
                    st.session_state[f"answered_{selected_category}"].add(q_uid)
            else:
                st.error(UI_STRINGS[lang_code]["incorrect"])
                
            with st.expander(UI_STRINGS[lang_code]["flip_label"]):
                st.markdown(f"""
                    <div class="answer-box {rtl_class}">
                        {UI_STRINGS[lang_code]['ans_key']}<br>➔ {correct_ans}
                    </div>
                """, unsafe_allow_html=True)
                
        st.write("---")
        
        nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
        
        with nav_col1:
            if st.button(UI_STRINGS[lang_code]["prev"]) and current_idx > 0:
                st.session_state[f"idx_{selected_category}"] -= 1
                st.rerun()
                
        with nav_col2:
            st.metric(
                label=UI_STRINGS[lang_code]["score_label"], 
                value=f"{st.session_state[f'score_{selected_category}']} / {total_questions}"
            )
            
        with nav_col3:
            if st.button(UI_STRINGS[lang_code]["next"]):
                if current_idx < total_questions - 1:
                    st.session_state[f"idx_{selected_category}"] += 1
                else:
                    st.session_state[f"idx_{selected_category}"] = 0
                st.rerun()

    st.write("")
    foot_col1, foot_col2 = st.columns([3, 1])
    with foot_col2:
        if st.button(UI_STRINGS[lang_code]["clear_btn"], key="reset_bt"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
