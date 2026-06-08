import anthropic

SYSTEM = """You write follow-up emails for sales reps. Rules:
- 3–5 sentences max
- Reference something specific from the thread
- One clear call to action
- Match the tone of the previous emails
- Never use: "I hope this finds you well", "just checking in", "touching base", "circle back"
- Sound like a human who actually read the thread, not a template
- No bullet points, no dashes, no em dashes, no markdown, no lists of any kind
- Plain prose only — write like a person typing an email, not a chatbot formatting a response"""


THREAD_CHAR_LIMIT = 3000


def generate_draft(contact_name: str, company: str, thread: str, goal: str) -> dict:
    client = anthropic.Anthropic()

    thread = thread[:THREAD_CHAR_LIMIT]

    prompt = f"""Email thread with {contact_name}{f' from {company}' if company else ''}:

---
{thread}
---

Goal for this follow-up: {goal}

Write the follow-up email. Format:
Subject: [subject line]

[email body only, no sign-off placeholder]"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text
    lines = raw.strip().split("\n", 2)
    subject = lines[0].replace("Subject:", "").strip()
    body = "\n".join(lines[2:]).strip() if len(lines) > 2 else lines[-1]

    return {"subject": subject, "body": body}
