import pandas as pd
from pathlib import Path


OUTPUT_DIR = Path("data/processed")


def export_to_excel(
    orders,
    customers,
    products
):
    # Create output folder if it doesn't exist
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        OUTPUT_DIR / "cleaned_sales_data.xlsx"
    )

    # Create Excel workbook
    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        orders.to_excel(
            writer,
            sheet_name="orders",
            index=False
        )

        customers.to_excel(
            writer,
            sheet_name="customers",
            index=False
        )

        products.to_excel(
            writer,
            sheet_name="products",
            index=False
        )

    print(
        f"\nClean Excel file created: "
        f"{output_file}"
    )