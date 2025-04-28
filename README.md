# ☕ Coffee Sales SQL Explorer

An interactive web application to query and visualize coffee sales database using Streamlit, PostgreSQL, and Render hosting.

## 🚀 Project Overview

This project provides an easy way to run SQL queries and generate visualizations (bar charts) based on coffee sales data.  
The app is deployed on **Streamlit Cloud** and connected to a live **PostgreSQL database** hosted on **Render**.

Users can log in as:
- **Admin**: Full SQL access (SELECT, INSERT, UPDATE, DELETE).
- **User**: Only SELECT queries allowed.

---

## 🛠 Tech Stack

- **Frontend & Web Hosting**: [Streamlit](https://streamlit.io/)
- **Database Hosting**: [Render](https://render.com/)
- **Database**: PostgreSQL
- **Version Control**: Git, GitHub

---

## ⚙️ Project Structure

```plaintext
coffee_sales_streamlit/
├── streamlit_app.py          # Main Streamlit app
├── config.py                 # Database connection setup
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── secrets.toml          # (Local secrets for testing only)
