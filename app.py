import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import json


# Database connection function
def get_db_connection():
    # Use the External Database UR from Render
    conn = psycopg2.connect("postgresql://products_sj7a_user:otz8QLIyvBcCtXlD5Nn38vyX7NqGcLS6@dpg-cupcg6lsvqrc73evo2rg-a.oregon-postgres.render.com/products_sj7a")  # Replace with actual details
    return conn


# Initialize database and create product table if not exists
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT,
            price REAL,
            image TEXT,
            description TEXT,
            reviews TEXT
        )
    ''')
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        # Sample products data
        products = [
            ("Laptop", 1000, "https://via.placeholder.com/150", "High-end laptop for professionals",
             '{"rating": 4.5, "review_count": 120}'),
            ("Smartphone", 800, "https://via.placeholder.com/150", "Latest smartphone with cutting-edge features",
             '{"rating": 4.2, "review_count": 200}'),
            ("Headphones", 150, "https://via.placeholder.com/150", "Noise-cancelling headphones",
             '{"rating": 4.8, "review_count": 85}'),
            ("Smartwatch", 200, "https://via.placeholder.com/150", "Smartwatch with fitness tracking",
             '{"rating": 4.3, "review_count": 50}'),
            ("Tablet", 500, "https://via.placeholder.com/150", "Portable tablet for on-the-go",
             '{"rating": 4.1, "review_count": 150}')
        ]
        c.executemany("INSERT INTO products (name, price, image, description, reviews) VALUES (%s, %s, %s, %s, %s)",
                      products)
        conn.commit()
    conn.close()


# Load products from the database
def load_products():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()
    return df


# Anomaly detection (for example, flagging transactions)
def detect_anomalies():
    # Simulated anomaly detection logic
    anomalies = {
        "status": "No major anomalies detected",
        "message": "All transactions appear normal."
    }
    return anomalies


# Navigation Bar
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

# Initialize the Database
init_db()

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
            st.write(f"Description: {row['description']}")
            reviews = json.loads(row['reviews'])
            st.write(f"Rating: {reviews['rating']} ({reviews['review_count']} reviews)")
            if st.button(f"Add to Cart {row['id']}"):
                st.session_state.setdefault("cart", []).append(row['name'])

# Admin Dashboard
elif page == "dashboard":
    st.title("Admin Dashboard")
    browsers = ["Chrome", "Firefox", "Edge", "Safari"]
    visits = np.random.randint(100, 500, size=len(browsers))

    fig, ax = plt.subplots()
    ax.pie(visits, labels=browsers, autopct='%1.1f%%', colors=['gold', 'lightblue', 'lightgreen', 'pink'])
    st.pyplot(fig)
    st.write("Chrome is the most used browser for shopping on our site with 40% of traffic.")

# Analytics Page
elif page == "analytics":
    st.title("Sales & Inventory Analytics")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    sales = np.random.randint(500, 2000, size=len(months))

    fig, ax = plt.subplots()
    ax.bar(months, sales, color='blue')
    ax.set_xlabel("Months")
    ax.set_ylabel("Sales ($)")
    st.pyplot(fig)

    st.write(f"Sales increased by {round(((sales[-1] - sales[0]) / sales[0]) * 100, 2)}% over the last 6 months.")

    # Generate Anomaly Report
    st.write("### Generate Anomaly Report")
    if st.button("Generate Report"):
        anomaly_report = detect_anomalies()
        st.json(anomaly_report)

# Chatbot Page
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
