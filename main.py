import os
from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
import textract
import re


import constants

# Set the OpenAI API key environment variable from a constant
os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Open the file 'data.txt' and read its content into the variable 'text'
with open('data.txt', 'r') as f:
    text = f.read()

# Initialize a tokenizer from the GPT-2 model for tokenization
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

# Define a function to count the number of tokens in a given text
def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

# Create a text splitter that divides text into smaller chunks suitable for processing.
# 'chunk_size' sets the maximum number of characters in each chunk,
# 'chunk_overlap' allows chunks to overlap by a certain number of characters to maintain context,
# 'length_function' uses the defined token count function to measure chunk length
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 512,
    chunk_overlap  = 24,
    length_function = count_tokens,
)

# Apply the text splitter to the read text, splitting it into manageable chunks
chunks = text_splitter.create_documents([text])

# Initialize a model to convert text chunks into vector embeddings
embeddings = OpenAIEmbeddings()

# Create a vector database using FAISS (Fast Approximate Nearest Neighbors) 
# for efficient similarity search. The database is populated with the chunk embeddings.
db = FAISS.from_documents(chunks, embeddings)

# Load a QA chain for integrating similarity search with user queries.
# This chain uses the OpenAI model for generating responses, tailored for a specific type of queries ("stuff").
chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")

# Example query for demonstration
query = "Who invented electricity?"

# Perform a similarity search in the vector database using the query,
# which returns the most relevant document chunks
docs = db.similarity_search(query)

# Run the QA chain with the retrieved documents and the query
chain.run(input_documents=docs, question=query)

# Create a conversational retrieval chain that combines a language model with the vector database retriever.
# This is used to generate responses in a conversational context.
qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.1), db.as_retriever())

# Define a function to get a response for a user input, taking into account the chat history
def get_response(user_input, chat_history):
    # Use the conversational retrieval chain to get a response
    # 'user_input' is the new question from the user, 'chat_history' contains previous dialogues
    result = qa({"question": user_input, "chat_history": chat_history})
    return result['answer']