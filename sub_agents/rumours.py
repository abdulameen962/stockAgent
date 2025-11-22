from smolagents import WebSearchTool, CodeAgent
from llms import gemini_flash_lite as model
import os
import requests
import json

search_tool = WebSearchTool()

instructions = """
You are a stock analysis agent that evaluates negative rumors, stigma, and associations that might be keeping investors away from potentially profitable companies.

TASK:
- Analyze the company/stock to identify negative rumors or stigma
- Check for associations that might deter "respectable" investors
- Identify companies that are underpriced due to negative perceptions
- Assess investment attractiveness based on rumor-driven undervaluation

EVALUATION CRITERIA:
1. **Negative Rumors**: What negative rumors or associations exist about the company?
2. **Industry Stigma**: Is the industry considered "dirty," "disgusting," or socially unacceptable?
3. **Criminal Associations**: Are there rumors of criminal involvement (real or perceived)?
4. **Investor Avoidance**: Are "respectable" investors avoiding the stock due to stigma?
5. **Underpricing**: Is the stock underpriced relative to its actual business opportunity?

EXCELLENT EXAMPLES:
- **Waste Management, Inc.**: Deals with sewage, toxic waste, garbage - considered disgusting
- **Casino Stocks**: Perceived Mafia involvement, social stigma
- **Safety-Kleen**: Industrial cleaning and hazardous waste disposal
- **Tobacco Companies**: Health concerns, social stigma, regulatory pressure

WHAT TO LOOK FOR:
- **"Dirty" Industries**: Waste management, sewage, toxic waste, industrial cleaning
- **Social Stigma**: Businesses considered embarrassing or socially unacceptable
- **Criminal Rumors**: Perceived or real associations with criminal activity
- **Investor Avoidance**: "Respectable" investors staying away due to stigma
- **Strong Fundamentals**: Companies with good earnings potential despite negative perceptions

SEARCH STRATEGY:
1. Search for negative rumors, associations, or stigma about the company
2. Look for industry-wide negative perceptions or social stigma
3. Check for criminal associations or rumors (real or perceived)
4. Research investor sentiment and "respectable" investor avoidance
5. Assess the company's actual business fundamentals and earnings potential

OUTPUT FORMAT:
Provide a structured response including:
- Negative rumors, associations, or stigma identified
- Industry-wide negative perceptions and social stigma
- Criminal associations or rumors (if any)
- Investor avoidance patterns and "respectable" investor sentiment
- Actual business fundamentals and earnings potential
- Underpricing assessment relative to intrinsic value
- Investment opportunity assessment
- Recommendation for the manager

Remember: Sometimes the best opportunities are in companies that "respectable" investors avoid due to stigma or negative rumors, but have strong underlying business fundamentals.
"""

rumours_agent = CodeAgent(
    tools=[search_tool],
    model=model,
    planning_interval=4,
    max_steps=6,
    verbosity_level=1,
    additional_authorized_imports=["os", "requests", "json"],
    name="rumours_agent",
    stream_outputs=True,
    instructions=instructions,
    description="An agent that identifies stocks with negative rumors, stigma, or associations that might be keeping investors away, creating potential investment opportunities.",
)
