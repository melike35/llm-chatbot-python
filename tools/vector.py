import streamlit as st
from llm import llm, embeddings
from graph import graph
# Here is where you will store the code for new tools you create. 

# Create the Neo4jVector
"""
1-The embeddings object to embed the user input.
2-The graph object to interact with the database.
3-The name of the index, in this case moviePlots
4-The label of node used to populate the index, in this case, Movie.
5-The name of the property that holds the original plain-text value, in this case, plot.
6-The name of the property that holds the embedding of the original text, in this case, plotEmbedding.

retrieval_query, is an optional parameter that allows you to define which information is returned by the Cypher statement,
"""
from langchain_neo4j import Neo4jVector

neo4jvector = Neo4jVector.from_existing_index(
    embeddings,                              # (1)
    graph=graph,                             # (2)
    index_name="moviePlots",                 # (3)
    node_label="Movie",                      # (4)
    text_node_property="plot",               # (5)
    embedding_node_property="plotEmbedding", # (6)
    retrieval_query="""
RETURN
    node.plot AS text,
    score,
    {
        title: node.title,
        directors: [ (person)-[:DIRECTED]->(node) | person.name ],
        actors: [ (person)-[r:ACTED_IN]->(node) | [person.name, r.role] ],
        tmdbId: node.tmdbId,
        source: 'https://www.themoviedb.org/movie/'+ node.tmdbId
    } AS metadata
"""
)
# Create the retriever
retriever = neo4jvector.as_retriever()


# Create the prompt
"""
The retrieval chain creates an embedding from the user’s input, 
calls the retriever to identify similar documents, and passes them to an LLM to generate a response.
"""
from langchain_core.prompts import ChatPromptTemplate

instructions = (
    "Use the given context to answer the question."
    "If you don't know the answer, say you don't know."
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instructions),
        ("human", "{input}"),
    ]
)
# Create the chain 
"""
    Create a retrieval chain that uses the llm, prompt, and retriever objects:
"""

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

question_answer_chain = create_stuff_documents_chain(llm, prompt)
plot_retriever = create_retrieval_chain(
    retriever, 
    question_answer_chain
)
# Create a function to call the chain
def get_movie_plot(input):
    return plot_retriever.invoke({"input": input})