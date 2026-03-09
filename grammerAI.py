import streamlit as st
import google.generativeai as genai

# הגדרת הגדרות עמוד
st.set_page_config(page_title="English Grammar Tutor", page_icon="📝")

# הזרקת CSS להגדרת כיוון טקסט ותצוגה מימין לשמאל (RTL)
st.markdown(
    """
    <style>
    /* הפיכת כל העמוד לימין-לשמאל */
    body, .stApp {
        direction: rtl;
    }
    /* יישור הטקסט לימין עבור כל האלמנטים הרלוונטיים */
    p, div, input, label, h1, h2, h3, h4, h5, h6 {
        direction: rtl;
        text-align: right !important;
    }
    /* התאמת מיקום ספינר הטעינה (Spinner) */
    .stSpinner > div {
        direction: rtl;
    }
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

# אתחול המודל - שימוש ב-flash למניעת חריגה ממכסה
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
                
                # הצגת התשובה
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                # הצגת הודעת שגיאה מותאמת אם יש בעיה ב-API
                st.error("אירעה שגיאה בתקשורת עם השרת. ייתכן שיש עומס כרגע, אנא נסה שוב בעוד מספר שניות.")
                st.exception(e) # מציג את השגיאה המלאה למטה למטרות דיבוג