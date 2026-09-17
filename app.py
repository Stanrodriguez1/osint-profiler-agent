import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="OSINT Profiler", page_icon="🕵️")
st.title("🕵️ Customer OSINT Profiling Agent")
st.write("Enter the details below. The AI will natively search Google, cross-reference data, and build an investment profile.")

name = st.text_input("Full Name (Required)")
phone = st.text_input("Phone Number (Optional)")
email = st.text_input("Email Address (Optional)")

if st.button("Start Search & Profile"):
    if not name:
        st.error("Please enter the customer's name.")
    else:
        with st.spinner("Agent is running..."):
            try:
                st.info("🧠 Agent is directly searching Google and analyzing data...")

                # Connect to Gemini securely
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                prompt = f"""
                You are an expert OSINT investigator and financial profiler.
                Target Name: {name}
                Target Phone: {phone}
                Target Email: {email}
                
                Task:
                1. Use your built-in Google Search tool to search the live web for this person (check LinkedIn, company pages, news, etc.).
                2. Identify their most likely professional profile.
                3. Estimate their Financial/Investment Capability (High/Medium/Low) based on their career.
                4. Extract ANY contact info (emails, phone numbers, company websites) you find.
                5. CITE YOUR SOURCES. Provide URLs to the websites where you found the information.
                
                Format the output beautifully in Markdown. If you cannot find any public data on Google, explain that they have no digital footprint.
                """
                
                # We turn on the powerful "google_search" tool here!
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[{"google_search": {}}]
                    )
                )
                
                st.success("✅ Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
