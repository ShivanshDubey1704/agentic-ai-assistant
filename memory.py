"""
Memory System for the Agent
Maintains conversation history and learning
"""

from typing import List, Dict, Any
from datetime import datetime
import json


class Memory:
    """
    Memory system for the agent to maintain context and learn.
    """
    
    def __init__(self, max_history: int = 100):
        """
        Initialize memory system.
        
        Args:
            max_history: Maximum number of messages to keep
        """
        self.messages: List[Dict[str, Any]] = []
        self.tool_usage: List[Dict[str, Any]] = []
        self.max_history = max_history
    
    def add_message(self, role: str, content: str):
        """
        Add a message to conversation history.
        
        Args:
            role: Role (user/assistant/system)
            content: Message content
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        
        # Trim if exceeds max
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def add_tool_use(self, tool_name: str, input_params: Dict, result: Any):
        """
        Record tool usage.
        
        Args:
            tool_name: Name of tool used
            input_params: Parameters passed to tool
            result: Result from tool
        """
        tool_record = {
            "tool": tool_name,
            "input": input_params,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self.tool_usage.append(tool_record)
    
    def get_recent_history(self, n: int = 10) -> str:
        """
        Get recent conversation history.
        
        Args:
            n: Number of recent messages
            
        Returns:
            Formatted history string
        """
        recent = self.messages[-n:] if len(self.messages) > n else self.messages
        
        history_str = ""
        for msg in recent:
            history_str += f"{msg['role']}: {msg['content']}\n"
        
        return history_str
    
    def get_tools_used(self) -> List[str]:
        """
        Get list of tools used in this session.
        
        Returns:
            List of unique tool names
        """
        return list(set([record["tool"] for record in self.tool_usage]))
    
    def get_tool_usage_stats(self) -> Dict[str, int]:
        """
        Get statistics on tool usage.
        
        Returns:
            Dictionary of tool names to usage counts
        """
        stats = {}
        for record in self.tool_usage:
            tool = record["tool"]
            stats[tool] = stats.get(tool, 0) + 1
        return stats
    
    def clear(self):
        """Clear all memory."""
        self.messages = []
        self.tool_usage = []
    
    def save_to_file(self, filepath: str):
        """
        Save memory to a JSON file.
        
        Args:
            filepath: Path to save file
        """
        data = {
            "messages": self.messages,
            "tool_usage": self.tool_usage
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath: str):
        """
        Load memory from a JSON file.
        
        Args:
            filepath: Path to load file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.messages = data.get("messages", [])
        self.tool_usage = data.get("tool_usage", [])
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the memory state.
        
        Returns:
            Summary dictionary
        """
        return {
            "total_messages": len(self.messages),
            "total_tool_uses": len(self.tool_usage),
            "unique_tools_used": len(self.get_tools_used()),
            "tool_usage_stats": self.get_tool_usage_stats()
        }


if __name__ == "__main__":
    # Test memory
    memory = Memory()
    
    memory.add_message("user", "Hello!")
    memory.add_message("assistant", "Hi there!")
    memory.add_tool_use("calculator", {"expression": "2+2"}, "4")
    
    print("Recent history:")
    print(memory.get_recent_history())
    
    print("\nMemory summary:")
    print(json.dumps(memory.get_summary(), indent=2))
