import requests
import matplotlib.pyplot as plt
import pandas as pd
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

BASE_URL = "http://localhost:8000"
response = requests.get(f"{BASE_URL}/auto-alarm-check")
data = response.json()

if not data:
    print("no abnormal events were detected")
    exit()

df = pd.DataFrame(data)

plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(8, 6))

# 设备类型柱状图：绿色，最大值用深绿色高亮
type_counts = df['device_type'].value_counts()
colors = ['#4ECDC4' if v == type_counts.max() else '#A0E7E5' for v in type_counts]

ax.bar(type_counts.index, type_counts.values, color=colors)
ax.set_title('Abnormal Events by Device Type')
ax.set_ylabel('Count')
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('device_type_abnormal_events_green.png', dpi=300, bbox_inches='tight')
plt.show()
