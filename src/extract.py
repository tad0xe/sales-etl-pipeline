import pandas as pd


FILE_PATH = "data/sales_data.xlsx"


def extract_orders():
    orders = pd.read_excel(
        FILE_PATH,
        sheet_name="orders"
    )

    return orders


def extract_customers():
    customers = pd.read_excel(
        FILE_PATH,
        sheet_name="dim_customers"
    )

    return customers


def extract_products():
    products = pd.read_excel(
        FILE_PATH,
        sheet_name="dim_products"
    )

    return products


if __name__ == "__main__":

    orders = extract_orders()
    customers = extract_customers()
    products = extract_products()

    print("\n========== ORDERS ==========")
    print(orders.head())

    print("\n========== CUSTOMERS ==========")
    print(customers.head())

    print("\n========== PRODUCTS ==========")
    print(products.head())

    print("\n========== ROW COUNTS ==========")
    print("Orders:", len(orders))
    print("Customers:", len(customers))
    print("Products:", len(products))