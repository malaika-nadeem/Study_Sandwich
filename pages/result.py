import streamlit as st
import os
from groq import Groq
import json

st.set_page_config(page_title="studysandwhich", page_icon="🥪")
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

# ✅ API key from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# ✅ Guard against direct page access
if "text" not in st.session_state:
    st.warning("Please upload your notes first!")
    st.switch_page("pages/quiz.py")
    st.stop()

# unpack from session state
text = st.session_state["text"]
num_mcq = st.session_state["num_mcq"]
num_short = st.session_state["num_short"]

st.subheader("*Your StudySandwich is ready!* 🥪")

with st.spinner("Generating your quiz..."):
    prompt = f"""
    You are a quiz generator. Based on the text below, generate:
    - {num_mcq} MCQs with 4 options each and the correct answer
    - {num_short} short questions with answers
    
    Return in JSON format only. No extra text. Use this structure:
    {{
      "mcqs": [
        {{"question": "...", "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}}, "correct": "A"}}
      ],
      "short_questions": [
        {{"question": "...", "answer": "..."}}
      ]
    }}
    
    Text: {text}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content
    result = result.strip().replace("```json", "").replace("```", "").strip()
    quiz_data = json.loads(result)

for i, mcq in enumerate(quiz_data["mcqs"]):
    st.write(f"**Q{i+1}: {mcq['question']}**")
    answer = st.radio("Choose:", list(mcq["options"].values()), key=f"mcq_{i}")

for i, sq in enumerate(quiz_data["short_questions"]):
    st.write(f"**Q{i+1}: {sq['question']}**")
    user_answer = st.text_input("Your answer:", key=f"short_{i}")

st.markdown("---")
if st.button("Submit Quiz 🥪"):
    score = 0
    total = len(quiz_data["mcqs"]) + len(quiz_data["short_questions"])

    st.subheader("MCQ Results:")
    for i, mcq in enumerate(quiz_data["mcqs"]):
        user_ans = st.session_state.get(f"mcq_{i}")
        correct_ans = mcq["options"][mcq["correct"]]
        if user_ans == correct_ans:
            st.success(f"Q{i+1}: ✅ Correct!")
            score += 1
        else:
            st.error(f"Q{i+1}: ❌ Wrong! Correct answer: {correct_ans}")

    st.subheader("Short Question Results:")
    for i, sq in enumerate(quiz_data["short_questions"]):
        user_ans = st.session_state.get(f"short_{i}", "")
        check_prompt = f"""
        Question: {sq['question']}
        Expected answer: {sq['answer']}
        User's answer: {user_ans}
        Reply only: CORRECT or INCORRECT or Blank and one sentence why and if user's does not gave answer reply U Don't gave answer.
        """
        check_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": check_prompt}]
        )
        feedback = check_response.choices[0].message.content
        if "CORRECT" in feedback.upper():
            st.success(f"Q{i+1}: ✅ {feedback}")
            score += 1
        elif "BLANK" in feedback.upper():
            st.error(f"Q{i+1}: ❌ {feedback}")
        else:
            st.error(f"Q{i+1}: ❌ {feedback}")

    st.markdown("---")
    st.subheader(f"🥪 Your Score: {score}/{total}")
