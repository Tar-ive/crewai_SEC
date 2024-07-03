from crewai import Agent
from textwrap import dedent
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools
from tools.sec_tools import SECTools
from tools.charting_writing_tools import ChartingTools, MarkdownTools
from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain.chat_models import ChatOpenAI
import os 
from textwrap import dedent
from dotenv import load_dotenv
from langchain_groq import ChatGroq 
from tools.groq_yf import AnalysisTools

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

llm1 = ChatOpenAI(model='gpt-3.5-turbo-0125', openai_api_key=api_key, temperature = 0.4)
llm2 = ChatGroq(groq_api_key=groq_api_key, model='llama3-70b-8192')

class StockAnalysisAgents():
    def __init__(self, llm):
        self.llm = llm
        

    def financial_analyst(self):
        return Agent(
            role='The Best Financial Analyst',
            goal="""Impress all customers with your financial data 
            and market trends analysis""",
            backstory="""The most seasoned financial analyst with 
            lots of expertise in stock market analysis and investment
            strategies that is working for a super important customer.""",
            verbose=True,
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
                CalculatorTools.calculate,
                SECTools.search_10q,
                SECTools.search_10k,
                YahooFinanceNewsTool()
            ],
            llm=llm2
        )

    def research_analyst(self):
        return Agent(
            role='Staff Research Analyst',
            goal="""Being the best at gather, interpret data and amaze
            your customer with it""",
            backstory="""Known as the BEST research analyst, you're
            skilled in sifting through news, company announcements, 
            and market sentiments. Now you're working on a super 
            important customer""",
            verbose=True,
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
                SearchTools.search_news,
                YahooFinanceNewsTool(),
                SECTools.search_10q,
                SECTools.search_10k
            ],
            llm=llm2
        )

    def investment_advisor(self):
        return Agent(
            role='Private Investment Advisor',
            goal="""Impress your customers with full analyses over stocks
            and complete investment recommendations""",
            backstory="""You're the most experienced investment advisor
            and you combine various analytical insights to formulate
            strategic investment advice. You are now working for
            a super important customer you need to impress.""",
            verbose=True,
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
                SearchTools.search_news,
                CalculatorTools.calculate,
                YahooFinanceNewsTool()
            ],
            llm=llm2
        )

    def chart_creator(self):
        return Agent(
            role="Chart Creator",
            goal=dedent(f"""Create a chart of the data provided using the tool."""),
            backstory=dedent(f"""Expert in creating charts. You are known for receiving a list of data points and meticulously creating an accurate chart. You must use the tool provided."""),
            tools=[ChartingTools.create_chart],
            verbose=True,
            llm=llm2,
        )
    
    def markdown_writer(self):
        return Agent(
            role="Data Report Creator",
            goal=dedent(f"""Use *.png files in same directory to add the correct syntax a markdown file."""),
            backstory=dedent(f"""Expert in writing text inside a markdown file. You take a text input and write the contents to a markdown file in the same directory. You always add a new line after inserting into the markdown file. **YOU USE MARKDOWN SYNTAX AT ALL TIMES NO MATTER WHAT** YOU NEVER INSERT ANYTHING INTO THE report.md FILE THAT ISN'T MARKDOWN SYNTAX."""),
            tools=[MarkdownTools.write_text_to_markdown_file],
            verbose=True,
            llm=llm2,
        )
    

    def interactive_analyst(self):
        return Agent(
            role='Interactive Stock Analyst',
            goal="""Provide detailed, real-time answers to specific questions about stocks and financial data""",
            backstory="""You are an AI-powered stock analyst capable of accessing real-time financial data and providing instant insights. You use the Groq language model for fast and accurate responses.""",
            verbose=True,
            tools=[
                AnalysisTools.get_stock_info,
                AnalysisTools.get_historical_price,
            ],
            llm=llm2
        )
