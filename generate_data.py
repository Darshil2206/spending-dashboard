import pandas as pd
import random
from datetime import datetime, timedelta

categories = ["Food", "Transport", "Shopping", "Bills", "Entertainment"]

start_date = datetime(2025, 1, 1)
data = []

for i in range(300):
    date = start_date + timedelta(days=i)
    for _ in range(random.randint(1, 3)):
        data.append([
            date.strftime("%Y-%m-%d"),
            random.choice(categories),
            random.randint(100, 2000)
        ])

df = pd.DataFrame(data, columns=["date", "category", "amount"])
df.to_csv("data/expenses.csv", index=False)

print("Dataset generated!")