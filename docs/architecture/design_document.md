# MedIntel AI: System Design & Architecture Document

## 1. Problem Statement
General-purpose LLMs are prone to hallucinations and lack the strict data privacy required for clinical medical research. Uploading sensitive patient data or proprietary clinical trials to public APIs (like OpenAI) violates healthcare compliance standards.

## 2. Solution Architecture
MedIntel AI utilizes a highly decoupled Retrieval-Augmented Generation (RAG) pipeline to ensure zero data leakage. 

* **Frontend:** Built with Next.js for a responsive, server-side rendered client interface.
* **Backend:** FastAPI was selected for its asynchronous capabilities and high performance with Python-based AI workloads.
* **Vector Store:** ChromaDB runs strictly locally.
* **Embeddings:** Hugging Face `sentence-transformers` execute on the local machine. 

## 3. Security & Authentication
To support multi-tenant research environments, the application uses industry-standard security protocols:
* **Password Hashing:** `bcrypt` is used to cryptographically salt and hash passwords before insertion into the SQLite database.
* **Stateless Auth:** JSON Web Tokens (JWT) are generated upon successful login, ensuring secure, scalable authentication across all frontend API requests without requiring persistent server memory.

## 4. Evaluation Strategy
The RAG pipeline is evaluated based on:
1. **Retrieval Latency:** The millisecond delay between user query and ChromaDB vector extraction.
2. **Context Precision:** The relevance of the retrieved document chunks against the medical prompt.