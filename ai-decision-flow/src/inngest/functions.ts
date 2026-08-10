import { inngest } from "./client";
import { groq } from "@/lib/groq";

interface WorkflowNode {
  id: string;
  data: {
    prompt: string;
  };
}

interface WorkflowEdge {
  source: string;
  target: string;
  sourceHandle: string;
}

interface WorkflowEventData {
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  startNodeId: string;
  context: string;
}

export const executeWorkflow = inngest.createFunction(
  { id: "execute-ai-decision-workflow" },
  { event: "workflow/execute" },
  async ({ event, step }) => {
    const { nodes, edges, startNodeId, context } = event.data as WorkflowEventData;

    let currentNodeId: string | null = startNodeId;
    const executionHistory: Array<{
      nodeId: string;
      prompt: string;
      decision: "YES" | "NO";
    }> = [];

    while (currentNodeId) {
      const activeNodeId: string = currentNodeId;
      const node = nodes.find((n) => n.id === activeNodeId);

      if (!node) break;

      // Execute Groq API call as a durable step
      const decision = await step.run(`eval-node-${activeNodeId}`, async () => {
        const response = await groq.chat.completions.create({
          model: "llama-3.3-70b-versatile",
          messages: [
            {
              role: "system",
              content:
                "You are an AI decision node. Output JSON ONLY with format: {\"decision\": \"YES\"} or {\"decision\": \"NO\"}.",
            },
            {
              role: "user",
              content: `Input Context: "${context}"\nQuestion: "${node.data.prompt}"`,
            },
          ],
          response_format: { type: "json_object" },
          temperature: 0,
        });

        const rawContent = response.choices[0]?.message?.content || "{}";
        const parsed = JSON.parse(rawContent);
        return parsed.decision === "YES" ? "YES" : "NO";
      });

      executionHistory.push({
        nodeId: activeNodeId,
        prompt: node.data.prompt,
        decision,
      });

      // Find the edge matching the output decision handle
      const matchingEdge = edges.find(
        (e) =>
          e.source === activeNodeId &&
          e.sourceHandle?.toLowerCase() === decision.toLowerCase()
      );

      currentNodeId = matchingEdge ? matchingEdge.target : null;
    }

    return { status: "completed", history: executionHistory };
  }
);