# 🔍 Stock Analysis AI Crew

A comprehensive stock analysis system built with **CrewAI** that uses multiple specialized AI agents to provide thorough investment analysis. This project demonstrates the power of multi-agent collaboration for complex financial analysis tasks.

## 🎯 Project Overview

This project creates a team of AI agents that work together to analyze stocks from multiple perspectives:

- **Market Research Analyst**: Gathers market data, industry trends, and competitive analysis
- **Financial Analyst**: Analyzes financial statements, ratios, and company health
- **Technical Analyst**: Performs technical analysis and chart pattern recognition
- **Risk Assessment Specialist**: Evaluates investment risks and scenarios
- **Investment Advisor**: Synthesizes all analysis into actionable recommendations

## 🚀 Features

### Core Capabilities

- **Multi-Agent Collaboration**: 5 specialized agents working in sequence
- **Comprehensive Analysis**: Market, fundamental, technical, and risk analysis
- **Local LLM Integration**: Uses Ollama with DeepSeek-R1 for advanced reasoning
- **Real-time Data**: Fetches live stock data using yfinance
- **Automated Reporting**: Generates detailed markdown reports
- **Risk Assessment**: Calculates VaR, volatility, and scenario analysis

### Technical Features

- **CrewAI Framework**: Orchestrates agent collaboration
- **Ollama Integration**: Runs locally on your MacBook Pro
- **Financial Tools**: Custom tools for data fetching and calculations
- **Streamlit Interface**: Optional web interface for easy interaction
- **Extensible Design**: Easy to add new agents and capabilities

## 🛠️ Installation & Setup

### Prerequisites

- **macOS** (tested on MacBook Pro with 24GB RAM)
- **Python 3.9+**
- **Ollama** installed and running
- **Internet connection** for stock data

### Step 1: Install Ollama and Model

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the recommended model for financial analysis
ollama pull deepseek-r1:8b
```

### Step 2: Clone and Setup Python Environment

```bash
# Navigate to your project directory
cd "Your Project Directory"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Verify Setup

```bash
# Check if Ollama is running
ollama list

# Should show deepseek-r1:8b in the list
```

## 🎮 Usage

### Quick Start Demo

The easiest way to get started is with the demo script:

```bash
python demo_stock_analysis.py
```

This will:

1. Connect to your local Ollama instance
2. Ask for a stock symbol (e.g., AAPL, TSLA, MSFT)
3. Run the analysis crew
4. Generate a comprehensive report

### Advanced Usage

For full functionality with real data:

```bash
python stock_analysis_crew.py
```

This includes:

- Real-time stock data fetching
- Financial statement analysis
- Technical indicator calculations
- Risk metrics computation

## 📊 Sample Output

The system generates comprehensive reports like this:

```markdown
# Investment Analysis Report: AAPL

## Executive Summary

**Recommendation**: BUY (High Conviction)
**Price Target**: $185-195 (12-month)
**Risk Level**: Medium

## Market Analysis

- Strong brand moat and ecosystem
- iPhone revenue showing resilience
- Services segment growing at 15% YoY
- AI integration driving new product cycles

## Financial Health

- ROE: 26.4% (Excellent)
- Debt-to-Equity: 0.31 (Conservative)
- Free Cash Flow: $95B annually
- Gross Margin: 45.2% (Industry leading)

## Risk Assessment

- Regulatory risks in EU and China
- Supply chain dependencies
- Market saturation in smartphones
- Overall Risk Score: 6/10 (Medium)

## Investment Thesis

Apple's strong fundamentals, growing services revenue, and AI integration
position it well for continued growth...
```

## 🏗️ Project Structure

```
Stock Analysis AI Crew/
├── stock_analysis_crew.py      # Main comprehensive analysis system
├── demo_stock_analysis.py      # Simplified demo version
├── stock_tools.py              # Custom tools for data and calculations
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── reports/                    # Generated analysis reports
    ├── investment_report_20241215_143022.md
    └── ...
```

## 🤖 Agent Roles & Responsibilities

### 1. Market Research Analyst

- **Role**: Gathers market intelligence and industry analysis
- **Capabilities**: Industry trends, competitive landscape, news sentiment
- **Output**: Market research report with catalysts and risks

