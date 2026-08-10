import { NextResponse } from "next/server";

export async function GET(
  _req: Request,
  { params }: { params: { eventId: string } }
) {
  try {
    const eventId = params.eventId;

    const res = await fetch(
      `http://127.0.0.1:8288/v1/events/${eventId}/runs`,
      { cache: "no-store" }
    );

    if (!res.ok) {
      return NextResponse.json({ status: "pending", history: [] });
    }

    const data = await res.json();
    const run = data?.data?.[0];

    if (!run) {
      return NextResponse.json({ status: "pending", history: [] });
    }

    return NextResponse.json({
      status: run.status,
      history: run.output?.history || [],
    });
  } catch {
    return NextResponse.json({ status: "pending", history: [] });
  }
}