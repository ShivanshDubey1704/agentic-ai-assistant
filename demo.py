"""
Demo Script for Agentic AI Assistant
Shows various use cases and capabilities
"""

from agent import AgenticAI
from colorama import Fore, Style
import time


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Fore.YELLOW}{'='*70}")
    print(f"{Fore.YELLOW}{text.center(70)}")
    print(f"{Fore.YELLOW}{'='*70}\n")


def demo_basic_calculation():
    """Demo: Basic calculation task."""
    print_header("DEMO 1: Basic Calculation")
    
    agent = AgenticAI(model="gpt-4", max_iterations=5)
    
    goal = "Calculate the result of (15 * 23) + 100 - 50"
    result = agent.execute(goal)
    
    print(f"\n{Fore.GREEN}✅ Demo 1 Complete!")
    print(f"{Fore.CYAN}Result: {result['result']}")
    print(f"{Fore.CYAN}Iterations: {result['iterations']}")
    print(f"{Fore.CYAN}Tools used: {result['tools_used']}")


def demo_multi_step_task():
    """Demo: Multi-step task with multiple tools."""
    print_header("DEMO 2: Multi-Step Task")
    
    agent = AgenticAI(model="gpt-4", max_iterations=10)
    
    goal = "Get the current time and calculate how many hours until midnight"
    result = agent.execute(goal)
    
    print(f"\n{Fore.GREEN}✅ Demo 2 Complete!")
    print(f"{Fore.CYAN}Result: {result['result']}")
    print(f"{Fore.CYAN}Tools used: {result['tools_used']}")


def demo_file_operations():
    """Demo: File operations."""
    print_header("DEMO 3: File Operations")
    
    agent = AgenticAI(model="gpt-4", max_iterations=10)
    
    goal = "Write 'Hello from Agentic AI!' to a file called test_output.txt"
    result = agent.execute(goal)
    
    print(f"\n{Fore.GREEN}✅ Demo 3 Complete!")
    print(f"{Fore.CYAN}Result: {result['result']}")


def demo_complex_reasoning():
    """Demo: Complex reasoning task."""
    print_header("DEMO 4: Complex Reasoning")
    
    agent = AgenticAI(model="gpt-4", max_iterations=15)
    
    goal = """
    If a train travels at 60 mph for 2.5 hours, then increases speed to 80 mph 
    for another 1.5 hours, what is the total distance traveled?
    """
    
    result = agent.execute(goal)
    
    print(f"\n{Fore.GREEN}✅ Demo 4 Complete!")
    print(f"{Fore.CYAN}Result: {result['result']}")


def demo_interactive():
    """Demo: Interactive mode."""
    print_header("DEMO 5: Interactive Mode")
    
    agent = AgenticAI(model="gpt-4", max_iterations=10)
    
    print(f"{Fore.CYAN}Interactive mode - Type 'quit' to exit\n")
    
    while True:
        goal = input(f"{Fore.GREEN}Enter your goal: {Style.RESET_ALL}")
        
        if goal.lower() in ['quit', 'exit', 'q']:
            print(f"{Fore.YELLOW}Goodbye!")
            break
        
        if not goal.strip():
            continue
        
        result = agent.execute(goal)
        
        print(f"\n{Fore.MAGENTA}Result: {result['result']}\n")


def run_all_demos():
    """Run all demos sequentially."""
    print(f"{Fore.CYAN}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║           AGENTIC AI ASSISTANT - DEMO SUITE                      ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)
    
    demos = [
        ("Basic Calculation", demo_basic_calculation),
        ("Multi-Step Task", demo_multi_step_task),
        ("File Operations", demo_file_operations),
        ("Complex Reasoning", demo_complex_reasoning),
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        print(f"\n{Fore.YELLOW}Running Demo {i}/{len(demos)}: {name}")
        time.sleep(1)
        
        try:
            demo_func()
        except Exception as e:
            print(f"{Fore.RED}Error in demo: {str(e)}")
        
        if i < len(demos):
            print(f"\n{Fore.CYAN}Press Enter to continue to next demo...")
            input()
    
    print(f"\n{Fore.GREEN}All demos completed!")
    print(f"\n{Fore.CYAN}Want to try interactive mode? (y/n): ", end="")
    
    if input().lower() == 'y':
        demo_interactive()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        demo_name = sys.argv[1].lower()
        
        demos = {
            "calc": demo_basic_calculation,
            "multi": demo_multi_step_task,
            "file": demo_file_operations,
            "reason": demo_complex_reasoning,
            "interactive": demo_interactive,
        }
        
        if demo_name in demos:
            demos[demo_name]()
        else:
            print(f"Unknown demo: {demo_name}")
            print(f"Available demos: {', '.join(demos.keys())}")
    else:
        run_all_demos()
