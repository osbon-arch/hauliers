import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("data.csv")

# Clean data
df['Revenue'] = df['Revenue'].str.replace(',', '').astype(float)
df['Year'] = df['Year'].astype(str)

# Sidebar filters
years = st.sidebar.multiselect("Select Year(s)", options=df['Year'].unique(), default=df['Year'].unique())
clients = st.sidebar.multiselect("Select Client(s)", options=df['Client'].unique(), default=df['Client'].unique())

# Filter data
filtered_df = df[(df['Year'].isin(years)) & (df['Client'].isin(clients))]

# Main dashboard
st.title("Sales by Customer Dashboard")

# KPIs
st.metric("Total Revenue", f"KES {filtered_df['Revenue'].sum():,.2f}")
st.metric("Unique Clients", filtered_df['Client'].nunique())

# Revenue by Client
st.subheader("Revenue by Client")
client_revenue = filtered_df.groupby('Client')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False)
st.plotly_chart(px.bar(client_revenue, x='Client', y='Revenue', title="Revenue by Client"))

# Revenue over Years
st.subheader("Revenue over Years")
year_revenue = filtered_df.groupby(['Year'])['Revenue'].sum().reset_index()
st.plotly_chart(px.line(year_revenue, x='Year', y='Revenue', markers=True, title="Yearly Revenue Trend"))

# Pie chart of revenue share
st.subheader("Revenue Share by Client")
st.plotly_chart(px.pie(client_revenue, names='Client', values='Revenue', title="Revenue Share"))

# Show filtered table
st.subheader("Filtered Data Table")
st.dataframe(filtered_df)
