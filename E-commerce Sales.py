import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(42)
sns.set(style="whitegrid")

n_customers = 500
customers = pd.DataFrame({
    "customer_id": np.arange(1, n_customers + 1),
    "age": np.random.randint(18, 60, n_customers),
    "gender": np.random.choice(["Male", "Female"], n_customers, p=[0.6, 0.4]),
    "city": np.random.choice(["Cairo", "Giza", "Alex", "Mansoura", "Tanta", "Sohag"], n_customers)
})

n_products = 50
products = pd.DataFrame({
    "product_id": np.arange(1, n_products + 1),
    "category": np.random.choice(["Electronics", "Clothes", "Books", "Food", "Home"], n_products),
    "price": np.random.randint(50, 2000, n_products)
})

n_orders = 2000
orders = pd.DataFrame({
    "order_id": np.arange(1, n_orders + 1),
    "customer_id": np.random.choice(customers["customer_id"], n_orders),
    "product_id": np.random.choice(products["product_id"], n_orders),
    "quantity": np.random.randint(1, 5, n_orders),
    "order_date": pd.to_datetime(np.random.choice(pd.date_range("2023-01-01", "2023-12-31"), n_orders))
})

df = orders.merge(customers, on="customer_id").merge(products, on="product_id")
df["total_price"] = df["quantity"] * df["price"]


bins = [17, 25, 35, 45, 60]
labels = ["18-25", "26-35", "36-45", "46-60"]
df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels)

df["order_month"] = df["order_date"].dt.to_period("M").astype(str)


total_revenue = df["total_price"].sum()
print(f"Total Revenue: {total_revenue:,.0f}")

monthly_revenue = df.groupby("order_month")["total_price"].sum().reset_index()

top_products = df.groupby("product_id")["total_price"].sum().sort_values(ascending=False).head(10)

top_customers = df.groupby("customer_id")["total_price"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
sns.lineplot(data=monthly_revenue, x="order_month", y="total_price", marker="o")
plt.xticks(rotation=45)
plt.title("Monthly Revenue (2023)")
plt.show()

plt.figure(figsize=(10,5))
sns.barplot(x=top_products.index.astype(str), y=top_products.values)
plt.title("Top 10 Products by Revenue")
plt.xlabel("Product ID")
plt.ylabel("Revenue")
plt.show()

plt.figure(figsize=(8,5))
sns.boxplot(x="gender", y="total_price", data=df)
plt.title("Spending per Order by Gender")
plt.show()

plt.figure(figsize=(8,6))
pivot = df.pivot_table(index="category", columns="age_group", values="total_price", aggfunc="sum").fillna(0)
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Blues")
plt.title("Revenue by Category and Age Group")
plt.show()

plt.figure(figsize=(6,6))
df.groupby("category")["total_price"].sum().plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Sales Share by Category")
plt.ylabel("")
plt.show()
