import streamlit as st
import pandas as pd
import io
import os

from src.transform import (
    clean_orders,
    clean_customers,
    clean_products
)

from src.load import (
    load_orders,
    load_customers,
    load_products
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Sales ETL Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# REQUIRED COLUMNS
# =========================================================

REQUIRED_ORDER_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "customer_name",
    "region",
    "country",
    "product_id",
    "product_name",
    "category",
    "quantity",
    "unit_price",
    "total_price",
    "payment_method",
    "order_status"
]

REQUIRED_CUSTOMER_COLUMNS = [
    "customer_id",
    "customer_name",
    "city",
    "country",
    "signup_date"
]

REQUIRED_PRODUCT_COLUMNS = [
    "product_id",
    "product_name",
    "category",
    "list_price"
]


# =========================================================
# HELPER - CLEAN COLUMN NAMES
# =========================================================

def clean_column_names(df):

    df = df.copy()

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    return df


# =========================================================
# VALIDATE COLUMNS
# =========================================================

def validate_columns(df, required_columns):

    df = clean_column_names(df)

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    return missing


# =========================================================
# COMPACT VALIDATION UI
# =========================================================

def show_validation(df, required_columns):

    df = clean_column_names(df)

    missing = validate_columns(
        df,
        required_columns
    )

    status = []

    for column in required_columns:

        if column in df.columns:
            status.append(f"✅ `{column}`")
        else:
            status.append(f"❌ `{column}`")

    st.markdown(
        " ".join(status)
    )

    if missing:

        st.warning(
            "Missing: "
            + ", ".join(
                f"`{column}`"
                for column in missing
            )
        )

        return False

    st.success(
        "✅ All required columns are present"
    )

    return True


# =========================================================
# CREATE EXCEL FILE
# =========================================================

def create_excel(
    orders,
    customers,
    products
):

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
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

    return output.getvalue()


# =========================================================
# RUN ETL
# =========================================================

def run_etl(
    orders,
    customers,
    products
):

    try:

        # =================================================
        # EXTRACT
        # =================================================

        with st.spinner("Extracting data..."):

            orders = clean_column_names(orders)
            customers = clean_column_names(customers)
            products = clean_column_names(products)

        st.success("✅ Extract complete")


        # =================================================
        # TRANSFORM
        # =================================================

        with st.spinner(
            "Cleaning and transforming..."
        ):

            clean_orders_data = clean_orders(
                orders
            )

            clean_customers_data = clean_customers(
                customers
            )

            clean_products_data = clean_products(
                products
            )

        st.success("✅ Transform complete")


        # =================================================
        # LOAD
        # =================================================

        with st.spinner(
            "Loading into PostgreSQL..."
        ):

            load_orders(
                clean_orders_data
            )

            load_customers(
                clean_customers_data
            )

            load_products(
                clean_products_data
            )

        st.success(
            "✅ PostgreSQL load complete"
        )


        # =================================================
        # RESULTS
        # =================================================

        st.divider()

        st.subheader("📊 Results")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Orders",
                len(clean_orders_data)
            )

        with col2:

            st.metric(
                "Customers",
                len(clean_customers_data)
            )

        with col3:

            st.metric(
                "Products",
                len(clean_products_data)
            )


        # =================================================
        # CLEAN DATA
        # =================================================

        st.divider()

        st.subheader("🧹 Cleaned Data")

        orders_tab, customers_tab, products_tab = st.tabs(
            [
                "🛒 Orders",
                "👥 Customers",
                "📦 Products"
            ]
        )

        with orders_tab:

            st.dataframe(
                clean_orders_data,
                use_container_width=True
            )

        with customers_tab:

            st.dataframe(
                clean_customers_data,
                use_container_width=True
            )

        with products_tab:

            st.dataframe(
                clean_products_data,
                use_container_width=True
            )


        # =================================================
        # EXPORT
        # =================================================

        st.divider()

        excel_data = create_excel(
            clean_orders_data,
            clean_customers_data,
            clean_products_data
        )

        st.download_button(
            label="⬇️ Download Clean Excel",
            data=excel_data,
            file_name="cleaned_sales_data.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            key="download_clean_excel"
        )

        st.success(
            "🎉 ETL pipeline completed successfully!"
        )

        return True

    except Exception as e:

        st.error(
            "❌ ETL pipeline failed"
        )

        st.exception(e)

        return False


