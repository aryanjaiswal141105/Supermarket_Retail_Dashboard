
import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(
    page_title="Supermarket Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Supermarket Smart Retail & Customer Dashboard")
st.write("Analyze supermarket sales and customer behavior.")

# Upload CSV file
file = st.sidebar.file_uploader("Upload Supermarket CSV", type="csv")

if file is not None:

    # Load dataset
    df = pd.read_csv(file, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()

    # Remove empty rows
    df = df.dropna(subset=["Net_Sales_INR", "Profit_INR"])

    # Sidebar filters
    st.sidebar.header("Filters")

    gender = st.sidebar.multiselect(
        "Select Gender",
        df["Gender"].dropna().unique(),
        default=list(df["Gender"].dropna().unique())
    )

    category = st.sidebar.multiselect(
        "Select Product Category",
        df["Product_Category"].dropna().unique(),
        default=list(df["Product_Category"].dropna().unique())
    )

    # Filter data
    data = df[
        (df["Gender"].isin(gender)) &
        (df["Product_Category"].isin(category))
    ]

    if not data.empty:

        # KPI calculations
        revenue = data["Net_Sales_INR"].sum()
        profit = data["Profit_INR"].sum()
        orders = data["Transaction_ID"].nunique()
        customers = data["Customer_ID"].nunique()

        # Display KPIs
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Revenue", f"₹{revenue:,.0f}")
        c2.metric("Total Profit", f"₹{profit:,.0f}")
        c3.metric("Total Orders", f"{orders:,}")
        c4.metric("Customers", f"{customers:,}")

        st.divider()

        # Sales by product category
        st.subheader("Sales by Product Category")

        sales = data.groupby("Product_Category")[
            "Net_Sales_INR"
        ].sum().reset_index()

        fig1 = px.bar(
            sales,
            x="Product_Category",
            y="Net_Sales_INR",
            color="Product_Category",
            title="Category-wise Revenue"
        )

        st.plotly_chart(fig1, use_container_width=True)

        # Payment method analysis
        st.subheader("Customer Payment Methods")

        payment = data.groupby("Payment_Method")[
            "Transaction_ID"
        ].nunique().reset_index(name="Transactions")

        fig2 = px.pie(
            payment,
            names="Payment_Method",
            values="Transactions",
            title="Transactions by Payment Method",
            hole=0.4
        )

        st.plotly_chart(fig2, use_container_width=True)

        # View filtered data
        with st.expander("View Customer Data"):
            st.dataframe(data, use_container_width=True)

    else:
        st.warning("No records match the selected filters.")

else:
    st.info("Upload your supermarket CSV file using the sidebar.")