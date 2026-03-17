# ai-financial-analyzer
Full‑stack AI system for financial document analysis
# AI Financial Analyzer 📊

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/YOUR_USERNAME/ai-financial-analyzer)
[![Python](https://img.shields.io/badge/python-3.10-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.0.340-orange)](https://langchain.com)

A full-stack AI system that analyzes financial documents (10-K, annual reports) using RAG (Retrieval-Augmented Generation). Upload PDFs, ask questions, and get insights powered by OpenAI.

## ✨ Features

- 📄 Upload multiple PDF financial reports
- 🤖 Ask natural language questions about your documents
- 🔍 RAG-based retrieval with LangChain + OpenAI
- 📊 Extract key financial metrics automatically
- 📈 Interactive dashboard with trend visualization
- 🐳 Docker containerization
- ☁️ Ready for cloud deployment

## 🚀 Quick Start

### Option 1: GitHub Codespaces (Recommended)

1. Click the "Open in GitHub Codespaces" badge above
2. Set your OpenAI API key as a secret:
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"