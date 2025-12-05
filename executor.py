"""
Tool Execution Engine
Handles safe and efficient tool execution with error handling
"""

from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToolExecutor:
    """
    Executes tools with retry logic, error handling, and logging.
    """
    
    def __init__(self, max_retries: int = 3):
        """
        Initialize the executor.
        
        Args:
            max_retries: Maximum number of retry attempts
        """
        self.max_retries = max_retries
        self.execution_history = []
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def execute_with_retry(
        self,
        tool_func: callable,
        parameters: Dict[str, Any]
    ) -> Any:
        """
        Execute a tool with automatic retry on failure.
        
        Args:
            tool_func: Tool function to execute
            parameters: Parameters for the tool
            
        Returns:
            Result from tool execution
        """
        logger.info(f"Executing tool: {tool_func.__name__}")
        logger.debug(f"Parameters: {parameters}")
        
        try:
            result = tool_func(**parameters)
            logger.info(f"Tool execution successful")
            
            # Record execution
            self._record_execution(
                tool_name=tool_func.__name__,
                parameters=parameters,
                result=result,
                success=True
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}")
            
            # Record failure
            self._record_execution(
                tool_name=tool_func.__name__,
                parameters=parameters,
                result=None,
                success=False,
                error=str(e)
            )
            
            raise
    
    def execute_safe(
        self,
        tool_func: callable,
        parameters: Dict[str, Any],
        default_value: Any = None
    ) -> Any:
        """
        Execute a tool safely, returning default value on failure.
        
        Args:
            tool_func: Tool function to execute
            parameters: Parameters for the tool
            default_value: Value to return on failure
            
        Returns:
            Result or default value
        """
        try:
            return self.execute_with_retry(tool_func, parameters)
        except Exception as e:
            logger.warning(f"Tool execution failed, returning default: {default_value}")
            return default_value
    
    def _record_execution(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        result: Any,
        success: bool,
        error: Optional[str] = None
    ):
        """Record tool execution in history."""
        from datetime import datetime
        
        record = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "parameters": parameters,
            "result": result,
            "success": success,
            "error": error
        }
        
        self.execution_history.append(record)
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """
        Get statistics about tool executions.
        
        Returns:
            Dictionary with execution statistics
        """
        total = len(self.execution_history)
        successful = sum(1 for r in self.execution_history if r["success"])
        failed = total - successful
        
        tool_counts = {}
        for record in self.execution_history:
            tool = record["tool"]
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        return {
            "total_executions": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0,
            "tool_usage": tool_counts
        }
    
    def clear_history(self):
        """Clear execution history."""
        self.execution_history = []


if __name__ == "__main__":
    # Test executor
    executor = ToolExecutor()
    
    def sample_tool(x: int, y: int) -> int:
        """Sample tool for testing."""
        return x + y
    
    result = executor.execute_with_retry(sample_tool, {"x": 5, "y": 3})
    print(f"Result: {result}")
    
    stats = executor.get_execution_stats()
    print(f"Stats: {stats}")
