from fastapi import FastAPI
from pydantic import BaseModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

CLEANED_TEXT_PATH = "./data/extracted_text_gemini/combined_text.txt"
CHROMA_PATH = "chroma_db"

with open(CLEANED_TEXT_PATH, "r", encoding="utf-8") as f:
    cleaned_text = f.read()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.create_documents([cleaned_text])

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory=CHROMA_PATH,
)

"""Only add documents if the collection is empty"""
# vectorstore.add_documents(docs)

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.5)

# Conversation memory for short-term context
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="question",
    return_messages=True
)

# ConversationalRetrievalChain for RAG with memory
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={'k': 7}),
    memory=memory,
    verbose=True,
    max_tokens_limit=4096
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    history: list[str] = []

@app.post("/ask")
async def ask_question(request: QueryRequest):
    # Pass both question and chat history for short-term memory
    answer = qa_chain.run({"question": request.question, "chat_history": request.history})
    return {"answer": answer}

