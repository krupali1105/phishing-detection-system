# Ollama Setup Guide for LLM Integration

## Prerequisites
- Docker Desktop installed and running
- Or Ollama installed locally

## Option 1: Docker Setup (Recommended)

### 1. Install Ollama Docker Image
```bash
# Pull Ollama Docker image
docker pull ollama/ollama

# Run Ollama container
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### 2. Pull a Model
```bash
# Pull Llama 2 (7B model - good balance of performance/size)
docker exec -it ollama ollama pull llama2

# Or pull Mistral (alternative, smaller model)
docker exec -it ollama ollama pull mistral

# Or pull CodeLlama (good for technical analysis)
docker exec -it ollama ollama pull codellama
```

### 3. Verify Installation
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Test a simple query
docker exec -it ollama ollama run llama2 "Hello, how are you?"
```

## Option 2: Local Installation

### 1. Install Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 2. Start Ollama Service
```bash
# Start Ollama service
ollama serve
```

### 3. Pull Models
```bash
# Pull Llama 2
ollama pull llama2

# Or Mistral
ollama pull mistral
```

## Testing LLM Integration

### 1. Start Backend
```bash
cd phishing-detection-system/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Test LLM Status
```bash
curl http://localhost:8000/llm-predict/status
```

Expected response:
```json
{
  "available": true,
  "current_model": "llama2",
  "available_models": ["llama2", "mistral"],
  "base_url": "http://localhost:11434"
}
```

### 3. Test LLM Analysis
```bash
curl -X POST http://localhost:8000/llm-predict/text \
  -H "Content-Type: application/json" \
  -d '{"text": "URGENT: Your account has been suspended. Click here immediately to verify your identity."}'
```

## Frontend Integration

### 1. Start Frontend
```bash
cd phishing-detection-system/frontend
npm install
npm run dev
```

### 2. Enable LLM Analysis
- Open http://localhost:3000
- Check "🤖 Use AI/LLM Analysis (Enhanced)" checkbox
- Enter URL or text and click "🤖 AI Analyze"

## Troubleshooting

### Common Issues

#### 1. Ollama Not Running
```bash
# Check if Ollama container is running
docker ps | grep ollama

# Restart if needed
docker restart ollama
```

#### 2. Model Not Found
```bash
# List available models
docker exec -it ollama ollama list

# Pull missing model
docker exec -it ollama ollama pull llama2
```

#### 3. Connection Refused
- Ensure Ollama is running on port 11434
- Check firewall settings
- Verify Docker port mapping

#### 4. Out of Memory
- Use smaller models (mistral instead of llama2)
- Increase Docker memory allocation
- Close other applications

### Performance Tips

#### 1. Model Selection
- **Llama2**: Best accuracy, requires 8GB+ RAM
- **Mistral**: Good balance, requires 4GB+ RAM  
- **CodeLlama**: Technical analysis, requires 8GB+ RAM

#### 2. Optimization
```bash
# Set environment variables for better performance
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=1
```

#### 3. Resource Monitoring
```bash
# Monitor Ollama resource usage
docker stats ollama
```

## Production Considerations

### 1. Security
- Run Ollama behind reverse proxy
- Implement rate limiting
- Use authentication for API access

### 2. Scaling
- Use GPU acceleration if available
- Implement model caching
- Consider cloud-based LLM services

### 3. Monitoring
- Monitor response times
- Track model performance
- Log analysis requests

## Alternative LLM Services

If Ollama is not suitable, you can modify the code to use:

### OpenAI API
```python
# In llm_analyzer.py
from langchain.llms import OpenAI

llm = OpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.1,
    openai_api_key="your-api-key"
)
```

### Hugging Face
```python
# In llm_analyzer.py
from langchain.llms import HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id="microsoft/DialoGPT-medium",
    task="text-generation"
)
```

## Next Steps

1. **Test Integration**: Verify LLM analysis works correctly
2. **Performance Tuning**: Optimize model parameters
3. **User Experience**: Enhance UI with LLM-specific features
4. **Monitoring**: Add logging and metrics for LLM usage
5. **Documentation**: Update API docs with LLM endpoints
