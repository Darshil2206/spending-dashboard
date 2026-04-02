import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Spending Dashboard", layout="wide")

st.title("💰 Personal Spending Insights Dashboard")

# Upload option
uploaded_file = st.file_uploader("Upload your expense CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/expenses.csv/expenses.csv")

# Data cleaning
df['date'] = pd.to_datetime(df['date'], errors='coerce')
# Sidebar filters
st.sidebar.header("Filters")
category_filter = st.sidebar.multiselect(
    "Select Category",
    df['category'].unique(),
    default=df['category'].unique()
)

df = df[df['category'].isin(category_filter)]

# KPIs
total = df['amount'].sum()
avg = df['amount'].mean()
max_spend = df['amount'].max()

col1, col2, col3 = st.columns(3)

col1.metric("Total Spending", f"₹{int(total)}")
col2.metric("Average Spending", f"₹{int(avg)}")
col3.metric("Max Transaction", f"₹{int(max_spend)}")

# Category Analysis
st.subheader("📊 Spending by Category")
category = df.groupby('category')['amount'].sum()
st.bar_chart(category)

# Daily Trend
st.subheader("📈 Daily Spending Trend")
daily = df.groupby('date')['amount'].sum()
st.line_chart(daily)

# Monthly Trend
st.subheader("📅 Monthly Spending")
df['month'] = df['date'].dt.to_period('M')
monthly = df.groupby('month')['amount'].sum()
st.bar_chart(monthly)

# Insights
st.subheader("💡 Insights")

top_category = category.idxmax()
st.write(f"👉 Highest spending category: **{top_category}**")

busy_day = daily.idxmax()
st.write(f"👉 Highest spending day: **{busy_day.date()}**")

# Forecasting
st.subheader("🔮 Spending Forecast")

df['day_num'] = df['date'].map(pd.Timestamp.toordinal)

X = df[['day_num']]
y = df['amount']

model = LinearRegression()
model.fit(X, y)

future_days = [[df['day_num'].max() + i] for i in range(1, 8)]
predictions = model.predict(future_days)

st.write("Next 7 days predicted spending:")

for i, pred in enumerate(predictions, 1):
    st.write(f"Day {i}: ₹{int(pred)}")
