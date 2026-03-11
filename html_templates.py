css = """
<style>
/* ── global ── */
body, .stApp {
    background-color: #0f1117;
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
}

/* ── sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #1a1d27;
    border-right: 1px solid #2e2e3e;
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #a78bfa;
}

/* ── chat container ── */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 10px 0;
    max-width: 860px;
    margin: 0 auto;
}

/* ── message bubbles ── */
.message {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    animation: fadeIn 0.25s ease;
}
.message.user  { flex-direction: row-reverse; }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

.avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.user  .avatar { background: linear-gradient(135deg, #6d28d9, #a78bfa); }
.bot   .avatar { background: linear-gradient(135deg, #0e7490, #22d3ee); }

.bubble {
    max-width: 75%;
    padding: 12px 18px;
    border-radius: 18px;
    line-height: 1.6;
    font-size: 15px;
    word-wrap: break-word;
}
.user .bubble {
    background: linear-gradient(135deg, #6d28d9, #7c3aed);
    color: #fff;
    border-bottom-right-radius: 4px;
}
.bot .bubble {
    background: #1e2130;
    color: #d1d5db;
    border: 1px solid #2e2e3e;
    border-bottom-left-radius: 4px;
}

/* ── source expander ── */
.source-box {
    background: #12151f;
    border: 1px solid #2e2e3e;
    border-radius: 10px;
    padding: 10px 14px;
    margin-top: 8px;
    font-size: 13px;
    color: #9ca3af;
}

/* ── header ── */
h1 { color: #a78bfa !important; }

/* ── input box ── */
.stTextInput > div > div > input {
    background-color: #1e2130 !important;
    color: #e0e0e0 !important;
    border: 1px solid #3b3f5c !important;
    border-radius: 10px !important;
}

/* ── buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6d28d9, #a78bfa);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85; }

/* ── spinner ── */
.stSpinner { color: #a78bfa !important; }
</style>
"""

# ── Jinja-style templates for chat messages ──

USER_TEMPLATE = """
<div class="message user">
    <div class="avatar">🧑</div>
    <div class="bubble">{{MSG}}</div>
</div>
"""

BOT_TEMPLATE = """
<div class="message bot">
    <div class="avatar">🤖</div>
    <div class="bubble">{{MSG}}</div>
</div>
"""
