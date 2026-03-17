docker build -t ai-financial-analyzer .
docker run -p 8000:8000 -p 8501:8501 -e OPENAI_API_KEY="sk-your-key" ai-financial-analyzer