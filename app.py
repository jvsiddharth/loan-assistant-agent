"""
app.py

Streamlit UI

Responsibilities:

1. Display chat
2. Accept user input
3. Send message to agent
4. Display response

No business logic.
"""

import streamlit as st

from agent import create_agent


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Home Loan AI Assistant",
    page_icon="🏠",
    layout="centered"
)


# =====================================================
# SESSION STATE
# =====================================================

if "agent" not in st.session_state:
    st.session_state.agent = create_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []


# =====================================================
# HEADER
# =====================================================

st.title("🏠 Home Loan AI Assistant")

st.caption(
    "Ask about your application status, "
    "documents, or home loan options."
)


# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# =====================================================
# CHAT INPUT
# =====================================================

user_input = st.chat_input(
    "Type your message..."
)

if user_input:

    # show user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # assistant response

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            response = (
                st.session_state.agent
                .process_message(
                    user_input
                )
            )

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("Demo Customers")

    st.markdown(
        """
### Rahul Sharma
Phone: `9876543210`

Stage:
Credit Review

---

### Ananya Patel
Phone: `9999999999`

Stage:
Sanction Approved

---

### Vikram Singh
Phone: `8888888888`

Stage:
Documents Pending

---

### Sneha Joshi
Phone: `7777777777`

Stage:
Disbursed
"""
    )

    st.divider()

    st.header("Try Asking")

    st.markdown(
        """
- My phone number is 9876543210

- What's my application status?

- What documents are pending?

- I uploaded my salary slip.

- I want a home loan.

- I want to speak with an advisor.
"""
    )

    st.divider()

    st.header("Architecture")

    st.markdown(
        """
User

↓

Streamlit UI

↓

Agent

↓

Tool Calls

↓

Services

↓

Mock Database
"""
    )