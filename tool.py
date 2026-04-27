from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_classic.agents import initialize_agent, AgentType
import pandas as pd
import io

model = ChatOllama(model="mistral")


@tool
def analytics_tool(file_path: str) -> str:
    """
    Analyze CSV or Excel file using file path.
    Example:
    C:/Users/YourName/Desktop/data.csv
    """

    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)

        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)

        else:
            return "Only CSV and XLSX files are supported."

        buffer = io.StringIO()
        df.info(buf=buffer)
        df_info = buffer.getvalue()

        df_describe = df.describe().to_string()
        df_head = df.head().to_string()
        df_null = df.isnull().sum().to_string()

        return f"""
DataFrame Info:
{df_info}

DataFrame Describe:
{df_describe}

DataFrame Head:
{df_head}

Missing Values:
{df_null}
"""

    except Exception as e:
        return f"Error: {str(e)}"


agent = initialize_agent(
    tools=[analytics_tool],
    llm=model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)