import streamlit as st
from google import genai

st.set_page_config(page_title="OSINT Profiler", page_icon="🕵️")
st.title("🕵️ Customer OSINT Profiling Agent (Free Tier)")
st.write("Enter the details below. The AI will build an investment profile based on its extensive internal knowledge base.")

name = st.text_input("Full Name (Required)")
phone = st.text_input("Phone Number (Optional)")
email = st.text_input("Email Address (Optional)")

if st.button("Start Search & Profile"):
    if not name:
        st.error("Please enter the customer's name.")
    else:
        with st.spinner("Agent is running..."):
            try:
                st.info("🧠 Analyzing customer data...")

                # Connect to Gemini securely
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                prompt = f"""
                You are an expert OSINT investigator and financial profiler.
                Target Name: {name}
                Target Phone: {phone}
                Target Email: {email}
                
                Task:
                1. Search your internal knowledge base for any information on this person.
                2. Identify their most likely professional profile and industry.
                3. Estimate their Financial/Investment Capability (High/Medium/Low) based on their likely career.
                4. Note: If the person is not famous or public enough to be in your training data, provide a general profile of what a person with their name/background in their region might look like financially, but explicitly state that you are making an educated guess due to a lack of public footprint.
                
                Format the output beautifully in Markdown.
                """
                
                # Using Gemini 3.6 Flash without the gated search tool
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
                
                st.success("✅ Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
