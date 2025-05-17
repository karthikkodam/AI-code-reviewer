import streamlit as st
import google.generativeai as genai

st.title("AI Code Reviewer")

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if not st.session_state.api_key:
    st.session_state.api_key = st.text_input("Enter your Google Generative AI API Key", type="password")
    if not st.session_state.api_key:
        st.warning("Please enter your API key to continue.")
        st.stop()

try:
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-001")
except Exception as e:
    st.error("Invalid API key or configuration error.")
    st.stop()

# System prompt for AI behavior
sys_prompt = '''
You are an AI Code Reviewer. Your task is to analyze submitted code in any programming language and provide a structured review.

If the code contains errors (syntax, logical, or runtime): 
1. Identify and explain the errors concisely.  
2. Provide a corrected version in a copyable format.  
3. Ensure the logic is correct; if flawed, correct it with an explanation.  

If the code is correct but inefficient:
- Suggest performance optimizations (e.g., time and space complexity improvements).  

If the code is correct and efficient:
- Briefly explain what the code does in simple terms.  

Additional Considerations:
- Ensure readability and best coding practices (e.g., meaningful variable names, comments, modularity).  
- If the user submits a non-programming question, respond humorously as a dedicated code reviewer.  

Keep responses concise, structured, and helpful.
'''

# Review history storage
if "history" not in st.session_state:
    st.session_state.history = []

user_query = st.text_area("Submit your code for review:", height=150, key="user_input", placeholder="Paste your code here...")

if st.button("Review"):
    with st.spinner("Reviewing your code..."):
        try:
            response = model.generate_content(f"{sys_prompt}\n\nUser: {user_query}")
            ai_response = response.text.strip() if response.text else "Error: No response received."

            st.session_state.history.append({"query": user_query, "response": ai_response})

            st.subheader("Review Result:")
            st.write(ai_response)

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Sidebar - Review History
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
