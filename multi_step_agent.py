import json
from typing import Dict, Any, List


# -----------------------------
# SIMPLE MOCK LLM (Replace with OpenAI/Ollama)
# -----------------------------
class LLM:
    def generate(self, prompt: str) -> str:
        """
        Replace this with OpenAI / Claude / Ollama API call.
        """
        return f"[LLM OUTPUT for prompt]: {prompt[:80]}..."


# -----------------------------
# AGENT MEMORY
# -----------------------------
class Memory:
    def __init__(self):
        self.store: Dict[str, Any] = {}

    def update(self, key: str, value: Any):
        self.store[key] = value

    def get_all(self):
        return self.store


# -----------------------------
# PLANNER AGENT
# -----------------------------
class PlannerAgent:
    def __init__(self, llm: LLM):
        self.llm = llm

    def create_plan(self, task: str) -> List[str]:
        prompt = f"""
        You are a senior system architect.

        Break this task into clear sequential steps:

        TASK: {task}

        Output ONLY a JSON list of steps like:
        ["step1", "step2", "step3"]
        """

        response = self.llm.generate(prompt)

        # For demo → fallback plan (replace with real LLM JSON parsing)
        return [
            "Generate requirements",
            "Generate user stories",
            "Generate database schema",
            "Generate API list",
            "Generate development roadmap"
        ]


# -----------------------------
# EXECUTOR AGENT
# -----------------------------
class ExecutorAgent:
    def __init__(self, llm: LLM, memory: Memory):
        self.llm = llm
        self.memory = memory

    def execute_step(self, step: str, task: str):
        context = self.memory.get_all()

        prompt = f"""
        You are an AI software engineer.

        TASK: {task}

        PREVIOUS CONTEXT:
        {json.dumps(context, indent=2)}

        CURRENT STEP:
        {step}

        Generate high-quality output for this step.
        """

        result = self.llm.generate(prompt)

        # store result in memory
        self.memory.update(step, result)

        return result


# -----------------------------
# ORCHESTRATOR AGENT
# -----------------------------
class MultiStepAgent:
    def __init__(self):
        self.llm = LLM()
        self.memory = Memory()
        self.planner = PlannerAgent(self.llm)
        self.executor = ExecutorAgent(self.llm, self.memory)

    def run(self, task: str):
        print("\n🚀 AI Multi-Step Agent Started\n")

        # STEP 1: PLAN
        print("📋 Creating plan...")
        steps = self.planner.create_plan(task)

        print("\nPlan:")
        for i, s in enumerate(steps, 1):
            print(f"{i}. {s}")

        # STEP 2: EXECUTE STEP BY STEP
        results = {}

        for step in steps:
            print(f"\n⚙️ Executing: {step}")
            output = self.executor.execute_step(step, task)
            results[step] = output

        # FINAL PACKAGE
        final_output = {
            "task": task,
            "steps_executed": steps,
            "results": results
        }

        return final_output


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    agent = MultiStepAgent()

    task = "Create a project plan for a Ride Booking App"

    result = agent.run(task)

    print("\n================ FINAL OUTPUT ================\n")
    print(json.dumps(result, indent=2)) 