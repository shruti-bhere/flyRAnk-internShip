"use client";

import { useState } from "react";

export default function HomePage() {
  const [userId, setUserId] = useState("user_123");
  const [loading, setLoading] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateReport = async () => {
    setLoading(true);
    setError(null);
    setJobId(null);

    try {
      const response = await fetch("/api/reports/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to trigger report generation");
      }

      setJobId(data.jobId);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-900 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="max-w-md w-full bg-slate-800 rounded-xl border border-slate-700 p-8 shadow-xl">
        <h1 className="text-2xl font-bold text-white mb-2">
          PDF Report Generator
        </h1>
        <p className="text-slate-400 text-sm mb-6">
          Query user metering data, render a PDF report, and store the artifact via Inngest background jobs.
        </p>

        <div className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              User ID
            </label>
            <input
              type="text"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-200 focus:outline-none focus:border-blue-500 text-sm"
              placeholder="Enter User ID"
            />
          </div>

          <button
            onClick={handleGenerateReport}
            disabled={loading || !userId}
            className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-medium py-2.5 rounded-lg transition-colors text-sm flex items-center justify-center space-x-2"
          >
            {loading ? (
              <span>Triggering Inngest Job...</span>
            ) : (
              <span>Generate PDF Report</span>
            )}
          </button>
        </div>

        {jobId && (
          <div className="mt-6 p-4 bg-emerald-950/50 border border-emerald-500/30 rounded-lg">
            <p className="text-emerald-400 text-xs font-semibold uppercase tracking-wider">
              Background Job Queued
            </p>
            <p className="text-slate-300 text-xs font-mono mt-1 break-all">
              Job Event ID: {jobId}
            </p>
            <p className="text-slate-400 text-xs mt-2">
              Check Inngest Dashboard at <code className="text-blue-400">localhost:8288</code> to trace execution.
            </p>
          </div>
        )}

        {error && (
          <div className="mt-6 p-4 bg-rose-950/50 border border-rose-500/30 rounded-lg">
            <p className="text-rose-400 text-xs font-semibold uppercase tracking-wider">
              Error
            </p>
            <p className="text-rose-300 text-xs mt-1">{error}</p>
          </div>
        )}
      </div>
    </main>
  );
}