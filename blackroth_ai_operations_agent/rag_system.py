class RAGSystem:

    def search(self, query):

        docs = {
            "leave policy":
                "Employees receive 24 annual leaves per year.",

            "payroll":
                "Payroll is processed on the last working day."
        }

        query = query.lower()

        for key, value in docs.items():
            if key in query:
                return value

        return "No document found."