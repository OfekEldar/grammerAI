import streamlit as st
import google.generativeai as genai

# הגדרת הגדרות עמוד
st.set_page_config(page_title="English Grammar Tutor", page_icon="📝")

# הגדרת מפתח ה-API של ג'מיני
# מומלץ להכניס את המפתח לקובץ .streamlit/secrets.toml
# לדוגמה: GEMINI_API_KEY = "your_api_key_here"
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("לא נמצא מפתח API. אנא ודא שהגדרת את GEMINI_API_KEY ב-st.secrets.")
    st.stop()

# אתחול המודל (gemini-1.5-flash אידיאלי ומהיר למשימות טקסט כאלו)
model = genai.GenerativeModel('gemini-1.5-flash')

# ממשק המשתמש
st.title("מורה פרטי לדקדוק באנגלית 📝")
st.write("הכנס משפט באנגלית שאתה רוצה לבדוק, והמערכת תנתח אותו עבורך.")

# תיבת קלט למשתמש
user_sentence = st.text_input("המשפט שלך באנגלית:", placeholder="לדוגמה: I has a car...")

# כפתור שליחה
if st.button("בדוק דקדוק", type="primary"):
    if user_sentence.strip() == "":
        st.warning("אנא הכנס משפט לפני הלחיצה על הכפתור.")
    else:
        with st.spinner("מנתח את המשפט..."):
            # הפרומפט הקבוע שמנחה את המודל איך להגיב
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
                # שליחת הבקשה לג'מיני
                response = model.generate_content(prompt)
                
                # הצגת התשובה המעוצבת
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"אירעה שגיאה בתקשורת עם ה-API: {e}")