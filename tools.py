"""
Tool Registry and Implementations
Defines all tools available to the agent
"""

import requests
import json
import math
from typing import Dict, Any, List, Callable
from datetime import datetime


class ToolRegistry:
    """Registry of all available tools for the agent."""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {
            "calculator": self.calculator,
            "web_search": self.web_search,
            "file_read": self.file_read,
            "file_write": self.file_write,
            "get_current_time": self.get_current_time,
            "weather": self.weather,
            "code_executor": self.code_executor,
        }
    
    def get_all_tools(self) -> List[str]:
        """Get list of all available tool names."""
        return list(self.tools.keys())
    
    def get_tool_descriptions(self) -> Dict[str, Dict[str, Any]]:
        """Get descriptions of all tools."""
        return {
            "calculator": {
                "description": "Perform mathematical calculations",
                "parameters": {
                    "expression": "Mathematical expression to evaluate (e.g., '2 + 2', '15 * 23')"
                }
            },
            "web_search": {
                "description": "Search the web for information",
                "parameters": {
                    "query": "Search query string"
                }
            },
            "file_read": {
                "description": "Read contents of a file",
                "parameters": {
                    "filepath": "Path to the file to read"
                }
            },
            "file_write": {
                "description": "Write content to a file",
                "parameters": {
                    "filepath": "Path to the file to write",
                    "content": "Content to write to the file"
                }
            },
            "get_current_time": {
                "description": "Get the current date and time",
                "parameters": {}
            },
            "weather": {
                "description": "Get current weather for a location",
                "parameters": {
                    "location": "City name or location"
                }
            },
            "code_executor": {
                "description": "Execute Python code safely",
                "parameters": {
                    "code": "Python code to execute"
                }
            }
        }
    
    def execute(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """
        Execute a tool with given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters to pass to the tool
            
        Returns:
            Result from tool execution
        """
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"
        
        try:
            return self.tools[tool_name](**parameters)
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    # Tool Implementations
    
    def calculator(self, expression: str) -> str:
        """
        Evaluate a mathematical expression.
        
        Args:
            expression: Math expression to evaluate
            
        Returns:
            Result of the calculation
        """
        try:
            # Safe evaluation of mathematical expressions
            allowed_names = {
                'abs': abs, 'round': round, 'min': min, 'max': max,
                'sum': sum, 'pow': pow, 'sqrt': math.sqrt,
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'pi': math.pi, 'e': math.e
            }
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    def web_search(self, query: str) -> str:
        """
        Search the web (simulated - would use real API in production).
        
        Args:
            query: Search query
            
        Returns:
            Search results
        """
        # In production, this would use SerpAPI or similar
        # For demo, returning simulated results
        return f"Search results for '{query}': [Simulated results - integrate with SerpAPI for real searches]"
    
    def file_read(self, filepath: str) -> str:
        """
        Read contents of a file.
        
        Args:
            filepath: Path to file
            
        Returns:
            File contents
        """
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            return f"File content:\n{content}"
        except FileNotFoundError:
            return f"Error: File '{filepath}' not found"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def file_write(self, filepath: str, content: str) -> str:
        """
        Write content to a file.
        
        Args:
            filepath: Path to file
            content: Content to write
            
        Returns:
            Success message
        """
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            return f"Successfully wrote to {filepath}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    def get_current_time(self) -> str:
        """
        Get current date and time.
        
        Returns:
            Current datetime string
        """
        now = datetime.now()
        return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def weather(self, location: str) -> str:
        """
        Get weather for a location (simulated).
        
        Args:
            location: City or location name
            
        Returns:
            Weather information
        """
        # In production, integrate with OpenWeatherMap or similar API
        return f"Weather in {location}: [Simulated - integrate with weather API for real data]"
    
    def code_executor(self, code: str) -> str:
        """
        Execute Python code safely (restricted).
        
        Args:
            code: Python code to execute
            
        Returns:
            Execution result
        """
        try:
            # Very restricted execution environment
            allowed_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                }
            }
            
            # Capture output
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            exec(code, allowed_globals)
            
            sys.stdout = old_stdout
            output = buffer.getvalue()
            
            return f"Code executed successfully:\n{output}"
        except Exception as e:
            return f"Code execution error: {str(e)}"


if __name__ == "__main__":
    # Test tools
    registry = ToolRegistry()
    
    print("Testing calculator:")
    print(registry.execute("calculator", {"expression": "15 * 23 + 100"}))
    
    print("\nTesting current time:")
    print(registry.execute("get_current_time", {}))
