"""
Minimal UI to try one intention × injection × defence against ChatBot.
Run from project root: streamlit run streamlit_app.py
"""

import streamlit as st

from chatbot import ChatBot
from main import DEFENCES_LIST, INTENTIONS_LIST, PROMPT_INJECTIONS_LIST

st.set_page_config(page_title="Prompt injection playground", layout="wide")

st.markdown(
    """
    <style>
    .stTextArea textarea {
        white-space: pre-wrap !important;
        overflow-x: hidden !important;
        overflow-wrap: anywhere;
        word-break: break-word;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Prompt injection playground")
st.caption("Pick an intention, injection template, and defence, then call the model once.")

left, right = st.columns([0.38, 0.62])

with left:
    st.subheader("Controls")
    intention = st.selectbox(
        "Intention",
        INTENTIONS_LIST,
        format_func=lambda x: x.name,
    )
    injection = st.selectbox(
        "Injection template",
        PROMPT_INJECTIONS_LIST,
        format_func=lambda x: x.name,
    )
    defence = st.selectbox(
        "Defence",
        DEFENCES_LIST,
        format_func=lambda x: x.name,
    )
    model = st.text_input(
        "Model",
        value="gpt-3.5-turbo",
        help="Names starting with gpt use OpenAI; others use Anthropic.",
    )
    run = st.button("Run", type="primary", use_container_width=True)

if run:
    built = injection.build_prompt(intention)
    bot = ChatBot()
    try:
        with st.spinner("Calling API…"):
            result = bot.simulate_interaction(built, defence, model=model.strip(), verbose=False)
    except Exception as e:
        st.error(f"Request failed: {e}")
        st.stop()
    intention_ok = intention.validate(result["response_text"])
    st.session_state["last_run"] = {
        "built": built,
        "result": result,
        "intention_ok": intention_ok,
    }

with right:
    st.subheader("Results")
    if "last_run" not in st.session_state:
        st.info("Configure the controls on the left and click **Run** to see the built prompt and model output here.")
    else:
        lr = st.session_state["last_run"]
        built = lr["built"]
        result = lr["result"]
        intention_ok = lr["intention_ok"]

        st.caption("Showing the most recent **Run** (persists while you change controls).")
        st.markdown("**Built user message** (before defence transforms)")
        st.text_area(
            "built_user_message",
            value=built,
            height=220,
            disabled=True,
            label_visibility="collapsed",
        )

        st.markdown("**Outcome**")
        st.markdown(f"**Intention satisfied** (`validate`): `{intention_ok}`")
        if result.get("total_tokens") is not None:
            st.caption(
                f"Tokens — prompt: {result.get('prompt_tokens')}, "
                f"completion: {result.get('completion_tokens')}, "
                f"total: {result.get('total_tokens')}"
            )

        with st.expander("Details", expanded=False):
            st.text_area(
                "System message",
                value=result.get("system_message", ""),
                height=120,
                disabled=True,
            )
            st.text_area(
                "Message sent to model (after defence)",
                value=str(result.get("prompt_to_model", "")),
                height=160,
                disabled=True,
            )
            st.text_area(
                "Model response",
                value=result.get("response_text", ""),
                height=240,
                disabled=True,
            )
