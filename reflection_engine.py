import json
from typing import Dict, Any

class LLM:
    def generate(self, prompt: str) -> str:
        prompt_lower = prompt.lower()

        # ---------------- Machine Learning ----------------
        if "machine learning" in prompt_lower:
            return (
                "Machine learning is a branch of Artificial Intelligence (AI) "
                "that enables systems to learn patterns from data and improve "
                "performance without being explicitly programmed."
            )

        # ---------------- Generic What is ----------------
        if "what is" in prompt_lower:
            topic = prompt.split("What is")[-1].strip().replace("?", "")
            return f"{topic} is a concept explained using AI-generated knowledge in simple terms."

        # ---------------- Default ----------------
        return "This is a helpful AI-generated response based on the query."


class ReflectionEngine:
    def __init__(self):
        self.llm = LLM()

    # -------------------------
    # STEP 1: INITIAL RESPONSE
    # -------------------------
    def generate_initial_response(self, query: str) -> str:
        return self.llm.generate(query)

    # -------------------------
    # STEP 2: VALIDATION (CRITIC)
    # -------------------------
    def validate_response(self, query: str, response: str) -> Dict[str, Any]:

        issues = []

        # Too short check
        if len(response.split()) < 8:
            issues.append("Response too short")

        # Missing keyword check
        if "machine learning" in query.lower():
            if "learning" not in response.lower():
                issues.append("Missing key concept explanation")

        # Bad placeholder detection
        if "prompt" in response.lower():
            issues.append("Response contains prompt leakage")

        return {
            "issues_found": issues,
            "needs_correction": len(issues) > 0
        }

    # -------------------------
    # STEP 3: SELF CORRECTION
    # -------------------------
    def self_correct(self, query: str, response: str, issues: Dict[str, Any]) -> str:

        correction_prompt = f"""
        You are an expert AI reviewer.

        Fix and improve the following answer.

        QUESTION:
        {query}

        ORIGINAL ANSWER:
        {response}

        ISSUES:
        {json.dumps(issues, indent=2)}

        TASK:
        - Make the answer accurate
        - Make it clear and complete
        - Remove missing or incorrect parts

        Return only final improved answer.
        """

        return self.llm.generate(correction_prompt)

    # -------------------------
    # STEP 4: FULL PIPELINE
    # -------------------------
    def run(self, query: str):

        print("\n🧠 User Query:", query)

        # Step 1
        initial_response = self.generate_initial_response(query)
        print("\n📌 Initial Response:", initial_response)

        # Step 2
        validation = self.validate_response(query, initial_response)
        print("\n🔍 Validation:", validation)

        # Step 3
        if validation["needs_correction"]:
            print("\n♻️ Self-Correction Triggered...")
            final_response = self.self_correct(query, initial_response, validation)
        else:
            print("\n✅ No correction needed.")
            final_response = initial_response

        return {
            "query": query,
            "initial_response": initial_response,
            "validation": validation,
            "final_response": final_response
        }


# =========================================================
# 🚀 MAIN LOOP
# =========================================================
if __name__ == "__main__":

    engine = ReflectionEngine()

    while True:
        user_input = input("\nUser: ")

        if user_input.lower() == "exit":
            break

        result = engine.run(user_input)

        print("\n================ FINAL OUTPUT ================\n")
        print(json.dumps(result, indent=2))