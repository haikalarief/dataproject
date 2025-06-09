import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="World Happiness Score", layout="wide")
#load gambar
image = Image.open("happy_world.png")
st.image(image, use_column_width=True)
#load cleaned data
df = pd.read_csv("cleaned_happiness.csv")

st.title("🌍 World Happiness Dashboard")

#display avergae score and gdp
avg_score = df['score'].mean()
avg_gdp = df['gdp_per_capita'].mean()
st.markdown(f"### 📈 Global Averages")
st.write(f"**Average Happiness Score:** {avg_score:.2f}")
st.write(f"**Average GDP per Capita:** {avg_gdp:.2f}")

#sidebar utk filter data
st.sidebar.header("Filter Options")
countries = st.sidebar.multiselect(
    "Select Countries", options=df['country_or_region'].unique(),
    default=["Finland", "Denmark", "Norway"]
)
x_axis = st.sidebar.selectbox("X-Axis", options=df.columns[3:], index=0)
y_axis = st.sidebar.selectbox("Y-Axis", options=df.columns[3:], index=1)

filtered_df = df[df['country_or_region'].isin(countries)]

#show filtered data
st.subheader("📊 Filtered Data Table")
st.dataframe(filtered_df)

#scatter plot
#intechangable on the x-axis and y-axis by data chosen from sidebar
st.subheader(f"📈 {y_axis.title()} vs {x_axis.title()}")
fig_scatter = px.scatter(
    filtered_df,
    x=x_axis,
    y=y_axis,
    color="country_or_region",
    hover_name="country_or_region",
    size_max=60,
    template="plotly_white",
    title=f"{y_axis.replace('_', ' ').title()} vs {x_axis.replace('_', ' ').title()}"
)
st.plotly_chart(fig_scatter, use_container_width=True)

#data correlation heatmap
st.subheader("🔥 Correlation Heatmap of Happiness Factors")

#calculate correlation for numeric data only
corr_df = df[df.columns[3:]].corr()

#plot heatmap
fig, ax = plt.subplots(figsize=(10, 7))
sns.heatmap(corr_df, annot=True, cmap="coolwarm", ax=ax, fmt=".2f")
st.pyplot(fig)

#happiness score on world map
st.subheader("🌏 World Happiness Scores Map")

#use plotly built-in country name
fig_map = px.choropleth(
    df,
    locations="country_or_region",
    locationmode="country names",
    color="score",
    hover_name="country_or_region",
    color_continuous_scale=px.colors.sequential.Plasma,
    title="Happiness Scores by Country"
)
st.plotly_chart(fig_map, use_container_width=True)

#table for happiest countries ranking
st.subheader("🏆 Happiest Countries Ranking")

top_n = st.slider("Select number of top countries to display", 5, 20, 10)

top_countries = df.sort_values(by="score", ascending=False).head(top_n)
st.table(top_countries[["overall_rank", "country_or_region", "score"]].reset_index(drop=True))
