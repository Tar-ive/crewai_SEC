import yfinance as yf
import pandas as pd
from langchain_core.tools import tool
from datetime import datetime, timedelta

class AnalysisTools:
    @tool
    def get_stock_info(symbol: str, key: str) -> str:
        """
        'Return the correct stock info value given the appropriate symbol and key. Infer valid key from the user prompt; it must be one of the following:
    address1, city, state, zip, country, phone, website, industry, industryKey, industryDisp, sector, sectorKey, sectorDisp, longBusinessSummary, fullTimeEmployees, 
    companyOfficers, auditRisk, boardRisk, compensationRisk, shareHolderRightsRisk, overallRisk, governanceEpochDate, compensationAsOfEpochDate, maxAge, priceHint, previousClose, open,
    dayLow, dayHigh, regularMarketPreviousClose, regularMarketOpen, regularMarketDayLow, regularMarketDayHigh, dividendRate, dividendYield, exDividendDate, beta, trailingPE, forwardPE,
    volume, regularMarketVolume, averageVolume, averageVolume10days, averageDailyVolume10Day, bid, ask, bidSize, askSize, marketCap, fiftyTwoWeekLow, fiftyTwoWeekHigh, priceToSalesTrailing12Months,
    fiftyDayAverage, twoHundredDayAverage, currency, enterpriseValue, profitMargins, floatShares, sharesOutstanding, sharesShort, sharesShortPriorMonth, sharesShortPreviousMonthDate, dateShortInterest,
    sharesPercentSharesOut, heldPercentInsiders, heldPercentInstitutions, shortRatio, shortPercentOfFloat, impliedSharesOutstanding, bookValue, priceToBook, lastFiscalYearEnd, nextFiscalYearEnd, mostRecentQuarter,
    earningsQuarterlyGrowth, netIncomeToCommon, trailingEps, forwardEps, pegRatio, enterpriseToRevenue, enterpriseToEbitda, 52WeekChange, SandP52WeekChange, lastDividendValue, lastDividendDate, exchange, quoteType, symbol, 
    underlyingSymbol, shortName, longName, firstTradeDateEpochUtc, timeZoneFullName, timeZoneShortName, uuid, messageBoardId, gmtOffSetMilliseconds, currentPrice, targetHighPrice, targetLowPrice, targetMeanPrice, targetMedianPrice, recommendationMean,
    recommendationKey, numberOfAnalystOpinions, totalCash, totalCashPerShare, ebitda, totalDebt, quickRatio, currentRatio, totalRevenue, debtToEquity, revenuePerShare, returnOnAssets, returnOnEquity, freeCashflow, operatingCashflow, earningsGrowth, revenueGrowth, grossMargins,
    ebitdaMargins, operatingMargins, financialCurrency, trailingPegRatio
        """
        try:
            data = yf.Ticker(symbol)
            stock_info = data.info
            
            if key in stock_info:
                return str(stock_info[key])
            else:
                return f"Key '{key}' not found in stock info for {symbol}."
        except Exception as e:
            return f"Error fetching stock info: {str(e)}"

    @tool
    def get_historical_price(symbol: str, start_date: str = None, end_date: str = None) -> str:
        """
        Fetches historical stock prices for a given symbol from 'start_date' to 'end_date'.
    - symbol (str): Stock ticker symbol.
    - end_date (date): Typically today unless a specific end date is provided. End date MUST be greater than start date
    - start_date (date): Set explicitly, or calculated as 'end_date - date interval' (for example, if prompted 'over the past 6 months',
      date interval = 6 months so start_date would be 6 months earlier than today's date).
      Default to '1900-01-01' if vaguely asked for historical price. Start date must always be before the current date
        """
        try:
            end = datetime.now() if end_date is None else datetime.strptime(end_date, '%Y-%m-%d')
            start = end - timedelta(days=180) if start_date is None else datetime.strptime(start_date, '%Y-%m-%d')
            
            data = yf.Ticker(symbol)
            hist = data.history(start=start, end=end)
            
            if hist.empty:
                return f"No historical data found for {symbol} in the specified date range."
            
            hist = hist.reset_index()
            hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
            hist_dict = hist[['Date', 'Close']].to_dict(orient='records')
            
            return pd.DataFrame(hist_dict).to_json(orient='records')
        except Exception as e:
            return f"Error fetching historical price data: {str(e)}"

    @tool
    def get_company_info(symbol: str) -> str:
        """
        Fetches basic company information for a given stock symbol.
        
        Args:
        symbol (str): Stock ticker symbol.
        
        Returns:
        str: A string containing basic company information.
        """
        try:
            data = yf.Ticker(symbol)
            info = data.info
            
            company_info = {
                "Name": info.get('longName', 'N/A'),
                "Sector": info.get('sector', 'N/A'),
                "Industry": info.get('industry', 'N/A'),
                "Country": info.get('country', 'N/A'),
                "Website": info.get('website', 'N/A'),
                "Summary": info.get('longBusinessSummary', 'N/A')
            }
            
            return "\n".join([f"{k}: {v}" for k, v in company_info.items()])
        except Exception as e:
            return f"Error fetching company info: {str(e)}"

    @tool
    def get_financial_ratios(symbol: str) -> str:
        """
        Fetches key financial ratios for a given stock symbol.
        
        Args:
        symbol (str): Stock ticker symbol.
        
        Returns:
        str: A string containing key financial ratios.
        """
        try:
            data = yf.Ticker(symbol)
            info = data.info
            
            ratios = {
                "P/E Ratio": info.get('trailingPE', 'N/A'),
                "Forward P/E": info.get('forwardPE', 'N/A'),
                "PEG Ratio": info.get('pegRatio', 'N/A'),
                "Price/Book": info.get('priceToBook', 'N/A'),
                "Dividend Yield": info.get('dividendYield', 'N/A'),
                "Return on Equity": info.get('returnOnEquity', 'N/A'),
                "Debt to Equity": info.get('debtToEquity', 'N/A')
            }
            
            return "\n".join([f"{k}: {v}" for k, v in ratios.items()])
        except Exception as e:
            return f"Error fetching financial ratios: {str(e)}"