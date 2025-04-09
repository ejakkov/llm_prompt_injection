import pandas as pd
import json

with open("results/ContentManipulation_results.json", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)


df_basic = df[df["defence"] == "BasicDefence"]


summary = df_basic.groupby("prompt_injection").agg(
    attempts=("injection_successful", "count"),
    success_count=("injection_successful", "sum"),
    success_rate=("injection_successful", "mean"),
    avg_response_time=("time_taken_seconds", "mean"),
    avg_total_tokens=("total_tokens", "mean")
).reset_index()

DEFENCES_LIST = [
    "Defence",
    "BasicDefence",
    "Encoding",
    "FewShotLearning",
    "Tagging",
    "DataMarking",
    "Paraphrasing",
    "LLMPiDetection"
]

for defence_name in DEFENCES_LIST:
    df_defence = df[df["defence"] == defence_name]

    if df_defence.empty:
        print(f"[!] Nav datu priekš: {defence_name}")
        continue

    summary = df_defence.groupby("prompt_injection").agg(
        attempts=("injection_successful", "count"),
        success_count=("injection_successful", "sum"),
        success_rate=("injection_successful", "mean"),
        avg_response_time=("time_taken_seconds", "mean"),
        avg_total_tokens=("total_tokens", "mean")
    ).reset_index()

    summary["success_rate"] = (summary["success_rate"] * 100).round(2)

    print(f"\n=== Summary for {defence_name} ===")
    print(summary)

summary["success_rate"] = (summary["success_rate"] * 100).round(2)

print(summary)

summary.to_csv("summary_table.csv", index=False)
summary.to_markdown("summary_table.md", index=False)