import streamlit as st

DB_PARAMS = {
    "host": st.secrets["DB_HOST"],
    "dbname": st.secrets["DB_NAME"],
    "user": st.secrets["DB_USER"],
    "password": st.secrets["DB_PASS"],
    "port": st.secrets["DB_PORT"]
}
