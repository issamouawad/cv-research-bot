from llm_interface import BaseLLM

class LangExtractLLMWrapper:
    """
    Wraps any BaseLLM adapter to work with LangExtract.
    """
    def __init__(self, llm_adapter: BaseLLM):
        self.llm_adapter = llm_adapter

    def __call__(self, prompt: str) -> str:
        return self.llm_adapter.generate(prompt)