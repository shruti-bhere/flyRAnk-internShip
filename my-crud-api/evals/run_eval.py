import json
import os
import requests

# Fix: Plain string URL without markdown square brackets/parentheses
API_URL = "http://127.0.0.1:8000"


def run_evaluation():
  with open("evals/cases.json", "r") as f:
    cases = json.load(f)

  passed = 0
  total = len(cases)

  print(f"--- Running Evaluation ({total} cases) ---\n")

  for idx, test in enumerate(cases, 1):
    create_res = requests.post(
        f"{API_URL}/tasks", json={"title": test["input"]}
    )
    if create_res.status_code != 201:
      print(f"Case {idx}: FAILED to create task")
      continue

    task_id = create_res.json()["id"]
    enrich_res = requests.post(f"{API_URL}/tasks/{task_id}/enrich")

    if enrich_res.status_code == 200:
      result = enrich_res.json()
      predicted = result.get("category")
      expected = test["expected_category"]

      if predicted == expected:
        passed += 1
        print(f"Case {idx} [PASS]: '{test['input']}' -> {predicted}")
      else:
        print(
            f"Case {idx} [FAIL]: '{test['input']}' -> Got '{predicted}',"
            f" Expected '{expected}'"
        )
    else:
      print(f"Case {idx} [ERROR]: HTTP {enrich_res.status_code}")

    requests.delete(f"{API_URL}/tasks/{task_id}")

  score_pct = (passed / total) * 100
  print(f"\nEval Score: {passed}/{total} ({score_pct:.1f}%)")


if __name__ == "__main__":
  run_evaluation()