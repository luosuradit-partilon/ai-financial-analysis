from mcp.server.fastmcp import FastMCP
from app.finance_crew import run_financial_analysis
import io
import sys
from contextlib import redirect_stdout

# create FastMCP instance
mcp = FastMCP("financial-analyst")

# In-memory storage for generated code
_code_storage = {"current_code": None}

@mcp.tool()
def analyze_stock(query: str) -> str:
    """
    Analyzes stock market data based on the query and generates executable Python code for analysis and visualization.
    Returns a formatted Python script ready for execution.
    
    The query is a string that must contain the stock symbol (e.g., TSLA, AAPL, NVDA, etc.), 
    timeframe (e.g., 1d, 1mo, 1y), and action to perform (e.g., plot, analyze, compare).

    Example queries:
    - "Show me Tesla's stock performance over the last 3 months"
    - "Compare Apple and Microsoft stocks for the past year"
    - "Analyze the trading volume of Amazon stock for the last month"

    Args:
        query (str): The query to analyze the stock market data.
    
    Returns:
        str: A nicely formatted python code as a string.
    """
    try:
        result = run_financial_analysis(query)
        # Automatically store the generated code
        _code_storage["current_code"] = result
        return result
    except Exception as e:
        return f"Error: {e}"
    

@mcp.tool()
def save_code(code: str) -> str:
    """
    Expects a nicely formatted, working and executable python code as input in form of a string. 
    Save the given code to a file stock_analysis.py, make sure the code is a valid python file, nicely formatted and ready to execute.

    Args:
        code (str): The nicely formatted, working and executable python code as string.
    
    Returns:
        str: A message indicating the code was saved successfully.
    """
    try:
        _code_storage["current_code"] = code
        return f"Code saved successfully in memory. Code length: {len(code)} characters."
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def run_code_and_show_plot() -> str:
    """
    Run the previously saved code from memory and generate the plot.
    Returns the output or any errors from execution.
    """
    try:
        if not _code_storage["current_code"]:
            return "Error: No code has been saved yet. Please use analyze_stock or save_code first."
        
        # Capture stdout
        output_buffer = io.StringIO()
        
        # Execute the code
        with redirect_stdout(output_buffer):
            exec(_code_storage["current_code"], {"__name__": "__main__"})
        
        output = output_buffer.getvalue()
        
        if output:
            return f"Code executed successfully. Output:\n{output}"
        else:
            return "Code executed successfully (no output generated)"
            
    except Exception as e:
        return f"Error executing code: {str(e)}"

@mcp.tool()
def get_saved_code() -> str:
    """
    Retrieve the currently saved code from memory.
    
    Returns:
        str: The saved code or a message if no code is saved.
    """
    if _code_storage["current_code"]:
        return _code_storage["current_code"]
    else:
        return "No code currently saved in memory."

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()