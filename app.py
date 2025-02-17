import streamlit as st
import pandas as pd
import json
import random
import numpy as np
import matplotlib.pyplot as plt
import sqlite3


# Database Setup
def init_db():
    conn = sqlite3.connect("ecommerce.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    price REAL,
                    image TEXT)''')

    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        products = [
            (1, "Laptop", 1000, "https://via.placeholder.com/150"),
            (2, "Smartphone", 800, "https://via.placeholder.com/150"),
            (3, "Headphones", 150, "https://via.placeholder.com/150"),
            (4, "Smartwatch", 200, "https://via.placeholder.com/150"),
            (5, "Tablet", 500, "https://via.placeholder.com/150")
        ]
        c.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)
        conn.commit()
    conn.close()


# Load Products from Database
def load_products():
    conn = sqlite3.connect("ecommerce.db")
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()
    return df


# Navigation Menu
st.markdown("""
    <style>
        .nav {background-color: #4CAF50; padding: 10px; text-align: center;}
        .nav a {margin: 10px; color: white; font-size: 18px; text-decoration: none;}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='nav'>
        <a href='?page=home'>Home</a>
        <a href='?page=dashboard'>Admin Dashboard</a>
        <a href='?page=analytics'>Analytics</a>
        <a href='?page=chatbot'>Chatbot</a>
    </div>
""", unsafe_allow_html=True)

# Extract Page Parameter
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["home"])[0]

# Home Page
if page == "home":
    st.title("E-Commerce Store")
    df = load_products()
    cols = st.columns(5)
    for i, row in df.iterrows():
        with cols[i % 5]:
            st.image(row["image"], width=100)
            st.write(f"**{row['name']}**")
            st.write(f"${row['price']}")
            if st.button(f"Add to Cart {row['id']}"):
                st.session_state.setdefault("cart", []).append(row['name'])

# Admin Dashboard (User Activity, Sales, Anomalies)
elif page == "dashboard":
    st.title("Admin Dashboard")
    browsers = ["Chrome", "Firefox", "Edge", "Safari"]
    visits = np.random.randint(100, 500, size=len(browsers))

    fig, ax = plt.subplots()
    ax.pie(visits, labels=browsers, autopct='%1.1f%%', colors=['gold', 'lightblue', 'lightgreen', 'pink'])
    st.pyplot(fig)
    st.write("{{{{{{ Chrome is the most used browser for shopping on our site with 40% of traffic. }}}}}}")

# Analytics (Sales, Inventory, Predictions)
elif page == "analytics":
    st.title("Sales & Inventory Analytics")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    sales = np.random.randint(500, 2000, size=len(months))

    fig, ax = plt.subplots()
    ax.bar(months, sales, color='blue')
    ax.set_xlabel("Months")
    ax.set_ylabel("Sales ($)")
    st.pyplot(fig)

    st.write("{{{{{{ Sales increased by " + str(
        round(((sales[-1] - sales[0]) / sales[0]) * 100, 2)) + "% over the last 6 months. }}}}}}")

    st.write("### Generate Anomaly Report")
    if st.button("Generate Report"):
        anomaly_report = {"status": "No major anomalies detected", "message": "All transactions appear normal."}
        st.json(anomaly_report)

# Chatbot
elif page == "chatbot":
    st.title("AI Chatbot")
    user_input = st.text_input("Ask about offers (e.g., 'Any offers on laptops?')")
    if user_input:
        if "laptop" in user_input.lower():
            st.write("Yes! Laptops have a 10% discount today.")
        elif "headphones" in user_input.lower():
            st.write("Yes! Headphones are available with a 15% discount.")
        else:
            st.write("No special offers on that product currently.")

# Initialize Database
init_db()

