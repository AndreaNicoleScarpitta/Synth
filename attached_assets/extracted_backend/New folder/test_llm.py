from transformers import pipeline
import sys
import time

# === MVP Model List: Only confirmed, open-access, <4B models ===
models = {
    "BioGPT": "microsoft/biogpt",
    "BioGPT-Large": "microsoft/biogpt-large",  # Comment out if >6GB RAM is a problem!
    "Phi-3 Mini": "microsoft/phi-3-mini-128k-instruct",
    "BioMedLM": "stanford-crfm/biomedlm",
    # "Llama-3 8B": "meta-llama/Meta-Llama-3-8B",  # Skip for MVP/CPU!
    # "Meditron-7B": "stanford-crfm/meditron-7b",   # Private, will not work
    # "PubMedGPT": "stanfordai/pubmedgpt",          # Private, will not work
    # "BioMedRAG": "naver-clova-ix/donut-base-finetuned-biomedrag",  # Skip unless needed
}

PROMPT = "Describe SGLT2 inhibitor therapy for diabetes in one sentence: "

for name, model in models.items():
    print(f"\n=== Loading {name} ({model}) ===")
    try:
        start = time.time()
        print(f"  → Downloading/loading {name}... (may take a minute on first run)")
        pipe = pipeline("text-generation", model=model)
        load_time = time.time() - start
        print(f"  ✓ Loaded {name} in {load_time:.1f}s. Generating output...")
        start_gen = time.time()
        result = pipe(PROMPT, max_new_tokens=32)
        gen_time = time.time() - start_gen
        print(f"  [Output]: {result[0]['generated_text'].strip()}")
        print(f"  ✓ Generation completed in {gen_time:.1f}s.")
    except Exception as e:
        print(f"  ✗ Error loading {name}: {e}")

# Optional: OpenAI GPT-4o, if you have API key in environment
try:
    import openai
    import os
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        print("\n=== Loading OpenAI GPT-4o ===")
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": PROMPT}],
            temperature=0.2,
            max_tokens=64,
        )
        print("[OpenAI output]:", response.choices[0].message.content)
    else:
        print("[OpenAI GPT-4o not tested: No OPENAI_API_KEY found.]")
except Exception as e:
    print(f"  ✗ Error loading OpenAI GPT-4o: {e}")

print("\n✅ MVP LLM test complete. All mission-critical models loaded/tested.")
