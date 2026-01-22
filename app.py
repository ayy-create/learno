import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from gtts import gTTS
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Learno | AI Board Tutor", layout="wide", page_icon="🎓")

# --- CUSTOM CSS FOR BRANDING ---
st.markdown("""
    <style>
    .main { background-color: #F3F4F6; }
    .stButton>button { background-color: #1E3A8A; color: white; border-radius: 10px; border: none; }
    .stButton>button:hover { background-color: #10B981; color: white; }
    h1 { color: #1E3A8A; font-family: 'Inter', sans-serif; }
    .card { background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #10B981; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SETTINGS ---
st.sidebar.title("🛠️ Learno Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
board = st.sidebar.selectbox("Select Your Board", ["ICSE", "CBSE", "HSC (State Board)"])
class_level = st.sidebar.slider("Select Class", 1, 12, 10)

# --- HEADER ---
st.title(f"🎓 Learno: {board} Intelligent Tutor")
st.write(f"Tailored study material for **Class {class_level}** based on official board scope.")

# --- MAIN INTERFACE ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📚 Learning Lab")
    topic = st.text_input("Enter a topic or textbook chapter name")
    mode = st.radio("What should Learno generate?", 
                    ["Summary & Notes", "Flashcards", "Exam PYQs", "Interactive Quiz"])
    
    generate_btn = st.button("Generate Material")

with col2:
    st.subheader("🖥️ Study Dashboard")
    if generate_btn:
        if not api_key:
            st.error("Please enter your API Key in the sidebar!")
        else:
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
            
            # Smart Prompt based on Board Choice
            prompt = f"""
            You are a senior {board} teacher. Create a {mode} for the topic: '{topic}' for Class {class_level}.
            - Follow the official scope from sites like cisce.org or cbse.gov.in.
            - Ensure factual accuracy and use the specific terminology used by {board}.
            - If mode is 'Exam PYQs', provide questions from previous years or high-probability specimens.
            """
            
            with st.spinner("AI is researching and fact-checking..."):
                response = llm.invoke(prompt)
                content = response.content
                st.markdown(f"<div class='card'>{content}</div>", unsafe_allow_html=True)
                
                # --- VOICE FEATURE ---
                st.subheader("🔊 Listen to this Lesson")
                tts = gTTS(text=content[:500], lang='en') # Limited for speed
                tts.save("summary.mp3")
                audio_file = open("summary.mp3", "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")

# --- CALENDAR & TRACKER ---
st.divider()
st.subheader("📅 Your Preparation Calendar")
st.info("Coming Soon: Tracking your progress across chapters using AI Spaced Repetition.")
