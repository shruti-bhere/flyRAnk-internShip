import { NextResponse } from "next/server";
import { inngest } from "@/inngest/client";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { nodes, edges, startNodeId, context } = body;

    const run = await inngest.send({
      name: "workflow/execute",
      data: { nodes, edges, startNodeId, context },
    });

    return NextResponse.json({ success: true, eventId: run.ids[0] });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}