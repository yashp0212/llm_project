import streamlit as st
import google.generativeai as genai
from apikey import google_gemini_api_key


genai.configure(api_key=google_gemini_api_key)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)


st.set_page_config(page_title="ContentGenie", page_icon="📜🤖", layout="wide")

st.title('📜 ContentGenie: Your AI Writing Companion')
st.subheader("Now You can Write your content here")


col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    blog_title = st.text_input("Blog Title", placeholder="Enter your blog title here")
    keywords = st.text_area("Keywords (comma-separated)", placeholder="e.g. AI, technology, future")
    num_words = st.slider("Number of Words", min_value=250, max_value=1000, step=250)
    submit_button = st.button("Generate My Blog")

if submit_button:
    with st.spinner("Generating your blog..."):
        prompt = f"""
        Generate a comprehensive, engaging blog post relevant to the given title "{blog_title}" and keywords "{keywords}". 
        Make sure to incorporate these keywords in the blog post. The blog should be approximately {num_words} words in length, 
        suitable for an online audience. Ensure the content is original, informative, and maintains a consistent tone throughout.
        """
        chat_session = model.start_chat(history=[{"role": "user", "parts": [prompt]}])
        response = chat_session.send_message("Please generate the blog content based on the provided details.")
    
    st.success("Blog generated successfully!")
    st.subheader(blog_title)
    st.write(response.text)
    st.session_state.chat_session = chat_session


st.markdown("---")
st.subheader("Chat with ContentGenie")

user_message = st.text_input("You:", placeholder="Ask ContentGenie something...", key="chat_input")

if user_message:
    if 'chat_session' not in st.session_state:
        st.error("Please generate the blog first to start the chat session.")
    else:
        chat_response = st.session_state.chat_session.send_message(user_message)
        st.markdown(f"**You:** {user_message}")
        st.markdown(f"**ContentGenie:** {chat_response.text}")


