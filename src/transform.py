import pandas as pd


def clean_country(country):

    if pd.isna(country):
        return None

    country = str(country).strip().lower()

    country_mapping = {
        "us": "United States",
        "usa": "United States",
        "u.s.a.": "United States",
        "united states": "United States",

        "germany": "Germany",

        "brzil": "Brazil",
        "brazil": "Brazil",

        "cnada": "Canada",
        "canada": "Canada",

        "japan": "Japan",
        "india": "India",
        "france": "France",
        "mexico": "Mexico",
        "australia": "Australia",

        "england": "United Kingdom",
        "united kingdom": "United Kingdom"
    }

    return country_mapping.get(
        country,
        country.title()
    )


def clean_price(value):

    if pd.isna(value):
        return None

    value = str(value)

    value = value.replace("$", "")
    value = value.replace(",", "")
    value = value.strip()

    try:
        return float(value)

    except ValueError:
        return None


def clean_orders(df):

    # Create copy
    df = df.copy()

    print("\n========== CLEANING ORDERS ==========")

    print("Rows before cleaning:", len(df))

    # -------------------------
    # 1. Remove duplicate rows
    # -------------------------

    df = df.drop_duplicates()

    print("Rows after removing duplicates:", len(df))

    # -------------------------
    # 2. Clean category
    # -------------------------

    df["category"] = (
        df["category"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # -------------------------
    # 3. Clean country
    # -------------------------

    df["country"] = df["country"].apply(
        clean_country
    )

    # -------------------------
    # 4. Clean prices
    # -------------------------

    df["unit_price"] = df["unit_price"].apply(
        clean_price
    )

    df["total_price"] = df["total_price"].apply(
        clean_price
    )

    # -------------------------
    # 5. Convert quantity
    # -------------------------

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    # -------------------------
    # 6. Remove invalid quantities
    # -------------------------

    invalid_quantity = df["quantity"] <= 0

    print(
        "Invalid quantities:",
        invalid_quantity.sum()
    )

    df = df[
        df["quantity"] > 0
    ]

    # -------------------------
    # 7. Remove invalid prices
    # -------------------------

    invalid_price = (
        df["unit_price"].isna()
        | (df["unit_price"] <= 0)
    )

    print(
        "Invalid prices:",
        invalid_price.sum()
    )

    df = df[
        df["unit_price"] > 0
    ]

    # -------------------------
    # 8. Calculate correct totals
    # -------------------------

    df["calculated_total"] = (
        df["quantity"]
        * df["unit_price"]
    )

    # Find incorrect totals

    incorrect_totals = (
        df["total_price"].round(2)
        !=
        df["calculated_total"].round(2)
    )

    print(
        "Incorrect totals found:",
        incorrect_totals.sum()
    )

    # Replace with correct total

    df["total_price"] = (
        df["calculated_total"]
    )

    # Remove temporary column

    df = df.drop(
        columns=["calculated_total"]
    )

    # -------------------------
    # 9. Clean order dates
    # -------------------------

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    invalid_dates = df["order_date"].isna()

    print(
        "Invalid dates:",
        invalid_dates.sum()
    )

    # Remove rows with invalid dates

    df = df.dropna(
        subset=["order_date"]
    )

    # -------------------------
    # Final result
    # -------------------------

    print(
        "Final cleaned rows:",
        len(df)
    )

    return df


def clean_customers(df):

    df = df.copy()

    print("\n========== CLEANING CUSTOMERS ==========")

    print(
        "Rows before cleaning:",
        len(df)
    )

    # Remove duplicates

    df = df.drop_duplicates()

    # Clean country

    df["country"] = df["country"].apply(
        clean_country
    )

    # Clean city

    df["city"] = (
        df["city"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # Convert signup date

    df["signup_date"] = pd.to_datetime(
        df["signup_date"],
        errors="coerce"
    )

    print(
        "Invalid signup dates:",
        df["signup_date"].isna().sum()
    )

    print(
        "Final customer rows:",
        len(df)
    )

    return df


def clean_products(df):

    df = df.copy()

    print("\n========== CLEANING PRODUCTS ==========")

    # Remove duplicates

    df = df.drop_duplicates()

    # Clean category

    df["category"] = (
        df["category"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # Convert price

    df["list_price"] = df["list_price"].apply(
        clean_price
    )

    print(
        "Final product rows:",
        len(df)
    )

    return df