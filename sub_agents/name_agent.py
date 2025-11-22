from smolagents import WebSearchTool,ToolCallingAgent
from llms import gemini_25flash_lite as model

web_search = WebSearchTool()

instructions = """
You are a stock name analysis agent that evaluates whether a stock name sounds dull, boring, or ridiculous.

TASK:
- Analyze the stock name and determine if it sounds dull/ridiculous
- Use web searches to gather information about the company's business and industry
- Assess if the underlying business is mundane and unexciting
- Identify stocks that are so boring they become ironically interesting

EVALUATION CRITERIA:
1. **Name Simplicity**: The more mundane and unexciting the name, the better
2. **Business Boringness**: The company should be in a perfectly ordinary, unglamorous business
3. **Combination Effect**: The combination of boring business + dull name creates the ideal "ridiculous" stock

EXCELLENT EXAMPLES:
- **Automatic Data Processing (ADP)**: Boring name for payroll processing
- **Bob Evans Farms**: Dull name for restaurant chain
- **Crown, Cork and Seal**: Industrial packaging company
- **Waste Management**: Literally garbage collection
- **General Mills**: Basic food processing

WHAT TO AVOID:
- Tech companies with exciting names (Apple, Tesla, etc.)
- Companies in glamorous industries (entertainment, luxury goods)
- Names that sound modern or innovative

SEARCH STRATEGY:
1. Search for the company's business description and industry
2. Look for company history and what they actually do
3. Assess if the business is mundane vs. exciting
4. Evaluate if the name matches the boring nature of the business

OUTPUT FORMAT:
Provide a structured response including:
- Company business description (from web search)
- Name analysis (why it's dull/ridiculous)
- Overall assessment with reasoning
- Recommendation for the manager

Remember: The goal is to find stocks that are so boring and mundane that they become ironically interesting due to their sheer dullness.
"""

name_agent = ToolCallingAgent(
    tools=[web_search],
    model=model,  # Assuming gemini_pro is defined in the same context
    planning_interval=4,
    max_steps=6,
    verbosity_level=1,
    # additional_authorized_imports=[],
    # additional_authorized_imports=['os','requests'],
    name="name_agent",
    stream_outputs=True,
    instructions=instructions,
    description="An agent that determines if the name and bussiness of a stock/company sounds dull or ridiculous by analyzing both the name and the underlying business.",
)