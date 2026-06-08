import streamlit as st
from draft import generate_draft
from feedback import save_feedback

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

if st.button("Generate follow-up", type="primary", disabled=not (contact and thread)):
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
