"use client";

import React, { useState, useCallback } from "react";
import {
  ReactFlow,
  Controls,
  Background,
  applyNodeChanges,
  applyEdgeChanges,
  addEdge,
  Edge,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
} from "@xyflow/react";
import { DecisionNode, DecisionNodeType } from "./nodes/DecisionNode";

const nodeTypes = { decisionNode: DecisionNode };

const initialNodes: DecisionNodeType[] = [
  {
    id: "node-1",
    type: "decisionNode",
    position: { x: 300, y: 50 },
    data: { label: "Classifier", prompt: "Does the user express urgency or distress in their message?" },
  },
  {
    id: "node-2",
    type: "decisionNode",
    position: { x: 100, y: 280 },
    data: { label: "Emergency Path", prompt: "Is this request related to server downtime or outages?" },
  },
  {
    id: "node-3",
    type: "decisionNode",
    position: { x: 500, y: 280 },
    data: { label: "Standard Path", prompt: "Is the user inquiring about pricing or billing?" },
  },
];

const initialEdges: Edge[] = [
  { id: "e1-2", source: "node-1", target: "node-2", sourceHandle: "yes", label: "YES", animated: true },
  { id: "e1-3", source: "node-1", target: "node-3", sourceHandle: "no", label: "NO", animated: true },
];

export default function FlowEditor() {
  const [nodes, setNodes] = useState<DecisionNodeType[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [inputContext, setInputContext] = useState("OUR PROD SERVER IS DOWN HELP IMMEDIATELY!");
  const [isExecuting, setIsExecuting] = useState(false);

  const onNodesChange: OnNodesChange<DecisionNodeType> = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );

  const onEdgesChange: OnEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );

  const onConnect: OnConnect = useCallback(
    (params) => setEdges((eds) => addEdge({ ...params, label: params.sourceHandle?.toUpperCase() }, eds)),
    []
  );

  const pollExecution = (eventId: string) => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`/api/workflow/status/${eventId}`);
        const data = await res.json();

        if (data.history && data.history.length > 0) {
          setNodes((nds) =>
            nds.map((node) => {
              const matchedStep = data.history.find((h: any) => h.nodeId === node.id);
              if (matchedStep) {
                return {
                  ...node,
                  data: { ...node.data, status: "completed", result: matchedStep.decision },
                };
              }
              return node;
            })
          );
        }

        if (data.status === "Completed" || data.status === "Failed") {
          clearInterval(interval);
          setIsExecuting(false);
        }
      } catch {
        clearInterval(interval);
        setIsExecuting(false);
      }
    }, 1000);
  };

  const runWorkflow = async () => {
    setIsExecuting(true);
    setNodes((nds) =>
      nds.map((node) => ({
        ...node,
        data: { ...node.data, status: "pending", result: undefined },
      }))
    );

    try {
      const res = await fetch("/api/workflow/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nodes,
          edges,
          startNodeId: "node-1",
          context: inputContext,
        }),
      });

      const { eventId } = await res.json();
      if (eventId) pollExecution(eventId);
    } catch {
      setIsExecuting(false);
    }
  };

  return (
    <div className="w-screen h-screen flex flex-col bg-slate-950 text-white overflow-hidden">
      <header className="p-4 border-b border-slate-800 flex items-center justify-between gap-4 bg-slate-900">
        <input
          type="text"
          value={inputContext}
          onChange={(e) => setInputContext(e.target.value)}
          placeholder="Enter execution context..."
          className="flex-1 bg-slate-950 border border-slate-700 px-4 py-2 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
        />
        <button
          onClick={runWorkflow}
          disabled={isExecuting}
          className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-semibold text-sm px-6 py-2 rounded-lg transition"
        >
          {isExecuting ? "Executing Flow..." : "Run Flow with Groq"}
        </button>
      </header>

      {/* Explicit Height Container for Canvas */}
      <div className="w-full h-[calc(100vh-73px)]">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          fitView
        >
          <Background color="#334155" gap={16} />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  );
}