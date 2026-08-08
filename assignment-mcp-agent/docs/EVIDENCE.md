# MCP Execution Evidence

## Task 1: Local File System Inspection (`mcp/filesystem`)
* **Prompt:** "Read `docs/EXPLAINER.md` and list all headings."
* **Tool Call Executed:** `read_file(path="docs/EXPLAINER.md")`
* **Output:** Successfully extracted text directly from local storage without manual copy-paste.

## Task 2: Live System / Environment Query
* **Prompt:** "Fetch system memory and current process runtime."
* **Tool Call Executed:** `get_system_stats()`
* **Output:** Returned active system memory and active Python process state.

## Task 3: Local Directory Search & Aggregation
* **Prompt:** "Find all PDF files in `data/inputs` and summarize file sizes."
* **Tool Call Executed:** `list_directory(path="data/inputs")`
* **Output:** Dynamically read the OS folder structure and reported local file metadata.