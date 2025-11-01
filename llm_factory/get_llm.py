import sys, os
# ensure the project root is in sys.path so config can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llama_index.llms.ollama import Ollama
from config.settings import Settings

# Load environment settings
settings = Settings()
OLLAMA_URL = settings.OLLAMA_URL

# Module-level cache for LLM instances
_current_model_name = None
_current_llm_instance = None


def get_ollama_llm(model_name: str):
    """
    Returns a cached Ollama LLM instance if available, 
    otherwise creates and stores a new one.
    """
    global _current_model_name, _current_llm_instance

    if _current_model_name == model_name and _current_llm_instance is not None:
        return _current_llm_instance

    llm = Ollama(base_url=OLLAMA_URL, model=model_name)
    _current_model_name = model_name
    _current_llm_instance = llm
    return llm


# if __name__ == "__main__":
#     check_llm = get_ollama_llm(model_name="gemma2:2b")
#     print("✅ Ollama LLM instance created:", check_llm)
#     print("🔍 Instance type:", type(check_llm))
