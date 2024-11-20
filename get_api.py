import streamlit as st

# Function to get api key from user if not already set
@st.dialog("Enter Your API Key")
def get_api():
    openai = st.text_input("OpenAI API Key", type="password", help="Your API key remains secure and is not saved.")
    st.markdown("[Create your OpenAI API Key](https://platform.openai.com/api-keys)", unsafe_allow_html=True)
    
    with st.container():
        st.write("Enter your neo4j database credentials")
        NEO4J_URI = st.text_input("NEO4J_URI", type="password", help="Your API key remains secure and is not saved.")
        NEO4J_USERNAME = st.text_input("NEO4J_USERNAME", type="password", help="Your API key remains secure and is not saved.")
        NEO4J_PASSWORD = st.text_input("NEO4J_PASSWORD", type="password", help="Your API key remains secure and is not saved.")
        st.markdown("[Create your neo4j graph database](https://console.neo4j.io/)", unsafe_allow_html=True)
    
    if st.button("Submit"):
        if openai and NEO4J_PASSWORD and NEO4J_URI and NEO4J_USERNAME:
            st.session_state.api_keys["OPENAI_API_KEY"] = openai
            st.session_state.api_keys["NEO4J_URI"] = NEO4J_URI
            st.session_state.api_keys["NEO4J_USERNAME"] = NEO4J_USERNAME
            st.session_state.api_keys["NEO4J_PASSWORD"] = NEO4J_PASSWORD
            st.success("API key set successfully!")
            st.rerun()
        else:
            st.error("API key cannot be empty.")