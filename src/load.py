import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import streamlit as st

load_dotenv()


def get_engine():

    # Try Streamlit Cloud Secrets first
    try:
        database_url = st.secrets["DATABASE_URL"]
    except Exception:
        # Use local .env when running on your computer
        database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is missing. "
            "Add it to .env locally or Streamlit Secrets when deployed."
        )

    return create_engine(database_url)


def load_orders(df):

    engine = get_engine()

    df.to_sql(
        "orders",
        engine,
        if_exists="replace",
        index=False
    )


def load_customers(df):

    engine = get_engine()

    df.to_sql(
        "customers",
        engine,
        if_exists="replace",
        index=False
    )


def load_products(df):

    engine = get_engine()

    df.to_sql(
        "products",
        engine,
        if_exists="replace",
        index=False
    )