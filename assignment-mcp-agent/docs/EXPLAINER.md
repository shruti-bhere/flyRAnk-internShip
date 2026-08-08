# Architectural Analysis: Workflows, Autonomous Agents, and the Model Context Protocol (MCP)

## 1. Workflows vs. Autonomous Agents

The AI industry frequently conflates "workflows" with "autonomous agents." However, Anthropic's *Building Effective Agents* establishes a clear boundary based on control flow and dynamic decision-making.

* **Workflows** are deterministic systems where Large Language Models (LLMs) operate within predefined code structures, control logic, and state transitions. In a workflow, programmatic logic dictates which prompt executes, in what sequence, and under what conditions. While individual LLM steps involve non-deterministic text generation, the orchestration remains static. Common workflow patterns include sequential chaining, parallel routing, evaluator-optimizer loops, and orchestrator-subworker patterns.

* **Autonomous Agents**, by contrast, operate under dynamic self-direction. Given a high-level user goal, an agent autonomously determines its execution path. It evaluates environment feedback, decides which external tools to invoke, dynamically generates sub-goals, and loops iteratively until it determines that the task is complete. Control logic resides inside the LLM rather than external code.

### Classification of the FL-04 Pipeline
The FL-04 document research pipeline is strictly a **Workflow (Sequential Chain)**, not an agent. It executes three hardcoded stages in lockstep:
1. **Step 1 (Gather & Extract):** Ingests raw PDF text and extracts key points using `pypdf` and Groq.
2. **Step 2 (Synthesize & Draft):** Transforms key points into an executive brief.
3. **Step 3 (Editorial Audit):** Reviews the brief for hallucinations and exports Markdown.

Because Step 1 always flows to Step 2, and Step 2 always flows to Step 3 regardless of intermediate output nuances, the control flow is entirely hardcoded. The pipeline cannot decide to re-read the PDF if information is missing or skip Step 3 if confidence is high. It is a highly reliable workflow, but not an agent.

---

## 2. Model Context Protocol (MCP) Demystified

Model Context Protocol (MCP) is an open standard designed by Anthropic that acts as a universal interface between AI applications (clients) and local or remote data stores/tools (servers). Often described as the "USB-C port for AI," MCP replaces brittle, custom API integrations with a standardized protocol.

MCP defines three primary architectural primitives:
* **Tools:** Callable functions exposed by the MCP server that allow the model to take actions or fetch real-time state (e.g., executing SQL queries, reading local directories, or invoking third-party web services).
* **Resources:** Passive, data-attached context exposed to the client (e.g., local files, database schemas, or system logs) that the model can inspect as context without execution side-effects.
* **Prompts:** Pre-configured template routines supplied by the server to guide user interaction and optimize tool execution.

---

## 3. Transforming FL-04 into a True Autonomous Agent

To transform the static FL-04 sequential workflow into an autonomous research agent, we must decouple the fixed 3-step loop and introduce a dynamic **ReAct (Reasoning + Acting)** execution loop backed by MCP tools.

### Concrete Agent Upgrade: Dynamic Deep-Research Loop with MCP Search & File Server
Currently, FL-04 fails on complex multi-document synthesis because it reads fixed text snippets once. In an upgraded agentic version:

1. **MCP Tool Integration:** The agent is supplied with MCP server tools: `mcp/file_system` (to read/write workspace documents) and `mcp/web_search` (to query live external databases).
2. **Dynamic Decision Loop:** Instead of executing Steps 1 → 2 → 3 sequentially, the agent is given a high-level objective: *"Draft a research brief on Document X and verify its key claims against live market data."*
3. **Autonomous Execution Path:**
   * The agent calls `read_file` via MCP to inspect the local document.
   * If it detects missing context or unverified data, it autonomously decides to execute a web search tool call (`search_web`).
   * It evaluates the search results. If unsatisfied, it formulates a refined query and re-executes tool calls.
   * Only when its internal evaluation criteria are met does it call `write_file` to save the final Markdown report.

By moving from a hardcoded execution chain to an environment-driven tool loop, the system transitions from a deterministic workflow to a resilient agent.