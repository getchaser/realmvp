import time

import streamlit as st
from counter import check_and_increment
from draft import generate_draft
from feedback import save_feedback

COOLDOWN = 15  # seconds between generations per session

st.set_page_config(page_title="AI Follow-up Drafter", layout="centered")
st.title("Write your follow-up in 10 seconds")
st.caption("Free. No signup. Paste your thread, get a draft.")

col1, col2 = st.columns(2)
contact = col1.text_input("Contact name *")
company = col2.text_input("Company (optional)")

thread = st.text_area("Paste your email thread (most recent first)", height=200)

goal = st.radio(
    "What do you want?",
    ["Schedule a call", "Get a decision", "Re-engage a cold lead", "Other"],
    horizontal=True,
)
if goal == "Other":
    goal = st.text_input("Describe your goal")

if "last_gen" not in st.session_state:
    st.session_state.last_gen = 0

if st.button("Generate follow-up", type="primary", disabled=not (contact and thread)):
    elapsed = time.time() - st.session_state.last_gen
    if elapsed < COOLDOWN:
        st.warning(f"Please wait {int(COOLDOWN - elapsed)}s before generating again.")
        st.stop()
    if not check_and_increment():
        st.error("Daily limit reached. Try again tomorrow.")
        st.stop()
    st.session_state.last_gen = time.time()
    with st.spinner("Drafting..."):
        result = generate_draft(contact, company, thread, goal)

    st.divider()
    st.text_input("Subject", value=result["subject"])
    st.text_area("Body", value=result["body"], height=180)
    st.code(result["body"], language=None)

    st.divider()
    useful = st.radio(
        "Was this useful?",
        ["👍 Yes, I'd send it", "✏️ Needed editing", "👎 Off the mark"],
        horizontal=True,
    )
    pay = st.text_input("Would you pay for this built into your Gmail? ($X/mo or 'no')")
    email_addr = st.text_input("Leave your email to hear when we launch (optional)")

    if st.button("Submit feedback"):
        save_feedback({"contact": contact, "useful": useful, "pay": pay, "email": email_addr})
        st.success("Thanks!")
