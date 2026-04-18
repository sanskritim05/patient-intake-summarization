# Patient Intake Summarization - Strands Agents Demo

A multi-agent pipeline that takes a raw patient intake submission and produces a structured clinician summary. Built with [Strands Agents](https://strandsagents.com/), an open-source SDK from AWS.

The AI never makes clinical decisions. It organizes, flags, and summarizes.

---

## Pipeline

```
intake_parser → completeness_check → symptom_organizer → summary_generator
                        │ (incomplete)
                        └──────────────────────────────→ summary_generator
```

If critical fields are missing, the pipeline skips symptom organization and routes directly to a flagged summary listing what the clinician still needs to collect.

---

## Project Structure

```
agents/
  intake_parser_agent.py      — parses and structures the raw submission
  completeness_agent.py       — checks for missing or vague fields
  symptom_agent.py            — organizes symptoms and sets priority level
  summary_agent.py            — generates the final clinician summary
tools/
  intake_tools.py             — @tool functions used by the agents
config.py                     — model provider selection (Ollama or Bedrock)
main.py                       — graph construction and sample scenarios
```

---

## Setup

**Requirements:** Python 3.10+, [Ollama](https://ollama.com/) installed and running locally.

```bash
git clone https://github.com/sanskritim05/agentic-ai-loan-application
cd agentic-ai-loan-application

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env if needed (default model: llama3.1)

ollama serve
ollama pull llama3.1
```

---

## Usage

```bash
python main.py      # run all three scenarios

python main.py 0    # Scenario A — complete intake (all 4 nodes)
python main.py 1    # Scenario B — incomplete intake (flagged path, 3 nodes)
python main.py 2    # Scenario C — complete intake with urgent flags
```

---

## Using AWS Bedrock

Set the following in your `.env`:

```
USE_BEDROCK=true
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-20250514-v1:0
AWS_REGION=us-east-1
```

Standard AWS credentials must be configured (`~/.aws/credentials` or environment variables). The graph code is identical — only the model provider changes.

---

## Dependencies

- [strands-agents](https://github.com/strands-agents/sdk-python) — agent framework and GraphBuilder
- [python-dotenv](https://github.com/theskumar/python-dotenv) — environment variable loading
