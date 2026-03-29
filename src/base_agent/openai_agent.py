from src.base_agent.base_agent import BaseAgent

try:
    from llama_index.llms.openai import OpenAI
except ImportError:
    OpenAI = None


class OpenAIAgent(BaseAgent):
    def connect(self, api_key: str, temperature: float):
        if OpenAI is None:
            raise ImportError(
                "llama-index-llms-openai is not installed. Install it with: pip install llama-index-llms-openai"
            )

        return OpenAI(
            api_key=api_key,
            temperature=temperature,
            model="gpt-3.5-turbo",
        )

    def generate_response(self, query: str) -> str:
        response = self.llm.complete(f"{self.prompt}\n\n{query}")
        return str(response)