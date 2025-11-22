from smolagents import (CodeAgent
                        ,GradioUI)
from llms import (gemini_25flash_lite as model)
from sub_agents import (name_agent,disagreeable_agent,
    spinoff_agent,institutions_agent,rumours_agent,depressing_agent,
    no_growth_agent,niche_agent,recurring_agent,technology_user_agent,
    insider_buying_agent,share_buyback_agent,financial_metrics_agent,
    stock_category_agent,pe_ratio_agent,earnings_growth_agent,
    balance_sheet_agent,cash_position_agent)
from tools.get_company_info import get_company_info

extra = """

"""

instructions = """
    You are a helpful stock analysis agent with the goal of providing the story of a stock or asset
    and determine if it should be bought

    For every stock or asset passed in a prompt,you are to go through the following criteria for each

    The initial step is to get general company info of the company,you are to use the get_company_info tool 
    to do this and pass it to managed agents

    1. The insiders are buyers
    2. The company is buying back shares
    3. Determine if the name of the stock sounds dull - or even better,ridiculous
    4. Determine whether the company attached to the stock does something dull
    5. Determine whether the company does something disagreeable
    6. Determine if the stock is a spinoff
    7. Determine if the institutions own it and if analysts follow it
    8. The rumours around,its involved with toxic waste and/or the mafia
    9. There is something depressing about it
    10. It's a no-growth industry
    11. It's got a niche
    12 If people have to keep buying the products the company makes
    13 Its a user of technology
    14 The p/e ratio,is it high or low for this particular company and 
    for similar companies in the same industry
    15 The record of earnings growth to date and whether the earnings are sporadic or consistent
    16 Whether the company has a strong balance sheet or a weak balance sheet(debt to equity ratio)
    17 The cash position of the company
    18 Determine what category/type of stock whether it is a slow grower,stalwart,fast grower,
    cyclical,turnaround,asset play or a new issue

    You are to distribute this to the managed agents in the order of the criteria above,and then give the story based on this and
    decide if the stock should be bought or not

    You must go through only all the criteria above and then give a final summary of the stock
    and whether it should be bought or not

    You must use the specialized agents for every criteria
    
    You must always go through the steps and after completion go through the'
    requirements
    to confirm if everything has been fulfilled before giving a final answer
"""

managed_agents = [name_agent,pe_ratio_agent,disagreeable_agent,
    spinoff_agent,institutions_agent,rumours_agent,depressing_agent,
    no_growth_agent,niche_agent,recurring_agent,technology_user_agent,
    insider_buying_agent,share_buyback_agent,financial_metrics_agent,
    stock_category_agent,earnings_growth_agent,balance_sheet_agent,cash_position_agent]

master_agent = CodeAgent(
    managed_agents=managed_agents,
    model=model,
    planning_interval=8,  # Activate planning
    max_steps=25,
    tools=[get_company_info],
    name="stock_ai_agent",
    provide_run_summary =True,
    instructions=instructions,
    stream_outputs=True,
    description="A stock agent that gets the story of a stock and determine category of stock"
)


def main():
    GradioUI(master_agent).launch()


if __name__ == "__main__":
    main()

# kindly get the story of
# 1. NIGERIAN AVIATION HANDLING COMPANY PLC ( NAHCO )
# 2. MUTUAL BENEFITS ASSURANCE PLC. ( MBENEFIT )
# 3. MULTIVERSE MINING AND EXPLORATION PLC ( MULTIVERSE )
# 4. HALDANE MCCALL PLC ( HMCALL ) 
# 5. LAFARGE AFRICA PLC. ( WAPCO )
# 6. EKOCORP PLC. ( EKOCORP ) 
# 7. DN TYRE & RUBBER PLC ( DUNLOP )
# 8. LIVESTOCK FEEDS PLC. ( LIVESTOCK ) 
# 9. HONEYWELL FLOUR MILL PLC ( HONYFLOUR )
# 10. FTN COCOA PROCESSORS PLC ( FTNCOCOA )
# 11. ROYAL EXCHANGE PLC. ( ROYALEX ) 
# 12. FIDSON HEALTHCARE PLC ( FIDSON )
# 13. BUA FOODS PLC ( BUAFOODS )
# 14. CADBURY NIGERIA PLC. ( CADBURY )
# 15. CHAMPION BREW. PLC. ( CHAMPION ) 
# 16. DANGOTE CEMENT PLC ( DANGCEM )
# 17. PRESCO PLC ( PRESCO ) 
# 18. ASSOCIATED BUS COMPANY PLC ( ABCTRANS )
# 19. U A C N PLC. ( UACN )