# Agentic AI Assistant 🤖

A practical implementation of an Agentic AI system that can autonomously execute tasks, use tools, make decisions, and learn from interactions.

## What is Agentic AI?

Agentic AI refers to autonomous AI systems that can:
- Set and pursue goals independently
- Make decisions based on context
- Use tools and APIs to accomplish tasks
- Learn from feedback and adapt behavior
- Plan multi-step workflows

## Features

- **Autonomous Task Execution**: AI agent breaks down complex tasks into steps
- **Tool Usage**: Agent can use multiple tools (web search, calculator, file operations, API calls)
- **Decision Making**: Context-aware decision making with reasoning
- **Memory System**: Maintains conversation history and learns from interactions
- **Goal-Oriented**: Pursues objectives until completion
- **Error Handling**: Gracefully handles failures and retries

## Architecture

```
┌─────────────────────────────────────┐
│         User Input/Goal             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Agent Core (LLM-powered)       │
│  - Task Planning                    │
│  - Decision Making                  │
│  - Tool Selection                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Tool Executor               │
│  - Web Search                       │
│  - Calculator                       │
│  - File Operations                  │
│  - API Calls                        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Memory & Learning              │
│  - Conversation History             │
│  - Task Results                     │
│  - Performance Metrics              │
└─────────────────────────────────────┘
```

## Installation

```bash
# Clone the repository
git clone https://github.com/ShivanshDubey1704/agentic-ai-assistant.git
cd agentic-ai-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

## Configuration

Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_KEY=your_serpapi_key_here  # Optional: for web search
```

## Usage

### Basic Usage

```python
from agent import AgenticAI

# Initialize the agent
agent = AgenticAI()

# Give it a goal
result = agent.execute("Find the current weather in New York and calculate if it's warmer than 70°F")

print(result)
```

### Advanced Usage

```python
from agent import AgenticAI

agent = AgenticAI(
    model="gpt-4",
    temperature=0.7,
    max_iterations=10
)

# Complex multi-step task
task = """
Research the top 3 AI companies by market cap,
calculate their average valuation,
and save the results to a file called ai_companies.json
"""

result = agent.execute(task)
```

### Running the Demo

```bash
python demo.py
```

## Available Tools

The agent has access to these tools:

1. **Web Search**: Search the internet for information
2. **Calculator**: Perform mathematical calculations
3. **File Operations**: Read/write files
4. **Weather API**: Get current weather data
5. **Code Executor**: Run Python code safely
6. **Data Analyzer**: Analyze datasets

## Example Use Cases

### 1. Research Assistant
```python
agent.execute("Research the latest developments in quantum computing and summarize in 3 bullet points")
```

### 2. Data Analysis
```python
agent.execute("Analyze sales_data.csv and identify the top 5 products by revenue")
```

### 3. Automation
```python
agent.execute("Check if Bitcoin price is above $50,000 and send me a notification if true")
```

### 4. Content Creation
```python
agent.execute("Generate a technical blog post outline about microservices architecture")
```

## Project Structure

```
agentic-ai-assistant/
├── agent.py              # Main agent implementation
├── tools.py              # Tool definitions and implementations
├── memory.py             # Memory and learning system
├── planner.py            # Task planning and decomposition
├── executor.py           # Tool execution engine
├── demo.py               # Demo examples
├── tests/                # Unit tests
│   ├── test_agent.py
│   ├── test_tools.py
│   └── test_memory.py
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md            # This file
```

## How It Works

1. **Task Reception**: User provides a goal or task
2. **Planning**: Agent breaks down the task into steps
3. **Tool Selection**: Agent chooses appropriate tools for each step
4. **Execution**: Agent executes tools and processes results
5. **Decision Making**: Agent evaluates results and decides next action
6. **Iteration**: Repeats until goal is achieved or max iterations reached
7. **Response**: Returns final result to user

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with OpenAI GPT models
- Inspired by AutoGPT, LangChain, and modern agentic AI research

## Contact

Created by Shivansh Dubey
- GitHub: [@ShivanshDubey1704](https://github.com/ShivanshDubey1704)
- LinkedIn: [Shivansh Dubey](https://www.linkedin.com/in/shivansh-dubey)

---

⭐ Star this repo if you find it useful!
