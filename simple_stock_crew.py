#!/usr/bin/env python3
"""
Simple Stock Analysis Crew (Python 3.9 Compatible)
==================================================

A simplified multi-agent stock analysis system that demonstrates the concepts
of CrewAI without requiring Python 3.10+. This is perfect for learning!

This version uses basic classes to simulate agent behavior and shows how
multiple AI agents can work together to analyze stocks.
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import yfinance as yf


class OllamaAgent:
    """Simple agent that uses Ollama for reasoning"""

    def __init__(self, role: str, goal: str, backstory: str):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.ollama_url = "http://localhost:11434/api/generate"

    def think(self, prompt: str, context: str = "") -> str:
        """Use Ollama to process the prompt and return response"""
        try:
            full_prompt = f"""
Role: {self.role}
Goal: {self.goal}
Background: {self.backstory}

Context: {context}

Task: {prompt}

Please provide a detailed analysis based on your role and expertise.
"""

            payload = {
                "model": "deepseek-r1:8b",
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 1000
                }
            }

            response = requests.post(
                self.ollama_url, json=payload, timeout=120)

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response generated")
            else:
                return f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            return f"Error communicating with Ollama: {str(e)}"


class StockDataFetcher:
    """Fetches real stock data"""

    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """Get basic stock information"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            hist = stock.history(period="1y")

            return {
                "symbol": symbol,
                "company_name": info.get("longName", "N/A"),
                "current_price": info.get("currentPrice", 0),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "beta": info.get("beta", 0),
                "dividend_yield": info.get("dividendYield", 0),
                "52_week_high": info.get("fiftyTwoWeekHigh", 0),
                "52_week_low": info.get("fiftyTwoWeekLow", 0),
                "year_performance": f"{((hist['Close'].iloc[-1] / hist['Close'].iloc[0] - 1) * 100):.2f}%" if not hist.empty else "N/A"
            }
        except Exception as e:
            return {"error": f"Failed to fetch data: {str(e)}"}


