import os
import streamlit as st
import openai

try:
    openai.api_key = st.secrets["openai"]["api_key"]
except KeyError:
    st.error("API key is not found in Streamlit secrets. Please check your secrets configuration.")
    openai.api_key = None
# Default compliance standards
DEFAULT_STANDARDS = """
1. No hardcoded sensitive data like passwords or API keys.
2. Proper error handling must be in place.
3. Input must be validated to avoid injections.
4. Use parameterized queries to avoid SQL injection.
5. No usage of deprecated functions or insecure libraries.
"""

# Function to send code and standards to GPT-4 or GPT-3.5 and receive analysis
def analyze_code_with_standards(code, standards):
    # Use a chat-based prompt for the OpenAI Chat API
    messages = [
        {"role": "system", "content": "You are a security expert. Analyze code based on user-defined security standards."},
        {"role": "user", "content": f"Standards: {standards}"},
        {"role": "user", "content": f"Code: {code}"}
    ]

    try:
        # Use the v1/chat/completions endpoint for chat-based models
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
            messages=messages,
            max_tokens=600,
            temperature=0.5
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.title("Custom Secure Code Review Tool")

st.markdown(
    """
    **Welcome to the Secure Code Review Tool!**
    
    This is a project made by **Jasmine and Chavi** for the **Cybersecurity course**.
    Use this tool to analyze code based on specific security standards.
    """
)

# Allow user to input or upload code
uploaded_file = st.file_uploader("Upload your code file", type=["py", "js", "java", "c", "cpp", "ts"])
user_code = st.text_area("Or, paste your code below:")

# User-defined standards
user_standards = st.text_area("Define your security standards or rules (e.g., 'No hardcoded passwords', 'SQL queries must use parameterized inputs'): ")

# Button to analyze code
if st.button("Analyze Code"):
    # If a file is uploaded, use the uploaded file content, otherwise, use the pasted code
    if uploaded_file is not None:
        # Read the content of the uploaded file
        user_code = uploaded_file.read().decode("utf-8")
    
    if user_code:  # Check if code is available
        # Use default standards if none are provided by the user
        standards_to_use = user_standards if user_standards.strip() else DEFAULT_STANDARDS

        with st.spinner('Analyzing your code based on the standards...'):
            # Analyze the code using the selected standards
            result = analyze_code_with_standards(user_code, standards_to_use)
            st.success("Analysis complete!")
            st.text_area("Code Review Results", result, height=300)
    else:
        st.warning("Please upload a code file or paste your code.")

