import json
from typing import Dict, List, Any


# =========================================================
# 🧠 SHORT-TERM MEMORY (Conversation Buffer)
# =========================================================
class ShortTermMemory:
    def __init__(self, max_size: int = 10):
        self.history: List[Dict[str, str]] = []
        self.max_size = max_size

    def add(self, role: str, message: str):
        self.history.append({"role": role, "message": message})

        # Keep only last N messages
        if len(self.history) > self.max_size:
            self.history.pop(0)

    def get_history(self):
        return self.history


# =========================================================
# 🧠 LONG-TERM MEMORY (Persistent User Profile)
# =========================================================
class LongTermMemory:
    def __init__(self):
        self.memory: Dict[str, Any] = {}

    def update(self, key: str, value: Any):
        self.memory[key] = value

    def get(self, key: str):
        return self.memory.get(key)

    def get_all(self):
        return self.memory


# =========================================================
# 🧠 SIMPLE INTENT + FACT EXTRACTION (AI SIMULATION)
# =========================================================
def extract_memory_facts(user_message: str):
    """
    Simple rule-based extraction (replace with LLM in real system)
    """

    message = user_message.lower()

    facts = {}

    # Name extraction
    if "my name is" in message:
        name = user_message.split("is")[-1].strip()
        facts["name"] = name

    # Employee ID extraction
    if "emp" in message.lower():
        for word in user_message.split():
            if "EMP" in word.upper():
                facts["employee_id"] = word.upper()

    # Language preference
    if "language" in message:
        if "english" in message.lower():
            facts["preferred_language"] = "English"
        elif "hindi" in message.lower():
            facts["preferred_language"] = "Hindi"

    return facts


# =========================================================
# 🧠 MEMORY-ENABLED AI AGENT
# =========================================================
class MemoryAgent:
    def __init__(self):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()

    # -------------------------
    # STORE MEMORY
    # -------------------------
    def store_memory(self, user_message: str):

        facts = extract_memory_facts(user_message)

        if facts:
            for key, value in facts.items():
                self.long_term.update(key, value)

    # -------------------------
    # RETRIEVE ANSWER USING MEMORY
    # -------------------------
    def generate_response(self, user_message: str):

        message = user_message.lower()

        # CASE 1: Asking name
        if "my name" in message or "what is my name" in message:
            name = self.long_term.get("name")
            if name:
                return f"Your name is {name}."
            return "I don't know your name yet."

        # CASE 2: Employee ID recall
        if "employee id" in message or "emp id" in message:
            emp_id = self.long_term.get("employee_id")
            if emp_id:
                return f"Your employee ID is {emp_id}."
            return "I don't know your employee ID yet."

        # CASE 3: Preferred language
        if "language" in message:
            lang = self.long_term.get("preferred_language")
            if lang:
                return f"Your preferred language is {lang}."
            return "I don't know your preferred language yet."

        return "I understand your message, but I have no stored memory for it."

    # -------------------------
    # MAIN AGENT FLOW
    # -------------------------
    def run(self, user_message: str):

        print("\n🧠 User:", user_message)

        # STEP 1: Store in short-term memory
        self.short_term.add("user", user_message)

        # STEP 2: Extract + store long-term memory
        self.store_memory(user_message)

        # STEP 3: Generate response using memory
        response = self.generate_response(user_message)

        # STEP 4: Save assistant response
        self.short_term.add("assistant", response)

        return response


# =========================================================
# 🚀 MAIN LOOP
# =========================================================
if __name__ == "__main__":

    agent = MemoryAgent()

    print("\n🧠 Memory Agent Started (type 'exit' to stop)\n")

    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            break

        response = agent.run(user_input)

        print("Agent:", response)

        # Debug view (optional)
        print("\n📌 Long-Term Memory:", json.dumps(agent.long_term.get_all(), indent=2))
        print("📌 Short-Term Memory:", json.dumps(agent.short_term.get_history(), indent=2))