# =========================================================
# HEADER
# =========================================================

st.title("📊 Sales ETL Pipeline")

st.caption(
    "Extract → Transform → Load → PostgreSQL"
)


# =========================================================
# MAIN TABS
# =========================================================

demo_tab, upload_tab = st.tabs(
    [
        "🏠 Demo Dataset",
        "📤 Upload Dataset"
    ]
)


# =========================================================
# DEMO DATASET
# =========================================================

with demo_tab:

    DATA_FILE = "data/sales_data.xlsx"

    st.subheader("🏠 Demo Dataset")

    if not os.path.exists(DATA_FILE):

        st.error(
            f"❌ Dataset not found: `{DATA_FILE}`"
        )

    else:

        try:

            # =================================================
            # READ DEMO EXCEL
            # =================================================

            excel_file = pd.ExcelFile(
                DATA_FILE
            )

            sheets = excel_file.sheet_names


            # =================================================
            # FIND SHEETS
            # =================================================

            if "orders" not in sheets:

                st.error(
                    "❌ `orders` sheet is missing."
                )

                st.stop()


            if "customers" in sheets:

                customer_sheet = "customers"

            elif "dim_customers" in sheets:

                customer_sheet = "dim_customers"

            else:

                st.error(
                    "❌ Customer sheet is missing."
                )

                st.stop()


            if "products" in sheets:

                product_sheet = "products"

            elif "dim_products" in sheets:

                product_sheet = "dim_products"

            else:

                st.error(
                    "❌ Product sheet is missing."
                )

                st.stop()


            # =================================================
            # LOAD DATA
            # =================================================

            demo_orders = pd.read_excel(
                DATA_FILE,
                sheet_name="orders"
            )

            demo_customers = pd.read_excel(
                DATA_FILE,
                sheet_name=customer_sheet
            )

            demo_products = pd.read_excel(
                DATA_FILE,
                sheet_name=product_sheet
            )


            # =================================================
            # DATA COUNTS
            # =================================================

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Orders",
                    len(demo_orders)
                )

            with col2:

                st.metric(
                    "Customers",
                    len(demo_customers)
                )

            with col3:

                st.metric(
                    "Products",
                    len(demo_products)
                )


            # =================================================
            # DOWNLOAD DEMO DATASET
            # =================================================

            with open(
                DATA_FILE,
                "rb"
            ) as file:

                demo_excel_data = file.read()


            st.download_button(
                label="⬇️ Download Demo Dataset",
                data=demo_excel_data,
                file_name="sales_data.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                key="download_demo_dataset"
            )


            # =================================================
            # PREVIEW
            # =================================================

            st.divider()

            st.subheader("👀 Preview")

            preview_orders, preview_customers, preview_products = st.tabs(
                [
                    "🛒 Orders",
                    "👥 Customers",
                    "📦 Products"
                ]
            )

            with preview_orders:

                st.dataframe(
                    demo_orders.head(10),
                    use_container_width=True
                )

            with preview_customers:

                st.dataframe(
                    demo_customers.head(10),
                    use_container_width=True
                )

            with preview_products:

                st.dataframe(
                    demo_products.head(10),
                    use_container_width=True
                )


            # =================================================
            # RUN DEMO ETL
            # =================================================

            st.divider()

            if st.button(
                "🚀 Run ETL",
                type="primary",
                use_container_width=True,
                key="demo_run_etl"
            ):

                run_etl(
                    demo_orders,
                    demo_customers,
                    demo_products
                )


        except Exception as e:

            st.error(
                "❌ Could not read demo Excel file."
            )

            st.exception(e)


