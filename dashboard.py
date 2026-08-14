import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Video Game Sales Dashboard", layout="wide")
st.title("🎮 Video Game Sales Explorer")

# 2. Load Data 
# (Ensure your cleaned dataset from the Jupyter notebook is in the same folder)
@st.cache_data
def load_data():
    return pd.read_csv('vgsales.csv')

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Options")

# Dropdown for Region
regions = ['Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
selected_region = st.sidebar.selectbox("Select Region to Analyze", regions)

# Multiselect for Genre
all_genres = df['Genre'].dropna().unique()
selected_genres = st.sidebar.multiselect("Select Genres", options=all_genres, default=all_genres[:3])

# 4. Apply Filters
filtered_df = df[df['Genre'].isin(selected_genres)]

# 5. Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"{selected_region} by Platform")
    # Group by platform and sum sales
    platform_sales = filtered_df.groupby('Platform')[selected_region].sum().reset_index()
    # Create interactive bar chart
    fig_bar = px.bar(platform_sales, x='Platform', y=selected_region, color='Platform')
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader(f"{selected_region} Over Time")
    # Group by year and sum sales
    yearly_sales = filtered_df.groupby('Year')[selected_region].sum().reset_index()
    # Create interactive line chart
    fig_line = px.line(yearly_sales, x='Year', y=selected_region, markers=True)
    st.plotly_chart(fig_line, use_container_width=True)