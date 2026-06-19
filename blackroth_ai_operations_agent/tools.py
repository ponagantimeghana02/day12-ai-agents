class DatabaseTool:

    def query_employee(self, emp_id):
        return {
            "id": emp_id,
            "name": "Ajay",
            "leave_balance": 12,
            "salary": 65000
        }


class EmailService:

    def send_email(self, recipient, subject, body):
        return f"Email sent to {recipient}"


class CalendarService:

    def create_meeting(self, title):
        return f"Meeting '{title}' scheduled"


class ProjectManagementAPI:

    def get_project_status(self, project):
        return {
            "project": project,
            "status": "On Track",
            "completion": "78%"
        }

    def create_task(self, task):
        return f"Task created: {task}"