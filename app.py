import streamlit as st
from transformers import pipeline

# Set up the page configuration for a wide layout and better experience
st.set_page_config(
    page_title="Translation App",
    layout="wide",  
)

# Add custom CSS for the header background
st.markdown("""
    <style>
    .header {
        background-image: url('https://images.unsplash.com/photo-1557682250-48bfe2db9041');
        background-size: cover;
        padding: 60px;
        text-align: center;
        border-radius: 15px;
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .header h1 {
        font-size: 50px;
        font-weight: bold;
    }
    .header p {
        font-size: 20px;
        margin-top: 10px;
    }
    .header a {
        color: #ffcc00;
        font-weight: bold;
        text-decoration: none;
    }
    .header a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="header">
        <h1>🤗 Translation App</h1>
        <p>Translate text using pre-trained models from <a href="https://huggingface.co/" target="_blank">Hugging Face</a>.</p>
    </div>
    """, unsafe_allow_html=True)

# Add explanation for the app
st.markdown("""
    This app allows you to translate text into multiple languages using Hugging Face's pre-trained models.
""")

# Input text from user
st.subheader("Enter the text you want to translate:")
user_input = st.text_area("Input text", height=150)

# Select the target language for translation
target_language = st.selectbox("Choose target language", [
    "French", "Spanish", "German", "Russian"
])

# Load the appropriate model for translation
@st.cache_resource(ttl=24*3600)
def load_translation_model(language):
    try:
        if language == "French":
            return pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
        elif language == "Spanish":
            return pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")
        elif language == "German":
            return pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-en-de")
        elif language == "Russian":
            return pipeline("translation_en_to_ru", model="Helsinki-NLP/opus-mt-en-ru")
        else:
            st.error("Unsupported language selected.")
            return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

translator = load_translation_model(target_language)

if translator:
    if st.button("Translate"):
        if user_input:
            translation = translator(user_input)
            st.write(translation[0]['translation_text'])
        else:
            st.error("Please enter text to translate.")
else:
    st.error("Please select a valid language.")
