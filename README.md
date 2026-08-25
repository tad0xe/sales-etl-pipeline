# 📊 Sales ETL Pipeline

A Python-based ETL (Extract, Transform, Load) pipeline that processes sales data from Excel, cleans and validates the data, loads it into PostgreSQL, and displays the results through a Streamlit dashboard.

## 🚀 Project Overview

This project simulates a real-world data engineering workflow.

The pipeline:

1. Extracts sales data from an Excel workbook.
2. Cleans and transforms inconsistent data.
3. Validates data quality.
4. Loads cleaned data into PostgreSQL.
5. Displays ETL results in a Streamlit dashboard.
6. Allows users to download the cleaned dataset as an Excel file.

## 🏗️ Architecture

```text
                Excel Dataset
                     │
                     ▼
                  EXTRACT
                     │
                     ▼
                 TRANSFORM
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
   Clean Data    Validate    Standardize
         │
         ▼
                    LOAD
                     │
                     ▼
                PostgreSQL
                     │
                     ▼
             Streamlit Dashboard
                     │
                     ▼
             Clean Excel Export
