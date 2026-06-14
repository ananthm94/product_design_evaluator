from langchain_openai import ChatOpenAI
from config.settings import OPENROUTER_BASE_URL, DEFAULT_LLM_MODEL


def get_llm(api_key: str, model: str = DEFAULT_LLM_MODEL, temperature: float = 0.3) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        temperature=temperature,
        model_kwargs={"response_format": {"type": "json_object"}},
    )
