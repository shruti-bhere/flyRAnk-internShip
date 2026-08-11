import { inngest } from "./client";
import { fetchBillingUsageData } from "@/lib/reports";
import { generateAndUploadPDF } from "@/lib/pdf";
import { db } from "@/lib/db";

export const processReportJob = inngest.createFunction(
  { id: "generate-billing-report" },
  [
    { event: "reports/generate.requested" },
    { cron: "0 0 1 * *" }
  ],
  async ({ event, step }: { event: any; step: any }) => {
    const eventData = event.data as Record<string, any> | undefined;
    const userId = eventData?.userId || "system_batch_user";
    const reportId = (event as any).id || `cron-${Date.now()}`;

    // Step 1: SQL Query
    const usageData = await step.run("fetch-metering-data", async () => {
      return await fetchBillingUsageData(userId);
    });

    // Step 2: Render PDF & Upload
    const artifactKey = await step.run("render-and-store-pdf", async () => {
      return await generateAndUploadPDF(reportId, usageData);
    });

    // Step 3: DB Record Update
    await step.run("save-report-record", async () => {
      try {
        await db.query(
          `INSERT INTO generated_reports (id, user_id, artifact_key, status)
           VALUES ($1, $2, $3, 'COMPLETED')
           ON CONFLICT (id) DO UPDATE 
           SET artifact_key = EXCLUDED.artifact_key, status = EXCLUDED.status`,
          [reportId, userId, artifactKey]
        );
      } catch (err) {
        console.error("DB Record insert error:", err);
      }
    });

    return { success: true, reportId, artifactKey };
  }
);