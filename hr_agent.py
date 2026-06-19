import json
from typing import Dict, Any, Callable, List


# =========================================================
# 🧠 MOCK LLM (Replace with OpenAI / Ollama)
# =========================================================
class LLM:
    def generate(self, prompt: str) -> str:
        """
        Replace with real LLM call.
        """
        return prompt


# =========================================================
# 📚 KNOWLEDGE BASE (Mock HR Documents)
# =========================================================
HR_POLICIES = {
    "leave_policy": {
        "content": "Employees are entitled to 18 paid leaves per year. Sick leave is separate.",
        "source": "HR Handbook v2.1"
    },
    "work_hours": {
        "content": "Standard work hours are 9 AM to 6 PM, Monday to Friday.",
        "source": "Company Policy Document"
    },
    "remote_policy": {
        "content": "Employees can work remotely 2 days per week with manager approval.",
        "source": "Remote Work Guidelines 2024"
    }
}


EMPLOYEE_DATA = {
    "EMP001": {"name": "Ajay", "leave_balance": 12},
    "EMP002": {"name": "Ravi", "leave_balance": 8},
}


# =========================================================
# 🧩 TOOLS (HR CAPABILITIES)
# =========================================================

def policy_search_tool(query: str):
    query = query.lower()

    results = []

    for key, value in HR_POLICIES.items():
        if key in query or any(word in query for word in key.split("_")):
            results.append(value)

    if not results:
        return {
            "answer": "No relevant policy found.",
            "source": None
        }

    return {
        "answer": results[0]["content"],
        "source": results[0]["source"]
    }


def leave_balance_tool(emp_id: str):
    data = EMPLOYEE_DATA.get(emp_id)

    if not data:
        return {
            "answer": "Employee not found",
            "source": "HR Database"
        }

    return {
        "answer": f"{data['name']} has {data['leave_balance']} leaves remaining.",
        "source": "Leave Management System"
    }


def payroll_faq_tool(query: str):
    faqs = {
        "salary date": {
            "answer": "Salary is credited on the last working day of every month.",
            "source": "Payroll Policy"
        },
        "tax": {
            "answer": "Tax declarations must be submitted before March 15 every year.",
            "source": "Finance Department"
        }
    }

    for key, value in faqs.items():
        if key in query.lower():
            return value

    return {
        "answer": "Payroll FAQ not found.",
        "source": "Payroll System"
    }


def onboarding_tool():
    return {
        "answer": (
            "New employees must complete onboarding tasks: "
            "1. HR documentation "
            "2. System setup "
            "3. Training modules "
            "4. Manager introduction"
        ),
        "source": "Onboarding Guide"
    }


# =========================================================
# 🧾 TOOL REGISTRY
# =========================================================
TOOLS: Dict[str, Callable] = {
    "policy_search": policy_search_tool,
    "leave_balance": leave_balance_tool,
    "payroll_faq": payroll_faq_tool,
    "onboarding": onboarding_tool
}


# =========================================================
# 🧠 AI HR AGENT (Function Calling + Routing)
# =========================================================
class HRAgent:
    def __init__(self):
        self.llm = LLM()

    def decide_tool(self, query: str) -> Dict[str, Any]:

        q = query.lower()

        # ---------------- Policy Search ----------------
        if "policy" in q or "leave" in q or "work" in q:
            if "leave balance" in q:
                emp_id = query.strip().split()[-1].upper()
                return {"tool": "leave_balance", "args": {"emp_id": emp_id}}

            return {"tool": "policy_search", "args": {"query": query}}

        # ---------------- Payroll ----------------
        if "salary" in q or "payroll" in q or "tax" in q:
            return {"tool": "payroll_faq", "args": {"query": query}}

        # ---------------- Onboarding ----------------
        if "onboard" in q or "join" in q or "new employee" in q:
            return {"tool": "onboarding", "args": {}}

        return {"tool": None, "args": {}}

    def execute(self, query: str):

        print("\n🧠 HR Agent Received Query:", query)

        decision = self.decide_tool(query)

        tool_name = decision["tool"]
        args = decision["args"]

        if not tool_name:
            return {
                "answer": "No relevant HR tool found.",
                "source": None
            }

        tool = TOOLS.get(tool_name)

        if not tool:
            return {
                "answer": "Tool not registered.",
                "source": None
            }

        result = tool(**args)

        # =====================================================
        # 🧠 RESPONSE GENERATION (LLM formatting layer)
        # =====================================================
        final_prompt = f"""
        You are an HR AI Assistant.

        Use the tool output below and create a helpful response.

        TOOL RESULT:
        {json.dumps(result, indent=2)}

        Return:
        - Clear answer
        - Include source citation
        """

        response = self.llm.generate(final_prompt)

        return {
            "answer": result["answer"],
            "source": result["source"],
            "formatted_response": response
        }


# =========================================================
# 🚀 MAIN
# =========================================================
if __name__ == "__main__":
    agent = HRAgent()

    while True:
        query = input("\nUser: ")

        if query.lower() == "exit":
            break

        result = agent.execute(query)

        print("\n📤 FINAL RESPONSE:")
        print(json.dumps(result, indent=2))