# 🚀 AI Research & Document Processing Pipeline

An automated, multi-step LLM pipeline built using **Python**, **Groq API (`llama-3.3-70b-versatile`)**, and **pypdf**. The system ingests PDF documents, extracts core themes, synthesizes structured study notes, and conducts an automated editorial review with human-in-the-loop audit flags.

---

## 📌 Project Overview

Single-prompt AI interactions save minutes, but structured workflows save hours. This project automates document research and report drafting by chaining **3 distinct steps** into a continuous pipeline:

1. **Step 1: Gather & Extract:** Extracts raw text from input PDFs and generates key concepts and themes.
2. **Step 2: Synthesize & Draft:** Takes extracted takeaways and expands them into a structured executive brief.
3. **Step 3: Review & Format:** Audits the draft for logical flow, identifies potential hallucination risks, and exports clean Markdown.

---

## 🛠️ Tech Stack & Requirements

* **Programming Language:** Python 3.10+
* **LLM Engine:** Groq API (`llama-3.3-70b-versatile`)
* **Libraries Used:** `groq`, `pypdf`, `python-dotenv`

---

## 📁 Repository Structure

```text
ai-research-pipeline/
├── data/
│   ├── inputs/               # Place your input PDF files here
│   └── outputs/              # Output Markdown files (run_1_output.md, etc.)
├── src/
│   └── pipeline.py           # Consolidated pipeline script (Steps 1 -> 2 -> 3)
├── .env                      # API keys and configuration (Git-ignored)
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
 
Use Groq API

cd ai-research-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/pipeline.py