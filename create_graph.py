import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
import streamlit as st

# Loading Neo4j credentials
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def create_graphdb():
    # Initializin the graph db
    graph = Neo4jGraph(url=st.session_state.api_keys["NEO4J_URI"], username=st.session_state.api_keys["NEO4J_USERNAME"], password=st.session_state.api_keys["NEO4J_PASSWORD"])

    # Query to create the graph db
    movies_query = """
    LOAD CSV WITH HEADERS FROM 
    'https://raw.githubusercontent.com/tomasonjo/blog-datasets/main/movies/movies_small.csv'
    AS row
    MERGE (m:Movie {id:row.movieId})
    SET m.released = date(row.released),
        m.title = row.title,
        m.imdbRating = toFloat(row.imdbRating)
    FOREACH (director in split(row.director, '|') | 
        MERGE (p:Person {name:trim(director)})
        MERGE (p)-[:DIRECTED]->(m))
    FOREACH (actor in split(row.actors, '|') | 
        MERGE (p:Person {name:trim(actor)})
        MERGE (p)-[:ACTED_IN]->(m))
    FOREACH (genre in split(row.genres, '|') | 
        MERGE (g:Genre {name:trim(genre)})
        MERGE (m)-[:IN_GENRE]->(g))
    """

    # Creating the graph db
    graph.query(movies_query)

    # Refreshing Schema
    graph.refresh_schema()

    return graph