# =========================================================
# UPLOAD DATASET
# =========================================================

with upload_tab:

    st.subheader("📤 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Choose Excel file",
        type=["xlsx"],
        key="excel_uploader"
    )


    # =====================================================
    # REQUIRED STRUCTURE
    # =====================================================

    with st.expander(
        "📋 Required Excel structure"
    ):

        st.write(
            "**Sheets:**"
        )

        st.code(
            "orders\n"
            "customers OR dim_customers\n"
            "products OR dim_products"
        )

        st.write(
            "**Orders:**"
        )

        st.code(
            "order_id | order_date | customer_id | "
            "customer_name | region | country | "
            "product_id | product_name | category | "
            "quantity | unit_price | total_price | "
            "payment_method | order_status"
        )

        st.write(
            "**Customers:**"
        )

        st.code(
            "customer_id | customer_name | city | "
            "country | signup_date"
        )

        st.write(
            "**Products:**"
        )

        st.code(
            "product_id | product_name | category | list_price"
        )


    # =====================================================
    # PROCESS UPLOAD
    # =====================================================

    if uploaded_file:

        try:

            excel_file = pd.ExcelFile(
                uploaded_file
            )

            sheets = excel_file.sheet_names


            # =================================================
            # FIND CUSTOMER SHEET
            # =================================================

            if "customers" in sheets:

                customer_sheet = "customers"

            elif "dim_customers" in sheets:

                customer_sheet = "dim_customers"

            else:

                customer_sheet = None


            # =================================================
            # FIND PRODUCT SHEET
            # =================================================

            if "products" in sheets:

                product_sheet = "products"

            elif "dim_products" in sheets:

                product_sheet = "dim_products"

            else:

                product_sheet = None


            # =================================================
            # ORDERS
            # =================================================

            if "orders" not in sheets:

                orders_valid = False

                st.error(
                    "❌ Orders sheet missing"
                )

                upload_orders = None

            else:

                upload_orders = pd.read_excel(
                    uploaded_file,
                    sheet_name="orders"
                )

                orders_valid = show_validation(
                    upload_orders,
                    REQUIRED_ORDER_COLUMNS
                )


            # =================================================
            # CUSTOMERS
            # =================================================

            if customer_sheet is None:

                customers_valid = False

                st.error(
                    "❌ Customer sheet missing"
                )

                upload_customers = None

            else:

                upload_customers = pd.read_excel(
                    uploaded_file,
                    sheet_name=customer_sheet
                )

                customers_valid = show_validation(
                    upload_customers,
                    REQUIRED_CUSTOMER_COLUMNS
                )


            # =================================================
            # PRODUCTS
            # =================================================

            if product_sheet is None:

                products_valid = False

                st.error(
                    "❌ Product sheet missing"
                )

                upload_products = None

            else:

                upload_products = pd.read_excel(
                    uploaded_file,
                    sheet_name=product_sheet
                )

                products_valid = show_validation(
                    upload_products,
                    REQUIRED_PRODUCT_COLUMNS
                )


            # =================================================
            # RUN UPLOAD ETL
            # =================================================

            st.divider()

            if (
                orders_valid
                and customers_valid
                and products_valid
            ):

                st.success(
                    "✅ Dataset ready"
                )

                if st.button(
                    "🚀 Run ETL",
                    type="primary",
                    use_container_width=True,
                    key="upload_run_etl"
                ):

                    run_etl(
                        upload_orders,
                        upload_customers,
                        upload_products
                    )

            else:

                st.warning(
                    "⚠️ Fix the missing columns before running ETL."
                )


        except Exception as e:

            st.error(
                "❌ Could not read Excel file."
            )

            st.exception(e)