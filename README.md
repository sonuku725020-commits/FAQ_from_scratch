# Smart FAQ Chatbot

An intelligent FAQ chatbot with dynamic temperature control, response caching, and urgency detection.

## Features

- Urgency Detection: Automatically detects urgent queries (URGENT, !!!, ASAP) and adjusts response style
- Response Caching: Caches responses in memory for faster, cheaper queries
- Conversation Memory: Maintains chat history for contextual responses
- Statistics Tracking: Tracks queries, cache hits, and response times
- Dynamic Temperature: 
  - Urgent queries -> Lower temperature (0.0-0.2) for direct, concise answers
  - Casual queries -> Higher temperature (0.7-0.9) for friendly, conversational responses

## Available FAQ Topics

- Hours of operation
- Location/address
- Contact information
- Returns policy
- Shipping options
- Payment methods
- Warranty information
- Order tracking

## Setup

### 1. Create Virtual Environment

```
python -m venv venv
```

### 2. Activate Virtual Environment

Windows (PowerShell):
```
.venv\Scripts\Activate.ps1
```

Windows (CMD):
```
venv\Scripts\activate.bat
```

Linux/Mac:
```
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Configure API Key

Edit the .env file and add your OpenRouter API key:

```
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

Get your free API key at: https://openrouter.ai/

## Usage

Run the chatbot:

```
python faq_bot.py
```

### Available Commands

| Command | Description |
|---------|-------------|
| quit / exit | Exit the chatbot |
| clear | Clear chat history |
| stats | Show statistics |
| help | Show available FAQ topics |

### Example Queries

Casual queries (friendly, conversational):
- "What are your hours?"
- "Can I return this item?"
- "How do I track my order?"

Urgent queries (direct, action-oriented):
- "URGENT: I need help NOW!"
- "My order hasn't arrived!!!"
- "ASAP - need to change my shipping address"

## Project Structure

- faq_bot.py - Main chatbot application
- cache.py - Caching module
- urgency.py - Urgency detection module
- requirements.txt - Python dependencies
- .env - Environment variables (API keys) - NOT committed to git
- .env.example - Template for environment variables
- .gitignore - Git ignore rules
- README.md - This file

## Upload to GitHub

### Prerequisites
- Git installed on your machine
- A GitHub account

### Steps

1. **Initialize Git** (if not already initialized):
```bash
git init
```

2. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Enter repository name (e.g., "faq-chatbot")
   - Choose Public or Private
   - Click "Create repository"

3. **Add files and commit**:
```bash
git add .
git commit -m "Initial commit: Smart FAQ Chatbot with dynamic temperature and caching"
```

4. **Add your GitHub repository as remote**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/faq-chatbot.git
```

5. **Push to GitHub**:
```bash
git branch -M main
git push -u origin main
```

### Important Notes

- The `.env` file is excluded from git (see `.gitignore`) to protect your API keys
- Users who clone your repository should copy `.env.example` to `.env` and add their own API key
- The `venv/` folder is also excluded to keep the repository small

## Statistics

The chatbot tracks:
- Total queries processed
- Urgent vs casual query breakdown
- Cache hits and misses
- Average response time
- Cache hit rate

Use the stats command to view these metrics.

## How It Works (User Query Processing Flow)

```
You type: "What are your hours?"
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Urgency Detection                                   │
│ ↓                                                            │
│ urgency.detect_urgency("What are your hours?")             │
│ ↓                                                            │
│ Check for urgent keywords: ❌ None found                    │
│ ↓                                                            │
│ Return: temperature = 0.9, urgency = "CASUAL"              │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Get/Create LLM                                      │
│ ↓                                                            │
│ _get_llm(0.9)                                               │
│ ↓                                                            │
│ Is current_llm None? or temperature changed?               │
│ ↓ YES                               ↓ NO                    │
│ Create new LLM(temp=0.9)           Reuse existing LLM      │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Build Prompt                                        │
│ ↓                                                            │
│ Combine:                                                    │
│ • System message (with FAQ data)                           │
│ • Chat history (previous messages)                         │
│ • Current question                                         │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Check Cache (from cache.py)                        │
│ ↓                                                            │
│ Is exact same prompt in cache?                             │
│ ↓ YES                               ↓ NO                    │
│ Return cached response (0.001s)    Call OpenRouter API     │
│                                     (1.234s)                │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Get Response                                        │
│ ↓                                                            │
│ Response: "We're open Monday-Friday 9 AM - 6 PM..."        │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 6: Update State                                        │
│ ↓                                                            │
│ • Add to chat_history                                      │
│ • Update statistics                                        │
│ • Store in cache (if new)                                  │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 7: Display to User                                     │
│ ↓                                                            │
│ [💬 CASUAL MODE (temp=0.9) | 📦 CACHED | 0.001s]          │
│ Bot: We're open Monday-Friday 9 AM - 6 PM...               │
└─────────────────────────────────────────────────────────────┘
```

## Customization

### Adding FAQ Topics

Edit the faq_data dictionary in faq_bot.py:

```python
self.faq_data = {
    "topic_name": "Your answer here",
}
```

### Adjusting Temperature Settings

Edit the values in urgency.py to customize urgency detection thresholds.
