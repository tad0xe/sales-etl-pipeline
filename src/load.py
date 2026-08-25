import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


# Load variables from .env
load_dotenv()


def get_engine():

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    connection_string = (
        f"postgresql+psycopg2://"
        f"{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )

    engine = create_engine(connection_string)

    return engine


def load_orders(df):

    engine = get_engine()

    df.to_sql(
        "orders",
        engine,
        if_exists="replace",
        index=False
    )

    print("Orders loaded successfully!")


def load_customers(df):

    engine = get_engine()

    df.to_sql(
        "customers",
        engine,
        if_exists="replace",
        index=False
    )

    print("Customers loaded successfully!")


def load_products(df):

    engine = get_engine()

    df.to_sql(
        "products",
        engine,
        if_exists="replace",
        index=False
    )

    print("Products loaded successfully!")