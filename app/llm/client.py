
from openai import OpenAI

from app.core.config import OPENAI_API_KEY, OPENAI_MODEL


class LLMClient:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is missing. Add it to your .env file."
            )

        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL

    def generate(
        self,
        prompt: str,
        system_prompt: str = (
            "You are RepoPilot, an AI software engineering assistant. "
            "Answer accurately and do not invent facts about the code."
        ),
    ) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=prompt,
        )

        return response.output_text
