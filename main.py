# import streamlit as st
# import google.generativeai as genai

# # Set up the app title
# st.title("AI Code Reviewer")

# # Read API key from file
# with open("API_key.txt", "r") as f:
#     api_key = f.read().strip()

# # Configure the GenAI model
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel(model_name="gemini-2.0-flash-001")

# # Define system prompt
# sys_prompt = """You are an AI Code Reviewer. Your task is to analyze the submitted code of any lanuage and provide feedback 
# if the code contains errors or bugs then correct then with the fixed code and explain the error , why it occured in short,
# if the code has no errors just explain the code what that code does in short. 

# If errors are found:
# 1. Briefly explain the issues present in the code.
# 2. Provide a corrected version of the code in a copyable format.

# If the code has no errors: reply with errors found and also explain what the code does.

# Keep responses concise, clear, and focused on code quality.
# if the topic is not about the data science related things or programming related things just kindly replay then i am a code reviewer.(in your own comic way.)"""

# # Initialize session state for history & text input
# if "history" not in st.session_state:
#     st.session_state.history = []
# if "user_input" not in st.session_state:
#     st.session_state.user_input = ""

# # User input field
# user_query = st.text_area("Submit your code for review :", value=st.session_state.user_input, height=150)

# # Generate response on button click
# if st.button("Submit") and user_query.strip():
#     # Generate content using AI model
#     response = model.generate_content(f"{sys_prompt}\n\nUser: {user_query}")

#     # Store query and response in history
#     st.session_state.history.append({"query": user_query, "response": response.text})

#     # Display the response under the button
#     st.subheader("Review Result:")
#     st.write(response.text)

#     # Clear text area for next input
#     st.session_state.user_input = ""
#     #st.st.query_params()  # This helps refresh the UI

# # Sidebar for query history
# st.sidebar.title("Review History")
# for idx, entry in enumerate(st.session_state.history):
#     if st.sidebar.button(f"Query {idx + 1}"):
#         st.subheader("Review Result:")
#         st.write(entry["response"])

import streamlit as st
import google.generativeai as genai

# Set up the app title
st.title("AI Code Reviewer ")

# Read API key from file
try:
    with open("API_key.txt", "r") as f:
        api_key = f.read().strip()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-001")
except Exception as e:
    st.error("API Key Error! Please check your API key file.")
    st.stop()  # Stop execution if API key fails

# Define system prompt
sys_prompt = """You are an AI Code Reviewer. Your task is to analyze submitted code in any programming language. 
If the code contains errors or bugs:
1. Explain the errors briefly and why they occurred.
2. Provide the corrected version in a copyable format.

If the code has no errors:
- Explain what the code does in short.

If the question is **not related to programming or data science**, reply humorously that you are a code reviewer. Keep responses concise and focused."""

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# User input field
user_query = st.text_area("Submit your code for review:", height=150, key="user_input")

# Process submission
if st.button("Submit") and user_query.strip():
    with st.spinner("Reviewing your code... "):
        try:
            response = model.generate_content(f"{sys_prompt}\n\nUser: {user_query}")
            ai_response = response.text.strip() if response.text else " Error: No response received."

            # Store in history
            st.session_state.history.append({"query": user_query, "response": ai_response})

            # Display response
            st.subheader("Review Result:")
            st.write(ai_response)

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Sidebar for query history with dropdown
st.sidebar.title("Review History")
if st.session_state.history:
    queries = [f"Query {i+1}" for i in range(len(st.session_state.history))]
    selected_query = st.sidebar.selectbox("Select a past query:", queries, index=len(queries)-1)

    # Display selected query result
    if selected_query:
        idx = queries.index(selected_query)
        st.sidebar.subheader("Selected Review Result:")
        st.sidebar.write(st.session_state.history[idx]["response"])
else:
    st.sidebar.write("No queries yet. Submit your code above!")