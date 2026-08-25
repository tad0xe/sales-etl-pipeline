import streamlit as st
import pandas as pd
import io

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


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Sales ETL Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("📊 Sales Data ETL Pipeline")

st.write(
    "Automated ETL pipeline for cleaning, validating "
    "and loading sales data."
)

st.divider()


# ==========================================
# DATASET LOCATION
# ==========================================

DATA_FILE = "data/sales_data.xlsx"


st.subheader("📁 Dataset")

st.info(
    "The application automatically uses the dataset "
    "stored in the project."
)

st.code(DATA_FILE)


# ==========================================
# RUN PIPELINE
# ==========================================

if st.button(
    "🚀 RUN ETL PIPELINE",
    type="primary"
):

    try:

        # ======================================
        # EXTRACT
        # ======================================

        with st.spinner("Extracting data..."):

            orders = pd.read_excel(
                DATA_FILE,
                sheet_name="orders"
            )

            customers = pd.read_excel(
                DATA_FILE,
                sheet_name="dim_customers"
            )

            products = pd.read_excel(
                DATA_FILE,
                sheet_name="dim_products"
            )

        st.success("✅ Data extracted successfully")


        # ======================================
        # TRANSFORM
        # ======================================

        with st.spinner("Cleaning and transforming data..."):

            clean_orders_data = clean_orders(
                orders
            )

            clean_customers_data = clean_customers(
                customers
            )

            clean_products_data = clean_products(
                products
            )

        st.success("✅ Data transformed successfully")


        # ======================================
        # LOAD
        # ======================================

        with st.spinner(
            "Loading data into PostgreSQL..."
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
            "✅ Data loaded into PostgreSQL"
        )


        # ======================================
        # SUMMARY
        # ======================================

        st.divider()

        st.header("📊 Pipeline Results")


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


        # ======================================
        # DATA PREVIEW
        # ======================================

        st.divider()

        st.header("🧹 Cleaned Data")


        tab1, tab2, tab3 = st.tabs(
            [
                "Orders",
                "Customers",
                "Products"
            ]
        )


        with tab1:

            st.dataframe(
                clean_orders_data,
                use_container_width=True
            )


        with tab2:

            st.dataframe(
                clean_customers_data,
                use_container_width=True
            )


        with tab3:

            st.dataframe(
                clean_products_data,
                use_container_width=True
            )


        # ======================================
        # EXPORT EXCEL
        # ======================================

        output = io.BytesIO()


        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            clean_orders_data.to_excel(
                writer,
                sheet_name="orders",
                index=False
            )

            clean_customers_data.to_excel(
                writer,
                sheet_name="customers",
                index=False
            )

            clean_products_data.to_excel(
                writer,
                sheet_name="products",
                index=False
            )


        st.divider()

        st.header("📥 Export")


        st.download_button(
            label="Download Clean Excel",
            data=output.getvalue(),
            file_name="cleaned_sales_data.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )


        st.success(
            "🎉 ETL PIPELINE COMPLETED SUCCESSFULLY!"
        )


    except Exception as e:

        st.error(
            "❌ ETL pipeline failed."
        )

        st.exception(e)