class StockAnalysisCrew:
    """Simple crew of agents for stock analysis"""

    def __init__(self):
        self.data_fetcher = StockDataFetcher()
        self.agents = self.create_agents()

    def create_agents(self) -> Dict[str, OllamaAgent]:
        """Create the analysis agents"""
        return {
            "market_analyst": OllamaAgent(
                role="Senior Market Research Analyst",
                goal="Analyze market conditions, industry trends, and competitive landscape",
                backstory="You are an experienced market analyst with 15+ years in equity research. You excel at identifying market trends, competitive dynamics, and growth catalysts."
            ),

            "financial_analyst": OllamaAgent(
                role="Senior Financial Analyst",
                goal="Evaluate financial health, ratios, and valuation metrics",
                backstory="You are a CFA charterholder with deep expertise in financial analysis. You can quickly assess company fundamentals, calculate key ratios, and identify financial strengths and weaknesses."
            ),

            "risk_analyst": OllamaAgent(
                role="Risk Assessment Specialist",
                goal="Identify and quantify investment risks and scenarios",
                backstory="You are a risk management expert with expertise in portfolio theory and risk assessment. You excel at identifying potential risks and developing mitigation strategies."
            ),

            "investment_advisor": OllamaAgent(
                role="Senior Investment Advisor",
                goal="Synthesize analysis and provide actionable investment recommendations",
                backstory="You are a seasoned investment advisor with 20+ years of experience. You excel at combining multiple analyses into clear, actionable investment recommendations."
            )
        }

    def analyze_stock(self, symbol: str) -> Dict[str, Any]:
        """Run complete stock analysis"""
        print(f"\n🚀 Starting Analysis for {symbol.upper()}")
        print("=" * 50)

        # Step 1: Fetch stock data
        print("📊 Fetching stock data...")
        stock_data = self.data_fetcher.get_stock_info(symbol)

        if "error" in stock_data:
            return {"error": stock_data["error"]}

        # Create context from stock data
        context = f"""
Stock: {stock_data['symbol']} - {stock_data['company_name']}
Current Price: ${stock_data['current_price']}
Market Cap: ${stock_data['market_cap']:,}
P/E Ratio: {stock_data['pe_ratio']}
Sector: {stock_data['sector']}
Industry: {stock_data['industry']}
Beta: {stock_data['beta']}
Dividend Yield: {stock_data['dividend_yield']}
52-Week Range: ${stock_data['52_week_low']} - ${stock_data['52_week_high']}
Year Performance: {stock_data['year_performance']}
"""

        results = {}

        # Step 2: Market Analysis
        print("🔍 Market Analyst working...")
        market_prompt = f"""
Analyze the market conditions for {symbol}:

1. Industry Analysis: What trends are affecting the {stock_data['sector']} sector?
2. Competitive Position: How does this company compare in the {stock_data['industry']} industry?
3. Market Catalysts: What factors could drive the stock price?
4. Economic Impact: How might macroeconomic factors affect this stock?

Provide specific insights about market dynamics and competitive positioning.
"""
        results["market_analysis"] = self.agents["market_analyst"].think(
            market_prompt, context)

        # Step 3: Financial Analysis
        print("💰 Financial Analyst working...")
        financial_prompt = f"""
Analyze the financial aspects of {symbol}:

1. Valuation Assessment: Is the P/E ratio of {stock_data['pe_ratio']} reasonable for this company?
2. Financial Health: What does the current market cap of ${stock_data['market_cap']:,} suggest?
3. Dividend Analysis: Evaluate the dividend yield of {stock_data['dividend_yield']}
4. Growth Potential: Based on the sector and industry, what growth prospects exist?

Focus on financial metrics and valuation analysis.
"""
        results["financial_analysis"] = self.agents["financial_analyst"].think(
            financial_prompt, context)

        # Step 4: Risk Analysis
        print("⚠️ Risk Analyst working...")
        risk_prompt = f"""
Assess the investment risks for {symbol}:

1. Market Risk: The beta is {stock_data['beta']} - what does this mean for volatility?
2. Sector Risk: What risks are specific to the {stock_data['sector']} sector?
3. Valuation Risk: Is the current valuation sustainable?
4. Scenario Analysis: What are the best and worst case scenarios?

Provide a comprehensive risk assessment with specific risk factors.
"""
        results["risk_analysis"] = self.agents["risk_analyst"].think(
            risk_prompt, context)

        # Step 5: Investment Recommendation
        print("🎯 Investment Advisor synthesizing...")
        recommendation_prompt = f"""
Based on all the analysis, provide a final investment recommendation for {symbol}:

Market Analysis Summary: {results['market_analysis'][:500]}...
Financial Analysis Summary: {results['financial_analysis'][:500]}...
Risk Analysis Summary: {results['risk_analysis'][:500]}...

Provide:
1. Investment Recommendation: BUY/HOLD/SELL with conviction level (1-10)
2. Price Target: 12-month target price with reasoning
3. Key Risks: Top 3 risks to monitor
4. Investment Thesis: Why invest or not invest
5. Position Sizing: Recommended allocation percentage

Make it actionable and specific.
"""
        results["investment_recommendation"] = self.agents["investment_advisor"].think(
            recommendation_prompt, context
        )

        # Compile final report
        report = {
            "symbol": symbol.upper(),
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stock_data": stock_data,
            "market_analysis": results["market_analysis"],
            "financial_analysis": results["financial_analysis"],
            "risk_analysis": results["risk_analysis"],
            "investment_recommendation": results["investment_recommendation"]
        }

        return report

    def save_report(self, report: Dict[str, Any], filename: str = None):
        """Save analysis report to file"""
        if not filename:
            filename = f"stock_analysis_{report['symbol']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📄 Report saved to: {filename}")
        return filename


def main():
    """Main function"""
    print("🔍 Simple Stock Analysis Crew")
    print("=" * 40)
    print("Multi-agent stock analysis using Ollama!")
    print()

    # Check if Ollama is available
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print("❌ Ollama not running. Please start Ollama first:")
            print("   ollama serve")
            return
    except:
        print("❌ Cannot connect to Ollama. Make sure it's running:")
        print("   ollama serve")
        return

    print("✅ Connected to Ollama")

    # Get stock symbol
    symbol = input(
        "\nEnter stock symbol (e.g., AAPL, TSLA, MSFT): ").strip().upper()

    if not symbol:
        print("❌ Please provide a valid stock symbol")
        return

    # Run analysis
    crew = StockAnalysisCrew()

    try:
        report = crew.analyze_stock(symbol)

        if "error" in report:
            print(f"❌ Error: {report['error']}")
            return

        print(f"\n✅ Analysis Complete for {symbol}")
        print("=" * 50)

        # Save report
        filename = crew.save_report(report)

        # Display summary
        print(f"\n📊 INVESTMENT SUMMARY for {symbol}")
        print("=" * 50)
        print(f"Company: {report['stock_data']['company_name']}")
        print(f"Current Price: ${report['stock_data']['current_price']}")
        print(f"Sector: {report['stock_data']['sector']}")
        print(f"Year Performance: {report['stock_data']['year_performance']}")
        print()
        print("🎯 INVESTMENT RECOMMENDATION:")
        print(report['investment_recommendation'])

        print(f"\n📄 Full report saved to: {filename}")

    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")


if __name__ == "__main__":
    main()
