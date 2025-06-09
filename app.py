import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image 

st.set_page_config(page_title="World Happiness Score", layout="wide")
#load gambar
image = Image.open("world happiness.jpg")
st.image(image, use_container_width=True)

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

st.markdown("### 😊 Distribution of Happiness Scores")

# Create figure and plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df['score'], bins=30, kde=True, color='teal', ax=ax)
ax.set_title('Distribution of Happiness Scores')
ax.set_xlabel('Happiness Score')
ax.set_ylabel('Frequency')

# Display in Streamlit
st.pyplot(fig)

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
st.markdown(
    """
    **How to use this scatter plot:**  
    Use the dropdown menus below to select which variables you'd like to plot on the X and Y axes.  
    For example, try plotting **GDP per Capita** against **Score** to see if wealth relates to happiness.  
    """
)
#data correlation heatmap
st.subheader("🔥 Correlation Heatmap of Happiness Factors")

#calculate correlation for numeric data only
corr_df = df[df.columns[3:]].corr()

#plot heatmap
fig, ax = plt.subplots(figsize=(10, 7))
sns.heatmap(corr_df, annot=True, cmap="coolwarm", ax=ax, fmt=".2f")
st.pyplot(fig)

st.markdown(
    """
    **What does this heatmap show?**  
    This heatmap reveals the strength and direction of relationships between the numerical variables in the dataset.  
    - A value close to **+1** indicates a strong **positive** correlation (as one increases, so does the other).  
    - A value near **-1** indicates a strong **negative** correlation (as one increases, the other decreases).  
    - Values near **0** suggest little to no correlation.  

    For example, you might notice that **GDP per Capita** is strongly correlated with **Happiness Score**,  
    while **Generosity** might show a weaker or even inverse trend.  
    """
)

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
