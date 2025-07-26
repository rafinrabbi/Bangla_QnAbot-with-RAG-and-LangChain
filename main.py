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
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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

# Only add documents if the collection is valid and empty
try:
    if vectorstore._collection.count() == 0:
        vectorstore.add_documents(docs)
except Exception as e:
    print(f"ChromaDB collection error: {e}")
    vectorstore.add_documents(docs)

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
    # Get retrieved docs and answer
    result = qa_chain({"question": request.question, "chat_history": request.history, "return_source_documents": True})
    answer = result["answer"] if isinstance(result, dict) and "answer" in result else result
    source_docs = result["source_documents"] if isinstance(result, dict) and "source_documents" in result else []

    # Compute similarity if possible
    clarification_threshold = 0.3  # Adjust as needed
    is_vague = False
    if source_docs:
        try:
            query_embedding = embeddings.embed_query(request.question)
            chunk_embeddings = [embeddings.embed_documents([doc.page_content])[0] for doc in source_docs]
            scores = [cosine_similarity([query_embedding], [chunk_emb])[0][0] for chunk_emb in chunk_embeddings]
            max_score = max(scores) if scores else 0
            if max_score < clarification_threshold:
                is_vague = True
        except Exception as e:
            print(f"Similarity check failed: {e}")

    if is_vague or not answer or answer.strip() == "":
        return {"answer": "Your question is unclear or not enough context was found. Could you please clarify or provide more details?"}
    return {"answer": answer}

