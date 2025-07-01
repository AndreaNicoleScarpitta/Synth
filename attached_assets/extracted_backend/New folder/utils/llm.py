# utils/llm.py

from typing import Literal, Optional
import os

# Optional imports (delay loading if needed)
try:
    from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
except ImportError:
    pipeline = None

try:
    import openai
except ImportError:
    openai = None


# Define supported models
SUPPORTED_MODELS = {
    "gpt-4": "openai",
    "gpt-3.5-turbo": "openai",
    "biogpt": "hf",
    "pubmedgpt": "hf",
    "llama-2": "hf",
    "mistral-med": "hf",
    "medpalm": "hf"
}


def ask_llm(
    prompt: str,
    model_name: str = "gpt-4",
    max_tokens: int = 300,
    temperature: float = 0.7,
    stop: Optional[list] = None
) -> str:
    """
    Main entry point for any LLM call.
    Automatically routes to Hugging Face or OpenAI backend.
    """
    backend = SUPPORTED_MODELS.get(model_name.lower())

    if backend == "openai":
        return _ask_openai(prompt, model_name, max_tokens, temperature, stop)
    elif backend == "hf":
        return _ask_huggingface(prompt, model_name, max_tokens, temperature)
    else:
        raise ValueError(f"Unsupported model: {model_name}")


# -------------------
# 🧠 OpenAI (GPT-4, GPT-3.5)
# -------------------

def _ask_openai(prompt, model_name, max_tokens, temperature, stop):
    if openai is None:
        raise ImportError("OpenAI SDK not installed. Run: pip install openai")

    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise EnvironmentError("Missing OPENAI_API_KEY in environment")

    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            stop=stop,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"❌ OpenAI error: {e}"


# -------------------
# 🤖 Hugging Face (BioGPT, PubMedGPT, LLaMA, etc.)
# -------------------

_cached_hf_pipelines = {}

def _ask_huggingface(prompt, model_name, max_tokens, temperature):
    if pipeline is None:
        raise ImportError("transformers not installed. Run: pip install transformers")

    model_lookup = {
        "biogpt": "microsoft/BioGPT",
        "pubmedgpt": "stanford-crfm/pubmedgpt",
        "llama-2": "meta-llama/Llama-2-7b-chat-hf",
        "mistral-med": "epfl-llm/mistral-med",
        "medpalm": "google/medpalm-2"  # placeholder
    }

    hf_model = model_lookup.get(model_name.lower())
    if not hf_model:
        raise ValueError(f"No HF model mapping for {model_name}")

    if model_name not in _cached_hf_pipelines:
        tokenizer = AutoTokenizer.from_pretrained(hf_model)
        model = AutoModelForCausalLM.from_pretrained(hf_model)
        _cached_hf_pipelines[model_name] = pipeline(
            "text-generation", model=model, tokenizer=tokenizer
        )

    gen = _cached_hf_pipelines[model_name](prompt, max_length=max_tokens, do_sample=True, temperature=temperature)
    return gen[0]["generated_text"].strip()
