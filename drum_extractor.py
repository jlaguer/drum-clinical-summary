import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

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

st.title("DRuM Clinical Summary Extractor")
text_input = st.text_area("Paste your clinical summary below:", height=300)

if st.button("Extract"):
    if not text_input.strip():
        st.warning("Please paste a summary first.")
    else:
        with st.spinner("Extracting..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text_input}
                ]
            )
            result = response['choices'][0]['message']['content']
            st.text_area("Structured Output:", value=result, height=300)
