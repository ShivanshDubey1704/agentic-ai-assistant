"""
Agentic AI Assistant - Main Agent Implementation
"""

import os
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
from tools import ToolRegistry
from memory import Memory
from planner import TaskPlanner
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

load_dotenv()


class AgenticAI:
    """
    Main Agentic AI class that orchestrates autonomous task execution.
    
    The agent can:
    - Break down complex tasks into steps
    - Select and use appropriate tools
    - Make decisions based on context
    - Learn from previous interactions
    - Pursue goals autonomously
    """
    
    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_iterations: int = 10
    ):
        """
        Initialize the Agentic AI system.
        
        Args:
            model: OpenAI model to use
            temperature: Creativity level (0-1)
            max_iterations: Maximum steps to achieve goal
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature
        self.max_iterations = max_iterations
        
        # Initialize components
        self.tools = ToolRegistry()
        self.memory = Memory()
        self.planner = TaskPlanner()
        
        print(f"{Fore.GREEN}🤖 Agentic AI Assistant initialized!")
        print(f"{Fore.CYAN}Model: {model}")
        print(f"{Fore.CYAN}Available tools: {len(self.tools.get_all_tools())}")
    
    def execute(self, goal: str) -> Dict[str, Any]:
        """
        Execute a goal autonomously.
        
        Args:
            goal: The objective to achieve
            
        Returns:
            Dictionary containing result and execution metadata
        """
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Fore.YELLOW}🎯 Goal: {goal}")
        print(f"{Fore.YELLOW}{'='*60}\n")
        
        # Add goal to memory
        self.memory.add_message("user", goal)
        
        # Plan the task
        plan = self.planner.create_plan(goal, self.tools.get_tool_descriptions())
        print(f"{Fore.MAGENTA}📋 Plan created with {len(plan['steps'])} steps\n")
        
        # Execute plan
        iteration = 0
        final_result = None
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"{Fore.CYAN}--- Iteration {iteration}/{self.max_iterations} ---\n")
            
            # Get next action from agent
            action = self._decide_next_action(goal, plan)
            
            if action["type"] == "complete":
                final_result = action["result"]
                print(f"{Fore.GREEN}✅ Goal achieved!")
                break
            
            elif action["type"] == "use_tool":
                # Execute tool
                tool_name = action["tool"]
                tool_input = action["input"]
                
                print(f"{Fore.BLUE}🔧 Using tool: {tool_name}")
                print(f"{Fore.BLUE}   Input: {tool_input}\n")
                
                tool_result = self.tools.execute(tool_name, tool_input)
                
                print(f"{Fore.GREEN}   Result: {tool_result}\n")
                
                # Add to memory
                self.memory.add_tool_use(tool_name, tool_input, tool_result)
            
            elif action["type"] == "think":
                print(f"{Fore.MAGENTA}💭 Thinking: {action['thought']}\n")
                self.memory.add_message("assistant", action["thought"])
        
        if final_result is None:
            final_result = "Maximum iterations reached without completing goal"
        
        # Save to memory
        self.memory.add_message("assistant", str(final_result))
        
        return {
            "success": iteration < self.max_iterations,
            "result": final_result,
            "iterations": iteration,
            "tools_used": self.memory.get_tools_used()
        }
    
    def _decide_next_action(self, goal: str, plan: Dict) -> Dict[str, Any]:
        """
        Decide the next action to take based on current state.
        
        Args:
            goal: The original goal
            plan: The execution plan
            
        Returns:
            Dictionary describing the next action
        """
        # Build context for decision making
        context = self._build_context(goal, plan)
        
        # Get decision from LLM
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {
                    "role": "system",
                    "content": self._get_system_prompt()
                },
                {
                    "role": "user",
                    "content": context
                }
            ]
        )
        
        # Parse response
        decision_text = response.choices[0].message.content
        
        try:
            decision = json.loads(decision_text)
        except json.JSONDecodeError:
            # Fallback if not valid JSON
            decision = {
                "type": "think",
                "thought": decision_text
            }
        
        return decision
    
    def _build_context(self, goal: str, plan: Dict) -> str:
        """Build context string for decision making."""
        context = f"""
Goal: {goal}

Plan:
{json.dumps(plan, indent=2)}

Available Tools:
{json.dumps(self.tools.get_tool_descriptions(), indent=2)}

Conversation History:
{self.memory.get_recent_history(5)}

Based on the goal, plan, and history, decide your next action.
Respond with a JSON object in one of these formats:

1. To use a tool:
{{"type": "use_tool", "tool": "tool_name", "input": {{"param": "value"}}}}

2. To think/reason:
{{"type": "think", "thought": "your reasoning here"}}

3. To complete the goal:
{{"type": "complete", "result": "final answer or result"}}
"""
        return context
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        return """You are an autonomous AI agent that can use tools to accomplish goals.

Your capabilities:
- Break down complex tasks into steps
- Select and use appropriate tools
- Make decisions based on context
- Learn from results and adapt
- Pursue goals until completion

Guidelines:
- Always think step-by-step
- Use tools when needed for information or actions
- Be efficient - don't repeat unnecessary steps
- If stuck, try a different approach
- Complete the goal as accurately as possible

Respond only with valid JSON in the specified format."""
    
    def reset(self):
        """Reset the agent's memory and state."""
        self.memory.clear()
        print(f"{Fore.YELLOW}🔄 Agent memory cleared")


if __name__ == "__main__":
    # Quick test
    agent = AgenticAI()
    result = agent.execute("Calculate 15 * 23 + 100")
    print(f"\n{Fore.GREEN}Final Result: {result}")
