import os
import groq
import json

class IntakeAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")

    def process(self, form_data):
        client = groq.Client(api_key=self.api_key)
        agentic_cot_prompt = f"""
You are a legal intake validation agent.

Instructions:
- First, outline your plan for validating the intake step by step.
- Follow your plan, thinking out loud (chain of thought) to check each required field and validate its content.
- If a field is missing or unclear, reflect on possible implications and suggest what is needed.
- At the end, clearly state whether the intake is valid or list missing/problematic fields, and explain why.
- Do NOT provide legal advice or strategy.
- Respond ONLY in valid JSON with these keys:
  "plan": [steps as strings],
  "chain_of_thought": [thoughts as strings],
  "conclusion": {{
    "intake_valid": true/false,
    "missing_or_invalid_fields": [field names as strings],
    "reasoning": explanation string
  }}
User intake:
{form_data}
"""
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": agentic_cot_prompt}]
        )
        try:
            result = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            result = {
                "error": "Could not parse response as JSON",
                "raw": response.choices[0].message.content
            }
        return result