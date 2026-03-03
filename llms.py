from smolagents import LiteLLMModel,InferenceClientModel
import os
from dotenv import load_dotenv
import litellm

load_dotenv()

gemini_pro = LiteLLMModel(
    model_id="openrouter/google/gemini/gemini-2.5-pro",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemma_en4b = LiteLLMModel(
    model_id="openrouter/google/gemma-3-4b-it:free",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemma_27b = LiteLLMModel(
    model_id="openrouter/google/gemini/gemma-3-27b-it:free",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemini_25flash = LiteLLMModel(
    model_id="openrouter/google/gemini/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemini_25flash_lite = LiteLLMModel(
    model_id="openrouter/google/gemini/gemini-2.5-flash-lite",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemini_flash = LiteLLMModel(
    model_id="openrouter/google/gemini/gemini-2.0-flash",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemini_flash_lite = LiteLLMModel(
    model_id="openrouter/google/gemini/gemini-2.0-flash-lite",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemini_pro_second = LiteLLMModel(
    model_id="openrouter/google/gemini/gemini-2.5-pro",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemma_en4b_second  = LiteLLMModel(
    model_id="openrouter/google/gemma-3-4b-it:free",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemma_27b_second  = LiteLLMModel(
    model_id="openrouter/google/gemini/gemma-3-27b-it:free",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemini_25flash_second  = LiteLLMModel(
    model_id="openrouter/google/gemini/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemini_25flash_lite_second  = LiteLLMModel(
    model_id="openrouter/google/gemini/gemini-2.5-flash-lite",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemini_flash_second  = LiteLLMModel(
    model_id="openrouter/google/gemini/gemini-2.0-flash",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

gemini_flash_lite_second = LiteLLMModel(
    model_id="openrouter/google/gemini/gemini-2.0-flash-lite",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

op_llama4_model = LiteLLMModel(
    model_id="openrouter/meta-llama/llama-4-maverick",
    api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
)

op_qwen_3_model = LiteLLMModel(
    model_id="openrouter/qwen/qwen3-235b-a22b",
    api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
)

op_gemma3_model = LiteLLMModel( 
    model_id="openrouter/google/gemma-3-27b-it",
    api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
)

qwen25_model = LiteLLMModel(
    model_id="ollama_chat/qwen2.5-coder:3b",  # Example
    api_base="http://localhost:11434",
    # api_key="ollama",
    # provider="ollama",        
    # max_tokens=2048,
    # temperature=0.1,   
)

gemma_model = LiteLLMModel(
    model_id="ollama_chat/gemma3:4b",  # Example
    api_base="http://localhost:11434",
    # api_key="ollama",
    # provider="ollama",        
    # max_tokens=2048,        
    # temperature=0.1,
)

hf_model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

# litellm._turn_on_debug()