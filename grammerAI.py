import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="English Grammar Tutor", page_icon="📝")
st.markdown(
    """
    <style>
    body, .stApp {
        direction: rtl;
    }
    p, div, input, label, h1, h2, h3, h4, h5, h6 {
        direction: rtl;
        text-align: right !important;
    }
    .stSpinner > div {
        direction: rtl;
    }
    </style>
    """,
    unsafe_allow_html=True
)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("לא נמצא מפתח API. אנא ודא שהגדרת את GEMINI_API_KEY ב-st.secrets.")
    st.stop()
model = genai.GenerativeModel('gemini-2.5-flash')
st.title("Grammer Test📝")
st.write("הכנס משפט באנגלית שאתה רוצה לבדוק, והמערכת תנתח אותו עבורך.")
user_sentence = st.text_input("המשפט שלך באנגלית:", placeholder="לדוגמה: I has a car...")
if st.button("בדוק דקדוק", type="primary"):
    if user_sentence.strip() == "":
        st.warning("אנא הכנס משפט לפני הלחיצה על הכפתור.")
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
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error("אירעה שגיאה בתקשורת עם השרת. ייתכן שיש עומס כרגע, אנא נסה שוב בעוד מספר שניות.")
                st.exception(e) 