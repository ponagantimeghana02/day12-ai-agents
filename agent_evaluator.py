import time
import json


class AgentEvaluator:

    def evaluate(
        self,
        task_completed,
        accurate,
        tools_used,
        response_time,
        hallucinations,
        user_rating
    ):

        metrics = {
            "Task Completion Rate": 100 if task_completed else 0,
            "Accuracy": 100 if accurate else 50,
            "Tool Usage": tools_used,
            "Response Time": round(response_time, 2),
            "Hallucination Rate": hallucinations * 10,
            "User Satisfaction": user_rating * 20
        }

        metrics["Overall Score"] = round(
            (
                metrics["Task Completion Rate"]
                + metrics["Accuracy"]
                + metrics["User Satisfaction"]
            ) / 3,
            2
        )

        return metrics


def generate_markdown_report(metrics):

    report = f"""# Agent Evaluation Report

## Evaluation Metrics

| Metric | Value |
|----------|----------|
| Task Completion Rate | {metrics['Task Completion Rate']}% |
| Accuracy | {metrics['Accuracy']}% |
| Tool Usage | {metrics['Tool Usage']} |
| Response Time | {metrics['Response Time']} sec |
| Hallucination Rate | {metrics['Hallucination Rate']}% |
| User Satisfaction | {metrics['User Satisfaction']}% |
| Overall Score | {metrics['Overall Score']}% |

---

## Analysis

### Task Completion
The agent successfully completed the assigned task.

### Accuracy
The generated response was evaluated as accurate.

### Tool Usage
The agent effectively used available tools.

### Response Time
Response was generated in {metrics['Response Time']} seconds.

### Hallucination Rate
Hallucination rate observed: {metrics['Hallucination Rate']}%.

### User Satisfaction
User satisfaction score: {metrics['User Satisfaction']}%.

---

## Conclusion

The agent achieved an overall score of {metrics['Overall Score']}%.
Performance is considered excellent based on the evaluation metrics.
"""

    with open("agent_evaluation_report.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("\n✅ agent_evaluation_report.md generated successfully.")


def main():

    print("🚀 Running Agent Evaluation...\n")

    start = time.time()

    # Simulated agent work
    time.sleep(1.5)

    end = time.time()

    evaluator = AgentEvaluator()

    metrics = evaluator.evaluate(
        task_completed=True,
        accurate=True,
        tools_used=3,
        response_time=end - start,
        hallucinations=1,
        user_rating=4
    )

    print(json.dumps(metrics, indent=4))

    generate_markdown_report(metrics)


if __name__ == "__main__":
    main()