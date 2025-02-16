import streamlit as st
import google.generativeai as genai

st.title("AI Code Reviewer ")

try:
    with open("API_key.txt", "r") as f:
        api_key = f.read().strip()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-001")
except Exception as e:
    st.error("API Key Error! Please check your API key file.")
    st.stop()

sys_prompt = """You are an AI Code Reviewer. Your task is to analyze submitted code in any programming language. 
If the code contains errors or bugs:
1. Explain the errors briefly and why they occurred.
2. Provide the corrected version in a copyable format.

If the code has no errors:
- Explain what the code does in short.

If the question is **not related to programming or data science**, reply humorously that you are a code reviewer. Keep responses concise and focused."""

if "history" not in st.session_state:
    st.session_state.history = []

user_query = st.text_area("Submit your code for review:", height=150, key="user_input")

if st.button("Submit") and user_query.strip():
    with st.spinner("Reviewing your code... "):
        try:
            response = model.generate_content(f"{sys_prompt}\n\nUser: {user_query}")
            ai_response = response.text.strip() if response.text else " Error: No response received."
            st.session_state.history.append({"query": user_query, "response": ai_response})
            st.subheader("Review Result:")
            st.write(ai_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.sidebar.title("Review History")
if st.session_state.history:
    queries = [f"Query {i+1}" for i in range(len(st.session_state.history))]
    selected_query = st.sidebar.selectbox("Select a past query:", queries, index=len(queries)-1)

    if selected_query:
        idx = queries.index(selected_query)
        st.sidebar.subheader("Selected Review Result:")
        st.sidebar.write(st.session_state.history[idx]["response"])
else:
    st.sidebar.write("No queries yet. Submit your code above!")
