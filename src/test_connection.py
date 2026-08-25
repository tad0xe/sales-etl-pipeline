import pandas as pd


FILE_PATH = "data/sales_data.xlsx"


def extract_orders():
    return pd.read_excel(
        FILE_PATH,
        sheet_name="orders"
    )


def extract_customers():
    return pd.read_excel(
        FILE_PATH,
        sheet_name="dim_customers"
    )


def extract_products():
    return pd.read_excel(
        FILE_PATH,
        sheet_name="dim_products"
    )


if __name__ == "__main__":

    orders = extract_orders()
    customers = extract_customers()
    products = extract_products()

    print("ORDERS")
    print(orders.head())

    print("\nCUSTOMERS")
    print(customers.head())

    print("\nPRODUCTS")
    print(products.head())

    print("\nROWS")
    print("Orders:", len(orders))
    print("Customers:", len(customers))
    print("Products:", len(products))