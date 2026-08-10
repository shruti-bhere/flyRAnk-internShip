"use client";

import React from "react";
import { Handle, Position, type Node, type NodeProps } from "@xyflow/react";

export type DecisionNodeData = {
  label: string;
  prompt: string;
  status?: "pending" | "running" | "completed";
  result?: "YES" | "NO";
};

export type DecisionNodeType = Node<DecisionNodeData, "decisionNode">;

export function DecisionNode({ data, selected }: NodeProps<DecisionNodeType>) {
  return (
    <div
      className={`w-64 bg-slate-900 border-2 rounded-xl p-4 text-white shadow-xl transition-all ${
        selected ? "ring-2 ring-indigo-500 ring-offset-2 ring-offset-slate-950" : ""
      } ${
        data.status === "running"
          ? "border-amber-400 animate-pulse"
          : data.status === "completed"
          ? "border-emerald-500"
          : "border-slate-700"
      }`}
    >
      <Handle type="target" position={Position.Top} className="!bg-slate-400 !w-3 !h-3" />
      
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <span className="text-[10px] font-bold tracking-widest text-slate-400 uppercase">
          {data.label || "Decision Node"}
        </span>
        {data.result && (
          <span
            className={`px-2 py-0.5 rounded text-[10px] font-black ${
              data.result === "YES" ? "bg-emerald-500/20 text-emerald-400" : "bg-rose-500/20 text-rose-400"
            }`}
          >
            {data.result}
          </span>
        )}
      </div>

      <p className="mt-3 text-xs text-slate-300 font-medium leading-relaxed">{data.prompt}</p>

      <div className="flex justify-between text-[10px] text-slate-500 mt-4 px-2">
        <span className="text-emerald-400 font-bold">YES</span>
        <span className="text-rose-400 font-bold">NO</span>
      </div>
      <Handle type="source" position={Position.Bottom} id="yes" style={{ left: "25%" }} className="!bg-emerald-500 !w-3 !h-3" />
      <Handle type="source" position={Position.Bottom} id="no" style={{ left: "75%" }} className="!bg-rose-500 !w-3 !h-3" />
    </div>
  );
}