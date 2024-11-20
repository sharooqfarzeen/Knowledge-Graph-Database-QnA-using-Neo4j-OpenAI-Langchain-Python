import streamlit as st
from PIL import Image

from get_response import get_response
from create_graph import create_graphdb

# Streamlit app

# Page title and layout settings
st.set_page_config(page_title="GraphDB QnA")

# Title
st.title("Graph Database QnA")

link = "https://github.com/tomasonjo/blog-datasets/blob/main/movies/movies_small.csv"

# Add instructions prompt for users
st.info(f"""
Welcome! This app allows you to explore a movie database using natural language queries.
You can ask questions about movies, actors, directors, genres, and release dates. Here are some example queries you can try:

- "List all movies directed by Martin Scorsese."
- "Who starred in the movie *Toy Story*?"
- "Show movies released after 1990 with an IMDb rating above 8."
- "Find all comedy movies featuring Robin Williams."
- "What genres are associated with the movie *Jumanji*?"

You can also explore combinations, such as movies in a specific genre directed by certain directors or movies featuring particular actors. Be specific with your queries to get the best results!
        
View Dataset: {link}
""")

# Initializing chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Creating the GraphDB
if "graphdb" not in st.session_state:
     with st.spinner(text="Creating Knowledge Graph"):
        st.session_state["graphdb"] = create_graphdb()
        # # Display assistant message in chat message container
        # st.chat_message("assistant").write("Knowledge Graph Created.")
        # Add user message to chat history
        st.session_state.messages.append({"role": "assistant", "content": "Knowledge Graph Created."})


# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

text = st.chat_input(placeholder="Who starred in the movie Toy Story?")

# React to user input
if text:
    # Display user message in chat message container
    st.chat_message("user").markdown(text)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": text})

    # Get response
    response = get_response(text, st.session_state["graphdb"])
    
    result = response["result"]
    cypher_query = response["intermediate_steps"][0]["query"] if response["intermediate_steps"][0]["query"] else ""
    
    with st.chat_message("assistant"):
        st.write(result)
        with st.expander("View Generated Cypher Query:"):
            st.write(cypher_query)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": result})