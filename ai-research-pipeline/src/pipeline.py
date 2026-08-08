import os
import time
from dotenv import load_dotenv

load_dotenv()

from step1_gather import extract_text_from_pdf, step1_gather_keypoints
from step2_synthesize import step2_generate_draft
from step3_review import step3_review_and_format

def run_pipeline_on_file(file_path: str, output_path: str):
    start_time = time.time()
    print(f"[+] Starting Groq Pipeline for: {file_path}")
    
    # Extract Raw Text
    raw_text = extract_text_from_pdf(file_path)
    
    # Step 1
    print(" -> Running Step 1: Gathering Key Points...")
    keypoints = step1_gather_keypoints(raw_text)
    
    # Step 2
    print(" -> Running Step 2: Synthesizing Draft...")
    draft = step2_generate_draft(keypoints)
    
    # Step 3
    print(" -> Running Step 3: Reviewing & Formatting...")
    final_output = step3_review_and_format(draft)
    
    # Save Output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_output)
        
    elapsed = round(time.time() - start_time, 2)
    print(f"[✔] Completed in {elapsed}s. Saved to {output_path}\n")
    return elapsed

if __name__ == "__main__":
    input_dir = "data/inputs"
    output_dir = "data/outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    total_time = 0
    files = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]
    
    if not files:
        print(f"[!] No PDF files found in '{input_dir}'. Please add 5 PDF files to run the pipeline.")
    else:
        for idx, file_name in enumerate(files[:5], 1):
            pdf_path = os.path.join(input_dir, file_name)
            out_path = os.path.join(output_dir, f"run_{idx}_output.md")
            total_time += run_pipeline_on_file(pdf_path, out_path)
            
        print(f"All 5 runs finished via Groq in total {total_time} seconds!")