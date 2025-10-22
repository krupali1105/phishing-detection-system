# Phishing Detection System - Comprehensive Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Objective & Purpose](#objective--purpose)
5. [Tools & Technologies Usage](#tools--technologies-usage)
6. [System Components](#system-components)
7. [API Documentation](#api-documentation)
8. [Machine Learning Models](#machine-learning-models)
9. [Database Schema](#database-schema)
10. [Testing Strategy](#testing-strategy)
11. [Deployment](#deployment)
12. [Configuration](#configuration)
13. [Security](#security)
14. [Performance](#performance)
15. [Development Workflow](#development-workflow)
16. [Troubleshooting](#troubleshooting)

---

## Project Overview

The Phishing Detection System is a full-stack AI-powered application designed to identify malicious/phishing websites and emails using advanced machine learning techniques. The system combines URL lexical analysis, WHOIS data extraction, and natural language processing to provide comprehensive phishing detection capabilities.

### Key Features
- **Multi-Model Detection**: URL-based, text-based, and hybrid analysis
- **AI/LLM Integration**: Enhanced analysis using Ollama and LangChain
- **Real-time Analysis**: Instant phishing detection via REST API
- **Analytics Dashboard**: Comprehensive insights and historical data
- **Responsive Web Interface**: Modern, mobile-friendly UI with hacker-themed animations
- **Advanced Loading States**: Matrix-style animations and skeleton loaders
- **Docker Support**: Containerized deployment for scalability
- **Database Logging**: Complete audit trail of all predictions
- **Hydration-Safe**: Server-side rendering compatible components

---

## Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   ML Models     │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (scikit-learn)│
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   TailwindCSS   │    │   SQLAlchemy    │    │   Feature       │
│   Components    │    │   Database      │    │   Extraction    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Component Architecture
- **Presentation Layer**: React/Next.js frontend with TailwindCSS
- **API Layer**: FastAPI with automatic documentation
- **Business Logic**: Feature extraction and model prediction services
- **Data Layer**: SQLAlchemy ORM with SQLite/PostgreSQL
- **ML Layer**: Scikit-learn models with joblib persistence

---

## Technology Stack

### Backend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Core programming language |
| **FastAPI** | 0.116.1 | Web framework and API development |
| **Uvicorn** | 0.35.0 | ASGI server for FastAPI |
| **SQLAlchemy** | 2.0.36 | Database ORM and management |
| **Pydantic** | 2.11.7 | Data validation and serialization |

### Machine Learning Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| **scikit-learn** | 1.7.1 | ML algorithms and model training |
| **XGBoost** | 3.0.5 | Gradient boosting for enhanced accuracy |
| **LightGBM** | 4.6.0 | Fast gradient boosting framework |
| **NLTK** | 3.9.1 | Natural language processing |
| **spaCy** | 3.8.7 | Advanced NLP and text processing |
| **Transformers** | 4.56.1 | BERT embeddings (optional) |
| **joblib** | 1.5.2 | Model serialization and persistence |

### AI/LLM Integration Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| **Ollama** | Latest | Local LLM server and model management |
| **LangChain** | 0.3.27 | LLM framework and prompt management |
| **LangChain Community** | 0.3.29 | Community integrations and tools |
| **LangChain Ollama** | 0.3.7 | Ollama integration for LangChain |
| **llama2** | Latest | Large language model for enhanced analysis |

### Frontend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | Latest | React framework with SSR/SSG |
| **React** | 18+ | Component-based UI library |
| **TypeScript** | Latest | Type-safe JavaScript development |
| **TailwindCSS** | Latest | Utility-first CSS framework |

### Infrastructure & DevOps
| Technology | Version | Purpose |
|------------|---------|---------|
| **Docker** | Latest | Containerization |
| **Docker Compose** | Latest | Multi-container orchestration |
| **SQLite** | Built-in | Development database |
| **PostgreSQL** | Optional | Production database |

---

## Objective & Purpose

### Primary Objectives
1. **Phishing Detection**: Accurately identify malicious URLs and suspicious text content
2. **Real-time Analysis**: Provide instant feedback on potential threats
3. **User Education**: Help users understand phishing indicators
4. **Data Analytics**: Track phishing trends and model performance
5. **Scalability**: Support high-volume analysis requests

### Target Use Cases
- **Individual Users**: Personal email and URL verification
- **Security Teams**: Bulk analysis of suspicious content
- **Educational Institutions**: Cybersecurity awareness training
- **Enterprise**: Integration into existing security workflows

---

## Tools & Technologies Usage

### FastAPI Usage
- **Purpose**: RESTful API development with automatic OpenAPI documentation
- **Features Used**:
  - Dependency injection for database sessions
  - Request/response models with Pydantic
  - CORS middleware for frontend integration
  - Automatic API documentation at `/docs`
  - Error handling and logging

### SQLAlchemy Usage
- **Purpose**: Database abstraction and ORM functionality
- **Features Used**:
  - Declarative base for model definitions
  - Session management with dependency injection
  - Query building and filtering
  - Database migrations (manual)

### Scikit-learn Usage
- **Purpose**: Machine learning model training and prediction
- **Algorithms Used**:
  - Random Forest: Robust ensemble method
  - Gradient Boosting: High-accuracy predictions
  - Logistic Regression: Linear baseline model
  - SVM: Support vector classification
  - Voting Classifier: Ensemble of multiple models

### NLTK/spaCy Usage
- **Purpose**: Natural language processing and text analysis
- **Features Used**:
  - Tokenization and text preprocessing
  - Stop word removal
  - TF-IDF vectorization
  - Named entity recognition (spaCy)
  - Sentiment analysis capabilities

### Next.js Usage
- **Purpose**: Modern React application with SSR capabilities
- **Features Used**:
  - App Router for file-based routing
  - Server-side rendering
  - TypeScript integration
  - Component-based architecture
  - API routes (if needed)

### TailwindCSS Usage
- **Purpose**: Rapid UI development with utility classes
- **Features Used**:
  - Responsive design utilities
  - Color system and theming
  - Component styling
  - Animation and transition effects

---

## System Components

### Backend Components

#### 1. Feature Extraction (`app/utils/feature_extraction.py`)
- **URLFeatureExtractor**: Extracts lexical features from URLs
- **WHOISFeatureExtractor**: Retrieves domain registration data
- **NLPFeatureExtractor**: Processes text content for NLP features
- **HybridFeatureExtractor**: Combines all feature types

#### 2. Model Management (`app/utils/load_models.py`)
- **ModelLoader**: Loads and manages trained ML models
- **Prediction Functions**: Interface for model predictions
- **Error Handling**: Graceful fallbacks for missing models

#### 3. API Routes
- **Predict Router** (`app/routers/predict.py`): Core prediction endpoints
- **LLM Predict Router** (`app/routers/llm_predict.py`): AI-enhanced analysis endpoints
- **Analytics Router** (`app/routers/analytics.py`): Analytics and reporting

#### 4. Database Models (`app/db.py`)
- **PredictionLog**: Stores all prediction results
- **URLBlacklist**: Maintains known malicious URLs
- **AnalyticsData**: Aggregated analytics information

### Frontend Components

#### 1. Main Application (`src/components/PhishingDetector.tsx`)
- **Tab Navigation**: Detection, Analytics, History
- **Model Selection**: URL, Text, Hybrid analysis
- **AI/LLM Toggle**: Enhanced analysis with Ollama integration
- **Input Forms**: URL and text input interfaces
- **Result Display**: Prediction results with confidence
- **Loading States**: Hacker-style animations and skeleton loaders

#### 2. Result Display (`src/components/ResultCard.tsx`)
- **Prediction Results**: Visual representation of analysis
- **Confidence Indicators**: Progress bars and risk levels
- **Action Buttons**: Copy, visit, and share functionality

#### 3. Analytics Dashboard (`src/components/AnalyticsDashboard.tsx`)
- **Summary Cards**: Key metrics and statistics
- **Charts**: Visual data representation
- **Model Performance**: Individual model statistics

#### 4. History Panel (`src/components/HistoryPanel.tsx`)
- **Prediction History**: Past analysis results
- **Filtering**: Search and filter capabilities
- **Export**: Data export functionality
- **Loading States**: Skeleton loaders and hacker animations

#### 5. New UI Components
- **LoadingSpinner** (`src/components/LoadingSpinner.tsx`): Multiple loading variants
- **HackerLoader** (`src/components/HackerLoader.tsx`): Matrix-style animations
- **EmptyState** (`src/components/EmptyState.tsx`): Hacker-themed empty states
- **SkeletonLoader** (`src/components/SkeletonLoader.tsx`): Content placeholders
- **LLMAnalysisCard** (`src/components/LLMAnalysisCard.tsx`): AI analysis results

---

## API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication
Currently no authentication required. Production deployment should implement API keys or OAuth.

### Endpoints

#### Prediction Endpoints

##### POST `/predict/url`
Analyze a URL for phishing indicators.

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "url": "https://example.com",
  "prediction": "Legitimate",
  "confidence": 0.85,
  "model_type": "url",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

##### POST `/predict/text`
Analyze text content for phishing indicators.

**Request Body:**
```json
{
  "text": "Verify your account immediately"
}
```

##### POST `/predict/hybrid`
Combined URL and text analysis.

**Request Body:**
```json
{
  "url": "https://example.com",
  "text": "Verify your account immediately"
}
```

#### LLM-Enhanced Analysis Endpoints

##### POST `/llm-predict/url`
AI-enhanced URL analysis using Ollama and LangChain.

**Request Body:**
```json
{
  "url": "https://suspicious-site.tk/login"
}
```

**Response:**
```json
{
  "url": "https://suspicious-site.tk/login",
  "prediction": "PHISHING",
  "confidence": 0.85,
  "explanation": "Hybrid ML+LLM analysis (ML + llama2)",
  "risk_factors": ["suspicious domain", "http instead of https"],
  "recommendations": ["Avoid clicking", "Report to security team"],
  "model_type": "url",
  "timestamp": "2024-01-01T12:00:00Z",
  "llm_model": "llama2"
}
```

##### POST `/llm-predict/text`
AI-enhanced text analysis.

**Request Body:**
```json
{
  "text": "URGENT: Your account has been suspended. Click here immediately."
}
```

##### POST `/llm-predict/hybrid`
AI-enhanced combined URL and text analysis.

**Request Body:**
```json
{
  "url": "https://suspicious-site.tk",
  "text": "URGENT: Your account has been suspended."
}
```

##### GET `/llm-predict/status`
Check LLM service status and available models.

**Response:**
```json
{
  "available": true,
  "current_model": "llama2",
  "available_models": ["llama2:latest"],
  "base_url": "http://localhost:11434"
}
```

#### Analytics Endpoints

##### GET `/analytics/summary`
Get overall system analytics.

**Response:**
```json
{
  "total_predictions": 1000,
  "phishing_count": 150,
  "legitimate_count": 850,
  "phishing_percentage": 15.0,
  "avg_confidence": 0.78,
  "model_usage": {
    "url": 600,
    "text": 300,
    "hybrid": 100
  }
}
```

##### GET `/analytics/history`
Get prediction history with optional filters.

**Query Parameters:**
- `limit`: Number of results (default: 100, max: 1000)
- `offset`: Pagination offset (default: 0)
- `model_type`: Filter by model type
- `prediction`: Filter by prediction result

##### GET `/analytics/daily-stats`
Get daily statistics for the last N days.

**Query Parameters:**
- `days`: Number of days (default: 7, max: 30)

##### GET `/analytics/model-performance`
Get performance metrics for each model.

##### GET `/health`
Health check endpoint.

---

## Machine Learning Models

### Model Types

#### 1. URL Model
- **Purpose**: Analyze URL structure and characteristics
- **Features**: 25+ lexical features including length, special characters, domain info
- **Algorithms**: Random Forest, Gradient Boosting, Logistic Regression, SVM
- **Training Data**: Synthetic phishing and legitimate URLs

#### 2. Text Model
- **Purpose**: Analyze text content for phishing indicators
- **Features**: TF-IDF vectors, text statistics, suspicious keywords
- **Algorithms**: Same as URL model
- **Training Data**: Synthetic phishing and legitimate text samples

#### 3. Hybrid Model
- **Purpose**: Combine URL and text analysis for comprehensive detection
- **Features**: All URL features + text features
- **Algorithms**: Voting classifier combining all individual models
- **Training Data**: Combined URL and text samples

### Feature Engineering

#### URL Features
- **Basic**: Length, character counts, special characters
- **Domain**: Subdomain count, TLD analysis, IP detection
- **Path**: Directory structure, file extensions
- **Query**: Parameter analysis, suspicious keywords
- **Patterns**: URL shortening detection, repeated characters

#### WHOIS Features
- **Domain Age**: Registration date analysis
- **Registrar**: Registration service provider
- **Country**: Geographic location of registration

#### Text Features
- **Basic**: Length, word count, average word length
- **NLP**: Stop word ratio, special character ratio
- **Keywords**: Suspicious phrase detection
- **TF-IDF**: Term frequency-inverse document frequency
- **BERT**: Contextual embeddings (optional)

### Model Training Process

1. **Data Collection**: Gather phishing and legitimate samples
2. **Feature Extraction**: Apply feature extractors to raw data
3. **Data Splitting**: Train/test split with stratification
4. **Model Selection**: Test multiple algorithms
5. **Hyperparameter Tuning**: Optimize model parameters
6. **Evaluation**: Cross-validation and performance metrics
7. **Persistence**: Save best models and scalers

---

## Database Schema

### Tables

#### PredictionLog
```sql
CREATE TABLE prediction_logs (
    id INTEGER PRIMARY KEY,
    url VARCHAR,
    text TEXT,
    prediction VARCHAR,
    confidence FLOAT,
    model_type VARCHAR,
    timestamp DATETIME,
    ip_address VARCHAR,
    user_agent VARCHAR
);
```

#### URLBlacklist
```sql
CREATE TABLE url_blacklist (
    id INTEGER PRIMARY KEY,
    url VARCHAR UNIQUE,
    domain VARCHAR,
    is_phishing BOOLEAN,
    confidence FLOAT,
    source VARCHAR,
    created_at DATETIME,
    updated_at DATETIME
);
```

#### AnalyticsData
```sql
CREATE TABLE analytics_data (
    id INTEGER PRIMARY KEY,
    date DATETIME,
    total_predictions INTEGER,
    phishing_count INTEGER,
    legitimate_count INTEGER,
    avg_confidence FLOAT
);
```

---

## Testing Strategy

### Backend Testing

#### Unit Tests
- Feature extraction functions
- Model prediction logic
- Database operations
- API endpoint responses

#### Integration Tests
- End-to-end API workflows
- Database integration
- Model loading and prediction

#### Performance Tests
- Load testing with multiple concurrent requests
- Response time benchmarks
- Memory usage monitoring

### Frontend Testing

#### Component Tests
- React component rendering
- User interaction handling
- State management
- API integration

#### E2E Tests
- Complete user workflows
- Cross-browser compatibility
- Mobile responsiveness

### Test Data
- **Synthetic Data**: Generated phishing and legitimate samples
- **Edge Cases**: Malformed URLs, empty text, special characters
- **Load Testing**: High-volume request simulation

---

## Deployment

### Docker Deployment

#### Backend Container
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Container
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["npm", "start"]
```

#### Docker Compose
```yaml
version: "3.9"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./phishing_detection.db
    volumes:
      - ./backend/app/models:/app/app/models

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_BASE=http://localhost:8000
    depends_on:
      - backend
```

### Production Deployment

#### Environment Setup
1. **Server Requirements**: Linux server with Docker support
2. **Domain Configuration**: Set up domain and SSL certificates
3. **Database**: Configure PostgreSQL for production
4. **Environment Variables**: Set production configuration

#### Deployment Steps
1. Clone repository
2. Configure environment variables
3. Build Docker images
4. Run with docker-compose
5. Set up reverse proxy (nginx)
6. Configure SSL certificates
7. Set up monitoring and logging

---

## Configuration

### Environment Variables

#### Backend Configuration
```bash
# Database
DATABASE_URL=sqlite:///./phishing_detection.db
# For production: postgresql://user:pass@host:port/db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

#### Frontend Configuration
```bash
# API Base URL
NEXT_PUBLIC_API_BASE=http://localhost:8000

# Environment
NODE_ENV=production
```

### Model Configuration
- **Model Paths**: Configure model file locations
- **Feature Scaling**: Enable/disable feature normalization
- **Confidence Thresholds**: Adjust prediction confidence levels
- **Cache Settings**: Configure model and feature caching

---

## Security

### API Security
- **Input Validation**: Pydantic models for request validation
- **SQL Injection**: SQLAlchemy ORM prevents injection attacks
- **Rate Limiting**: Implement request rate limiting
- **CORS**: Configured for specific origins
- **HTTPS**: SSL/TLS encryption for production

### Data Security
- **Sensitive Data**: No storage of personal information
- **Database Encryption**: Encrypt database files
- **Access Control**: Implement authentication and authorization
- **Audit Logging**: Complete audit trail of all operations

### Model Security
- **Model Validation**: Verify model integrity
- **Input Sanitization**: Clean and validate all inputs
- **Output Validation**: Validate prediction results
- **Error Handling**: Secure error messages without information leakage

---

## Performance

### Backend Performance
- **Async Processing**: FastAPI async/await support
- **Database Optimization**: Indexed queries and connection pooling
- **Caching**: Model and feature caching
- **Load Balancing**: Multiple worker processes

### Frontend Performance
- **Code Splitting**: Dynamic imports for components
- **Image Optimization**: Next.js automatic image optimization
- **Bundle Optimization**: Tree shaking and minification
- **CDN**: Static asset delivery

### Monitoring
- **Response Times**: Track API response times
- **Error Rates**: Monitor error frequencies
- **Resource Usage**: CPU, memory, and disk monitoring
- **User Metrics**: Track user interactions and performance

---

## Recent Updates & Improvements

### Version 2.0 Features (Latest)

#### 🚀 AI/LLM Integration
- **Ollama Integration**: Local LLM server for enhanced analysis
- **LangChain Framework**: Advanced prompt engineering and chain management
- **Hybrid Analysis**: Combined ML + LLM predictions for higher accuracy
- **Fallback System**: Graceful degradation when LLM is unavailable

#### 🎨 Enhanced UI/UX
- **Hacker-Themed Animations**: Matrix-style loading animations
- **Skeleton Loaders**: Professional content placeholders
- **Empty States**: Contextual empty state components
- **Loading States**: Multiple loading variants (default, hacker, dots, pulse)
- **Hydration-Safe**: Server-side rendering compatibility

#### 🔧 Technical Improvements
- **Model Loading**: Improved feature alignment and scaling
- **Error Handling**: Enhanced error messages and logging
- **API Endpoints**: New LLM-enhanced prediction endpoints
- **Performance**: Optimized loading and rendering

#### 🛡️ Security Enhancements
- **Input Validation**: Enhanced request validation
- **Error Logging**: Comprehensive error tracking
- **Fallback Mechanisms**: Robust error recovery
- **Type Safety**: Improved TypeScript integration

---

## Development Workflow

### Local Development
1. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\Activate.ps1  # Windows
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Model Training**:
   ```bash
   cd models
   python train_all_models.py
   ```

### Code Quality
- **Linting**: ESLint for frontend, flake8 for backend
- **Formatting**: Prettier for frontend, black for backend
- **Type Checking**: TypeScript for frontend, mypy for backend
- **Testing**: Jest for frontend, pytest for backend

### Version Control
- **Git Workflow**: Feature branches with pull requests
- **Commit Messages**: Conventional commit format
- **Code Review**: Required for all changes
- **CI/CD**: Automated testing and deployment

---

## Troubleshooting

### Common Issues

#### Backend Issues
1. **Import Errors**: Ensure virtual environment is activated
2. **Model Loading**: Check model files exist in correct location
3. **Database Errors**: Verify database connection and permissions
4. **NLTK Errors**: Download required NLTK data

#### Frontend Issues
1. **API Connection**: Check backend is running on correct port
2. **CORS Errors**: Verify CORS configuration
3. **Build Errors**: Check Node.js version and dependencies
4. **Styling Issues**: Verify TailwindCSS configuration

#### Docker Issues
1. **Build Failures**: Check Dockerfile syntax and dependencies
2. **Port Conflicts**: Ensure ports are not already in use
3. **Volume Mounts**: Verify file paths and permissions
4. **Network Issues**: Check Docker network configuration

### Debugging
- **Logging**: Enable debug logging for detailed information
- **API Testing**: Use `/docs` endpoint for API testing
- **Database Inspection**: Use SQLite browser for database inspection
- **Performance Profiling**: Use profiling tools for performance analysis

### Support
- **Documentation**: Refer to this documentation and code comments
- **Issues**: Check GitHub issues for known problems
- **Community**: Join relevant communities for support
- **Professional Support**: Consider professional support for production deployments

---

## Conclusion

The Phishing Detection System represents a comprehensive solution for identifying malicious content using modern AI/ML techniques. The modular architecture, extensive documentation, and robust testing ensure reliability and maintainability. The system is designed to scale from individual use to enterprise deployment while maintaining security and performance standards.

For additional support or contributions, please refer to the project repository and community guidelines.
