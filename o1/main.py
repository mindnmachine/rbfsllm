
import langchain_helper as lch
import streamlit as st
from dotenv import load_dotenv
import time
import os

# Load environment variables
load_dotenv()

# Initialize session state
if 'shutdown_requested' not in st.session_state:
    st.session_state.shutdown_requested = False
if 'beach_location' not in st.session_state:
    st.session_state.beach_location = ""

def shutdown():
    st.session_state.shutdown_requested = True
    st.cache_data.clear()
    st.rerun()

# generate Beach Name 
def generate_name():
    openai_api_key = os.getenv('OPEN_AI_KEY')
    if not openai_api_key:
        st.error("OpenAI API key is missing. Please check your environment variables.")
        return

    with st.spinner("Find a Beach Location..."):
        try:
            print(st.session_state.country, st.session_state.attribute)
            response = lch.generate_beach_location(st.session_state.country, st.session_state.attribute)
            st.session_state.beach_location = response['beach_location']
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def main():
    st.set_page_config(page_title="Beach Location Assist", page_icon="🐶")

    if st.session_state.shutdown_requested:
        st.write("Shutting down...")
        time.sleep(2)
        os._exit(0)

    st.title("Beach Location ")

    # Sidebar
    with st.sidebar:
        st.session_state.country = st.selectbox("Where do you want to vacation", ("USA", "Brazil", "Spain", "India", "Australia", "Thailand", "Tahiti"))
        st.session_state.attribute = st.selectbox("Which adjective best describes the beach ",("Sandy Shores","Backwater Oasis","Tropical Paradise","Stinky and Sunny", "Sweaty and Party", "Shark Infested"))
        
        if st.button("Find a Beach"):
            generate_name()
        
        if st.button("Shut Down"):
            shutdown()

    # Main content
    if st.session_state.beach_location:
        st.success(f"Suggested Holiday Locations: {st.session_state.beach_location}")
    
    #st.markdown("---")
    #st.markdown("1. Select the C.")
    #st.markdown("2. Enter the color of your pet.")
    #st.markdown("3. Click 'Generate Name' to get a unique pet name!")

if __name__ == "__main__":
    main()
