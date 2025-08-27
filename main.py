# main.py
import streamlit as st
from candidate_data import CandidateData
from chatbot_core import Chatbot
from utils import check_exit_words

# -----------------------
# Session state setup
# -----------------------
if "candidate" not in st.session_state:
    st.session_state["candidate"] = CandidateData()
if "chatbot" not in st.session_state:
    st.session_state["chatbot"] = Chatbot()
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "chat_active" not in st.session_state:
    st.session_state["chat_active"] = True
if "tech_questions" not in st.session_state:
    st.session_state["tech_questions"] = []
if "tech_question_index" not in st.session_state:
    st.session_state["tech_question_index"] = 0
if "awaiting_tech_answer" not in st.session_state:
    st.session_state["awaiting_tech_answer"] = False

# -----------------------
# Page title
# -----------------------
st.title("TalentScout Hiring Assistant")

# -----------------------
# Reset button
# -----------------------
if st.button("Reset Chat"):
    st.session_state.clear()
    st.rerun()

# -----------------------
# Initial greeting
# -----------------------
if not st.session_state["messages"]:
    st.session_state["messages"].append({
        "role": "bot",
        "content": (
            "Hello! I’m TalentScout- Your virtual Hiring Assistant. "
            "I’ll collect your info and ask technical questions based on your skills. "
            "Type exit/bye/thank you/quit anytime to end the chat. "
            "So to start, may I know your full name?"
        )
    })

# -----------------------
# Display chat history
# -----------------------
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -----------------------
# Hardcoded validation
# -----------------------
def validate_and_update(candidate, field, text):
    text = text.strip()
    if field == "name":
        if text.replace(" ", "").isalpha() and len(text.split()) >= 2:
            candidate.update(field, text.title())
            return True, f"VALID That's a great start, {text.title()}!"
        return False, "INVALID Please enter your full name with letters and spaces only."

    elif field == "email":
        if "@" in text and "." in text.split("@")[-1]:
            candidate.update(field, text)
            return True, f"VALID Your email {text} looks perfect."
        return False, "INVALID Please enter a valid email with '@' and domain."

    elif field == "phone":
        digits = ''.join(filter(str.isdigit, text))
        if len(digits) == 10:
            candidate.update(field, digits)
            return True, "VALID Phone number recorded correctly."
        return False, "INVALID Phone must be exactly 10 digits."

    elif field == "years_of_experience":
        if text.isdigit():
            candidate.update(field, text)
            return True, f"VALID Experience recorded: {text} years."
        return False, "INVALID Please enter numeric years of experience."

    elif field == "desired_position":
        if text:
            candidate.update(field, text.title())
            return True, "VALID Desired position noted."
        return False, "INVALID Please provide a valid role."

    elif field == "location":
        if text:
            candidate.update(field, text.title())
            return True, f"VALID Location noted: {text.title()}."
        return False, "INVALID Please provide your location."

    elif field == "tech_stack":
        skills = [s.strip() for s in text.split(",") if s.strip()]
        if skills:
            candidate.update(field, ",".join(skills))
            return True, f"VALID Tech stack recorded: {', '.join(skills)}."
        return False, "INVALID Please list your tech skills separated by commas."

    return False, "INVALID Unknown field."

# -----------------------
# Determine next missing field
# -----------------------
def next_missing_field(candidate):
    field_order = [
        "name","email","phone","years_of_experience",
        "desired_position","location","tech_stack"
    ]
    for f in field_order:
        if not candidate.data.get(f):
            return f
    return None

# -----------------------
# Chat input + processing
# -----------------------
if st.session_state["chat_active"]:
    user_input = st.chat_input("Your message...")
    if user_input:
        candidate = st.session_state["candidate"]
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Exit check
        if check_exit_words(user_input):
            st.session_state["messages"].append({
                "role": "bot",
                "content": "Thank you! We'll contact you soon. Goodbye!"
            })
            st.session_state["chat_active"] = False
            st.rerun()

        # Check if waiting for tech answers
        if st.session_state["tech_questions"] and st.session_state["awaiting_tech_answer"]:
            st.session_state["awaiting_tech_answer"] = False
            st.session_state["messages"].append({
                "role": "bot",
                "content": "Got it! Let's move on to the next technical question."
            })
        else:
            # Candidate info collection & validation
            field = next_missing_field(candidate)
            valid = False
            if field:
                valid, reply = validate_and_update(candidate, field, user_input)
                st.session_state["messages"].append({"role": "bot", "content": reply})

            # Ask next missing field only if current input is valid
            if valid:
                next_field = next_missing_field(candidate)
                if next_field:
                    st.session_state["messages"].append({
                        "role": "bot",
                        "content": f"Please provide your {next_field.replace('_',' ')}:"
                    })

        # Generate tech questions once info complete using LLM
        if candidate.is_info_complete() and not st.session_state["tech_questions"]:
            st.session_state["tech_questions"] = st.session_state["chatbot"].generate_tech_questions(candidate)

        # Ask technical questions one-by-one
        if st.session_state["tech_questions"] and not st.session_state["awaiting_tech_answer"]:
            index = st.session_state["tech_question_index"]
            if index < len(st.session_state["tech_questions"]):
                question = st.session_state["tech_questions"][index]
                st.session_state["messages"].append({"role": "bot", "content": question})
                st.session_state["tech_question_index"] += 1
                st.session_state["awaiting_tech_answer"] = True
            else:
                st.session_state["messages"].append({
                    "role": "bot",
                    "content": (
                        "🎉 That's all the technical questions! "
                        "Thank you for taking the time to answer them. "
                        "Our team will review your responses and get back to you soon regarding the next steps. "
                        "We appreciate your effort and wish you the best!"
                    )
                })
                st.session_state["chat_active"] = False

        st.rerun()
