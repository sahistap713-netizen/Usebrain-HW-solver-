import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import time

# === GEMINI API KEY ===
API_KEY = "AIzaSyDLv-pKn3kpK50SbGU65bEEKBSQNdzzxlw"
genai.configure(api_key=API_KEY)

# === THEME: Dark Green & White ===
st.set_page_config(page_title="usebrain HW Solver", page_icon="brain", layout="centered")
st.markdown("""
<style>
    .stApp { background-color: #0a3d0a; color: white; }
    .stButton>button { background-color: white; color: #0a3d0a; font-weight: bold; border-radius: 10px; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #e8f5e8; color: #0a3d0a; }
    h1, h2, h3 { color: white !important; }
    .stSidebar { background-color: #083108; }
</style>
""", unsafe_allow_html=True)

# === SUBJECTS (1 to 12) ===
subjects_by_class = {
    1: ["Hindi", "English", "Math"],
    2: ["Hindi", "English", "Math"],
    3: ["Hindi", "English", "Math", "EVS"],
    4: ["Hindi", "English", "Math", "EVS"],
    5: ["Hindi", "English", "Math", "EVS"],
    6: ["Hindi", "English", "Math", "Science", "Social Science", "Sanskrit"],
    7: ["Hindi", "English", "Math", "Science", "Social Science", "Sanskrit"],
    8: ["Hindi", "English", "Math", "Science", "Social Science", "Sanskrit"],
    9: ["Hindi", "English", "Math", "Physics", "Chemistry", "Biology", "History", "Civics", "Geography", "Economics", "Sanskrit"],
    10: ["Hindi", "English", "Math", "Physics", "Chemistry", "Biology", "History", "Civics", "Geography", "Economics", "Sanskrit"],
    11: ["Hindi", "English", "Math", "Physics", "Chemistry", "Biology", "History", "Civics", "Geography", "Economics", "Accounts", "Business Studies", "Entrepreneurship", "Health and Physical Education", "Computer Science", "Python", "Sanskrit", "Business Arithmetic", "Urdu", "Fine Arts"],
    12: ["Hindi", "English", "Math", "Physics", "Chemistry", "Biology", "History", "Civics", "Geography", "Economics", "Accounts", "Business Studies", "Entrepreneurship", "Health and Physical Education", "Computer Science", "Python", "Sanskrit", "Business Arithmetic", "Urdu", "Fine Arts"]
}

# === LOGO ===
st.sidebar.image("https://img.icons8.com/ios-filled/100/ffffff/brain.png", width=80)
st.sidebar.markdown("<h2 style='color:white; text-align:center;'>usebrain</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#a8d5a8; text-align:center; font-size:12px;'>by Sahista</p>", unsafe_allow_html=True)

# === CLASS & SUBJECT ===
st.sidebar.header("Select Class & Subject")
selected_class = st.sidebar.selectbox("Class", list(range(1,13)))
selected_subject = st.sidebar.selectbox("Subject", subjects_by_class[selected_class])

# === MAIN UI ===
col1, col2 = st.columns([1,4])
with col1: st.image("https://img.icons8.com/ios-filled/100/ffffff/brain.png", width=70)
with col2: st.markdown("<h1>usebrain HW Solver</h1>", unsafe_allow_html=True)

st.markdown("---")
tab1, tab2 = st.tabs(["Type Question", "Upload Images (up to 10)"])

with tab1:
    question = st.text_area("Enter your question:", height=120)

with tab2:
    images = st.file_uploader("Upload images", type=["png","jpg","jpeg"], accept_multiple_files=True)
    if images and len(images)>10: images = images[:10]

# === SOLVE BUTTON ===
if st.button("SOLVE THE HOMEWORK", type="primary"):
    if not question and not images:
        st.error("Please type or upload something!")
    else:
        with st.spinner("Solving in <2 sec..."):
            start = time.time()
            prompt = f"Class {selected_class} {selected_subject}. Solve step-by-step in clear format. Use LaTeX for math.\n"
            if question: prompt += f"Question: {question}\n"
            model = genai.GenerativeModel('gemini-1.5-flash')
            content = [prompt]
            for img in images or []:
                content.append(Image.open(img))
            response = model.generate_content(content)
            answer = response.text
            st.success(f"Solved in {time.time()-start:.2f} sec!")
            st.markdown("### Solution")
            st.markdown(answer)
            st.download_button("Download Answer", answer, "solution.txt")
            st.markdown(f"[Share on WhatsApp](https://wa.me/?text=usebrain%20Solution:%20{answer[:100]}...)")

# === EXIT ===
if st.button("Exit App"):
    st.balloons()
    st.success("Thank you for using usebrain!")
    time.sleep(2)
    st.stop()
