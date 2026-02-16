# 🤖 AI Calendar Assistant

A modern, AI-powered calendar management system that lets you manage your Google Calendar using natural language. Built with Flask, Google Gemini AI, LangChain, and RAG (Retrieval-Augmented Generation).

![AI Calendar Assistant](https://img.shields.io/badge/AI-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Flask](https://img.shields.io/badge/Flask-3.0-red)
![LangChain](https://img.shields.io/badge/LangChain-0.2-yellow)

## ✨ Features

### 🎯 Natural Language Processing
- **Create Events**: "Create a team meeting tomorrow at 2pm"
- **Delete Events**: "Delete my 3pm event today"
- **Query Information**: "What is RAG?" (powered by RAG system)
- **Smart Conflict Detection**: Automatically detects scheduling conflicts

### 🤖 AI-Powered
- **Google Gemini Flash** for intent detection and parsing
- **LangChain** for AI workflow orchestration
- **RAG System** with FAISS vector store for knowledge retrieval
- **Multi-agent architecture** for intelligent task routing

### 🎨 Modern UI
- Beautiful gradient animations
- Glassmorphism design
- Responsive layout (mobile, tablet, desktop)
- Real-time typing indicators
- Quick action suggestions

### 🔐 Secure Authentication
- Google OAuth 2.0 integration
- Session-based authentication
- Secure credential management
- Per-user calendar isolation

## 🏗️ Architecture

### AI Components

```
User Input
    ↓
Intent Detector (Gemini AI)
    ↓
Router
    ↓
┌─────────────┬──────────────┬─────────────┐
│   Create    │    Delete    │    Query    │
│   Handler   │    Handler   │   (RAG)     │
└─────────────┴──────────────┴─────────────┘
    ↓               ↓              ↓
Google Calendar API            FAISS Vector Store
```

### Tech Stack

**Backend:**
- Flask (Python web framework)
- Google Calendar API
- Google Gemini AI (via LangChain)
- FAISS (vector similarity search)
- LangChain (AI orchestration)

**Frontend:**
- HTML5, CSS3, JavaScript
- Modern CSS animations
- Responsive design

**AI/ML:**
- Google Generative AI Embeddings
- LangChain for prompt engineering
- FAISS for vector storage
- RAG for knowledge retrieval

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud Project with Calendar API enabled
- Google OAuth 2.0 credentials

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-calendar-assistant.git
cd ai-calendar-assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file:
```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:5000/oauth2callback
GOOGLE_API_KEY=your-gemini-api-key
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
```
http://localhost:5000
```

## 📖 Usage Examples

### Creating Events
```
"Create a team standup tomorrow at 9am"
"Schedule a client meeting next Monday at 2pm for 1 hour"
"Add a lunch break today at 12:30pm"
```

### Deleting Events
```
"Delete my 3pm meeting today"
"Remove the team standup tomorrow"
"Cancel my lunch appointment"
```

### Asking Questions
```
"What is RAG?"
"Tell me about LangChain"
"How does this system work?"
```

## 🔧 Configuration

### Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Google Calendar API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs
6. Download credentials and update `.env`

### RAG Knowledge Base

Edit `rag/rag.txt` to add your own knowledge base content. The system will automatically:
- Generate embeddings
- Store in FAISS vector database
- Use for answering questions

## 📁 Project Structure

```
ai-calendar-assistant/
├── app.py                      # Main Flask application
├── router.py                   # Message routing logic
├── intent_detector.py          # AI intent classification
├── gemini_parser.py           # Event parsing with Gemini
├── gemini_delete_parser.py    # Delete request parsing
├── config.py                   # Configuration management
│
├── handlers/                   # Request handlers
│   ├── calendar_create.py     # Create event handler
│   ├── calendar_delete.py     # Delete event handler
│   ├── conflict_resolution.py # Conflict handling
│   └── rag_query.py           # RAG query handler
│
├── services/                   # Business logic
│   └── calendar_service.py    # Google Calendar operations
│
├── rag/                        # RAG system
│   ├── rag_pipeline.py        # RAG orchestration
│   ├── rag_store.py           # Vector store management
│   ├── rag_chain.py           # LangChain RAG chain
│   └── rag.txt                # Knowledge base
│
├── templates/                  # HTML templates
│   └── index.html             # Main UI
│
├── static/                     # Static assets
│   ├── css/
│   │   └── styles.css         # Modern UI styles
│   └── js/
│       └── chat.js            # Chat functionality
│
└── requirements.txt            # Python dependencies
```

## 🎯 Key Features Explained

### Conflict Detection
When creating an event, the system:
1. Checks for existing events at that time
2. Shows conflicting events
3. Offers options: delete & create, create anyway, or cancel

### RAG System
- Stores knowledge in FAISS vector database
- Retrieves relevant context for questions
- Generates accurate answers based on your knowledge base

### Multi-Agent Architecture
- **Intent Agent**: Classifies user intent
- **Parser Agent**: Extracts structured data
- **RAG Agent**: Answers questions
- **Router**: Orchestrates all agents

## 🔒 Security

- OAuth 2.0 for secure authentication
- Session-based credential storage
- CSRF protection with state verification
- No permanent storage of sensitive data
- Per-user calendar isolation

## 🚀 Deployment

### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku config:set GOOGLE_CLIENT_ID=your-id
heroku config:set GOOGLE_CLIENT_SECRET=your-secret
```

### Vercel/Railway
- Connect your GitHub repository
- Add environment variables
- Deploy automatically

## 📝 License

MIT License - feel free to use this project for learning or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Google Gemini AI, LangChain, and Flask**
