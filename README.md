# Intelligent Chat Agent

A Python-based intelligent chat agent with OpenAI-style interfaces and asynchronous display capabilities.

## Features

- OpenAI-style API interface
- Question and answer training format
- Asynchronous chat display with streaming responses
- Message Coherence Protocol (MCP) instead of function calls
- Web search integration for enhanced responses
- Modular and extensible architecture

## Project Structure

```
.
├── app.py                  # Main FastAPI application
├── requirements.txt        # Python dependencies
├── model/
│   ├── agent.py            # Main agent implementation
│   ├── mcp.py              # Message Coherence Protocol implementation
│   └── training.py         # Training utilities for Q&A data
├── utils/
│   └── web_search.py       # Web search integration
├── frontend/
│   ├── index.html          # Main HTML page
│   └── static/
│       ├── css/
│       │   └── styles.css  # CSS styles
│       └── js/
│           ├── chat.js     # Chat functionality
│           └── stream.js   # Streaming text display
└── data/
    ├── raw/                # Raw training data
    └── processed/          # Processed Q&A data
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/dieellin/first.git
cd first
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create necessary directories:
```bash
python init_project.py
```

4. Run the application:
```bash
python app.py
```

The application will be available at http://localhost:8000

## Training Data Format

Training data should be prepared in question-answer format. The system supports several input formats:

### CSV Format
```csv
question,answer
"What is machine learning?","Machine learning is a branch of artificial intelligence..."
"How does the agent work?","The agent processes queries using a Message Coherence Protocol..."
```

### JSON Format
```json
[
  {
    "question": "What is machine learning?",
    "answer": "Machine learning is a branch of artificial intelligence..."
  },
  {
    "question": "How does the agent work?",
    "answer": "The agent processes queries using a Message Coherence Protocol..."
  }
]
```

### Text Format
```
Q: What is machine learning?
A: Machine learning is a branch of artificial intelligence...

Q: How does the agent work?
A: The agent processes queries using a Message Coherence Protocol...
```

## API Reference

### Chat Endpoint

```
POST /api/chat
```

Request body:
```json
{
  "message": "Your question here"
}
```

Response:
```json
{
  "response": "Agent's response here"
}
```

### WebSocket Endpoint

```
WebSocket /ws/chat
```

Send:
```json
{
  "message": "Your question here"
}
```

Receive (multiple chunks):
```json
{
  "chunk": "Partial response text"
}
```

Final message:
```json
{
  "done": true
}
```

### Training Endpoint

```
POST /api/train
```

Request body:
```json
{
  "data_path": "data/processed",
  "epochs": 5
}
```

Response:
```json
{
  "status": "success",
  "result": {
    "epochs_completed": 5,
    "final_loss": 0.05,
    "accuracy": 0.95,
    "training_time": 2.0
  }
}
```

## Message Coherence Protocol (MCP)

The MCP is an alternative to function calls that maintains dialogue coherence. It:

1. Detects user intent from the message
2. Determines if web search is needed
3. Extracts relevant entities
4. Checks coherence with conversation history
5. Selects the appropriate response strategy

## Web Search Integration

The agent can enhance responses by searching the web when needed. The current implementation provides a placeholder that can be connected to search APIs like Google Custom Search, Bing Search, or DuckDuckGo.

## License

MIT
