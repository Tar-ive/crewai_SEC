from langchain.tools import tool
from typing import List
import random
import matplotlib.pyplot as plt
from pydantic import BaseModel, Field

class CreateChartInput(BaseModel):
    metric_name: str = Field(..., description="The name of the metric to be visualized on the chart")
    data: List[float] = Field(..., description="A list of numerical data points representing the metric over time")

class CreateChartOutput(BaseModel):
    file_path: str = Field(..., description="The file path to the saved chart image")

class ChartingTools:
    @tool("Create a chart of the data")
    def create_chart(metric_name: str, data: List[float]) -> str:
        """
        Creates a bar chart graphic based on the provided metric and data.

        Parameters:
        - metric_name (str): The name of the metric to be visualized on the chart.
        - data (List[float]): A list of numerical data points representing the metric over time.

        Returns:
        - str: The file path to the saved chart image.

        Example:
        - create_chart(metric_name='revenue', data=[100, 150, 120, 200, 180])
        - Returns: './revenue_chart.png'
        """
        years = list(range(len(data)))
        
        # Generate a random color for all bars
        bar_color = f'#{random.randint(0, 0xFFFFFF):06x}'
        
        fig, ax = plt.subplots()
        ax.bar(years, data, color=bar_color)
        ax.set_xlabel('Years')
        ax.set_ylabel(metric_name)
        ax.set_title(f'{metric_name} Over Time')
        
        # Save the figure to the current directory
        file_path = f"./{metric_name.replace(' ', '_')}_chart.png"
        fig.savefig(file_path, format='png')
        plt.close(fig)  # Close the Matplotlib figure to free resources
        
        return file_path

class MarkdownTools:
    @tool("Write text to markdown file")
    def write_text_to_markdown_file(text: str) -> str:
        """
        Writes markdown text to a file.

        The input to this tool should be a string representing markdown syntax.
        It creates or overwrites a file named 'report.md' with the provided content.

        Parameters:
        - text (str): The markdown content to write to the file.

        Returns:
        - str: A confirmation message or an error message.

        Example:
        - write_text_to_markdown_file("# Report\n\n![](fcf_chart.png)")
        - Returns: "File written to report.md."
        """
        try:
            markdown_file_path = 'report.md'
            
            if not isinstance(text, str):
                return f"Error: Input must be a string, not {type(text)}. Please provide the markdown content as a string."
            
            with open(markdown_file_path, 'w') as file:
                file.write(text)
            
            return f"File written to {markdown_file_path}."
        except Exception as e:
            return f"An error occurred while writing to the markdown file: {str(e)}"