import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="Store Sales & Profit Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Store Sales and Profit Analysis Dashboard")
st.markdown("Interactive analysis of sales, profit, categories, and customer segments")

# ----------------------------------
# Load Dataset
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Sample - Superstore.csv", encoding="ISO-8859-1")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df.fillna(0, inplace=True)
    return df

df = load_data()

# ----------------------------------
# Sidebar Filters
# ----------------------------------
st.sidebar.header("🔍 Filters")

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

segment_filter = st.sidebar.multiselect(
    "Select Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Category"].isin(category_filter)) &
    (df["Segment"].isin(segment_filter)) &
    (df["Region"].isin(region_filter))
]

# ----------------------------------
# KPI Metrics
# ----------------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("🧾 Total Orders", total_orders)

st.divider()

# ----------------------------------
# DOWNLOAD BUTTON
# ----------------------------------
st.subheader("⬇️ Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="filtered_store_sales.csv",
    mime="text/csv"
)

st.divider()

# ----------------------------------
# Monthly Sales Trend
# ----------------------------------
filtered_df["Month"] = filtered_df["Order Date"].dt.to_period("M").astype(str)
monthly_sales = filtered_df.groupby("Month")["Sales"].sum().reset_index()

fig1 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    title="📅 Monthly Sales Trend",
    markers=True
)
st.plotly_chart(fig1, use_container_width=True)

# ----------------------------------
# Category-wise Sales
# ----------------------------------
category_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()

fig2 = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="📦 Sales by Category"
)
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------
# Sub-Category Profit
# ----------------------------------
subcat_profit = filtered_df.groupby("Sub-Category")["Profit"].sum().reset_index()

fig3 = px.bar(
    subcat_profit.sort_values("Profit", ascending=False),
    x="Sub-Category",
    y="Profit",
    title="💹 Profit by Sub-Category"
)
st.plotly_chart(fig3, use_container_width=True)

# ----------------------------------
# Customer Segment Profit
# ----------------------------------
segment_profit = filtered_df.groupby("Segment")["Profit"].sum().reset_index()

fig4 = px.pie(
    segment_profit,
    names="Segment",
    values="Profit",
    title="👥 Profit by Customer Segment"
)
st.plotly_chart(fig4, use_container_width=True)

# ----------------------------------
# Sales-to-Profit Ratio
# ----------------------------------
filtered_df["Sales_to_Profit_Ratio"] = filtered_df["Profit"] / filtered_df["Sales"]

ratio_category = filtered_df.groupby("Category")["Sales_to_Profit_Ratio"].mean().reset_index()

fig5 = px.bar(
    ratio_category,
    x="Category",
    y="Sales_to_Profit_Ratio",
    title="⚙️ Sales-to-Profit Ratio by Category"
)
st.plotly_chart(fig5, use_container_width=True)

# ----------------------------------
# Raw Data
# ----------------------------------
st.subheader("📄 Raw Data View")
st.dataframe(filtered_df)
