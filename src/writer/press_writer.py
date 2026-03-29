from src.base_agent.base_agent import BaseAgent

class Writer:
    def __init__(self, llm: BaseAgent, writer_type: str):
        self.writer_type = writer_type
        self.llm = llm

    def write(self, rag_context: str = ""):
        return self.llm.generate_response(rag_context)