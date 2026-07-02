import os

def create_directory_structure():
    structure = [
        # Backend Core & Application Layers
        "backend/app/api/v1/endpoints",
        "backend/app/core",
        "backend/app/db",
        "backend/app/domain/models",
        "backend/app/domain/services",
        "backend/app/infrastructure/security",
        "backend/app/infrastructure/repositories",
        
        # Advanced AI & RAG Layers
        "backend/app/ai/agents",
        "backend/app/ai/prompts",
        "backend/app/ai/workflows",
        "backend/app/rag/embeddings",
        "backend/app/rag/retrievers",
        "backend/app/rag/rerankers",
        "backend/app/graph",
        "backend/app/mcp/servers",
        "backend/app/evaluation",
        
        # Frontend Layer (Next.js placeholder folders)
        "frontend/src/app",
        "frontend/src/components/ui",
        "frontend/src/hooks",
        "frontend/src/store",
        
        # DevOps & Configuration
        "devops/docker",
        "devops/nginx",
        "devops/prometheus",
        "docs/architecture",
        "docs/api",
        "tests/unit",
        "tests/integration",
    ]
    
    files = {
        "backend/app/main.py": "# FastAPI Entrypoint\n",
        "backend/app/core/config.py": "# Configuration management\n",
        "backend/app/db/session.py": "# Database connection setup\n",
        "backend/requirements.txt": "fastapi>=0.110.0\nuvicorn>=0.28.0\npydantic[email]>=2.6.4\nsqlalchemy>=2.0.28\nalembic>=1.13.1\nchromadb>=0.4.24\nlangchain>=0.1.12\nlanggraph>=0.0.26\npython-dotenv>=1.0.1\n",
        ".env.example": "DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/medintel\nCHROMA_DB_PATH=./backend/app/data/chroma\nOPENAI_API_KEY=your-api-key-here\nSECRET_KEY=your-jwt-secret-key\n",
        "README.md": "# MEDINTEL AI\nAn Explainable Retrieval-Augmented Medical Research Assistant\n"
    }

    print("🚀 Initializing MEDINTEL AI Enterprise Architecture...")
    
    for folder in structure:
        os.makedirs(folder, exist_ok=True)
        # Create an empty __init__.py file for Python module resolution where appropriate
        if "backend" in folder:
            init_file = os.path.join(folder, "__init__.py")
            with open(init_file, "w") as f:
                f.write("")
                
    for file_path, content in files.items():
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
    print("✅ Project directory structure created successfully.")

if __name__ == "__main__":
    create_directory_structure()