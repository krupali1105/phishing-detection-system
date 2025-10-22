# 🛡️ Phishing Detection System (AI + Cybersecurity)

Advanced full-stack AI-powered system to detect phishing in URLs and text using machine learning and large language models.

## ✨ Key Features
- **🤖 AI/LLM Integration**: Enhanced analysis using Ollama and LangChain
- **🎯 Multi-Model Detection**: URL, text, and hybrid analysis
- **⚡ Real-time Analysis**: Instant phishing detection via REST API
- **📊 Analytics Dashboard**: Comprehensive insights and historical data
- **🎨 Hacker-Themed UI**: Matrix-style animations and loading states
- **📱 Responsive Design**: Modern, mobile-friendly interface
- **🐳 Docker Support**: Containerized deployment for scalability
- **🔒 Security-First**: Hydration-safe SSR with robust error handling

## 🚀 Tech Stack
- **Backend**: FastAPI, Uvicorn, SQLAlchemy, Pydantic
- **ML/AI**: scikit-learn, spaCy/NLTK, Transformers, Ollama, LangChain
- **Frontend**: Next.js, TailwindCSS, TypeScript
- **Deployment**: Docker, docker-compose

## 📁 Project Structure
```
phishing-detection-system/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── routers/           # API endpoints
│   │   │   ├── predict.py     # Core ML predictions
│   │   │   ├── llm_predict.py # AI/LLM enhanced analysis
│   │   │   └── analytics.py   # Analytics & reporting
│   │   ├── utils/             # Feature extraction & LLM
│   │   └── models/            # Trained ML models
│   └── requirements.txt
├── frontend/                   # Next.js frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── PhishingDetector.tsx
│   │   │   ├── LoadingSpinner.tsx
│   │   │   ├── HackerLoader.tsx
│   │   │   └── ...
│   │   └── app/               # Next.js app router
│   └── package.json
├── models/                     # Training scripts
├── docker-compose.yml
└── DOCUMENTATION.md           # Comprehensive docs
```

## 🔧 Backend Setup

### Prerequisites
- Python 3.11+
- Ollama (for AI/LLM features)
- Node.js 18+ (for frontend)

### Run Backend
```bash
cd backend
python -m venv venv
./venv/Scripts/Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Setup Ollama (Optional - for AI features)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull llama2 model
ollama pull llama2

# Start Ollama server
ollama serve
```

### 🚀 API Endpoints

#### Core ML Predictions
- `POST /predict/url` - URL analysis
- `POST /predict/text` - Text analysis  
- `POST /predict/hybrid` - Combined analysis

#### 🤖 AI/LLM Enhanced Analysis
- `POST /llm-predict/url` - AI-enhanced URL analysis
- `POST /llm-predict/text` - AI-enhanced text analysis
- `POST /llm-predict/hybrid` - AI-enhanced combined analysis
- `GET /llm-predict/status` - LLM service status

#### 📊 Analytics & Monitoring
- `GET /analytics/summary` - System analytics
- `GET /analytics/history` - Prediction history
- `GET /analytics/daily-stats` - Daily statistics
- `GET /health` - Health check

## 🎨 Frontend Setup

### Run Frontend
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:3000

### Features
- **🎯 Multi-Model Detection**: URL, text, and hybrid analysis
- **🤖 AI/LLM Toggle**: Enhanced analysis with Ollama integration
- **📊 Analytics Dashboard**: Real-time insights and statistics
- **📜 History Panel**: Complete audit trail with filtering
- **🎨 Hacker Animations**: Matrix-style loading states
- **📱 Responsive Design**: Mobile-friendly interface

## 🐳 Docker Deployment

### Quick Start
```bash
docker compose up --build
```

### Services
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## 🤖 AI/LLM Setup (Optional)

### Install Ollama
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### Setup Models
```bash
# Pull recommended model
ollama pull llama2

# Start Ollama server
ollama serve
```

## 🧠 Model Training

### Train All Models
```bash
cd models
python train_all_models.py
```

### Individual Training
```bash
python train_url_model.py      # URL analysis model
python train_text_model.py     # Text analysis model  
python train_hybrid.py         # Hybrid model
```

Models will be saved to `backend/app/models/`.

## ⚙️ Configuration

### Environment Variables
```bash
# Database (optional)
DATABASE_URL=postgresql://user:pass@localhost/db

# Frontend API base (optional)
NEXT_PUBLIC_API_BASE=http://localhost:8000

# Ollama configuration (optional)
OLLAMA_BASE_URL=http://localhost:11434
```

## 🚀 Quick Start

1. **Clone & Setup**:
   ```bash
   git clone <repository>
   cd phishing-detection-system
   ```

2. **Backend**:
   ```bash
   cd backend
   python -m venv venv
   ./venv/Scripts/Activate.ps1
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Optional - AI Features**:
   ```bash
   ollama pull llama2
   ollama serve
   ```

## 📚 Documentation

- **Full Documentation**: See `DOCUMENTATION.md`
- **API Reference**: http://localhost:8000/docs
- **Component Guide**: Check `frontend/src/components/`

## ⚠️ Production Notes

- Replace synthetic data with real datasets
- Add rate limiting for WHOIS/web scraping
- Configure proper database for production
- Set up monitoring and logging
- Use HTTPS in production
