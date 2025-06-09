import requests
import pandas as pd
import plotly.express as px

# 获取数据
response = requests.post("http://localhost:8000/auto-alarm-check")
data = response.json()

# 转为 DataFrame
df = pd.DataFrame(data)

# 转换时间格式
df["timestamp"] = pd.to_datetime(df["timestamp"])

# 示例 1：按严重等级统计
fig1 = px.histogram(df, x="severity", color="severity", title="警报数量按严重等级统计")
fig1.show()

# 示例 2：按小时分布
df["hour"] = df["timestamp"].dt.hour
fig2 = px.histogram(df, x="hour", nbins=24, title="警报时间分布（小时）")
fig2.show()

# 示例 3：按设备分布
fig3 = px.histogram(df, x="device_name", color="severity", title="各设备触发警报统计")
fig3.show()
