"""
Task Planning Module
Breaks down complex goals into executable steps
"""

from typing import Dict, List, Any
import json


class TaskPlanner:
    """
    Plans and decomposes complex tasks into executable steps.
    """
    
    def __init__(self):
        self.current_plan = None
    
    def create_plan(self, goal: str, available_tools: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an execution plan for a goal.
        
        Args:
            goal: The goal to achieve
            available_tools: Dictionary of available tools
            
        Returns:
            Execution plan with steps
        """
        # Simple heuristic-based planning
        # In production, this could use LLM for more sophisticated planning
        
        plan = {
            "goal": goal,
            "steps": self._decompose_goal(goal, available_tools),
            "status": "pending"
        }
        
        self.current_plan = plan
        return plan
    
    def _decompose_goal(self, goal: str, tools: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Decompose a goal into steps.
        
        Args:
            goal: Goal to decompose
            tools: Available tools
            
        Returns:
            List of steps
        """
        # Simple keyword-based decomposition
        # In production, use LLM for intelligent decomposition
        
        steps = []
        goal_lower = goal.lower()
        
        # Check for calculation needs
        if any(op in goal_lower for op in ['calculate', 'compute', '+', '-', '*', '/', 'sum']):
            steps.append({
                "action": "use_tool",
                "tool": "calculator",
                "description": "Perform calculation"
            })
        
        # Check for search needs
        if any(word in goal_lower for word in ['search', 'find', 'look up', 'research']):
            steps.append({
                "action": "use_tool",
                "tool": "web_search",
                "description": "Search for information"
            })
        
        # Check for file operations
        if 'read' in goal_lower and 'file' in goal_lower:
            steps.append({
                "action": "use_tool",
                "tool": "file_read",
                "description": "Read file contents"
            })
        
        if 'write' in goal_lower or 'save' in goal_lower:
            steps.append({
                "action": "use_tool",
                "tool": "file_write",
                "description": "Write to file"
            })
        
        # Check for time/date needs
        if any(word in goal_lower for word in ['time', 'date', 'when', 'current']):
            steps.append({
                "action": "use_tool",
                "tool": "get_current_time",
                "description": "Get current time"
            })
        
        # Check for weather
        if 'weather' in goal_lower:
            steps.append({
                "action": "use_tool",
                "tool": "weather",
                "description": "Get weather information"
            })
        
        # If no specific steps identified, add a thinking step
        if not steps:
            steps.append({
                "action": "think",
                "description": "Analyze the goal and determine approach"
            })
        
        # Always add a final step to synthesize results
        steps.append({
            "action": "synthesize",
            "description": "Combine results and provide final answer"
        })
        
        return steps
    
    def update_plan_status(self, step_index: int, status: str):
        """
        Update the status of a plan step.
        
        Args:
            step_index: Index of the step
            status: New status (pending/in_progress/completed/failed)
        """
        if self.current_plan and step_index < len(self.current_plan["steps"]):
            self.current_plan["steps"][step_index]["status"] = status
    
    def get_next_step(self) -> Dict[str, Any]:
        """
        Get the next pending step in the plan.
        
        Returns:
            Next step dictionary or None
        """
        if not self.current_plan:
            return None
        
        for step in self.current_plan["steps"]:
            if step.get("status", "pending") == "pending":
                return step
        
        return None
    
    def is_plan_complete(self) -> bool:
        """
        Check if the current plan is complete.
        
        Returns:
            True if all steps are completed
        """
        if not self.current_plan:
            return False
        
        for step in self.current_plan["steps"]:
            if step.get("status", "pending") != "completed":
                return False
        
        return True
    
    def get_plan_summary(self) -> str:
        """
        Get a summary of the current plan.
        
        Returns:
            Formatted plan summary
        """
        if not self.current_plan:
            return "No active plan"
        
        summary = f"Goal: {self.current_plan['goal']}\n\n"
        summary += "Steps:\n"
        
        for i, step in enumerate(self.current_plan["steps"], 1):
            status = step.get("status", "pending")
            summary += f"{i}. [{status.upper()}] {step['description']}\n"
        
        return summary


if __name__ == "__main__":
    # Test planner
    planner = TaskPlanner()
    
    goal = "Calculate the sum of 15 and 23, then save the result to a file"
    tools = {
        "calculator": {"description": "Math operations"},
        "file_write": {"description": "Write files"}
    }
    
    plan = planner.create_plan(goal, tools)
    print("Plan created:")
    print(json.dumps(plan, indent=2))
    
    print("\nPlan summary:")
    print(planner.get_plan_summary())
