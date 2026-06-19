import json

class Agent:
    def __init__(self, name):
        self.name = name

    def process(self, data):
        raise NotImplementedError


class ResearchAgent(Agent):

    def process(self, user_request):
        research = {
            "project": user_request,
            "research_findings": [
                "Users need a simple and intuitive interface",
                "System should be scalable",
                "Data security is important",
                "API integration may be required"
            ]
        }

        print("\n🔍 Research Agent Output")
        print(json.dumps(research, indent=2))

        return research


class BusinessAnalystAgent(Agent):

    def process(self, research_data):

        requirements = {
            "functional_requirements": [
                "User Registration",
                "User Login",
                "Dashboard",
                "Reports"
            ],
            "non_functional_requirements": [
                "Scalability",
                "Security",
                "Performance"
            ]
        }

        print("\n📋 Business Analyst Agent Output")
        print(json.dumps(requirements, indent=2))

        return {
            **research_data,
            "requirements": requirements
        }



class ArchitectAgent(Agent):

    def process(self, ba_output):

        architecture = {
            "frontend": "React",
            "backend": "FastAPI",
            "database": "PostgreSQL",
            "authentication": "JWT",
            "deployment": "Docker + Cloud"
        }

        print("\n🏗️ Architect Agent Output")
        print(json.dumps(architecture, indent=2))

        return {
            **ba_output,
            "architecture": architecture
        }


class ProjectManagerAgent(Agent):

    def process(self, architecture_output):

        roadmap = {
            "Phase 1": "Requirement Gathering",
            "Phase 2": "System Design",
            "Phase 3": "Development",
            "Phase 4": "Testing",
            "Phase 5": "Deployment"
        }

        print("\n📅 Project Manager Agent Output")
        print(json.dumps(roadmap, indent=2))

        return {
            **architecture_output,
            "roadmap": roadmap
        }

class MultiAgentSystem:

    def __init__(self):

        self.research_agent = ResearchAgent("Research Agent")

        self.ba_agent = BusinessAnalystAgent(
            "Business Analyst Agent"
        )

        self.architect_agent = ArchitectAgent(
            "Architect Agent"
        )

        self.pm_agent = ProjectManagerAgent(
            "Project Manager Agent"
        )

    def run(self, user_request):

        print("\n🚀 Starting Multi-Agent Workflow")

        research_output = self.research_agent.process(
            user_request
        )

        ba_output = self.ba_agent.process(
            research_output
        )

        architect_output = self.architect_agent.process(
            ba_output
        )

        final_report = self.pm_agent.process(
            architect_output
        )

        return final_report



if __name__ == "__main__":

    system = MultiAgentSystem()

    request = input(
        "\nEnter Project Idea: "
    )

    report = system.run(request)

    print("\n" + "=" * 50)
    print("📄 FINAL REPORT")
    print("=" * 50)

    print(json.dumps(report, indent=2))