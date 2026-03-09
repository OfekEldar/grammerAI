import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
from io import BytesIO

# הגדרת הגדרות עמוד
st.set_page_config(page_title="English Grammar Tutor", page_icon="📝")

# הזרקת CSS להגדרת כיוון טקסט ותצוגה מימין לשמאל (RTL)
st.markdown(
    """
    <style>
    body, .stApp { direction: rtl; }
    p, div, input, label, h1, h2, h3, h4, h5, h6 { direction: rtl; text-align: right !important; }
    .stSpinner > div { direction: rtl; }
    </style>
    """,
    unsafe_allow_html=True
)

# הגדרת מפתח ה-API של ג'מיני
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("לא נמצא מפתח API. אנא ודא שהגדרת את GEMINI_API_KEY ב-st.secrets.")
    st.stop()

# אתחול המודל 
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("Grammer Test📝")
st.write("הקלד משפט באנגלית או השתמש במיקרופון כדי להקליט, והמערכת תנתח אותו עבורך.")

st.markdown("---")

# --- אזור קלט המשתמש (הקלטה או הקלדה) ---

# רכיב ההקלטה - מוגדר לזהות אנגלית
audio_text = speech_to_text(
    language='en-US',
    start_prompt="🎙️ לחץ כאן כדי להקליט משפט באנגלית",
    stop_prompt="🛑 עצור הקלטה",
    just_once=True,
    key='STT'
)

# עדכון תיבת הטקסט אם המשתמש הקליט משהו
if audio_text:
    st.session_state.text_input_key = audio_text

# תיבת הטקסט (מקושרת ל-session_state כדי להתעדכן מההקלטה)
user_sentence = st.text_input(
    "המשפט שלך באנגלית:", 
    key="text_input_key", 
    placeholder="לדוגמה: I has a car..."
)

# --- אזור העיבוד והתשובה ---

if st.button("בדוק דקדוק", type="primary"):
    if not user_sentence or user_sentence.strip() == "":
        st.warning("אנא הכנס או הקלט משפט לפני הלחיצה על הכפתור.")
    else:
        with st.spinner("מנתח את המשפט..."):
            prompt = f"""
            You are an expert, encouraging English grammar tutor. 
            Analyze the following sentence provided by a user:
            Sentence: "{user_sentence}"
            
            Please provide your response in Hebrew, structured exactly like this:
            
            **סטטוס:** (ציין בבירור האם המשפט נכון דקדוקית או שיש בו שגיאה).
            
            **הסבר ותיקון:** (אם יש שגיאה, ספק את המשפט המתוקן והסבר בפשטות מה הייתה השגיאה ומה הכלל הדקדוקי. אם המשפט נכון, הסבר בקצרה למה המבנה שלו נכון).
            
            **דוגמאות נוספות:** (ספק 3 משפטים שונים באנגלית המדגימים את אותו כלל דקדוקי שעליו מבוסס המשפט/התיקון, עם תרגום קצר לעברית בסוגריים).
            """
            
            try:
                # קבלת התשובה מג'מיני
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(response.text)
                
                # --- יצירת ההקראה הקולית (TTS) ---
                with st.spinner("מכין הקראה קולית..."):
                    # המרת הטקסט לשמע (מוגדר לעברית כדי שיקרא נכון את ההסברים)
                    tts = gTTS(text=response.text, lang='he')
                    
                    # שמירת קובץ השמע בזיכרון (כדי לא לשמור קבצים פיזיים על המחשב)
                    audio_fp = BytesIO()
                    tts.write_to_fp(audio_fp)
                    audio_fp.seek(0)
                    
                    # הצגת נגן השמע למשתמש
                    st.write("🔊 **השמע את ההסבר:**")
                    st.audio(audio_fp, format='audio/mp3')
                
            except Exception as e:
                st.error("אירעה שגיאה בתקשורת עם השרת. ייתכן שיש עומס כרגע, אנא נסה שוב בעוד מספר שניות.")
                st.exception(e)