from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.rag_pipeline import process_pdf, ask_question
from app.services.financial_extractor import extract_financials
import tempfile
import os
import shutil
from typing import Optional

app = FastAPI(
    title="AI Financial Analyzer API",
    description="Upload financial PDFs and ask questions about them",
    version="1.0.0"
)

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store vectorstores in memory (in production, use a database)
vectorstores = {}
current_doc_id = None

@app.get("/")
async def root():
    return {"message": "AI Financial Analyzer API", "status": "running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a PDF file"""
    global current_doc_id
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files are allowed")
    
    # Check file size (max 10MB)
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(400, "File too large (max 10MB)")
    
    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    
    try:
        # Process PDF
        vectorstore = process_pdf(tmp_path)
        
        # Store with timestamp as ID
        import time
        doc_id = f"{file.filename}_{time.time()}"
        vectorstores[doc_id] = vectorstore
        current_doc_id = doc_id
        
        return {
            "message": f"File '{file.filename}' processed successfully",
            "doc_id": doc_id,
            "chunks": vectorstore.index.ntotal
        }
    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")
    finally:
        # Clean up temp file
        os.unlink(tmp_path)

@app.post("/query")
async def query(question: str, doc_id: Optional[str] = None):
    """Ask a question about an uploaded document"""
    global current_doc_id
    
    # Determine which document to query
    if doc_id is None:
        doc_id = current_doc_id
    
    if doc_id is None or doc_id not in vectorstores:
        raise HTTPException(400, "No document uploaded yet or invalid doc_id")
    
    if not question or len(question.strip()) == 0:
        raise HTTPException(400, "Question cannot be empty")
    
    try:
        vectorstore = vectorstores[doc_id]
        answer = ask_question(vectorstore, question)
        
        return {
            "question": question,
            "answer": answer,
            "doc_id": doc_id
        }
    except Exception as e:
        raise HTTPException(500, f"Query failed: {str(e)}")

@app.post("/extract")
async def extract_metrics(doc_id: Optional[str] = None):
    """Extract financial metrics from the document"""
    global current_doc_id
    
    if doc_id is None:
        doc_id = current_doc_id
    
    if doc_id is None or doc_id not in vectorstores:
        raise HTTPException(400, "No document uploaded yet")
    
    try:
        # For now, return sample data
        # In production, you'd actually extract from the document
        metrics = {
            "revenue": "100,000,000",
            "net_income": "25,000,000",
            "total_assets": "500,000,000",
            "eps": "2.50"
        }
        
        return {"metrics": metrics, "doc_id": doc_id}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")

@app.get("/documents")
async def list_documents():
    """List all processed documents"""
    return {"documents": list(vectorstores.keys())}