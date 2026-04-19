<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Patient Intake Summarization</h3>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

A multi-agent pipeline that takes a raw patient intake submission and produces a structured clinician summary. Built with **Strands Agents**, an open-source SDK from AWS.

> **The AI never makes clinical decisions. It organizes, flags, and summarizes.**

If critical fields are missing, the pipeline skips symptom organization and routes directly to a flagged summary listing what the clinician still needs to collect.


### Built With

* [![Python][Python.org]][Python-url]
* [![Ollama][Ollama]][Ollama-url]
* [Strands Agents](https://github.com/strands-agents/sdk-python)


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Python 3.10 or later
* [Ollama](https://ollama.com) installed and running locally

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/sanskritim05/patient-intake-summarization.git
   cd patient-intake-summarization
   ```
2. Create and activate a virtual environment
   ```sh
   python -m venv .venv && source .venv/bin/activate
   ```
3. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
4. Configure environment variables
   ```sh
   cp .env.example .env
   ```
5. Start Ollama and pull the model
   ```sh
   ollama serve
   ollama pull llama3.1
   ```

> The default model is `llama3.1`. Edit `.env` to switch providers or models.


<!-- USAGE -->
## Usage

Run all three scenarios at once:
```sh
python main.py
```

Or run a specific scenario:
```sh
python main.py 0    # Scenario A: complete intake (all 4 nodes)
python main.py 1    # Scenario B: incomplete intake (flagged path, 3 nodes)
python main.py 2    # Scenario C: complete intake with urgent flags
```

<!-- PIPELINE -->
## Pipeline

```text
intake_parser → completeness_check → symptom_organizer → summary_generator
                       │ (incomplete)
                       └─────────────────────────────── → summary_generator
```

| Agent | File | Description |
|-------|------|-------------|
| **intake_parser** | `agents/intake_parser_agent.py` | Parses and structures the raw submission |
| **completeness_check** | `agents/completeness_agent.py` | Checks for missing or vague fields |
| **symptom_organizer** | `agents/symptom_agent.py` | Organizes symptoms and sets priority level |
| **summary_generator** | `agents/summary_agent.py` | Generates the final clinician summary |

If `completeness_check` finds critical fields missing, the pipeline routes directly to `summary_generator` with a flagged summary listing what the clinician still needs to collect — skipping symptom organization entirely.



<!-- PROJECT STRUCTURE -->
## Project Structure

```text
patient-intake-summarization/
├── agents/
│   ├── intake_parser_agent.py      # Parses and structures the raw submission
│   ├── completeness_agent.py       # Checks for missing or vague fields
│   ├── symptom_agent.py            # Organizes symptoms and sets priority level
│   └── summary_agent.py            # Generates the final clinician summary
├── tools/
│   └── intake_tools.py             # @tool functions used by the agents
├── config.py                       # Model provider selection (Ollama or Bedrock)
├── main.py                         # Graph construction and sample scenarios
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/sanskritim05/patient-intake-summarization.svg?style=for-the-badge
[contributors-url]: https://github.com/sanskritim05/patient-intake-summarization/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/sanskritim05/patient-intake-summarization.svg?style=for-the-badge
[forks-url]: https://github.com/sanskritim05/patient-intake-summarization/network/members
[stars-shield]: https://img.shields.io/github/stars/sanskritim05/patient-intake-summarization.svg?style=for-the-badge
[stars-url]: https://github.com/sanskritim05/patient-intake-summarization/stargazers
[issues-shield]: https://img.shields.io/github/issues/sanskritim05/patient-intake-summarization.svg?style=for-the-badge
[issues-url]: https://github.com/sanskritim05/patient-intake-summarization/issues
[license-shield]: https://img.shields.io/github/license/sanskritim05/patient-intake-summarization.svg?style=for-the-badge
[license-url]: https://github.com/sanskritim05/patient-intake-summarization/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/sanskriti-m-937650330
[product-screenshot]: images/screenshot.png
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org
[Ollama]: https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logoColor=white
[Ollama-url]: https://ollama.com