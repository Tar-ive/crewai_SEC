from crewai import Crew
from textwrap import dedent
from langchain_openai import ChatOpenAI
from stock_analysis_agents import StockAnalysisAgents
from stock_analysis_tasks import StockAnalysisTasks
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os 
from langchain_groq import ChatGroq
from logger import log_crew_response


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

llm1 = ChatOpenAI(model='gpt-3.5-turbo-0125', openai_api_key=api_key, temperature = 0.4)
llm2 = ChatGroq(groq_api_key=groq_api_key, model='llama3-70b-8192')
llm3 = ChatGroq(groq_api_key=groq_api_key, model='mixtral-8x7b-32768')


class FinancialCrew:
  def __init__(self, company):
    self.company = company
    self.llm1 = llm1
    #self.llm2 = llm2
    #self.llm3 = llm3


  def run(self):
    agents = StockAnalysisAgents(self.llm1)
    tasks = StockAnalysisTasks()

    research_analyst_agent = agents.research_analyst()
    financial_analyst_agent = agents.financial_analyst()
    investment_advisor_agent = agents.investment_advisor()
    chart_creator_agent = agents.chart_creator()
    markdown_writer_agent = agents.markdown_writer()
    interactive_analyst_agent = agents.interactive_analyst()

    research_task = tasks.research(research_analyst_agent, self.company)
    interactive_analysis_task = tasks.interactive_analysis(interactive_analyst_agent)
    financial_task = tasks.financial_analysis(financial_analyst_agent)
    filings_task = tasks.filings_analysis(financial_analyst_agent)
    recommend_task = tasks.recommend(investment_advisor_agent)
    chart_task = tasks.create_charts(chart_creator_agent)
    report_task = tasks.create_markdown_report(markdown_writer_agent)
    

    crew = Crew(
      agents=[
        interactive_analyst_agent,
        research_analyst_agent,
        financial_analyst_agent,
        investment_advisor_agent,
        chart_creator_agent,
        markdown_writer_agent
       
      ],
      tasks=[
        interactive_analysis_task,
        research_task,
        financial_task,
        filings_task,
        recommend_task, 
        chart_task,
        report_task
        
      ],
      verbose=True
    )

    result = crew.kickoff()
    log_crew_response(self.company, result)
    return result

if __name__ == "__main__":
  print("## Welcome to Financial Analysis Crew")
  print('-------------------------------')
  company = input(
    dedent("""
      What is the company you want to analyze?
    """))
  
  financial_crew = FinancialCrew(company)
  result = financial_crew.run()
  print("\n\n########################")
  print("## Here is the Report")
  print("########################\n")
  print(result)
