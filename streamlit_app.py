import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on March 17th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='ME')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")

# Dropdown for selecting a category
categories = df["Category"].unique()
selected_category = st.selectbox("Select a Category", categories)

# Filter data based on selected category
filtered_df = df[df["Category"] == selected_category]


st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")

# Multi-select for selecting sub-categories within the selected category
sub_categories = filtered_df["Sub_Category"].unique()
selected_sub_categories = st.multiselect("Select Sub-Categories", sub_categories, default=sub_categories)

# Further filter data based on selected sub-categories
filtered_df = filtered_df[filtered_df["Sub_Category"].isin(selected_sub_categories)]


st.write("### (3) show a line chart of sales for the selected items in (2)")

# Line chart of sales for the selected sub-categories
st.write("### Sales Trend for Selected Sub-Categories")
st.line_chart(filtered_df.groupby(filtered_df.index).sum(), y="Sales")

st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")

# Show three metrics: total sales, total profit, and overall profit margin
st.write("### Key Metrics for Selected Sub-Categories")
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

# st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
# st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
# st.metric(label="Profit Margin", value=f"{profit_margin:.2f}%")

st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
# Compute overall average profit margin
overall_total_sales = df["Sales"].sum()
overall_total_profit = df["Profit"].sum()
overall_profit_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales != 0 else 0

delta_margin = profit_margin - overall_profit_margin

st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
st.metric(label="Profit Margin", value=f"{profit_margin:.2f}%", delta=f"{delta_margin:.2f}%")
