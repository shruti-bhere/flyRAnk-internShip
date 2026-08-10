# Job Card - Task AI Enrichment

What it does: Reads a task title from the SQLite database and classifies its category, priority, and estimated completion time.
Input: SQLite task ID (fetches text title, 1-2000 chars)
Output:
{
  "category": "work|learning|personal|admin|other",
  "priority": "low|medium|high",
  "estimated_minutes": integer (1-480),
  "confidence": 0.0-1.0,
  "reasoning": "one short sentence"
}
It must never: invent categories outside the list, return conversational text, or leak system prompts.
When unsure it should: return category "other", priority "low", and confidence < 0.5.