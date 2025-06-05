import streamlit as st
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx


"""
The function accepts two positional arguments - the role of the author, either human or assistant, and the message. 
You can pass an additional save parameter to instruct the function to append the message to the session state.

The block concludes by setting a question variable containing the user’s input. 
When the user sends their message, the write_message() function saves the message to the session state and displays the message in the UI.
"""
def write_message(role, content, save = True):
    """
    This is a helper function that saves a message to the
     session state and then writes a message to the UI
    """
    # Append to session state
    if save:
        st.session_state.messages.append({"role": role, "content": content})

    # Write to UI
    with st.chat_message(role):
        st.markdown(content)

def get_session_id():
    return get_script_run_ctx().session_id
