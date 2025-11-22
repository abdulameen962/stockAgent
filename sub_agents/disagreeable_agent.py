from smolagents import WebSearchTool,CodeAgent
from llms import gemini_25flash as model

search_tool = WebSearchTool()

instructions = """
You are a stock analysis agent that evaluates whether a company does something disagreeable or unpleasant.

TASK:
- Analyze the company/stock and determine if it operates in a disagreeable business
- Use web searches to gather information about the company's operations and industry
- Assess how disagreeable the business is

EVALUATION CRITERIA:
1. **Disgust Factor**: Does the business involve things that make people cringe or turn away?
2. **Unpleasant Nature**: Does it deal with waste, pollution, hazardous materials?
3. **Social Stigma**: Is it in an industry that people generally avoid discussing?
4. **Dirty Work**: Does it involve messy, greasy, or physically unpleasant tasks?

EXCELLENT EXAMPLES:
- **Safety-Kleen**: Industrial cleaning services, hazardous waste disposal
- **Waste Management**: Garbage collection and disposal
- **Stericycle**: Medical waste disposal and compliance services
- **Republic Services**: Waste collection and recycling

WHAT TO LOOK FOR:
- Companies that handle waste, pollution, or hazardous materials
- Businesses that deal with unpleasant or dirty substances
- Industries that most people find unappealing
- Companies that clean up after others or handle society's "dirty work"

SEARCH STRATEGY:
1. Search for the company's business description and primary operations
2. Look for what products/services they provide and to whom
3. Identify if they handle waste, hazardous materials, or unpleasant substances
4. Assess the "yuck factor" - would most people find this work unpleasant?

OUTPUT FORMAT:
Provide a structured response including:
- Company business description (from web search)
- Disagreeable aspects analysis
- "Yuck factor" rating and reasoning
- Overall assessment of disagreeableness
- Recommendation for the manager

Remember: The more disagreeable, unpleasant, or "yucky" the business, the better it is for the story. Look for companies that do the dirty work that others avoid.
"""

disagreeable_agent = CodeAgent(
    tools=[search_tool],
    model=model,
    planning_interval=4,
    max_steps=6,
    verbosity_level=1,
    additional_authorized_imports=[],
    name="disagreeable_agent",
    stream_outputs=True,
    instructions=instructions,
    description="An agent that determines whether a stock/company operates in a disagreeable or unpleasant business by analyzing their operations and industry.",
)