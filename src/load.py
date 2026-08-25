import os

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()


def get_engine():

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is missing from your .env file."
        )

    # Make sure we are using the full Neon URL
    if not database_url.startswith("postgresql://"):
        raise ValueError(
            "DATABASE_URL must start with postgresql://"
        )

    return create_engine(database_url)


def load_orders(df):

    engine = get_engine()

    df.to_sql(
        "orders",
        engine,
        if_exists="append",
        index=False
    )


def load_customers(df):

    engine = get_engine()

    df.to_sql(
        "customers",
        engine,
        if_exists="append",
        index=False
    )


def load_products(df):

    engine = get_engine()

    df.to_sql(
        "products",
        engine,
        if_exists="append",
        index=False
    )