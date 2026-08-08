# 📄 Assignment Walkthrough & Submission Document

**Project:** Source-Grounded AI Research & Document Processing Pipeline  
**Model:** Groq API (`llama-3.3-70b-versatile`)  
**Execution Platform:** Local Python Environment  

---

## 1. System Architecture & Workflow Diagram

The pipeline automates research and brief creation by breaking down document processing into 3 distinct, sequential steps:

```text
[Input PDF] 
     │
     ▼
 Step 1: Text Extraction & Key Point Gathering           
 (pypdf + Groq llama-3.3-70b)                            
                │ Key Takeaways
                ▼

 Step 2: Synthesis & Structured Study Brief Drafting  
 (Groq llama-3.3-70b)                                    

                │ Draft Report
                ▼

  Step 3: Editorial Audit, Risk Flagging & Formatting  
  (Groq llama-3.3-70b)                                    
                │
                ▼
     [Output Markdown (.md)]