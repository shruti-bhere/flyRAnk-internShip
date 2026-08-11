# AI PDF Report Generator & Billing Engine

An automated background billing and PDF report generation system built with **Next.js**, **Inngest**, and **Supabase**. It handles background event queuing, usage data fetching from PostgreSQL, dynamic PDF creation, and cloud storage upload.

---

## 🚀 What It Does (हा प्रोजेक्ट काय करतो?)

1. **User Request Processing:** User triggers report generation from the UI without blocking the main browser thread.
2. **Background Job Orchestration:** Inngest queues the task asynchronously to process heavy data operations safely.
3. **Data Aggregation:** Step 1 fetches usage metrics (metered units and billing totals) from PostgreSQL.
4. **PDF Generation & Cloud Storage:** Step 2 generates a formatted PDF report using `jsPDF` and uploads it to Supabase Storage (`reports` bucket).
5. **Scheduled Reports (Cron):** Automatically runs monthly batch billing jobs via scheduled CRON triggers (`0 0 1 * *`).

---

## 🛠️ Tech Stack (काय वापरले आहे?)

* **Framework:** Next.js 14 (App Router, TypeScript)
* **Background Jobs & Workflow:** Inngest
* **Database & Storage:** Supabase (PostgreSQL & Supabase Storage)
* **PDF Library:** jsPDF
* **Styling:** Tailwind CSS

---

## ⚙️ How To Run / Getting Started (कसे सुरु करायचे?)

### 1. Prerequisites
Ensure you have Node.js (v18+) and npm installed.

### 2. Clone & Install Dependencies
```bash
git clone <your-repository-url>
cd ai-pdf-report-generator
npm install