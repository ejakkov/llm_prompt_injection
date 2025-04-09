import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

with open(f'results\\2025-04-08_21-51-39\ContentManipulation_gpt-3.5-turbo_results.json', encoding="utf-8") as f:  # <- nomaini uz savu JSON failu
    data = json.load(f)
df = pd.DataFrame(data)

summary = df.groupby("prompt_injection").agg(
    attempts=("injection_successful", "count"),
    success_rate=("injection_successful", "mean")
).reset_index()

summary["success_rate"] = (summary["success_rate"] * 100).round(2)

plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

plot = sns.barplot(
    data=summary,
    x="prompt_injection",
    y="success_rate",
    palette="viridis"
)

plt.title("Prompt Injection Success Rate by Method", fontsize=14)
plt.ylabel("Success Rate (%)", fontsize=12)
plt.xlabel("Prompt Injection Method", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.ylim(0, 100)

for i, row in summary.iterrows():
    plot.text(i, row["success_rate"] + 1, f"{row['success_rate']}%", ha='center', fontsize=10)

plt.tight_layout()
plt.show()