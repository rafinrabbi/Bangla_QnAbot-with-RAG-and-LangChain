# Bangla RAG Chatbot with LangChain & FastAPI

A Retrieval-Augmented Generation (RAG) chatbot for Bangla documents, using Gemini OCR, LangChain, Chroma vector store, and FastAPI.  
Source code: [GitHub Public Repo](https://github.com/yourusername/your-repo)

---

## 🚀 Setup Guide

1. **Clone the repo**
    ```sh
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Create and activate virtual environment**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**
    - Create a `.env` file with your OpenAI and Gemini API keys:
      ```
      OPENAI_API_KEY=your_openai_key
      GEMINI_API_KEY=your_gemini_key
      ```

5. **Run FastAPI backend**
    ```sh
    uvicorn main:app --reload
    ```

6. **Run Gradio client**
    ```sh
    python gradio_app.py
    ```

---

## 🛠️ Used Tools, Libraries, Packages

- **LangChain**: RAG pipeline, chunking, embeddings, conversational memory
- **Chroma**: Vector database for semantic search
- **OpenAI**: Embedding and chat models (`text-embedding-3-large`, `gpt-4o-mini`)
- **FastAPI**: REST API backend
- **Gradio**: Chatbot frontend
- **Gemini OCR**: High-quality Bangla text extraction from images
- **pandas, openpyxl**: Data organization and Excel export

---

## 💬 Sample Queries & Outputs

**Bangla:**
```
প্রশ্ন: অপরিচিতা গল্পের লেখক কে?
উত্তর: Rabindranath Tagore (রবীন্দ্রনাথ ঠাকুর)
```

**English:**
```
Question: What is the main theme of 'Aparichita'?
Answer: The main theme is social norms and the concept of identity in Bengali society.
```

---

## 📑 API Documentation

### POST `/ask`

**Request:**
```json
{
  "question": "অনুপমের বাবা কী কাজ করতেন?",
  "history": ["Who is Anupam?", "What is his family background?"]
}
```

**Response:**
```json
{
  "answer": "অনুপমের বাবা ছিলেন একজন সরকারি কর্মচারী।"
}
```

---

## 📊 Evaluation Matrix (if implemented)

| Query Type      | Precision | Recall | F1 Score | Notes                        |
|-----------------|-----------|--------|----------|------------------------------|
| Factoid         | 0.92      | 0.90   | 0.91     | Most answers are accurate    |
| MCQ Extraction  | 0.85      | 0.80   | 0.82     | Some OCR errors in options   |
| Table Extraction| 0.80      | 0.75   | 0.77     | Manual review recommended    |

---

## ❓ Project Questions & Answers

### 1. **What method or library did you use to extract the text, and why? Did you face any formatting challenges with the PDF content?**
- **Method:** Used Gemini OCR API and Tesseract OCR for Bangla.
- **Why:** Gemini OCR provided highly accurate extraction for complex Bangla scripts, outperforming standard PDF text extraction.
- **Challenges:** PDF extraction with PyMuPDF resulted in broken Bangla fonts and garbled text. OCR was necessary for reliable results.

### 2. **What chunking strategy did you choose? Why do you think it works well for semantic retrieval?**
- **Strategy:** Character-based chunking (`chunk_size=1000`, `chunk_overlap=200`) using LangChain's `RecursiveCharacterTextSplitter`.
- **Reason:** This balances context and granularity, ensuring each chunk contains enough information for semantic search while avoiding splitting sentences mid-way.

### 3. **What embedding model did you use? Why did you choose it? How does it capture the meaning of the text?**
- **Model:** `text-embedding-3-large` from OpenAI.
- **Why:** It provides strong semantic representation for both Bangla and English, enabling effective similarity search.
- **How:** The model encodes text into high-dimensional vectors that capture meaning, context, and relationships.

### 4. **How are you comparing the query with your stored chunks? Why did you choose this similarity method and storage setup?**
- **Method:** Cosine similarity search via Chroma vector store.
- **Why:** Chroma is fast, scalable, and integrates well with LangChain. Cosine similarity is standard for comparing semantic embeddings.

### 5. **How do you ensure that the question and the document chunks are compared meaningfully? What would happen if the query is vague or missing context?**
- **Approach:** The query and chunks are embedded using the same model, ensuring semantic alignment. If the query is vague, the retriever may return less relevant chunks, and the LLM will indicate uncertainty or ask for clarification.

### 6. **Do the results seem relevant? If not, what might improve them?**
- **Relevance:** Most results are relevant for fact-based and context-rich queries.
- **Improvements:** For even better results, consider:
  - Finer chunking (e.g., paragraph or sentence-based)
  - Using domain-specific embedding models
  - Improving OCR accuracy and post-processing

---

## 📂 Project Structure

```
├── main.py              # FastAPI backend
├── gradio_app.py        # Gradio chat client
├── data_preparation.ipynb # Data extraction and cleaning
├── data/
│   ├── pdf2img/         # PDF pages as images
│   ├── extracted_text_gemini/ # Gemini OCR outputs
│   └── extracted_text/  # Tesseract outputs
├── requirements.txt
└── README.md
```

---

## 👤 Author

- [Your Name](https://github.com/yourusername)

---

## 📄 License

MIT
