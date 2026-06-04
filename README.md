# Multi-Agent AI Research System

A fully automated multi-agent AI research pipeline that orchestrates specialized agents to search the web, scrape content, generate reports, and critique output end-to-end. Built with LangChain and powered by advanced LLMs.

## 🎯 Overview

This project demonstrates a sophisticated AI research automation system that combines multiple specialized agents working together:

- **Search Agent**: Live web data retrieval using Tavily API
- **Reader Agent**: Deep URL scraping and content extraction
- **Writer Chain**: Structured research report generation
- **Critic Chain**: Automatic quality scoring and output critique

## ✨ Features

- **Automated Web Research**: Search for the latest information on any topic
- **Content Extraction**: Deep scraping with intelligent text cleanup
- **Multi-Agent Orchestration**: Coordinated agent workflows using LangChain
- **LLM Integration**: Support for multiple LLM providers (Google, Mistral)
- **Report Generation**: Automatically generate structured research reports
- **Quality Assessment**: Automatic critique and quality scoring
- **Streamlit UI**: Professional user interface for interaction

## 🏗️ Architecture

The system consists of four main components:

### 1. **Tools** (`tools.py`)
- `web_search()`: Searches the internet for relevant information
- `scrape_url()`: Extracts and cleans text content from web pages

### 2. **Agents** (`agents.py`)
- Search Agent: Orchestrates web searches
- Reader Agent: Manages content extraction
- Writer Agent: Generates research reports
- Critic Agent: Evaluates and scores output

### 3. **Main Pipeline** (`pipeline.py`)
- Coordinates the multi-agent workflow
- Manages agent communication and data flow

### 4. **User Interface**
- Streamlit-based UI for professional interaction

## 📋 Requirements

- Python >=3.13
- LangChain ecosystem
- LLM API keys (OpenAI, Google Gemini, or Mistral)
- Tavily API key for web search
- Internet connection

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Gaurang-Khator/multi-agent-AI-research-system
   cd multi-agent-AI-research-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   
   On Windows:
   ```bash
   .venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Create a `.env` file in the project root with the following API keys:

```env
# Web Search
TAVILY_API_KEY=your_tavily_api_key

# LLM Provider (choose one or more)
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_gemini_api_key
MISTRAL_API_KEY=your_mistral_api_key
```

## 💻 Usage

### Run the Main Pipeline
```bash
python pipeline.py
```

### Run with Streamlit UI
```bash
streamlit run app.py
```

## 📁 Project Structure

```
multi-agent-AI-research-system/
├── pipeline.py          # Entry point and main pipeline
├── agents.py            # Agent definitions and orchestration
├── tools.py             # Tool implementations (web search, scraping)
├── pyproject.toml       # Project metadata and dependencies
├── requirements.txt     # Python package requirements
├── .env                 # Environment variables (create this)
└── README.md            # This file
```

## 🔧 Dependencies

### Core Libraries
- **langchain**: LLM framework and orchestration
- **langchain-core**: Core components
- **langchain-community**: Community integrations
- **langchain-openai**: OpenAI integration
- **langchain-google-genai**: Google Gemini integration
- **langchain-mistralai**: Mistral AI integration

### Utilities
- **tavily-python**: Web search API client
- **requests**: HTTP library
- **beautifulsoup4**: HTML/XML parsing
- **python-dotenv**: Environment variable management
- **rich**: Rich terminal output

## 🛠️ Development

To extend the system:

1. Add new tools in `tools.py`
2. Define new agents in `agents.py`
3. Update the main workflow in `pipeline.py`
4. Test with different LLM providers

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

**Built with ❤️ using LangChain and Advanced LLMs**