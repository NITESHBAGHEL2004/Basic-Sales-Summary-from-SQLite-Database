
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create database with sample data if it doesn't exist
db_file = "sales_data.db"

if not os.path.exists(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create sales table
    cursor.execute("""
    CREATE TABLE sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
    """)

    #sample data
    sample_data = [
        ("Laptop", 5, 60000),
        ("Laptop", 3, 62000),
        ("Mouse", 10, 800),
        ("Mouse", 7, 750),
        ("Keyboard", 4, 1500),
        ("Keyboard", 6, 1400),
        ("Monitor", 2, 12000),
        ("Monitor", 1, 12500)
    ]
    cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
    conn.commit()
    conn.close()
    print("✅ Database created and sample data inserted.\n")


# Connect to the database
conn = sqlite3.connect(db_file)

# SQL Query
query = """
SELECT product, 
       SUM(quantity) AS total_qty, 
       SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
"""

# Load into pandas
df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Print results
print("📊 Sales Summary:")
print(df)

# Plot simple bar chart
df.plot(kind='bar', x='product', y='revenue', color='skyblue', legend=False)
plt.ylabel("Revenue (INR)")
plt.title("Revenue by Product")
plt.tight_layout()

# Save chart
plt.savefig("sales_chart.png")
plt.show()
