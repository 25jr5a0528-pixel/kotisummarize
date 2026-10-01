
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Groq Text Summarizer",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Groq Text Summarization")
st.write("Enter your text below and generate a summary using AI.")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is missing. Check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

text = st.text_area(
    "Enter text to summarize",
    height=250,
    placeholder="Paste your paragraph or article here..."
)

if st.button("✨ Summarize Text", use_container_width=True):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        prompt = f"""
Summarize the following text clearly and accurately.

Requirements:
- Keep the important information.
- Remove unnecessary repetition.
- Use simple language.
- Do not add information not present in the original.
- Give the summary in 5 to 8 sentences.

Text:
{text}
"""

        try:
            with st.spinner("Generating summary..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert text summarization assistant."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,
                    max_completion_tokens=500
                )

                summary = response.choices[0].message.content

            st.subheader("📄 Summary")
            st.write(summary)

            st.download_button(
                label="Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error generating summary: {e}")