from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, api_key: str, prompt: str, temperature: float = 0.0):
        self.api_key = api_key
        self.prompt = prompt
        self.temperature = temperature
        self.llm = self.connect(api_key, temperature)

    @abstractmethod
    def connect(self, api_key: str, temperature: float):
        """
        Establish a connection with the LLM provider.
        """
        pass

    @abstractmethod
    def generate_response(self, query: str) -> str:
        """
        Generate text from the LLM.
        """
        pass