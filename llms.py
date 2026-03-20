from smolagents import LiteLLMModel,InferenceClientModel,OpenAIModel
import os
from dotenv import load_dotenv
import litellm

load_dotenv()

minimax_27 = OpenAIModel(
    model_id="minimax/minimax-m2.7",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    api_base="https://openrouter.ai/api/v1",
    temperature=0.1,
    max_tokens=2048,
)

minimax_25 = OpenAIModel(
    model_id="minimax/minimax-m2.5",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    api_base="https://openrouter.ai/api/v1",
    temperature=0.1,
    max_tokens=2048,
)

z_ai_glm_47flash = OpenAIModel(
    model_id="z-ai/glm-4.7-flash",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    api_base="https://openrouter.ai/api/v1",
    temperature=0.1,
    max_tokens=2048,
)

step_35flash = OpenAIModel(
    model_id="stepfun/step-3.5-flash",
    api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    temperature=0.1,
    max_tokens=2048,
)

deepseek_v32 = OpenAIModel(
    model_id="deepseek/deepseek-v3.2",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    api_base="https://openrouter.ai/api/v1",
    temperature=0.1,
    max_tokens=2048,
)

kimi_k25 = OpenAIModel(
    model_id="moonshotai/kimi-k2.5",
    api_key=os.getenv("OPENROUTER_KEY", ""),
    api_base="https://openrouter.ai/api/v1",
    temperature=0.1,
    max_tokens=2048,
)

# qwen25_model = LiteLLMModel(
#     model_id="ollama_chat/qwen2.5-coder:3b",  # Example
#     api_base="http://localhost:11434",
#     # api_key="ollama",
#     # provider="ollama",        
#     # max_tokens=2048,
#     # temperature=0.1,   
# )

# gemma_model = LiteLLMModel(
#     model_id="ollama_chat/gemma3:4b",  # Example
#     api_base="http://localhost:11434",
#     # api_key="ollama",
#     # provider="ollama",        
#     # max_tokens=2048,        
#     # temperature=0.1,
# )

# hf_model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

# litellm._turn_on_debug()