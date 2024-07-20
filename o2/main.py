import langchain_agent as lcha
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize session state
if 'shutdown_requested' not in st.session_state:
    st.session_state.shutdown_requested = False
if 'technical documents' not in st.session_state:
    st.session_state.technicaldocuments = ""


def shutdown():
    st.session_state.shutdown_requested = True
    st.cache_data.clear()
    st.rerun()

# generate Beach Name 
def generate_document():
    openai_api_key = os.getenv('OPEN_AI_KEY')
    if not openai_api_key:
        st.error("OpenAI API key is missing. Please check your environment variables.")
        return

    with st.spinner("RBFS IQ"):
        try:
            print(st.session_state.technology)
            response = lcha.rbfs_response(st.session_state.technology)
            st.session_state.technicaldocuments = response['response']
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def main():
    st.set_page_config(page_title="RBFS IQ Assist", page_icon="🐶")

    if st.session_state.shutdown_requested:
        st.write("Shutting down...")
        time.sleep(2)
        os._exit(0)

    st.title("RBFS IQ Assist ")

    # Sidebar
    with st.sidebar:
        st.session_state.technology = st.selectbox("You want to learn about Technology", ("BGP", "ISIS", "PPPoE", "DHCP", "OSPFv2", "OSPFv3", "LDP", "CG-NAT", "MPLS"))
        
        if st.button("Find Technical Details"):
            generate_document()
        
        if st.button("Shut Down"):
            shutdown()

    # Main content
    if st.session_state.technicaldocuments:
        st.success(f"Technical Documentation {st.session_state.technicaldocuments}")

if __name__ == "__main__":
    main()
