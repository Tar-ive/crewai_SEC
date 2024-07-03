from crewai import Task
from textwrap import dedent

class StockAnalysisTasks():
  def research(self, agent, company):
    return Task(description=dedent(f"""
        Collect and summarize recent news articles, press
        releases, and market analyses related to the stock and
        its industry.
        Pay special attention to any significant events, market
        sentiments, and analysts' opinions. Also include upcoming 
        events like earnings and others.
  
        Your final answer MUST be a report that includes a
        comprehensive summary of the latest news, any notable
        shifts in market sentiment, and potential impacts on 
        the stock.
        Also make sure to return the stock ticker.
        
        {self.__tip_section()}
  
        Make sure to use the most recent data as possible.
  
        Selected company by the customer: {company}
      """),
      agent=agent
    )
    
  def financial_analysis(self, agent): 
    return Task(description=dedent(f"""
        Conduct a thorough analysis of the stock's financial
        health and market performance. 
        This includes examining key financial metrics such as
        P/E ratio, EPS growth, revenue trends, and 
        debt-to-equity ratio. 
        
        Also, analyze the stock's performance in comparison 
        to its industry peers and overall market trends.
                                   
        Try to answer these 5 questions: 
        1. Is the business behind the stock good?

        2. If its a good business, why is it good? What is its Moat? 

        3. Can it remain a good business in future too?

        4. Is it run by competent and honest people?
        4. Is it available at a fair price? 

        Your final report MUST expand on the summary provided
        but now including a clear assessment of the stock's
        financial standing, its strengths and weaknesses, 
        and how it fares against its competitors in the current
        market scenario.{self.__tip_section()}

        Make sure to use the most recent data possible.
      """),
      agent=agent
    )

  def filings_analysis(self, agent):
    return Task(description=dedent(f"""
        Analyze the latest 10-Q and 10-K filings from EDGAR for
        the stock in question. 
        Focus on key sections like Management's Discussion and
        Analysis, financial statements, insider trading activity, 
        and any disclosed risks.
        Extract relevant data and insights that could influence
        the stock's future performance.

        Your final answer must be an expanded report that now
        also highlights significant findings from these filings,
        including any red flags or positive indicators for
        your customer.
        {self.__tip_section()}        
      """),
      agent=agent
    )

  def recommend(self, agent):
    return Task(description=dedent(f"""
        Review and synthesize the analyses provided by the
        Financial Analyst and the Research Analyst.
        Combine these insights to form a comprehensive
        investment recommendation. 
        
        You MUST Consider all aspects, including financial
        health, market sentiment, and qualitative data from
        EDGAR filings.

        Make sure to include a section that shows insider 
        trading activity, and upcoming events like earnings.

        Your final answer MUST be a recommendation for your
        customer. It should be a full super detailed report, providing a 
        clear investment stance and strategy with supporting evidence.
        Make it pretty and well formatted for your customer.
        {self.__tip_section()}
      """),
      agent=agent
    )

  def __tip_section(self):
    return "If you do your BEST WORK, I'll give you a $10,000 commission!"
  
  def create_charts(self, agent):
    return Task(description=dedent(f"""
        Create charts for key financial metrics of the analyzed company.
        Use the ChartingTools to create visual representations of important data such as revenue, profit margins, and stock price trends.

        Your final answer MUST be a list of file paths to the created chart images.

        {self.__tip_section()}
      """),
      agent=agent
    )

  def create_markdown_report(self, agent):
    return Task(description=dedent(f"""
        Compile a comprehensive markdown report of the stock analysis.
        Use the MarkdownTools to write the report, including the charts created in the previous task.

        IMPORTANT: Ensure that you pass a single string containing all the markdown content to the write_text_to_markdown_file tool.
        DO NOT pass a dictionary or any other data type.

        Your markdown string should include:
        1. A title for the report
        2. Sections for each analysis (revenue, profit margins, stock price trends)
        3. Markdown syntax to embed the charts (e.g., ![](chart_name.png))
        4. A summary of the key findings

        Your final answer MUST be a confirmation that the report has been created,
        along with a summary of the key points included in the report.

        {self.__tip_section()}
      """),
      agent=agent, 
      human_input=True
    )
  
  def interactive_analysis(self, agent):
        return Task(description=dedent(f"""
            Engage in an interactive session with the user, answering specific questions about the analyzed stock or any other stock-related queries.
            Use the provided tools to fetch real-time data and provide accurate, up-to-date information.

            Your responses should be:
            1. Accurate and based on the most recent data available
            2. Concise yet informative
            3. Tailored to the user's specific question

            If asked to provide historical data or comparisons, use the appropriate tools to fetch and visualize this information.

            Your final answer for each query should directly address the user's question and provide any relevant context or insights. It should have the answer to these headings "P/E Ratio": 
                "Forward P/E": 
                "PEG Ratio": 
                "Price/Book": 
                "Dividend Yield": 
                "Return on Equity": 
                "Debt to Equity"

            {self.__tip_section()}
        """),
        agent=agent
    )


                