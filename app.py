import streamlit as st #build interactive web app
import pdfplumber# to read pdf file via upload by user
from docx import Document#to read word or .doc file via upload by user
from pptx import Presentation#to read pptx file via upload by user


##let's start
st.set_page_config(
    page_title="studysandwich",
    page_icon="🥪"
)
st.markdown("""
    <style>
    @keyframes bounce {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    .sandwich {
        text-align: center;
        font-size: 80px;
        animation: bounce 1s ease-in-out infinite;
    }
    </style>
    <div class="sandwich">🥪</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #FDF6EC !important;
}

.stButton button {
    background-color: #A0522D;
    color: white;
    border-radius: 20px;
    border: none;
}

@keyframes float {
    0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
}

.bubble {
    position: fixed;
    font-size: 30px;
    animation: float linear infinite;
    pointer-events: none;
    z-index: 0;
}

.b1 { left: 5%;  animation-duration: 6s;  animation-delay: 0s;  }
.b2 { left: 15%; animation-duration: 8s;  animation-delay: 1s;  }
.b3 { left: 30%; animation-duration: 7s;  animation-delay: 2s;  }
.b4 { left: 45%; animation-duration: 9s;  animation-delay: 0.5s;}
.b5 { left: 60%; animation-duration: 6s;  animation-delay: 3s;  }
.b6 { left: 75%; animation-duration: 8s;  animation-delay: 1.5s;}
.b7 { left: 88%; animation-duration: 7s;  animation-delay: 2.5s;}
</style>

<div class="bubble b1">🧋</div>
<div class="bubble b2">🥪</div>
<div class="bubble b3">🧋</div>
<div class="bubble b4">🥪</div>
<div class="bubble b5">🧋</div>
<div class="bubble b6">🥪</div>
<div class="bubble b7">🧋</div>
""", unsafe_allow_html=True)

st.markdown("""
    <p style="
        text-align: center;
        font-size: 22px;
        font-weight: 900;
        color: #A0522D;
        letter-spacing: 2px;
        line-height: 2;
        font-family: 'Georgia', serif;
    ">
    StudySandwich wraps up your study topics between two slices —<br>
    upload your notes, pick your range, and enjoy every bite of knowledge! 🥪📖
    </p>
""", unsafe_allow_html=True)
col1,col2=st.columns(2)
with col2:
  if st.button("let's start study"):
      st.switch_page("pages/quiz.py")

