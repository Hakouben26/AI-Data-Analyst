
import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_loader import load_data
from src.data_profiler import (
    get_dataset_overview,
    get_column_profile,
    get_numeric_statistics,
    get_categorical_summary
)
from src.data_cleaner import clean_data
from src.visualizer import create_chart
from src.ai_analyst import (
    ask_data_question,
    generate_ai_insights
)


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. PREMIUM MODERN DESIGN
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 85% 0%, rgba(91, 73, 180, 0.12), transparent 30%),
        #0B1120;
    color: #E5E7EB;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111B30 0%, #0D1527 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.13);
}

[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

h1, h2, h3 {
    color: #F8FAFC !important;
    font-weight: 750 !important;
}

p, label, span {
    color: #CBD5E1;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #17243B, #111B2E);
    border: 1px solid rgba(148, 163, 184, 0.16);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
    font-size: 13px !important;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    color: #2DD4BF !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: rgba(148, 163, 184, 0.16) !important;
    border-radius: 16px !important;
    background: rgba(20, 32, 52, 0.72);
}

.stButton > button {
    border: 0;
    border-radius: 10px;
    background: linear-gradient(90deg, #7357E8, #3989E8);
    color: white !important;
    font-weight: 700;
    padding: 0.65rem 1rem;
    transition: 0.2s ease;
}

.stButton > button:hover {
    filter: brightness(1.12);
    transform: translateY(-1px);
}

.stDownloadButton > button {
    border-radius: 10px;
    background: #17243B;
    color: #E2E8F0 !important;
    border: 1px solid #334155;
}

[data-testid="stFileUploader"] {
    background: rgba(20, 32, 52, 0.65);
    border: 1px dashed #64748B;
    border-radius: 12px;
    padding: 10px;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 12px;
}

.stSelectbox div[data-baseweb="select"] > div,
.stTextInput input,
.stTextArea textarea {
    background-color: #17243B !important;
    color: #F8FAFC !important;
    border-color: #334155 !important;
}

hr {
    border-color: rgba(148, 163, 184, 0.16);
}

.hero {
    padding: 26px 30px;
    border-radius: 20px;
    background: linear-gradient(115deg, #202B50 0%, #30245D 52%, #123B50 100%);
    border: 1px solid rgba(167, 139, 250, 0.25);
    margin-bottom: 24px;
}

.hero-title {
    color: #FFFFFF;
    font-size: 30px;
    font-weight: 800;
    margin-bottom: 6px;
}

.hero-subtitle {
    color: #CBD5E1;
    font-size: 14px;
}

.section-caption {
    color: #94A3B8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.status-pill {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 30px;
    background: rgba(45, 212, 191, 0.12);
    border: 1px solid rgba(45, 212, 191, 0.3);
    color: #5EEAD4;
    font-size: 12px;
    font-weight: 700;
}

.small-muted {
    color: #94A3B8;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. SESSION STATE
# =========================================================

defaults = {
    "raw_df": None,
    "cleaned_df": None,
    "file_signature": None,
    "cleaning_report": None,
    "ai_report": None,
    "chat_history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 4. HELPER FUNCTIONS
# =========================================================

def show_header(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_title(title, subtitle=None):
    st.markdown(f"### {title}")

    if subtitle:
        st.caption(subtitle)


def get_active_data():
    if st.session_state.cleaned_df is not None:
        return st.session_state.cleaned_df

    return st.session_state.raw_df


def build_revenue_frame(df):
    """
    Calculate revenue only for valid financial records.
    Missing quantity, unit price or discount rows are excluded.
    """

    required = ["Quantity", "Unit_Price"]

    if not all(column in df.columns for column in required):
        return pd.DataFrame(), (
            "Revenue cannot be calculated: Quantity and "
            "Unit_Price columns are required."
        )

    sales = df.copy()

    sales["Quantity"] = pd.to_numeric(
        sales["Quantity"], errors="coerce"
    )

    sales["Unit_Price"] = pd.to_numeric(
        sales["Unit_Price"], errors="coerce"
    )

    if "Discount" in sales.columns:
        sales["Discount"] = pd.to_numeric(
            sales["Discount"], errors="coerce"
        )

        discount = sales["Discount"].copy()

        non_missing = discount.dropna()

        if not non_missing.empty and non_missing.abs().max() > 1:
            discount = discount / 100

        valid = sales[
            ["Quantity", "Unit_Price", "Discount"]
        ].notna().all(axis=1)

    else:
        discount = pd.Series(0.0, index=sales.index)

        valid = sales[
            ["Quantity", "Unit_Price"]
        ].notna().all(axis=1)

    valid &= sales["Quantity"].ge(0)
    valid &= sales["Unit_Price"].ge(0)
    valid &= discount.ge(0) & discount.le(1)

    sales["Revenue"] = pd.NA

    sales.loc[valid, "Revenue"] = (
        sales.loc[valid, "Quantity"]
        * sales.loc[valid, "Unit_Price"]
        * (1 - discount.loc[valid])
    )

    valid_sales = sales.loc[valid].copy()

    if valid_sales.empty:
        return valid_sales, "No complete financial records were found."

    note = (
        f"{len(valid_sales)} of {len(sales)} records included "
        f"in revenue calculations."
    )

    if "Discount" not in df.columns:
        note += " No Discount column was found; discount assumed to be 0%."

    return valid_sales, note


def format_currency(value):
    return f"{value:,.2f} DZD"


def make_chart_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter",
            color="#CBD5E1"
        ),
        title_font=dict(
            size=16,
            color="#F8FAFC"
        ),
        margin=dict(l=15, r=15, t=55, b=15),
        height=350,
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )
    )

    fig.update_xaxes(
        gridcolor="rgba(148,163,184,0.10)",
        zerolinecolor="rgba(148,163,184,0.10)"
    )

    fig.update_yaxes(
        gridcolor="rgba(148,163,184,0.10)",
        zerolinecolor="rgba(148,163,184,0.10)"
    )

    return fig


def apply_filters(df, city, category, product):
    filtered = df.copy()

    if city != "All" and "City" in filtered.columns:
        filtered = filtered[filtered["City"].astype(str) == city]

    if category != "All" and "Category" in filtered.columns:
        filtered = filtered[
            filtered["Category"].astype(str) == category
        ]

    if product != "All" and "Product" in filtered.columns:
        filtered = filtered[
            filtered["Product"].astype(str) == product
        ]

    return filtered


# =========================================================
# 5. SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 10px 4px 22px 4px;">
            <div style="font-size:27px;font-weight:800;color:white;">
                ◈ Data<span style="color:#A78BFA;">Mind</span>
            </div>
            <div style="font-size:11px;color:#94A3B8;letter-spacing:2px;">
                AI ANALYTICS PLATFORM
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Data Explorer",
            "Data Cleaning",
            "Visualization",
            "AI Insights",
            "AI Data Chat"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("#### DATA SOURCE")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:

        signature = (
            uploaded_file.name,
            uploaded_file.size
        )

        if signature != st.session_state.file_signature:

            try:
                uploaded_file.seek(0)
                loaded_df = load_data(uploaded_file)

                st.session_state.raw_df = loaded_df
                st.session_state.cleaned_df = None
                st.session_state.file_signature = signature
                st.session_state.cleaning_report = None
                st.session_state.ai_report = None
                st.session_state.chat_history = []

                st.success("Dataset loaded successfully.")

            except Exception as error:
                st.error(str(error))

    if st.session_state.raw_df is not None:

        active_df = get_active_data()

        st.markdown(
            f"""
            <div style="padding:12px;background:#17243B;border-radius:12px;">
                <div style="font-size:12px;color:#94A3B8;">CURRENT DATASET</div>
                <div style="font-weight:700;color:white;overflow-wrap:anywhere;">
                    {uploaded_file.name if uploaded_file else "Loaded dataset"}
                </div>
                <div style="font-size:12px;color:#2DD4BF;margin-top:7px;">
                    {len(active_df):,} rows · {len(active_df.columns)} columns
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Reset Dataset", use_container_width=True):
            st.session_state.raw_df = None
            st.session_state.cleaned_df = None
            st.session_state.file_signature = None
            st.session_state.cleaning_report = None
            st.session_state.ai_report = None
            st.session_state.chat_history = []
            st.rerun()

    else:
        st.info("Upload a dataset to start your analysis.")

    st.divider()

    st.markdown(
        """
        <div style="font-size:11px;color:#64748B;">
            POWERED BY PYTHON · PANDAS · PLOTLY · GROQ AI
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 6. CHECK DATASET
# =========================================================

df = get_active_data()

if df is None:

    show_header(
        "Welcome to AI Data Analyst",
        "Transform your raw data into meaningful business intelligence."
    )

    st.markdown("## Start your analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### 📂 Upload")
            st.write("Import CSV and Excel datasets.")

    with col2:
        with st.container(border=True):
            st.markdown("### 🧹 Clean")
            st.write("Detect missing values and duplicates.")

    with col3:
        with st.container(border=True):
            st.markdown("### 🤖 Analyze")
            st.write("Generate charts, insights and AI reports.")

    st.info(
        "Upload a CSV or Excel file from the left sidebar "
        "to open your analytics workspace."
    )

    st.stop()


# =========================================================
# 7. DASHBOARD FILTERS
# =========================================================

if page == "Dashboard":

    show_header(
        "Executive Dashboard",
        "Your business performance at a glance."
    )

    filter_columns = st.columns(3)

    with filter_columns[0]:
        city_options = ["All"]

        if "City" in df.columns:
            city_options += sorted(
                df["City"].dropna().astype(str).unique().tolist()
            )

        selected_city = st.selectbox("City", city_options)

    with filter_columns[1]:
        category_options = ["All"]

        if "Category" in df.columns:
            category_options += sorted(
                df["Category"].dropna().astype(str).unique().tolist()
            )

        selected_category = st.selectbox(
            "Category", category_options
        )

    with filter_columns[2]:
        product_options = ["All"]

        if "Product" in df.columns:
            product_options += sorted(
                df["Product"].dropna().astype(str).unique().tolist()
            )

        selected_product = st.selectbox(
            "Product", product_options
        )

    dashboard_df = apply_filters(
        df,
        selected_city,
        selected_category,
        selected_product
    )

    revenue_df, revenue_note = build_revenue_frame(dashboard_df)

    st.markdown('<div class="section-caption">KEY PERFORMANCE INDICATORS</div>',
                unsafe_allow_html=True)

    total_orders = len(dashboard_df)

    total_customers = (
        dashboard_df["Customer"].nunique()
        if "Customer" in dashboard_df.columns else 0
    )

    total_products = (
        dashboard_df["Product"].nunique()
        if "Product" in dashboard_df.columns else 0
    )

    total_revenue = (
        float(revenue_df["Revenue"].sum())
        if not revenue_df.empty else 0
    )

    average_order_value = (
        total_revenue / len(revenue_df)
        if not revenue_df.empty else 0
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "Total Revenue",
            format_currency(total_revenue)
        )

    with k2:
        st.metric(
            "Total Orders",
            f"{total_orders:,}"
        )

    with k3:
        st.metric(
            "Total Customers",
            f"{total_customers:,}"
        )

    with k4:
        st.metric(
    "Avg. Revenue / Valid Order",
    format_currency(average_order_value)
)

    st.caption(revenue_note)

    st.markdown("---")

    # Secondary KPIs

    s1, s2, s3 = st.columns(3)

    with s1:
        st.metric("Products", f"{total_products:,}")

    with s2:
        st.metric(
            "Units Sold",
            f"{revenue_df['Quantity'].sum():,.0f}"
            if not revenue_df.empty else "0"
        )

    with s3:
        st.metric(
            "Valid Revenue Records",
            f"{len(revenue_df):,}"
        )

    st.markdown("---")

    # Revenue trend

    left, right = st.columns([1.65, 1])

    with left:
        section_title(
            "Revenue Overview",
            "Revenue calculated from quantity, unit price and discount."
        )

        if (
            not revenue_df.empty
            and "Order_Date" in revenue_df.columns
        ):

            revenue_df["Order_Date"] = pd.to_datetime(
                revenue_df["Order_Date"],
                errors="coerce"
            )

            trend_df = revenue_df.dropna(
                subset=["Order_Date"]
            ).copy()

            if not trend_df.empty:

                trend_df["Date"] = (
                    trend_df["Order_Date"].dt.date
                )

                trend = (
                    trend_df.groupby("Date", as_index=False)["Revenue"]
                    .sum()
                    .sort_values("Date")
                )

                fig = px.area(
                    trend,
                    x="Date",
                    y="Revenue",
                    markers=True,
                    title="Revenue Over Time"
                )

                fig.update_traces(
                    line=dict(color="#8B7CFF", width=3),
                    fillcolor="rgba(139,124,255,0.16)"
                )

                st.plotly_chart(
                    make_chart_theme(fig),
                    use_container_width=True
                )

            else:
                st.info("No valid dates are available.")

        else:
            st.info(
                "Revenue trend requires valid Order_Date values "
                "and financial columns."
            )

    with right:
        section_title("Revenue by Category")

        if (
            not revenue_df.empty
            and "Category" in revenue_df.columns
        ):

            category_revenue = (
                revenue_df.groupby("Category", as_index=False)["Revenue"]
                .sum()
                .sort_values("Revenue", ascending=False)
            )

            fig = px.pie(
                category_revenue,
                names="Category",
                values="Revenue",
                hole=0.65
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )

            st.plotly_chart(
                make_chart_theme(fig),
                use_container_width=True
            )

        else:
            st.info("Category revenue is unavailable.")

    # Product and city charts

    left, right = st.columns(2)

    with left:
        section_title("Top Products by Revenue")

        if (
            not revenue_df.empty
            and "Product" in revenue_df.columns
        ):

            top_products = (
                revenue_df.groupby("Product", as_index=False)["Revenue"]
                .sum()
                .sort_values("Revenue", ascending=True)
                .tail(10)
            )

            fig = px.bar(
                top_products,
                x="Revenue",
                y="Product",
                orientation="h",
                text_auto=".2s"
            )

            fig.update_traces(
                marker_color="#8B7CFF",
                textposition="outside"
            )

            st.plotly_chart(
                make_chart_theme(fig),
                use_container_width=True
            )

        else:
            st.info("Product revenue is unavailable.")

    with right:
        section_title("Revenue by City")

        if (
            not revenue_df.empty
            and "City" in revenue_df.columns
        ):

            city_revenue = (
                revenue_df.groupby("City", as_index=False)["Revenue"]
                .sum()
                .sort_values("Revenue", ascending=False)
            )

            fig = px.bar(
                city_revenue,
                x="City",
                y="Revenue",
                text_auto=".2s"
            )

            fig.update_traces(
                marker_color="#2DD4BF",
                textposition="outside"
            )

            st.plotly_chart(
                make_chart_theme(fig),
                use_container_width=True
            )

        else:
            st.info("City revenue is unavailable.")

    # Data table

    section_title("Top Customers")

    if (
        not revenue_df.empty
        and "Customer" in revenue_df.columns
    ):

        top_customers = (
            revenue_df.groupby("Customer", as_index=False)
            .agg(
                Revenue=("Revenue", "sum"),
                Orders=("Revenue", "count")
            )
            .sort_values("Revenue", ascending=False)
            .head(10)
        )

        st.dataframe(
            top_customers,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Customer revenue is unavailable.")


# =========================================================
# 8. DATA EXPLORER
# =========================================================

elif page == "Data Explorer":

    show_header(
        "Data Explorer",
        "Explore your dataset structure, quality and statistical profile."
    )

    overview = get_dataset_overview(df)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", f"{overview['rows']:,}")
    c2.metric("Columns", f"{overview['columns']:,}")
    c3.metric("Missing Values", f"{overview['missing_values']:,}")
    c4.metric("Duplicate Rows", f"{overview['duplicate_rows']:,}")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Data Preview",
            "Column Profile",
            "Numeric Statistics",
            "Categorical Summary"
        ]
    )

    with tab1:
        section_title("Dataset Preview")
        st.dataframe(
            df,
            use_container_width=True,
            height=420
        )

    with tab2:
        section_title("Column Profile")
        st.dataframe(
            get_column_profile(df),
            use_container_width=True,
            hide_index=True
        )

    with tab3:
        section_title("Numerical Statistics")
        numeric_stats = get_numeric_statistics(df)

        if not numeric_stats.empty:
            st.dataframe(
                numeric_stats,
                use_container_width=True
            )
        else:
            st.info("No numerical columns found.")

    with tab4:
        section_title("Categorical Summary")
        categorical_summary = get_categorical_summary(df)

        if not categorical_summary.empty:
            st.dataframe(
                categorical_summary,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No categorical columns found.")

    st.markdown("---")

    st.download_button(
        "Download Current Dataset as CSV",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="dataset_export.csv",
        mime="text/csv"
    )


# =========================================================
# 9. DATA CLEANING
# =========================================================

elif page == "Data Cleaning":

    show_header(
        "Data Cleaning Studio",
        "Prepare your data for accurate and reliable analysis."
    )

    section_title("Cleaning Configuration")

    with st.container(border=True):

        missing_strategy = st.selectbox(
            "Missing Values Strategy",
            [
                "Keep original",
                "Drop rows with missing values",
                "Fill with median/mode"
            ]
        )

        remove_duplicates = st.checkbox(
            "Remove duplicate rows",
            value=True
        )

        trim_text = st.checkbox(
            "Remove extra spaces from text",
            value=True
        )

        if st.button(
            "Run Data Cleaning",
            use_container_width=True
        ):

            try:
                cleaned, report = clean_data(
                    df,
                    missing_strategy=missing_strategy,
                    remove_duplicates=remove_duplicates,
                    trim_text=trim_text
                )

                st.session_state.cleaned_df = cleaned
                st.session_state.cleaning_report = report
                st.session_state.ai_report = None

                st.success("Data cleaning completed successfully.")

            except Exception as error:
                st.error(f"Cleaning failed: {error}")

    if st.session_state.cleaning_report is not None:

        report = st.session_state.cleaning_report
        cleaned = st.session_state.cleaned_df

        st.markdown("---")
        section_title("Cleaning Report")

        r1, r2, r3 = st.columns(3)

        r1.metric(
            "Original Rows",
            report["initial_rows"]
        )

        r2.metric(
            "Final Rows",
            report["final_rows"]
        )

        r3.metric(
            "Removed Rows",
            report["removed_rows"]
        )

        r4, r5, r6 = st.columns(3)

        r4.metric(
            "Remaining Missing Values",
            report["remaining_missing"]
        )

        r5.metric(
            "Initial Duplicates",
            report["initial_duplicates"]
        )

        r6.metric(
            "Remaining Duplicates",
            report["remaining_duplicates"]
        )

        st.markdown("---")
        section_title("Cleaned Dataset Preview")

        st.dataframe(
            cleaned,
            use_container_width=True,
            height=350
        )

        st.download_button(
            "Download Cleaned Dataset",
            data=cleaned.to_csv(index=False).encode("utf-8-sig"),
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )


# =========================================================
# 10. VISUALIZATION STUDIO
# =========================================================

elif page == "Visualization":

    show_header(
        "Visualization Studio",
        "Build interactive charts from your own dataset."
    )

    columns = df.columns.tolist()

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    chart_type = st.selectbox(
        "Chart Type",
        [
            "Bar Chart",
            "Line Chart",
            "Scatter Plot",
            "Histogram",
            "Pie Chart"
        ]
    )

    x_column = st.selectbox(
        "X Axis / Category",
        columns
    )

    if chart_type == "Histogram":
        y_column = None

    else:
        if not numeric_columns:
            st.warning(
                "This chart requires a numerical column. "
                "Please check your dataset data types."
            )
            y_column = None

        else:
            y_column = st.selectbox(
                "Y Axis / Numerical Value",
                numeric_columns
            )

    color_options = ["None"] + columns

    color_column = st.selectbox(
        "Color / Group By",
        color_options
    )

    aggregation = "Average"

    if chart_type == "Bar Chart":
        aggregation = st.selectbox(
            "Aggregation",
            [
                "Average",
                "Sum",
                "Count",
                "Maximum",
                "Minimum"
            ]
        )

    if st.button("Generate Chart", use_container_width=True):

        try:
            if chart_type != "Histogram" and y_column is None:
                raise ValueError(
                    "Choose a numerical Y-axis column."
                )

            fig = create_chart(
                df=df,
                chart_type=chart_type,
                x_column=x_column,
                y_column=y_column,
                color_column=(
                    None if color_column == "None"
                    else color_column
                ),
                aggregation=aggregation
            )

            st.plotly_chart(
                make_chart_theme(fig),
                use_container_width=True
            )

        except Exception as error:
            st.error(f"Unable to generate chart: {error}")


# =========================================================
# 11. AI INSIGHTS GENERATOR
# =========================================================

elif page == "AI Insights":

    show_header(
        "AI Insights",
        "Turn your dataset into a professional analytical report."
    )

    st.markdown(
        """
        <div class="status-pill">● GROQ AI ENGINE</div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Generate an analytical report with business findings, "
        "data quality observations and actionable recommendations."
    )

    if st.button(
        "✨ Generate AI Analytical Report",
        use_container_width=True
    ):

        try:
            with st.spinner(
                "AI is analyzing your dataset. Please wait..."
            ):

                report = generate_ai_insights(df)

                st.session_state.ai_report = report

            st.success("Analytical report generated.")

        except Exception as error:
            st.error(f"AI report generation failed: {error}")

    if st.session_state.ai_report:

        st.markdown("---")

        section_title("Generated Analytical Report")

        st.markdown(st.session_state.ai_report)

        st.download_button(
            "Download AI Report",
            data=st.session_state.ai_report.encode("utf-8"),
            file_name="AI_Analytical_Report.md",
            mime="text/markdown"
        )


# =========================================================
# 12. AI DATA CHAT
# =========================================================

elif page == "AI Data Chat":

    show_header(
        "AI Data Assistant",
        "Ask questions about your dataset and receive data-driven answers."
    )

    st.markdown(
        '<div class="status-pill">● QWEN · GROQ API</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Examples: Which product has the highest average price? "
        "What are the main data quality issues?"
    )

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask a question about your dataset..."
    )

    if question:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            try:
                with st.spinner("Analyzing your data..."):

                    answer = ask_data_question(
                        df,
                        question
                    )

                st.markdown(answer)

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as error:

                error_message = (
                    f"Unable to answer your question: {error}"
                )

                st.error(error_message)

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )


# =========================================================
# 13. FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;padding:10px;color:#64748B;font-size:12px;">
        AI DATA ANALYST · BUILT WITH PYTHON, STREAMLIT, PANDAS,
        PLOTLY AND GROQ AI
    </div>
    """,
    unsafe_allow_html=True
)
