from typing import List, Dict, Any


class ExecutionState:
    """
    Tracks execution lifecycle of a task.
    Enables structured logging, debugging, and future streaming.
    """

    def __init__(self, goal: str):
        self.goal = goal
        self.steps: List[Dict[str, Any]] = []
        self.current_step: int = 0
        self.status: str = "RUNNING"

    def add_step(self, description: str, result: str):
        """
        Records a completed step.
        """
        self.steps.append({
            "step_number": self.current_step + 1,
            "description": description,
            "result": result
        })
        self.current_step += 1

    def fail(self, error_message: str):
        """
        Marks execution as failed.
        """
        self.status = "FAILED"
        self.steps.append({
            "step_number": self.current_step + 1,
            "description": "Execution Failure",
            "result": error_message
        })

    def complete(self):
        """
        Marks execution as successful.
        """
        self.status = "SUCCESS"

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns structured state for API or reporting.
        """
        return {
            "goal": self.goal,
            "status": self.status,
            "steps": self.steps
        }
