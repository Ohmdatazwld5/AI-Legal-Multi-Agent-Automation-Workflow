import os
import groq
import json

DISCLAIMER = (
    "\n\n---\n"
    "This letter was generated by an AI assistant for draft and review purposes only. "
    "It is not legal advice. Please consult a qualified attorney before acting on its contents."
)

class DocumentGenerationAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")

    def generate(self, client_data, analysis):
        client = groq.Client(api_key=self.api_key)
        prompt = f"""
You are an AI legal document generator. You must NOT give legal advice or recommend legal actions. Draft a professional letter or summary based only on the provided analysis.

Respond ONLY in valid JSON with these keys:
{{
  "document": "...",
  "explanation": "..."
}}

Client intake:
{client_data}
Fault analysis:
{analysis}
"""
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        try:
            result = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            result = {
                "error": "Could not parse response as JSON",
                "raw": response.choices[0].message.content
            }
        # Add disclaimer if document present (robust to type)
        if "document" in result:
            if isinstance(result["document"], str):
                result["document"] += DISCLAIMER
            elif isinstance(result["document"], dict):
                result["document"] = json.dumps(result["document"], indent=2) + DISCLAIMER
            else:
                result["document"] = str(result["document"]) + DISCLAIMER
        return result