# ml/context_provider.py

class ContextProvider:
    """
    Builds the prompt sent to the language model.
    This is a pure function: no I/O, no model calls.
    """

    def build(
        self,
        user_input: str,
        system_state: dict,
        allowed_actions: list[str]
    ) -> str:
        return f"""You are a system assistant inside an operating system.

Rules:
- You must obey system policies.
- You may only choose from the allowed actions.
- You must respond in valid JSON only.

System state:
{system_state}

Allowed actions:
{allowed_actions}

User request:
{user_input}

Response format:
{{
  "action": "<action_name>",
  "args": {{ }}
}}
"""
