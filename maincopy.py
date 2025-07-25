# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

# File paths
CLEANED_TEXT_PATH = "./data/extracted_text_gemini/cleaned_gemini_output.txt"
CHROMA_PATH = "chroma_db"

# Load text
with open(CLEANED_TEXT_PATH, "r", encoding="utf-8") as f:
    cleaned_text = f.read()

# Split text into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.create_documents([cleaned_text])

# Create embeddings and vectorstore
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory=CHROMA_PATH,
)
vectorstore.add_documents(docs)

# Create QA chain
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.5)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={'k': 5})
)

# FastAPI app
app = FastAPI()

# CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    answer = qa_chain.run(request.question)
    return {"answer": answer}


