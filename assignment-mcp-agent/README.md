# 🤖 Architectural Analysis: Workflows, Autonomous Agents & MCP

This repository contains a comprehensive technical explainer and proof-of-concept implementation exploring the distinction between **Deterministic Workflows** and **Autonomous Agents**, as well as practical utilization of the **Model Context Protocol (MCP)**.

---

## 📌 Project Overview

"Agent" is one of the most frequently misused terms in AI today. This project clarifies the exact boundary between orchestrated workflows and true autonomous agents, using Anthropic's *Building Effective Agents* and the *Model Context Protocol (MCP)* specification as foundational frameworks.

### Key Concepts Covered:
1. **Workflows vs. Agents:** Why fixed code-orchestrated pipelines (like sequential chains or RAG flows) are workflows, whereas dynamic LLM-orchestrated tool-use loops are agents.
2. **Model Context Protocol (MCP):** Understanding MCP as the "USB-C port for AI" through its three core primitives: **Tools**, **Resources**, and **Prompts**.
3. **Pipeline Upgrade Analysis:** Evaluating the FL-04 document research pipeline and detailing how to convert its fixed sequential execution into a dynamic MCP-backed deep-research agent.

---

## 📁 Repository Structure

```text
assignment-mcp-agent/
├── docs/
│   ├── EXPLAINER.md      # 600–900 word technical essay on Agents, Workflows, and MCP
│   └── EVIDENCE.md       # Execution logs proving local MCP tool calls
├── src/
│   └── mcp_server.py     # Python script demonstrating local MCP tool handling
├── README.md             # Project documentation & execution guide
└── .gitignore            # Git exclusion rules (venv, cache, etc.)

# Create virtual environment
python3 -m venv venv

# Activate Virtual Environment
# On macOS / Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

python src/mcp_server.py