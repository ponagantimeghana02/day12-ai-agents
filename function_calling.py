import json
from datetime import datetime


# -----------------------------
# MOCK DATABASE (Employee Tool)
# -----------------------------
EMPLOYEE_DB = {
    "EMP001": {"id": "EMP001", "name": "Ajay", "department": "Engineering"},
    "EMP002": {"id": "EMP002", "name": "Ravi", "department": "HR"},
    "EMP003": {"id": "EMP003", "name": "Sneha", "department": "Finance"},
}


# -----------------------------
# WEATHER TOOL (Mock API)
# -----------------------------
def weather_tool(city: str):
    mock_weather = {
        "mumbai": {"city": "Mumbai", "temp": "32°C", "condition": "Sunny"},
        "delhi": {"city": "Delhi", "temp": "28°C", "condition": "Cloudy"},
        "pune": {"city": "Pune", "temp": "27°C", "condition": "Rainy"},
    }

    city = city.lower()
    return mock_weather.get(city, {"error": "Weather data not found"})


# -----------------------------
# CURRENCY TOOL (Mock API)
# -----------------------------
def currency_tool(from_currency: str, to_currency: str, amount: float):
    mock_rates = {
        ("USD", "INR"): 83,
        ("INR", "USD"): 0.012,
        ("EUR", "INR"): 90,
    }

    rate = mock_rates.get((from_currency, to_currency))

    if not rate:
        return {"error": "Currency pair not supported"}

    converted = amount * rate

    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "converted_amount": round(converted, 2),
        "rate": rate
    }


# -----------------------------
# EMPLOYEE LOOKUP TOOL
# -----------------------------
def employee_lookup(emp_id: str):
    return EMPLOYEE_DB.get(emp_id, {"error": "Employee not found"})


# -----------------------------
# TOOL ROUTER (Function Calling Engine)
# -----------------------------
def function_call_router(user_query: str):
    query = user_query.lower()

    # Employee Tool
    if "employee" in query or "emp" in query:
        emp_id = user_query.strip().split()[-1].upper()
        return employee_lookup(emp_id)

    # Weather Tool
    if "weather" in query:
        city = user_query.split("for")[-1].strip()
        return weather_tool(city)

    # Currency Tool
    if "currency" in query or "convert" in query:
        try:
            parts = user_query.split()
            amount = float(parts[0])
            from_currency = parts[1].upper()
            to_currency = parts[-1].upper()
            return currency_tool(from_currency, to_currency, amount)
        except:
            return {"error": "Invalid currency query format"}

    return {"error": "No matching tool found"}


# -----------------------------
# MAIN AGENT LOOP
# -----------------------------
def run_agent():
    print("Function Calling Agent Started (type 'exit' to stop)\n")

    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            break

        result = function_call_router(user_input)

        print("Agent:", json.dumps(result, indent=2))


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    run_agent()