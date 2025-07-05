#!/usr/bin/env python3
"""
Stock Analysis Tools
===================

Custom tools for the Stock Analysis AI Crew to enhance analysis capabilities.
These tools provide data fetching, financial calculations, and analysis utilities.
"""

import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd


class StockDataTool:
    """Tool for fetching stock data and financial information"""

    def __init__(self):
        self.name = "Stock Data Fetcher"
        self.description = "Fetches real-time and historical stock data, financial statements, and company information"

    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """Get basic stock information"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            return {
                "symbol": symbol,
                "company_name": info.get("longName", "N/A"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "market_cap": info.get("marketCap", 0),
                "current_price": info.get("currentPrice", 0),
                "previous_close": info.get("previousClose", 0),
                "day_high": info.get("dayHigh", 0),
                "day_low": info.get("dayLow", 0),
                "volume": info.get("volume", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "forward_pe": info.get("forwardPE", 0),
                "dividend_yield": info.get("dividendYield", 0),
                "beta": info.get("beta", 0),
                "52_week_high": info.get("fiftyTwoWeekHigh", 0),
                "52_week_low": info.get("fiftyTwoWeekLow", 0),
            }
        except Exception as e:
            return {"error": f"Failed to fetch stock info: {str(e)}"}

    def get_historical_data(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """Get historical price data"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)

            if hist.empty:
                return {"error": "No historical data available"}

            return {
                "symbol": symbol,
                "period": period,
                "data_points": len(hist),
                "latest_close": float(hist['Close'].iloc[-1]),
                "period_high": float(hist['High'].max()),
                "period_low": float(hist['Low'].min()),
                "average_volume": float(hist['Volume'].mean()),
                "price_change": float(hist['Close'].iloc[-1] - hist['Close'].iloc[0]),
                "price_change_percent": float((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100),
                # Annualized volatility
                "volatility": float(hist['Close'].pct_change().std() * (252**0.5)),
                "raw_data": hist.to_dict()
            }
        except Exception as e:
            return {"error": f"Failed to fetch historical data: {str(e)}"}

    def get_financial_statements(self, symbol: str) -> Dict[str, Any]:
        """Get financial statements data"""
        try:
            stock = yf.Ticker(symbol)

            # Get financial statements
            income_stmt = stock.financials
            balance_sheet = stock.balance_sheet
            cash_flow = stock.cashflow

            result = {
                "symbol": symbol,
                "has_income_statement": not income_stmt.empty,
                "has_balance_sheet": not balance_sheet.empty,
                "has_cash_flow": not cash_flow.empty,
            }

            if not income_stmt.empty:
                latest_year = income_stmt.columns[0]
                result["income_statement"] = {
                    "latest_year": str(latest_year),
                    "total_revenue": float(income_stmt.loc["Total Revenue", latest_year]) if "Total Revenue" in income_stmt.index else 0,
                    "gross_profit": float(income_stmt.loc["Gross Profit", latest_year]) if "Gross Profit" in income_stmt.index else 0,
                    "operating_income": float(income_stmt.loc["Operating Income", latest_year]) if "Operating Income" in income_stmt.index else 0,
                    "net_income": float(income_stmt.loc["Net Income", latest_year]) if "Net Income" in income_stmt.index else 0,
                }

            if not balance_sheet.empty:
                latest_year = balance_sheet.columns[0]
                result["balance_sheet"] = {
                    "latest_year": str(latest_year),
                    "total_assets": float(balance_sheet.loc["Total Assets", latest_year]) if "Total Assets" in balance_sheet.index else 0,
                    "total_debt": float(balance_sheet.loc["Total Debt", latest_year]) if "Total Debt" in balance_sheet.index else 0,
                    "stockholder_equity": float(balance_sheet.loc["Stockholders Equity", latest_year]) if "Stockholders Equity" in balance_sheet.index else 0,
                    "cash_and_equivalents": float(balance_sheet.loc["Cash And Cash Equivalents", latest_year]) if "Cash And Cash Equivalents" in balance_sheet.index else 0,
                }

            return result

        except Exception as e:
            return {"error": f"Failed to fetch financial statements: {str(e)}"}


class FinancialCalculatorTool:
    """Tool for financial calculations and ratio analysis"""

    def __init__(self):
        self.name = "Financial Calculator"
        self.description = "Performs financial calculations, ratio analysis, and valuation metrics"

    def calculate_financial_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate key financial ratios"""
        ratios = {}

        try:
            # Extract data
            income = financial_data.get("income_statement", {})
            balance = financial_data.get("balance_sheet", {})
            stock_info = financial_data.get("stock_info", {})

            revenue = income.get("total_revenue", 0)
            net_income = income.get("net_income", 0)
            gross_profit = income.get("gross_profit", 0)
            total_assets = balance.get("total_assets", 0)
            total_debt = balance.get("total_debt", 0)
            equity = balance.get("stockholder_equity", 0)
            market_cap = stock_info.get("market_cap", 0)
            current_price = stock_info.get("current_price", 0)

            # Profitability Ratios
            if revenue > 0:
                ratios["gross_margin"] = (gross_profit / revenue) * 100
                ratios["net_margin"] = (net_income / revenue) * 100

            if total_assets > 0:
                ratios["roa"] = (net_income / total_assets) * \
                    100  # Return on Assets

            if equity > 0:
                ratios["roe"] = (net_income / equity) * 100  # Return on Equity

            # Leverage Ratios
            if total_assets > 0:
                ratios["debt_to_assets"] = (total_debt / total_assets) * 100

            if equity > 0:
                ratios["debt_to_equity"] = (total_debt / equity) * 100

            # Valuation Ratios
            if net_income > 0 and market_cap > 0:
                ratios["pe_ratio"] = market_cap / net_income

            if revenue > 0 and market_cap > 0:
                ratios["price_to_sales"] = market_cap / revenue

            if equity > 0 and market_cap > 0:
                ratios["price_to_book"] = market_cap / equity

        except Exception as e:
            ratios["error"] = f"Calculation error: {str(e)}"

        return ratios

    def calculate_technical_indicators(self, price_data: List[float], volume_data: List[float] = None) -> Dict[str, Any]:
        """Calculate basic technical indicators"""
        if not price_data or len(price_data) < 2:
            return {"error": "Insufficient price data"}

        try:
            indicators = {}

            # Simple Moving Averages
            if len(price_data) >= 20:
                indicators["sma_20"] = sum(price_data[-20:]) / 20
            if len(price_data) >= 50:
                indicators["sma_50"] = sum(price_data[-50:]) / 50

            # Price momentum
            if len(price_data) >= 10:
                indicators["momentum_10"] = (
                    (price_data[-1] / price_data[-10]) - 1) * 100

            # Volatility (standard deviation of returns)
            if len(price_data) >= 20:
                returns = [(price_data[i] / price_data[i-1] - 1)
                           for i in range(1, len(price_data))]
                volatility = (
                    sum([(r - sum(returns)/len(returns))**2 for r in returns]) / len(returns))**0.5
                indicators["volatility_20d"] = volatility * 100

            # Support and Resistance (simple version)
            if len(price_data) >= 20:
                recent_prices = price_data[-20:]
                indicators["support_level"] = min(recent_prices)
                indicators["resistance_level"] = max(recent_prices)

            return indicators

        except Exception as e:
            return {"error": f"Technical indicator calculation error: {str(e)}"}


class NewsAnalysisTool:
    """Tool for analyzing news sentiment and market events"""

    def __init__(self):
        self.name = "News Analyzer"
        self.description = "Analyzes news sentiment and identifies market-moving events"

    def get_recent_news(self, symbol: str) -> Dict[str, Any]:
        """Get recent news for a stock (simulated for demo)"""
        # In a real implementation, this would connect to news APIs
        # For demo purposes, we'll return a structured format

        return {
            "symbol": symbol,
            "news_count": 5,
            "sentiment_score": 0.2,  # -1 to 1 scale
            "sentiment_label": "Slightly Positive",
            "key_topics": ["earnings", "product launch", "market expansion"],
            "recent_headlines": [
                f"{symbol} reports strong quarterly earnings",
                f"Analysts upgrade {symbol} price target",
                f"{symbol} announces new product line",
                f"Market volatility affects {symbol} trading",
                f"{symbol} CEO speaks at industry conference"
            ],
            "last_updated": datetime.now().isoformat()
        }

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text (basic implementation)"""
        # Simple keyword-based sentiment analysis
        positive_words = ["good", "great", "excellent",
                          "strong", "positive", "growth", "profit", "success"]
        negative_words = ["bad", "poor", "weak", "negative",
                          "decline", "loss", "risk", "concern"]

        text_lower = text.lower()
        positive_count = sum(
            1 for word in positive_words if word in text_lower)
        negative_count = sum(
            1 for word in negative_words if word in text_lower)

        total_words = len(text.split())

        if total_words == 0:
            return {"sentiment": "neutral", "score": 0.0, "confidence": 0.0}

        sentiment_score = (positive_count - negative_count) / total_words

        if sentiment_score > 0.1:
            sentiment = "positive"
        elif sentiment_score < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "score": sentiment_score,
            "positive_indicators": positive_count,
            "negative_indicators": negative_count,
            "confidence": min(abs(sentiment_score) * 10, 1.0)
        }


