import streamlit as st 
import os
from main import FinancialCrew
import time

def run_analysis(company):
    financial_crew = FinancialCrew(company)
    result = financial_crew.run()
    return result

def read_markdown_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

st.title('Stock Analysis App')

company = st.text_input('Enter the company name you want to analyze:')

if st.button('Run Analysis'):
    if company:
        with st.spinner(f'Analyzing {company}... This may take a few minutes.'):
            result = run_analysis(company)
            st.success('Analysis complete!')
            
        st.subheader('Analysis Summary')
        st.write(result)
        
        if os.path.exists('report.md'):
            st.subheader('Detailed Report')
            report_content = read_markdown_file('report.md')
            st.markdown(report_content)
            
            # Display images
            image_files = [f for f in os.listdir('.') if f.endswith('_chart.png')]
            for image_file in image_files:
                st.image(image_file, caption=image_file, use_column_width=True)
        else:
            st.warning('Detailed report not found. The agents might not have generated a markdown report.')
    else:
        st.warning('Please enter a company name.')

st.sidebar.header('About')
st.sidebar.info('This app uses AI agents to analyze stocks based on the company name you provide. It generates a detailed report including financial analysis, charts, and investment recommendations.')