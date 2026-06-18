from datetime import datetime
import ast
import operator as op


# ----------------------------
# TOOL 1: CALCULATOR TOOL
# ----------------------------

# Safe operators (prevents unsafe eval)
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod
}

def safe_eval(expr):
    """
    Safely evaluate arithmetic expressions like: 250 * 45
    """

    def eval_node(node):
        if isinstance(node, ast.Num):  # numbers
            return node.n
        elif isinstance(node, ast.BinOp):
            return OPERATORS[type(node.op)](
                eval_node(node.left),
                eval_node(node.right)
            )
        else:
            raise ValueError("Unsupported expression")

    tree = ast.parse(expr, mode='eval')
    return eval_node(tree.body)


def calculator_tool(expression: str):
    return safe_eval(expression)


# ----------------------------
# TOOL 2: CURRENT DATE TOOL
# ----------------------------

def current_date_tool():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ----------------------------
# TOOL 3: TEXT SUMMARY TOOL
# ----------------------------

def text_summary_tool(text: str):
    """
    Simple extractive summary:
    returns first 2–3 sentences
    """
    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if s.strip()]
    
    summary = ". ".join(sentences[:3])
    return summary + "." if summary else ""


# ----------------------------
# AGENT LOGIC (TOOL ROUTER)
# ----------------------------

def agent(query: str):
    query_lower = query.lower()

    # Detect Calculator intent
    if any(op in query for op in ["+", "-", "*", "/", "%"]):
        try:
            result = calculator_tool(query)
            return f"🧮 Calculator Result: {result}"
        except Exception as e:
            return f"Calculator Error: {str(e)}"

    # Detect Date intent
    if "date" in query_lower or "time" in query_lower:
        return f"📅 Current Date: {current_date_tool()}"

    # Detect Summary intent
    if "summarize" in query_lower or "summary" in query_lower:
        text = query.replace("summarize", "").replace("summary", "")
        return f"📝 Summary: {text_summary_tool(text)}"

    return "❌ No suitable tool found for the query."


# ----------------------------
# MAIN RUNNER
# ----------------------------

if __name__ == "__main__":
    print("Tool Calling Agent is running...\n")

    while True:
        user_input = input("Enter query (or 'exit'): ")

        if user_input.lower() == "exit":
            break

        response = agent(user_input)
        print(response)