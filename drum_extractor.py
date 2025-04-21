import streamlit as st
import openai

# UI
st.title("DRuM Clinical Summary Extractor (BYO Key)")
user_key = st.text_input("Enter your OpenAI API key:", type="password")
text_input = st.text_area("Paste your clinical summary below:", height=300)

# GPT prompt
system_prompt = """
You are a clinical assistant extracting structured, concise text from clinical summaries.
For each summary, extract the following fields in this order:
1) Study – Name, NCT ID, design, population, enrollment, and status/date.
2) Target Population – Who was studied (demographics, diagnosis, inclusion criteria).
3) Key Findings – Main outcomes, efficacy, safety, time to effect.
4) Milestones – Publications, interim/final results, regulatory updates.
5) Dosing – Dose, route, frequency if available.
Use short, complete sentences. Do not include bullets or markdown.
Do not include Drug Name, Mechanism, or Indications.
"""

# Button
if st.button("Extract"):
    if not user_key:
        st.error("Please enter your OpenAI API key.")
    elif not text_input.strip():
        st.warning("Paste a summary before extracting.")
    else:
        try:
            client = openai.OpenAI(api_key=user_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # change to gpt-4 if users have access
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text_input}
                ]
            )
            result = response.choices[0].message.content
            st.text_area("Structured Output:", value=result, height=300)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
