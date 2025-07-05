#!/usr/bin/env python3
"""
Stock Analysis Demo
===================

A simplified demo of the Stock Analysis AI Crew that showcases the agent interactions
without requiring complex external dependencies. This is perfect for learning CrewAI!
"""

import os
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

# Initialize Ollama with DeepSeek-R1 model
try:
    llm = Ollama(
        model="deepseek-r1:8b",
        base_url="http://localhost:11434",
        temperature=0.1
    )
    print("✅ Connected to Ollama with DeepSeek-R1:8b")
except Exception as e:
    print(f"⚠️  Ollama connection failed: {e}")
    print("Make sure Ollama is running and DeepSeek-R1:8b is installed")
    exit(1)


def create_market_analyst() -> Agent:
    """Creates a Market Research Analyst agent"""
    return Agent(
        role="Senior Market Research Analyst",
        goal="Research and analyze market conditions for {stock_symbol}",
        backstory="""You are an experienced market research analyst with deep knowledge 
        of financial markets, industry trends, and economic indicators. You excel at 
        gathering market intelligence and identifying key factors that drive stock performance.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def create_financial_analyst() -> Agent:
    """Creates a Financial Analyst agent"""
    return Agent(
        role="Senior Financial Analyst",
        goal="Analyze financial health and performance metrics for {stock_symbol}",
        backstory="""You are a CFA charterholder with expertise in financial statement 
        analysis, ratio calculations, and valuation methods. You can quickly assess a 
        company's financial strength and identify potential red flags.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def create_investment_advisor() -> Agent:
    """Creates an Investment Advisor agent"""
    return Agent(
        role="Senior Investment Advisor",
        goal="Provide actionable investment recommendations for {stock_symbol}",
        backstory="""You are a seasoned investment advisor with 20+ years of experience. 
        You excel at synthesizing complex analysis into clear, actionable investment 
        recommendations that consider risk, return, and market conditions.""",
        verbose=True,
        allow_delegation=True,
        llm=llm
    )


def create_market_research_task(agent: Agent) -> Task:
    """Creates market research task"""
    return Task(
        description="""Conduct comprehensive market research for {stock_symbol}:
        
        1. **Company Overview**: What does this company do? What are their main products/services?
        2. **Industry Analysis**: What industry trends are affecting this company?
        3. **Market Position**: How does this company compare to competitors?
        4. **Recent News**: What recent developments might impact the stock?
        5. **Economic Factors**: What macroeconomic factors could affect this stock?
        
        Provide insights based on your knowledge of markets and general business principles.
        Focus on qualitative analysis and market dynamics.""",

        expected_output="""A comprehensive market research report containing:
        - Company business model and competitive advantages
        - Industry trends and growth prospects  
        - Competitive positioning analysis
        - Recent market developments and catalysts
        - Macroeconomic impact assessment""",

        agent=agent
    )


def create_financial_analysis_task(agent: Agent) -> Task:
    """Creates financial analysis task"""
    return Task(
        description="""Perform financial analysis for {stock_symbol}:
        
        1. **Business Model Analysis**: How does the company make money?
        2. **Revenue Streams**: What are the main sources of revenue?
        3. **Profitability Assessment**: What factors drive profitability?
        4. **Financial Health Indicators**: What should investors look for?
        5. **Valuation Considerations**: What metrics are most relevant?
        
        Focus on fundamental analysis principles and financial health assessment.
        Use your knowledge of financial analysis best practices.""",

        expected_output="""A detailed financial analysis including:
        - Business model evaluation
        - Revenue and profitability analysis
        - Financial health assessment
        - Key financial metrics to monitor
        - Valuation framework recommendations""",

        agent=agent
    )


def create_investment_recommendation_task(agent: Agent) -> Task:
    """Creates final investment recommendation task"""
    return Task(
        description="""Synthesize the market research and financial analysis to provide 
        a comprehensive investment recommendation for {stock_symbol}:
        
        1. **Executive Summary**: Key findings from all analyses
        2. **Investment Thesis**: Why should someone invest (or not invest)?
        3. **Risk Assessment**: What are the main risks to consider?
        4. **Investment Recommendation**: BUY/HOLD/SELL with reasoning
        5. **Key Monitoring Points**: What should investors watch going forward?
        
        Provide clear, actionable recommendations with supporting rationale.""",

        expected_output="""A comprehensive investment recommendation containing:
        - Clear BUY/HOLD/SELL recommendation with conviction level
        - Investment thesis with bull and bear case scenarios
        - Risk assessment and mitigation strategies
        - Key metrics and events to monitor
        - Executive summary for decision-making""",

        agent=agent,
        context=["market_research_task", "financial_analysis_task"],
        output_file=f"investment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    )


def run_stock_analysis(stock_symbol: str):
    """Run the stock analysis crew"""

    print(f"\n🚀 Starting Stock Analysis for {stock_symbol.upper()}")
    print("=" * 60)

    # Create agents
    market_analyst = create_market_analyst()
    financial_analyst = create_financial_analyst()
    investment_advisor = create_investment_advisor()

    # Create tasks
    market_research_task = create_market_research_task(market_analyst)
    financial_analysis_task = create_financial_analysis_task(financial_analyst)
    investment_recommendation_task = create_investment_recommendation_task(
        investment_advisor)

    # Create crew
    crew = Crew(
        agents=[market_analyst, financial_analyst, investment_advisor],
        tasks=[market_research_task, financial_analysis_task,
               investment_recommendation_task],
        process=Process.sequential,
        verbose=2,
        memory=True
    )

    # Run analysis
    try:
        result = crew.kickoff(inputs={"stock_symbol": stock_symbol.upper()})

        print(f"\n✅ Analysis Complete for {stock_symbol.upper()}")
        print("=" * 60)
        print(f"\n📊 Final Investment Recommendation:\n{result}")

        return result

    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return None


def main():
    """Main function"""
    print("🔍 Stock Analysis AI Crew - Demo Version")
    print("=" * 50)
    print("This demo showcases CrewAI agents working together to analyze stocks!")
    print("The agents will use their reasoning capabilities to provide insights.")
    print()

    # Get stock symbol from user
    stock_symbol = input(
        "Enter a stock symbol to analyze (e.g., AAPL, TSLA, MSFT): ").strip().upper()

    if not stock_symbol:
        print("❌ Please provide a valid stock symbol")
        return

    # Run analysis
    result = run_stock_analysis(stock_symbol)

    if result:
        print(
            f"\n🎉 Analysis completed! Check the generated report file for detailed results.")
    else:
        print("\n❌ Analysis failed. Please check your Ollama setup.")


if __name__ == "__main__":
    main()
