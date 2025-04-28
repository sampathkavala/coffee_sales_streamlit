import streamlit as st
import pandas as pd
import psycopg2
from config import DB_PARAMS

# --------------------- PAGE CONFIG ------------------------
st.set_page_config(page_title="Maven Roasters Coffee Sales SQL Explorer", layout="wide")

# --------------------- SIDEBAR: Default Queries ------------------------
with st.sidebar:
    st.title("Default Queries")
    st.markdown("### Explore Maven Roasters Coffee Sales!")

    selected_query = st.selectbox("Choose a Preloaded Query:", [
        "SELECT * FROM products LIMIT 10;",
        "SELECT product_type, unit_price FROM products ORDER BY unit_price DESC LIMIT 5;",
        "SELECT s.store_location, SUM(oi.quantity) AS total_quantity FROM order_items oi JOIN orders o ON oi.order_id = o.order_id JOIN stores s ON o.store_id = s.store_id GROUP BY s.store_location ORDER BY total_quantity DESC;",
        "SELECT pc.category_name, AVG(p.unit_price) AS avg_price FROM products p JOIN product_categories pc ON p.category_id = pc.category_id GROUP BY pc.category_name ORDER BY avg_price DESC;"
    ])

# --------------------- PAGE HEADER ------------------------
st.title("☕ Maven Roasters Coffee Sales SQL Explorer")
st.write("---")

# --------------------- USER ROLE LOGIN ------------------------

user_type = st.radio("Select User Type", ["Admin", "User"])
password = st.text_input("Enter Password", type="password")

# ✅ Secure: Fetch passwords from Streamlit Secrets
admin_password = st.secrets["ADMIN_PASSWORD"]
user_password = st.secrets["USER_PASSWORD"]

role_authenticated = False

# Authenticate
if user_type == "Admin" and password == admin_password:
    st.success("Logged in as Admin")
    role_authenticated = "admin"
elif user_type == "User" and password == user_password:
    st.success("Logged in as End User")
    role_authenticated = "user"
elif password:
    st.error("Incorrect Password. Please try again.")

# --------------------- MAIN APPLICATION ------------------------

if role_authenticated:

    st.write("---")
    st.header("Database Schema Overview")

    schema_text = """
    **Tables and Key Columns:**

    **products**
      - `product_id` (PK)
      - `category_id` (FK)
      - `product_type`
      - `product_detail`
      - `unit_price`
    
    **product_categories**
      - `category_id` (PK)
      - `category_name`
    
    **stores**
      - `store_id` (PK)
      - `store_location`
    
    **orders**
      - `order_id` (PK)
      - `order_date`
      - `order_time`
      - `store_id` (FK)
    
    **order_items**
      - `order_id` (FK)
      - `product_id` (FK)
      - `quantity`

    ---
    **Notes:**
    - **orders** ➔ links to **stores**
    - **order_items** ➔ connects **orders** and **products**
    - **products** ➔ categorized by **product_categories**
    """
    st.markdown(schema_text)

    st.write("---")
    st.header("📑 Database Query Interface")

    query = st.text_area("Enter your SQL query below:", selected_query, height=150)

    if st.button("Run Query"):
        with st.spinner('⏳ Running Query... Please wait...'):
            try:
                query_check = query.strip().lower()

                if role_authenticated == "user" and not query_check.startswith("select"):
                    st.error(" Permission Denied: End Users can only perform SELECT queries.")
                else:
                    with psycopg2.connect(**DB_PARAMS) as conn:
                        df = pd.read_sql_query(query, conn)

                    st.success(" Query executed successfully!")
                    st.write("### Query Results")
                    st.dataframe(df)

                    # Auto Bar Chart
                    numeric_cols = df.select_dtypes(include="number").columns.tolist()
                    non_numeric_cols = df.select_dtypes(exclude="number").columns.tolist()

                    if numeric_cols and non_numeric_cols:
                        try:
                            x_axis = non_numeric_cols[0]
                            y_axis = numeric_cols[0]

                            chart_data = df.groupby(x_axis)[y_axis].sum().sort_values(ascending=False)

                            st.write("###  Bar Chart for the Query Results")
                            st.bar_chart(chart_data)

                        except Exception as e:
                            st.warning(f"Could not generate bar chart: {e}")
                    else:
                        st.info(" No suitable data available for dynamic bar chart.")

            except Exception as e:
                st.error(f"Query Error: {e}")

else:
    st.info("Please login to access database operations.")
