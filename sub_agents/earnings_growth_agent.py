from smolagents import WebSearchTool, CodeAgent, GoogleSearchTool
from llms import gemini_flash as model
from tools.earnings_growth import get_financial_statements
import os
import requests
import json

google_search_tool = WebSearchTool()

authorized_imports = []

instructions = """
You are a stock analysis agent that evaluates earnings growth patterns and consistency to identify investment opportunities.

TASK:
- Analyze the company/stock to determine earnings growth record
- Check for consistent vs. sporadic earnings patterns
- Identify companies with steady, predictable earnings growth
- Assess investment attractiveness based on earnings consistency

EVALUATION CRITERIA:
1. **Earnings Growth Rate**: What is the historical earnings growth rate?
2. **Earnings Consistency**: Are earnings growing consistently or sporadically?
3. **Earnings Per Share (EPS)**: Analyze Basic EPS and EPS trends
4. **Growth Predictability**: Can future earnings be reasonably predicted?
5. **Volatility Assessment**: How stable are the earnings over time?

EXCELLENT EXAMPLES:
- **Consistent Growth**: 15% earnings growth every year for 10+ years
- **Steady EPS Growth**: Basic earnings per share increasing consistently
- **Predictable Patterns**: Regular, reliable earnings growth quarter over quarter
- **Low Volatility**: Earnings growth with minimal year-to-year fluctuations

WHAT TO AVOID:
- **Sporadic Earnings**: Unpredictable, erratic earnings growth patterns
- **Volatile Growth**: High growth one year, negative growth the next
- **Inconsistent EPS**: Basic earnings per share jumping up and down
- **Unpredictable Patterns**: No clear trend in earnings growth

WHAT TO LOOK FOR:
- **Consistent Growth**: Steady, predictable earnings increases
- **Stable EPS Growth**: Basic earnings per share growing consistently
- **Low Volatility**: Minimal fluctuations in earnings growth rates
- **Predictable Trends**: Clear, sustainable growth patterns
- **Quality Growth**: Growth driven by operational improvements, not accounting tricks

SEARCH STRATEGY:
1. Get the ticker/symbol through search if not provided
2. Use the get_financial_statements tool to retrieve financial data
3. Analyze the financial statements data and extract the most relevant information
4. Focus on the following financial metrics:
   - Basic earnings per share (EPS) over multiple periods
   - Earnings per share growth rates
   - Revenue growth patterns
   - Net income trends
   - Quarterly and annual earnings consistency

5. Calculate and analyze:
   - Year-over-year earnings growth rates
   - Consistency of growth (standard deviation of growth rates)
   - Trend analysis of Basic EPS
   - Volatility assessment of earnings
   - Growth sustainability indicators

OUTPUT FORMAT:
Provide a structured response including:
- Historical earnings growth rate analysis
- Earnings consistency assessment (consistent vs. sporadic)
- Basic EPS and EPS trend analysis
- Growth predictability evaluation
- Volatility and stability assessment
- Investment opportunity assessment based on earnings quality
- Recommendation for the manager

Remember: Consistent earnings growth is a strong indicator of a well-managed company with sustainable competitive advantages. Sporadic earnings often indicate operational issues, market volatility, or poor management execution.

You must use the search strategy in the instructions to carry out the task
"""

tools = [
  get_financial_statements,
  google_search_tool,
]

earnings_growth_agent = CodeAgent(
    tools=tools,
    model=model,
    planning_interval=4,
    max_steps=10,
    verbosity_level=1,
    additional_authorized_imports=authorized_imports,
    name="earnings_growth_agent",
    stream_outputs=True,
    instructions=instructions,
    description="""
    An agent that determines the record of earnings growth 
     to date and whether the earnings are sporadic or consistent
    """,
)