### 2. Financial Analyst

- **Role**: Analyzes company financials and health metrics
- **Capabilities**: Ratio analysis, trend identification, valuation
- **Output**: Financial health assessment and metrics

### 3. Technical Analyst

- **Role**: Performs technical analysis and chart patterns
- **Capabilities**: Price action, indicators, support/resistance
- **Output**: Technical analysis with entry/exit points

### 4. Risk Assessment Specialist

- **Role**: Evaluates investment risks and scenarios
- **Capabilities**: VaR calculation, scenario analysis, risk scoring
- **Output**: Comprehensive risk assessment

### 5. Investment Advisor

- **Role**: Synthesizes all analysis into recommendations
- **Capabilities**: Portfolio theory, risk-return optimization
- **Output**: Final investment recommendation with conviction

## 🔧 Customization

### Adding New Agents

```python
def create_custom_agent() -> Agent:
    return Agent(
        role="Your Custom Role",
        goal="Your specific goal for {stock_symbol}",
        backstory="Your agent's background and expertise",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
```

### Modifying Analysis Tasks

```python
def create_custom_task(agent: Agent) -> Task:
    return Task(
        description="Your custom analysis task",
        expected_output="What you expect the agent to produce",
        agent=agent
    )
```

## 📈 Performance Optimization

### For 24GB MacBook Pro:

- **Recommended Model**: DeepSeek-R1:8b (4.7GB)
- **Alternative**: Qwen2.5:14b (8.2GB) for more complex analysis
- **Concurrent Agents**: Up to 3 agents can run simultaneously
- **Memory Usage**: ~12-16GB during analysis

### Speed Optimization:

- Use `temperature=0.1` for consistent financial analysis
- Enable `memory=True` for context retention
- Set `max_iter=3` to prevent infinite loops

## 🚀 Advanced Features

### Real-time Data Integration

```python
# Enable real-time data fetching
from stock_tools import StockDataTool

stock_data = StockDataTool()
info = stock_data.get_stock_info("AAPL")
```

### Custom Risk Metrics

```python
# Calculate custom risk metrics
from stock_tools import RiskCalculatorTool

risk_calc = RiskCalculatorTool()
var_analysis = risk_calc.calculate_var(returns_data)
```

## 🎯 Learning Objectives

This project teaches you:

1. **CrewAI Fundamentals**: Agent creation, task definition, crew orchestration
2. **Multi-Agent Systems**: How agents collaborate and share context
3. **Financial Analysis**: Real-world application of AI in finance
4. **Local LLM Integration**: Using Ollama for private, powerful analysis
5. **Tool Development**: Creating custom tools for specialized tasks

## 🔍 Troubleshooting

### Common Issues:

**Ollama Connection Error:**

```bash
# Check if Ollama is running
ollama list

# Start Ollama if needed
ollama serve
```

**Model Not Found:**

```bash
# Pull the required model
ollama pull deepseek-r1:8b
```

**Memory Issues:**

- Reduce model size: Use `deepseek-r1:8b` instead of larger models
- Limit concurrent agents: Set `max_iter=2`
- Close other applications to free RAM

**Import Errors:**

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 🎉 Next Steps

Once you're comfortable with this project, try:

1. **Add More Agents**: ESG analyst, Options analyst, Crypto analyst
2. **Integrate APIs**: Real news APIs, economic data feeds
3. **Build Web Interface**: Streamlit dashboard for easy interaction
4. **Portfolio Analysis**: Analyze multiple stocks simultaneously
5. **Backtesting**: Test recommendations against historical data

## 📚 Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Ollama Models](https://ollama.ai/library)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [Financial Analysis Fundamentals](https://www.investopedia.com/)

## 🤝 Contributing

Feel free to contribute by:

- Adding new agent types
- Improving analysis algorithms
- Enhancing the UI/UX
- Adding more financial data sources
- Optimizing performance

## 📄 License

This project is for educational purposes. Please ensure compliance with financial data usage terms and regulations.

---

**Happy Analyzing! 📊🚀**

_Built with CrewAI, Ollama, and ❤️ for learning multi-agent systems_
