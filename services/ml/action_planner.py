# ml/action_planner.py

import json


class ActionPlanner:
    """
    Converts raw model output into a structured action.

    The model is expected to return JSON in the form:
    {
      "action": "<string>",
      "args": { ... }
    }
    """

    def plan(self, model_output: str) -> dict:
        try:
            return json.loads(model_output)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Model output is not valid JSON:\n{model_output}"
            ) from e
