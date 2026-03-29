from src.base_agent.base_agent import BaseAgent

try:
    from google import genai
except ImportError:
    genai = None


class GeminiAgent(BaseAgent):
    def connect(self, api_key: str, temperature: float):
        if genai is None:
            raise ImportError(
                "google-genai is not installed. Install it with: pip install google-genai"
            )

        client = genai.Client(api_key=api_key)
        return {
            "client": client,
            "temperature": temperature,
        }

    def generate_response(self, query: str) -> str:
        client = self.llm["client"]
        temperature = self.llm["temperature"]

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{self.prompt}\n\n{query}",
            config={
                "temperature": temperature,
            },
        )

        return response.text