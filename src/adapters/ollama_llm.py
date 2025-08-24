from llm_interface import BaseLLM
from ollama import Client


class OllamaLLM(BaseLLM):
    def __init__(self, model_name="mistral"):
        self.client = Client(host='http://localhost:11434')
    
    def generate(self, prompt: str) -> str:
        response = self.client.generate(prompt)
        return response['content']