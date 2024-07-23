import pdf_lc_helper as lch
import streamlit as st
from dotenv import load_dotenv
import textwrap
import time
import os
import asyncio

# Load environment variables
load_dotenv()

# Initialize session state
if 'shutdown_requested' not in st.session_state:
    st.session_state.shutdown_requested = False
if 'db' not in st.session_state:
    st.session_state.db = None
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

def shutdown():
    st.session_state.shutdown_requested = True
    st.cache_data.clear()
    st.rerun()

@st.cache_resource
def load_vector_db(url:str):
    return lch.create_vector_db_from_doc(url)

async def async_generate_response_to_query(db, query):
    return await lch.generate_response_to_query(db, query)

def main():

    st.set_page_config(page_title="RBFS IQ Assist", layout="wide")
    openai_api_key = os.getenv('OPENAI_API_KEY')

    if not openai_api_key:
        st.error("OpenAI API key is missing. Please check your environment variables.")
        return
    
    if st.session_state.shutdown_requested:
        st.write("Shutting down...")
        time.sleep(2)
        os._exit(0)

    st.title("RBFS IQ Assist")

    # Sidebar
    st.sidebar.title("Options")
    
    url = st.sidebar.text_area(
        label="Please provide URL of the documentation",
        max_chars=200,
        key="locator"
    )
    query = st.sidebar.text_area(
        label="What do you want to learn about RBFS ?",
        max_chars=200,
    )

    if st.session_state.db is None:
        with st.spinner("Loading document database..."):
            st.session_state.db = load_vector_db(url)

    if st.sidebar.button("Submit Query"):
        if query:
            with st.spinner("Generating response..."):
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response, docs = loop.run_until_complete(async_generate_response_to_query(st.session_state.db, query))
                    st.session_state.query_history.append((query, response))
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.sidebar.warning("Please enter a query.")

    if st.sidebar.button("Clear History"):
        st.session_state.query_history = []
        st.experimental_rerun()

    if st.sidebar.button("Shut Down"):
        shutdown()

    # Main content area
    if st.session_state.query_history:
        for i, (past_query, past_response) in enumerate(reversed(st.session_state.query_history)):
            with st.expander(f"Query {len(st.session_state.query_history) - i}: {past_query[:50]}...", expanded=(i == 0)):
                st.write("**Query:**")
                st.write(past_query)
                st.write("**Response:**")
                st.write(textwrap.fill(past_response, width=90))
    else:
        st.info("No queries yet. Use the sidebar to ask a question!")

if __name__ == "__main__":
    main()