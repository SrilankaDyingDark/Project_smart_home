import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

response = requests.get("http://localhost:8000/analysis/area-vs-usage")
data = response.json()

df = pd.DataFrame(data["raw_data"])
outlier_ids = {u['user_id'] for u in data.get("outliers", [])}
df["is_outlier"] = df["user_id"].apply(lambda x: x in outlier_ids)

plt.figure(figsize=(10, 6))
plt.title("Relationship Between House Area And Equipment Use Frequency", fontsize=16)

sns.scatterplot(
    data=df,
    x="house_area",
    y="usage_count",
    hue="is_outlier",
    palette={True: "red", False: "blue"},
    s=80,
    legend=False
)

for _, row in df[df["is_outlier"]].iterrows():
    plt.text(row["house_area"] + 1, row["usage_count"] + 0.5,
                f"用户{row['user_id']}", fontsize=9, color="darkred")

plt.axhline(df["usage_count"].mean(), color="gray", linestyle="--", linewidth=1, label="average frequency of use")
plt.axvline(df["house_area"].mean(), color="gray", linestyle="--", linewidth=1, label="average house area")

plt.xlabel("housing area", fontsize=12)
plt.ylabel("equipment usage frequency", fontsize=12)

plt.text(0.95, 0.02, "red dot abnormal user", transform=plt.gca().transAxes, fontsize=10, color="red", ha="right")

plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
