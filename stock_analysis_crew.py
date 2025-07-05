#!/usr/bin/env python3
"""
Stock Analysis AI Crew
======================

A comprehensive stock analysis system using CrewAI with specialized agents:
- Market Research Analyst: Gathers market data and news
- Financial Analyst: Analyzes financial statements and ratios
- Technical Analyst: Performs technical analysis and chart patterns
- Risk Assessment Specialist: Evaluates investment risks
- Investment Advisor: Provides final recommendations

Uses Ollama with DeepSeek-R1 for advanced financial reasoning.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any

from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

# Initialize Ollama with DeepSeek-R1 model
llm = Ollama(
    model="deepseek-r1:8b",
    base_url="http://localhost:11434",
    temperature=0.1  # Low temperature for more consistent financial analysis
)


class StockAnalysisCrew:
    """Stock Analysis AI Crew for comprehensive financial analysis"""

    def __init__(self):
        self.llm = llm

    def create_market_research_analyst(self) -> Agent:
        """Creates a Market Research Analyst agent"""
        return Agent(
            role="Senior Market Research Analyst",
            goal="Gather comprehensive market data, news, and industry trends for {stock_symbol}",
            backstory="""You are a seasoned market research analyst with 15+ years of experience 
            in equity research. You excel at gathering and synthesizing market data, news sentiment, 
            industry trends, and competitive landscape analysis. You have access to multiple data 
            sources and can quickly identify key market drivers and catalysts.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            memory=True
        )

    def create_financial_analyst(self) -> Agent:
        """Creates a Financial Analyst agent"""
        return Agent(
            role="Senior Financial Analyst",
            goal="Analyze financial statements, calculate key ratios, and assess financial health of {stock_symbol}",
            backstory="""You are a CFA charterholder with extensive experience in financial statement 
            analysis. You specialize in calculating and interpreting financial ratios, identifying 
            trends in revenue, profitability, and cash flow. You can quickly spot red flags and 
            strengths in a company's financial position.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            memory=True
        )

    def create_technical_analyst(self) -> Agent:
        """Creates a Technical Analyst agent"""
        return Agent(
            role="Senior Technical Analyst",
            goal="Perform technical analysis including chart patterns, indicators, and price action for {stock_symbol}",
            backstory="""You are a technical analysis expert with deep knowledge of chart patterns, 
            technical indicators, and market psychology. You can identify support/resistance levels, 
            trend patterns, and momentum indicators. You provide insights on optimal entry/exit points 
            and short-term price movements.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            memory=True
        )

    def create_risk_analyst(self) -> Agent:
        """Creates a Risk Assessment Specialist agent"""
        return Agent(
            role="Risk Assessment Specialist",
            goal="Evaluate investment risks, volatility, and potential downside scenarios for {stock_symbol}",
            backstory="""You are a risk management expert with expertise in quantitative risk models, 
            scenario analysis, and portfolio theory. You excel at identifying and quantifying various 
            types of investment risks including market risk, sector risk, company-specific risk, and 
            macroeconomic risks.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            memory=True
        )

    def create_investment_advisor(self) -> Agent:
        """Creates an Investment Advisor agent"""
        return Agent(
            role="Senior Investment Advisor",
            goal="Synthesize all analysis and provide actionable investment recommendations for {stock_symbol}",
            backstory="""You are a senior investment advisor with 20+ years of experience managing 
            portfolios for high-net-worth clients. You excel at synthesizing complex financial analysis 
            into clear, actionable investment recommendations. You consider risk tolerance, investment 
            horizon, and market conditions in your recommendations.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            max_iter=3,
            memory=True
        )

    def create_market_research_task(self, agent: Agent) -> Task:
        """Creates market research task"""
        return Task(
            description="""Conduct comprehensive market research for {stock_symbol}:
            
            1. **Company Overview**: Basic company information, business model, key products/services
            2. **Industry Analysis**: Industry trends, growth prospects, competitive landscape
            3. **Recent News & Events**: Recent earnings, announcements, news sentiment
            4. **Market Position**: Market share, competitive advantages, key competitors
            5. **Macroeconomic Factors**: Relevant economic indicators affecting the stock
            
            Focus on gathering factual, current information that will inform investment decisions.
            Identify key catalysts and risk factors from a market perspective.""",

            expected_output="""A comprehensive market research report containing:
            - Company overview and business model analysis
            - Industry trends and competitive positioning
            - Recent news sentiment and key events
            - Market catalysts and risk factors
            - Macroeconomic impact assessment""",

            agent=agent
        )

    def create_financial_analysis_task(self, agent: Agent) -> Task:
        """Creates financial analysis task"""
        return Task(
            description="""Perform detailed financial analysis for {stock_symbol}:
            
            1. **Financial Statements Review**: Latest income statement, balance sheet, cash flow
            2. **Key Financial Ratios**: Profitability, liquidity, efficiency, leverage ratios
            3. **Trend Analysis**: 3-5 year historical trends in key metrics
            4. **Valuation Metrics**: P/E, P/B, P/S, EV/EBITDA, PEG ratio analysis
            5. **Financial Health**: Debt levels, cash position, working capital analysis
            6. **Growth Analysis**: Revenue growth, earnings growth, margin trends
            
            Provide quantitative analysis with specific numbers and calculations.""",

            expected_output="""A detailed financial analysis report including:
            - Key financial ratios with industry comparisons
            - Trend analysis of financial performance
            - Valuation assessment using multiple methods
            - Financial strength and weakness identification
            - Growth trajectory analysis""",

            agent=agent
        )

    def create_technical_analysis_task(self, agent: Agent) -> Task:
        """Creates technical analysis task"""
        return Task(
            description="""Perform comprehensive technical analysis for {stock_symbol}:
            
            1. **Price Action Analysis**: Current trend, support/resistance levels
            2. **Chart Patterns**: Identify key chart patterns and formations
            3. **Technical Indicators**: RSI, MACD, Moving averages, Volume analysis
            4. **Momentum Analysis**: Price momentum, trend strength indicators
            5. **Entry/Exit Points**: Optimal buying/selling levels based on technicals
            6. **Short-term Outlook**: Technical forecast for next 1-3 months
            
            Focus on actionable technical insights for trading and investment timing.""",

            expected_output="""A comprehensive technical analysis report containing:
            - Current trend analysis and key levels
            - Chart pattern identification
            - Technical indicator signals
            - Momentum and volume analysis
            - Recommended entry/exit strategies
            - Short-term price targets and stop-loss levels""",

            agent=agent
        )

    def create_risk_assessment_task(self, agent: Agent) -> Task:
        """Creates risk assessment task"""
        return Task(
            description="""Conduct thorough risk assessment for {stock_symbol}:
            
            1. **Market Risk**: Beta analysis, correlation with market indices
            2. **Sector Risk**: Industry-specific risks and cyclical factors
            3. **Company Risk**: Business model risks, management risks, operational risks
            4. **Financial Risk**: Leverage, liquidity, credit risks
            5. **Regulatory Risk**: Compliance, regulatory changes, legal issues
            6. **Scenario Analysis**: Best case, worst case, and base case scenarios
            7. **Risk-Reward Assessment**: Risk-adjusted return potential
            
            Quantify risks where possible and provide mitigation strategies.""",

            expected_output="""A comprehensive risk assessment report including:
            - Quantified risk metrics (Beta, volatility, VaR if applicable)
            - Identified key risk factors by category
            - Scenario analysis with probability assessments
            - Risk mitigation recommendations
            - Overall risk rating and justification""",

            agent=agent,
            context=["market_research_task",
                     "financial_analysis_task", "technical_analysis_task"]
        )

    def create_investment_recommendation_task(self, agent: Agent) -> Task:
        """Creates final investment recommendation task"""
        return Task(
            description="""Synthesize all analysis and provide final investment recommendation for {stock_symbol}:
            
            1. **Executive Summary**: Key findings from all analyses
            2. **Investment Thesis**: Bull and bear case scenarios
            3. **Valuation Assessment**: Fair value estimate and current valuation
            4. **Risk-Reward Analysis**: Expected returns vs. identified risks
            5. **Investment Recommendation**: BUY/HOLD/SELL with conviction level
            6. **Price Targets**: 12-month price target with ranges
            7. **Portfolio Allocation**: Recommended position size considerations
            8. **Monitoring Points**: Key metrics and events to watch
            
            Provide clear, actionable recommendations with supporting rationale.""",

            expected_output="""A comprehensive investment recommendation report containing:
            - Clear BUY/HOLD/SELL recommendation with conviction level
            - 12-month price target with upside/downside scenarios
            - Key investment thesis and supporting evidence
            - Risk-reward assessment and position sizing guidance
            - Monitoring checklist for ongoing evaluation
            - Executive summary suitable for decision-making""",

            agent=agent,
            context=["market_research_task", "financial_analysis_task",
                     "technical_analysis_task", "risk_assessment_task"],
            output_file=f"stock_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )

    def create_crew(self, stock_symbol: str) -> Crew:
        """Creates and returns the stock analysis crew"""

        # Create agents
        market_analyst = self.create_market_research_analyst()
        financial_analyst = self.create_financial_analyst()
        technical_analyst = self.create_technical_analyst()
        risk_analyst = self.create_risk_analyst()
        investment_advisor = self.create_investment_advisor()

        # Create tasks
        market_research_task = self.create_market_research_task(market_analyst)
        financial_analysis_task = self.create_financial_analysis_task(
            financial_analyst)
        technical_analysis_task = self.create_technical_analysis_task(
            technical_analyst)
        risk_assessment_task = self.create_risk_assessment_task(risk_analyst)
        investment_recommendation_task = self.create_investment_recommendation_task(
            investment_advisor)

        # Create and return crew
        return Crew(
            agents=[
                market_analyst,
                financial_analyst,
                technical_analyst,
                risk_analyst,
                investment_advisor
            ],
            tasks=[
                market_research_task,
                financial_analysis_task,
                technical_analysis_task,
                risk_assessment_task,
                investment_recommendation_task
            ],
            process=Process.sequential,
            verbose=2,
            memory=True
        )

    def analyze_stock(self, stock_symbol: str) -> str:
        """Run the complete stock analysis for a given symbol"""
        print(f"\n🚀 Starting Stock Analysis for {stock_symbol.upper()}")
        print("=" * 60)

        # Create crew
        crew = self.create_crew(stock_symbol)

        # Run analysis
        result = crew.kickoff(inputs={"stock_symbol": stock_symbol.upper()})

        print(f"\n✅ Analysis Complete for {stock_symbol.upper()}")
        print("=" * 60)

        return result


def main():
    """Main function to run stock analysis"""
    print("🔍 Stock Analysis AI Crew")
    print("=" * 40)

    # Get stock symbol from user
    stock_symbol = input(
        "Enter stock symbol to analyze (e.g., AAPL, TSLA, MSFT): ").strip().upper()

    if not stock_symbol:
        print("❌ Please provide a valid stock symbol")
        return

    # Create and run analysis
    crew = StockAnalysisCrew()

    try:
        result = crew.analyze_stock(stock_symbol)
        print(f"\n📊 Final Analysis Result:\n{result}")

    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        print("Make sure Ollama is running and DeepSeek-R1:8b model is available")


if __name__ == "__main__":
    main()
