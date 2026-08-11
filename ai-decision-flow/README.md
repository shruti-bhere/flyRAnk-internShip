# AI Decision Flow

An interactive, visual AI workflow engine built with Next.js 14, React Flow, Groq AI, and Inngest. This project allows users to evaluate complex decision trees step-by-step using high-speed AI inference and durable background job execution.

---

## Features

* Visual Workflow Canvas: Interactive node graph powered by React Flow for displaying complex decision paths.
* Ultra-Fast AI Reasoning: Automated binary YES/NO decision evaluation using Groq API (Llama 3.3).
* Durable Background Execution: State orchestration and failure-proof step execution handled by Inngest.
* Real-Time UI Updates: Dynamic visual indicators that highlight nodes as they transition between pending, processing, and completed states.
* Full Event Tracing: Complete trace histories and step-level logs available through the local Inngest Dev Server dashboard.

---

## Tech Stack

* Next.js 14 (App Router): Core framework for frontend rendering and backend API routes.
* React Flow (@xyflow/react): Graph visualization library for rendering decision nodes and edges.
* SDK: High-performance LLM provider used for rapid binary evaluation.
* Inngest: Event-driven orchestration engine for step-based background workflow execution.
* Tailwind CSS: Modern styling framework for node states and dark theme interface.
* TypeScript: End-to-end type safety for API requests, parameters, and workflow payloads.

---

## How the Workflow Works

The system operates on an event-driven architecture designed to process dynamic prompts without blocking the user interface:

1. User Initiation: The user enters a context message in the UI top bar and clicks the execution button.
2. Event Dispatch: A POST request hits the Next.js API endpoint `/api/workflow/run`, which dispatches a `workflow/execute` event to Inngest.
3. Step-by-Step AI Evaluation:** Inngest picks up the workflow and evaluates nodes sequentially starting from the root classifier node. For each node, it sends the current context to Groq LLM, which returns a structured binary response (YES or NO).
4. Path Traversal: Based on the AI response, the workflow engine follows the matching edge to the next child node (e.g., branching into Emergency Path or Standard Path).
5. Frontend Polling: The Next.js frontend periodically requests status updates from `/api/workflow/status/[eventId]` to illuminate active nodes on the canvas in real time.

---

## Getting Started

### 1. Prerequisites

* Node.js: Version 18.0.0 or higher.
* Groq API Key: Obtain a valid API key from the Groq console.

### 2. Environment Configuration

Create a `.env.local` file in the root directory of the project and add your API key:

```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
npm install
Access the frontend at http://localhost:3000.

Terminal 1: Next.js Web Server
npm run dev

Terminal 2: Inngest Engine
npx inngest-cli@latest dev
http://localhost:8288