class RiskCalculatorTool:
    """Tool for risk assessment and calculation"""

    def __init__(self):
        self.name = "Risk Calculator"
        self.description = "Calculates various risk metrics and assessments"

    def calculate_var(self, returns: List[float], confidence_level: float = 0.95) -> Dict[str, float]:
        """Calculate Value at Risk (VaR)"""
        if not returns or len(returns) < 10:
            return {"error": "Insufficient return data for VaR calculation"}

        try:
            returns_sorted = sorted(returns)
            var_index = int((1 - confidence_level) * len(returns_sorted))
            var_value = returns_sorted[var_index]

            return {
                "var_95": var_value,
                "confidence_level": confidence_level,
                "worst_case_scenario": min(returns_sorted),
                "best_case_scenario": max(returns_sorted),
                "average_return": sum(returns) / len(returns)
            }
        except Exception as e:
            return {"error": f"VaR calculation error: {str(e)}"}

    def assess_portfolio_risk(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall investment risk"""
        risk_assessment = {
            "overall_risk": "Medium",
            "risk_factors": [],
            "risk_score": 5.0,  # 1-10 scale
            "recommendations": []
        }

        try:
            # Analyze volatility
            volatility = stock_data.get("volatility", 0)
            if volatility > 0.3:
                risk_assessment["risk_factors"].append("High volatility")
                risk_assessment["risk_score"] += 1

            # Analyze beta
            beta = stock_data.get("beta", 1.0)
            if beta > 1.5:
                risk_assessment["risk_factors"].append(
                    "High market sensitivity")
                risk_assessment["risk_score"] += 1
            elif beta < 0.5:
                risk_assessment["risk_factors"].append(
                    "Low market correlation")

            # Analyze debt levels
            debt_to_equity = stock_data.get("debt_to_equity", 0)
            if debt_to_equity > 100:
                risk_assessment["risk_factors"].append("High debt levels")
                risk_assessment["risk_score"] += 1

            # Determine overall risk level
            if risk_assessment["risk_score"] <= 3:
                risk_assessment["overall_risk"] = "Low"
            elif risk_assessment["risk_score"] <= 6:
                risk_assessment["overall_risk"] = "Medium"
            else:
                risk_assessment["overall_risk"] = "High"

            # Add recommendations
            if risk_assessment["overall_risk"] == "High":
                risk_assessment["recommendations"].append(
                    "Consider position sizing carefully")
                risk_assessment["recommendations"].append(
                    "Implement stop-loss strategies")

        except Exception as e:
            risk_assessment["error"] = f"Risk assessment error: {str(e)}"

        return risk_assessment

# Factory function to create all tools


def create_stock_analysis_tools():
    """Create and return all stock analysis tools"""
    return {
        "stock_data": StockDataTool(),
        "financial_calculator": FinancialCalculatorTool(),
        "news_analyzer": NewsAnalysisTool(),
        "risk_calculator": RiskCalculatorTool()
    }
