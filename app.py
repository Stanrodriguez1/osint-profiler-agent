import streamlit as st
from duckduckgo_search import DDGS
from google import genai

st.set_page_config(page_title="OSINT Profiler", page_icon="🕵️")
st.title("🕵️ Customer OSINT Profiling Agent")
st.write("Enter the details below. The AI will scour the web, cross-reference data, and build an investment profile.")

name = st.text_input("Full Name (Required)")
phone = st.text_input("Phone Number (Optional)")
email = st.text_input("Email Address (Optional)")

if st.button("Start Search & Profile"):
    if not name:
        st.error("Please enter the customer's name.")
    else:
        with st.spinner("Agent is running..."):
            try:
                queries = [
                    f'{name} {phone if phone else ""} {email if email else ""}',
                    f'{name} LinkedIn OR Business OR Director'
                ]
                
                st.info("📡 Step 1: Searching the web for public records...")
                
                ddgs = DDGS()
                search_results = []
                for q in queries:
                    results = ddgs.text(q, max_results=5, backend="lite")
                    if results:
                        search_results.extend(results)
                
                formatted_results = ""
                for r in search_results:
                    formatted_results += f"Source URL: {r.get('href')}\nTitle: {r.get('title')}\nSnippet: {r.get('body')}\n\n"
                
                if not formatted_results:
                    st.warning("No public data found on the web for this person. Try adding their city or company name next to their name.")
                    st.stop()

                st.info("🧠 Step 2: Web data found! Feeding into Gemini AI for analysis...")

                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                prompt = f"""
                You are an expert OSINT investigator and financial profiler.
                Target Name: {name}
                Target Phone: {phone}
                Target Email: {email}
                
                Here is raw search data found on the live web:
                {formatted_results}
                
                Task:
                1. Identify the most likely professional profile(s) for this person.
                2. Estimate their Financial/Investment Capability (High/Medium/Low) based on their career.
                3. Look closely at the snippets and extract ANY new/missing contact info (emails, phone numbers, company websites).
                4. CITE YOUR SOURCES. Always list the exact Source URLs where you found the information.
                
                Format the output beautifully in Markdown.
                """
                
                # Gemini models do not constantly deprecate like NVIDIA
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                st.success("✅ Analysis Complete!")
                st.markdown(response.text)
                
                with st.expander("View Raw Web Data Sources"):
                    st.text(formatted_results)
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
