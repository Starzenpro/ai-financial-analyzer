from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os

def process_pdf(file_path):
    """Load PDF, split into chunks, create embeddings, and store in FAISS"""
    # Load PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # Split into chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separator="\n"
    )
    docs = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    return vectorstore

def ask_question(vectorstore, query):
    """Query the vector store with a question"""
    # Create QA chain
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.3,
            max_tokens=500
        ),
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 3}  # Return top 3 chunks
        )
    )
    
    # Get answer
    answer = qa.run(query)
    return answer
