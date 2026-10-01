
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from groq import APIConnectionError, APIStatusError, RateLimitError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

st.set_page_config(
    page_title="Groq Text Summarizer",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Groq Text Summarization")
st.write("Transform lengthy text into a clear, concise summary using AI.")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is missing. Add it to your .env file.")
    st.stop()

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"

text = st.text_area(
    "Enter text to summarize",
    height=250,
    placeholder="Paste your article, paragraph, or notes here..."
)

if st.button("✨ Summarize Text", use_container_width=True):
    if not text.strip():
        st.warning("Please enter some text before summarizing.")
    else:
        prompt = f"""
Summarize the following text clearly and accurately.

Requirements:
- Write 5 to 8 sentences when the text contains enough information.
- Preserve the main ideas and important facts.
- Use simple, easy-to-understand language.
- Remove unnecessary repetition.
- Do not introduce information absent from the original text.
- If the input is very short, provide a proportionately short summary.

TEXT:
{text}
"""

        try:
            with st.spinner("AI is generating your summary..."):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an expert text summarization "
                                "assistant. Summarize accurately and "
                                "never invent facts."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,
                    max_completion_tokens=800
                )

                summary = response.choices[0].message.content

            if not summary or not summary.strip():
                st.warning("The model returned an empty summary. Please try again.")
            else:
                st.subheader("📄 Generated Summary")
                st.write(summary)

                st.download_button(
                    label="⬇️ Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )

                st.success("Summary generated successfully!")

        except RateLimitError:
            st.error(
                "Groq API rate limit reached. Please wait and try again."
            )

        except APIConnectionError:
            st.error(
                "Cannot connect to Groq. Check your internet connection."
            )

        except APIStatusError as e:
            st.error(f"Groq API error ({e.status_code}): {e.message}")

        except Exception as e:
            st.error(f"Unexpected error: {e}")
