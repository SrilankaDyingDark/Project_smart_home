import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

with open("D:/homework/data/期末/response.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

avg_freq = pd.DataFrame(data['average_daily_frequency'].items(), columns=['Device', 'Frequency'])
avg_freq = avg_freq.sort_values('Frequency', ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(x='Frequency', y='Device', data=avg_freq, palette='viridis')
plt.title('Average Daily Usage Frequency by Device')
plt.tight_layout()
plt.show()

hourly_data = []
for device, hours in data['hourly_distribution'].items():
    for hour, count in hours.items():
        hourly_data.append({'Device': device, 'Hour': int(hour), 'Count': count})
        
hourly_df = pd.DataFrame(hourly_data)
heatmap_data = hourly_df.pivot_table(index='Device', columns='Hour', values='Count', fill_value=0)

plt.figure(figsize=(16, 10))
sns.heatmap(heatmap_data, cmap='YlOrRd', linewidths=0.5)
plt.title('Hourly Usage Distribution by Device')
plt.tight_layout()
plt.show()