# BeeAI Framework (workshop / live coding)

This repository contains scripts and code samples created live during a TechXChange session.

> **TIP:** To learn more, visit the [BeeAI Framework repository](https://github.com/i-am-bee/beeai-framework/).

---

## 🛠️ Requirements

- **Python** >= 3.11
- **[Poetry](https://python-poetry.org/)** (for dependency management)
- **[Ollama](https://ollama.com/)** (for running local LLMs)

---

## ⚡ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/i-am-bee/beeai-framework-workshop.git
cd beeai-framework-workshop

# Install Python dependencies
poetry install

# Download the required LLM model
ollama pull granite3.3:8b
```

## 🏃 Usage

Run any of the example scripts:

```
python src/name_of_the_file.py
```

Replace `name_of_the_file.py` with the script you want to try.

## 🗺️ Where to Start?

Explore these key files to understand the framework:

- `src/llms.py` — LLMs
- `src/tools.py` — Tools
- `src/agents` — Agents
- `src/workflow.py` — Workflows