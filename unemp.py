# %%
import numpy as np
import pandas as pd

# %%
df1 = pd.read_csv("Unemployment in India.csv")
df2 = pd.read_csv("Unemployment_Rate_upto_11_2020.csv")

# %%
df1.head(5)

# %%
df2.head(5)

# %%
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# %%
df1['Date'] = pd.to_datetime(df1['Date'], dayfirst=True)
df2['Date'] = pd.to_datetime(df2['Date'], dayfirst=True)
print(df1.dtypes)
print(df2.dtypes)

# %%
unemp_trend = df2.groupby("Date")["Estimated Unemployment Rate (%)"].mean()


# %%
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 4))
plt.style.use('dark_background')
plt.plot(unemp_trend.index, unemp_trend.values, marker='*', color='purple')
plt.title("Average Unemployment Rate Over Time in India", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.grid(True)
plt.tight_layout()
plt.show()


# %%
# Before March 2020
pre_covid = df2[df2['Date'] < '2020-03-01']
# March to June 2020 (lockdown period)
during_covid = df2[(df2['Date'] >= '2020-03-01') & (df2['Date'] <= '2020-06-30')]

# %%
print("Average Unemployment Rate (Pre-COVID):", pre_covid["Estimated Unemployment Rate (%)"].mean())
print("Average Unemployment Rate (During COVID):", during_covid["Estimated Unemployment Rate (%)"].mean())

# %%
import matplotlib.pyplot as plt
plt.style.use('dark_background')
plt.figure(figsize=(14, 8))
for state in df2['Region'].unique():
    state_data = df2[df2['Region'] == state]
    plt.plot(state_data['Date'], 
             state_data['Estimated Unemployment Rate (%)'], 
             label=state)
plt.title("Unemployment Rate by State Over Time", fontsize=16, color='white')
plt.xlabel("Date", color='white')
plt.ylabel("Unemployment Rate (%)", color='white')
plt.tick_params(colors='white')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()


# %%
import plotly.express as px
# Filter dataset for April 2020
april_data = df2[df2['Date'] == '2020-04-30']

# %%
df2.head(5)

# %%
fig=px.scatter_geo(april_data,
                   lat='latitude',
                   lon='longitude',
                   text='Region',
                   size='Estimated Unemployment Rate (%)',
                   color='Estimated Unemployment Rate (%)',
                   color_continuous_scale='Reds',
                   projection='mercator',
                   title='Unemployment Rate in India (April 2020)',
)
fig.update_layout(
    title_font_color='white',
    paper_bgcolor='black',
    geo=dict(bgcolor='black'),
    font=dict(color='white')
)
fig.show()

# %%
import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.set_page_config(page_title="India Unemployment Dashboard", layout="wide")
st.title("📊 Unemployment Analysis During COVID-19 (India)")

# Load Data
df = pd.read_csv("Unemployment_Rate_upto_11_2020.csv")
df.columns = df.columns.str.strip()
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# Summary Metrics
pre_covid = df[df['Date'] < '2020-03-01']
during_covid = df[(df['Date'] >= '2020-03-01') & (df['Date'] <= '2020-06-30')]

avg_pre = pre_covid["Estimated Unemployment Rate (%)"].mean()
avg_during = during_covid["Estimated Unemployment Rate (%)"].mean()

# Trend Chart
st.subheader("📈 National Unemployment Trend")
national_trend = df.groupby("Date")["Estimated Unemployment Rate (%)"].mean()
st.line_chart(national_trend)

# Heatmap (April 2020)
st.subheader("📍 State-wise Unemployment (April 2020)")
april_data = df[df['Date'] == '2020-04-30']
fig = px.scatter_geo(
    april_data,
    lat='latitude',
    lon='longitude',
    text='Region',
    size='Estimated Unemployment Rate (%)',
    color='Estimated Unemployment Rate (%)',
    color_continuous_scale='Reds',
    projection='mercator'
)
fig.update_layout(
    geo=dict(center={'lat': 22, 'lon': 80}, projection_scale=5),
    margin=dict(l=0, r=0, t=0, b=0)
)
st.plotly_chart(fig, use_container_width=True)

# Top 5 Affected States
st.subheader("🔥 Top 5 Most Affected States in April 2020")
top5 = april_data.sort_values("Estimated Unemployment Rate (%)", ascending=False).head(5)
st.table(top5[["Region", "Estimated Unemployment Rate (%)"]])

# Summary
st.subheader("📝 Summary")
st.markdown(f"""
- **Average unemployment before COVID**: {avg_pre:.2f}%
- **Average unemployment during early COVID (Mar–Jun 2020)**: {avg_during:.2f}%
- Unemployment rate **tripled** in many states during the lockdown.
- Worst affected states in April 2020: **{', '.join(top5['Region'].values)}**
""")



