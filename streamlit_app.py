import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("📄 Document question answering with Gemini")
st.write(
    "Upload a document below and ask a question about it – Gemini will answer! "
    "To use this app, you need to provide a Google AI Studio API key, which you can get [here](https://ai.google.dev/). "
)

# Ask user for their Google AI Studio API key.
google_api_key = st.text_input("Google AI Studio API Key", type="password")
if not google_api_key:
    st.info("Please add your Google AI Studio API key to continue.", icon="🗝️")
else:

    # Configure the Google API.
    genai.configure(api_key=google_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        prompt = f"Here's a document: {document} \n\n---\n\n {question}"

        # Create a Gemini Pro model instance.
        model = genai.GenerativeModel('gemini-pro')

        # Generate a response using the Gemini API.
        try:
            # The gemini-pro model does not currently support streaming with
            # `generate_content` in the same way as the OpenAI API's `chat.completions.create`.
            # So we get the full response and then write it.
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
