"""
config.py - Model provider setup for the Strands Loan Application demo.

Supports two providers:
  • Ollama         (default, local model served by Ollama)
  • AWS Bedrock    (optional, set USE_BEDROCK=true plus standard AWS credentials)
"""

import os
from dotenv import load_dotenv

load_dotenv()


def get_model():
    """Return a Strands model instance based on environment configuration."""

    use_bedrock = os.getenv("USE_BEDROCK", "false").lower() == "true"

    if use_bedrock:
        from strands.models import BedrockModel

        model_id = os.getenv(
            "BEDROCK_MODEL_ID", "anthropic.claude-sonnet-4-20250514-v1:0"
        )
        region = os.getenv("AWS_REGION", "us-east-1")
        print(f"[config] Using AWS Bedrock — model: {model_id} | region: {region}")
        return BedrockModel(model_id=model_id, region_name=region)

    # Default: Ollama
    from strands.models.ollama import OllamaModel

    model_id = os.getenv("OLLAMA_MODEL", "llama3.1")
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    return OllamaModel(
        host=host,
        model_id=model_id,
        max_tokens=4096,
    )
