from dotenv import load_dotenv
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
import streamlit as st

# Loading OpenAI API Keys
load_dotenv()

def get_response(text, graph):
    examples = [
        {
            "question": "How many artists are there?",
            "query": "MATCH (a:Person)-[:ACTED_IN]->(:Movie) RETURN count(DISTINCT a)",
        },
        {
            "question": "Which actors played in the movie Casino?",
            "query": "MATCH (m:Movie {{title: 'Casino'}})<-[:ACTED_IN]-(a) RETURN a.name",
        },
        {
            "question": "How many movies has Tom Hanks acted in?",
            "query": "MATCH (a:Person {{name: 'Tom Hanks'}})-[:ACTED_IN]->(m:Movie) RETURN count(m)",
        },
        {
            "question": "List all the genres of the movie Schindler's List",
            "query": "MATCH (m:Movie {{title: 'Schindler\\'s List'}})-[:IN_GENRE]->(g:Genre) RETURN g.name",
        },
        {
            "question": "Which actors have worked in movies from both the comedy and action genres?",
            "query": "MATCH (a:Person)-[:ACTED_IN]->(:Movie)-[:IN_GENRE]->(g1:Genre), (a)-[:ACTED_IN]->(:Movie)-[:IN_GENRE]->(g2:Genre) WHERE g1.name = 'Comedy' AND g2.name = 'Action' RETURN DISTINCT a.name",
        },
        {
            "question": "Which directors have made movies with at least three different actors named 'John'?",
            "query": "MATCH (d:Person)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(a:Person) WHERE a.name STARTS WITH 'John' WITH d, COUNT(DISTINCT a) AS JohnsCount WHERE JohnsCount >= 3 RETURN d.name",
        },
        {
            "question": "Identify movies where directors also played a role in the film.",
            "query": "MATCH (p:Person)-[:DIRECTED]->(m:Movie), (p)-[:ACTED_IN]->(m) RETURN m.title, p.name",
        },
        {
            "question": "Find the actor with the highest number of movies in the database.",
            "query": "MATCH (a:Actor)-[:ACTED_IN]->(m:Movie) RETURN a.name, COUNT(m) AS movieCount ORDER BY movieCount DESC LIMIT 1",
        },

        {
            "question": "Find all comedy movies featuring Robin Williams.",
            "query": "MATCH (a:Person {{name: 'Robin Williams'}})-[:ACTED_IN]->(m:Movie)-[:IN_GENRE]->(g:Genre {{name: 'Comedy'}}) RETURN DISTINCT m.title"
        }
    ]

    example_prompt = PromptTemplate.from_template(
        "User input: {question}\nCypher query: {query}")
    
    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="You are a Neo4j expert. Given an input question, create a syntactically correct Cypher query to run. Return only the Cypher query and nothing else.\n\nHere is the schema information\n{schema}.\n\nBelow are a number of examples of questions and their corresponding Cypher queries.",
        suffix="User input: {question}",
        input_variables=["question", "schema"],
    )
    

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=st.session_state.api_keys["OPENAI_API_KEY"])
    
    chain = GraphCypherQAChain.from_llm(
        graph=graph, llm=llm, cypher_prompt=prompt, verbose=True, allow_dangerous_requests=True, return_intermediate_steps=True
    )
    
    response = chain.invoke({"query": text})

    return response