from export import export_to_excel

from extract import (
    extract_orders,
    extract_customers,
    extract_products
)

from transform import (
    clean_orders,
    clean_customers,
    clean_products
)

from load import (
    load_orders,
    load_customers,
    load_products
)


def run_pipeline():

    print("\n" + "=" * 50)
    print("STARTING ETL PIPELINE")
    print("=" * 50)

    # =========================
    # EXTRACT
    # =========================

    print("\nSTEP 1: EXTRACTING DATA")

    orders = extract_orders()
    customers = extract_customers()
    products = extract_products()

    print("Orders extracted:", len(orders))
    print("Customers extracted:", len(customers))
    print("Products extracted:", len(products))

    # =========================
    # TRANSFORM
    # =========================

    print("\nSTEP 2: TRANSFORMING DATA")

    clean_orders_data = clean_orders(orders)
    clean_customers_data = clean_customers(customers)
    clean_products_data = clean_products(products)

    # =========================
    # LOAD
    # =========================

    print("\nSTEP 3: LOADING DATA INTO POSTGRESQL")

    load_orders(clean_orders_data)
    load_customers(clean_customers_data)
    load_products(clean_products_data)

    # =========================
    # EXPORT CLEAN EXCEL
    # =========================

    print("\nSTEP 4: EXPORTING CLEAN EXCEL")

    export_to_excel(
        clean_orders_data,
        clean_customers_data,
        clean_products_data
    )

    # =========================
    # COMPLETE
    # =========================

    print("\n" + "=" * 50)
    print("ETL PIPELINE COMPLETE")
    print("=" * 50)

    print("\nFINAL DATA SUMMARY")

    print("Clean Orders:", len(clean_orders_data))
    print("Clean Customers:", len(clean_customers_data))
    print("Clean Products:", len(clean_products_data))

    print("\nPipeline Status: SUCCESS")


if __name__ == "__main__":
    run_pipeline()