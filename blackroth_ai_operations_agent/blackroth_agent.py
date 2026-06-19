import json

from tools import (
    DatabaseTool,
    EmailService,
    CalendarService,
    ProjectManagementAPI
)

from rag_system import RAGSystem


class BlackRothAgent:

    def __init__(self):

        self.db = DatabaseTool()

        self.email = EmailService()

        self.calendar = CalendarService()

        self.project_api = ProjectManagementAPI()

        self.rag = RAGSystem()

    # -------------------------
    # PLANNER
    # -------------------------

    def decide_tools(self, query):

        query = query.lower()

        if "leave" in query:
            return ["database", "rag"]

        if "payroll" in query:
            return ["database", "rag"]

        if "project" in query:
            return ["project_api"]

        if "meeting" in query:
            return ["calendar"]

        if "task" in query:
            return ["project_api"]

        if "document" in query:
            return ["rag"]

        return []

    # -------------------------
    # EXECUTION
    # -------------------------

    def execute(self, query):

        tools = self.decide_tools(query)

        outputs = {}

        for tool in tools:

            if tool == "database":

                outputs["employee_data"] = (
                    self.db.query_employee("EMP001")
                )

            elif tool == "rag":

                outputs["document_context"] = (
                    self.rag.search(query)
                )

            elif tool == "calendar":

                outputs["calendar"] = (
                    self.calendar.create_meeting(
                        "Project Review"
                    )
                )

            elif tool == "project_api":

                if "status" in query:

                    outputs["project_status"] = (
                        self.project_api
                        .get_project_status(
                            "AI Operations"
                        )
                    )

                else:

                    outputs["task"] = (
                        self.project_api
                        .create_task(
                            "New AI Task"
                        )
                    )

        return self.combine_outputs(
            query,
            outputs
        )

    # -------------------------
    # AGGREGATION
    # -------------------------

    def combine_outputs(
        self,
        query,
        outputs
    ):

        return {
            "query": query,
            "tools_used": list(outputs.keys()),
            "results": outputs
        }


if __name__ == "__main__":

    agent = BlackRothAgent()

    while True:

        user_query = input(
            "\nAsk BlackRoth Agent: "
        )

        if user_query.lower() == "exit":
            break

        result = agent.execute(
            user_query
        )

        print(
            json.dumps(
                result,
                indent=4
            )
        )