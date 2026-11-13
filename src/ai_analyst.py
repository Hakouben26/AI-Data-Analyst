
import os
import json
import pandas as pd

from dotenv import load_dotenv
from groq import Groq


# =========================================================
# 1. CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH, override=True)

MODEL = os.getenv(
    "GROQ_MODEL",
    "qwen/qwen3.8-27b"
)

MAX_OUTPUT_TOKENS = 900


# =========================================================
# 2. GROQ CLIENT
# =========================================================

def get_groq_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found in .env file."
        )

    return Groq(
        api_key=api_key,
        timeout=120.0,
        max_retries=2
    )


# =========================================================
# 3. FINANCIAL DATA PREPARATION
# =========================================================

def prepare_financial_data(df):

    data = df.copy()

    required = ["Quantity", "Unit_Price"]

    for column in required:

        if column not in data.columns:
            raise ValueError(
                f"Missing column: {column}"
            )

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    if "Discount" in data.columns:

        data["Discount"] = pd.to_numeric(
            data["Discount"],
            errors="coerce"
        )

        valid_discounts = data["Discount"].dropna()

        if (
            not valid_discounts.empty
            and valid_discounts.abs().max() > 1
        ):
            data["Discount"] = (
                data["Discount"] / 100
            )

    else:
        data["Discount"] = 0.0

    valid = (
        data["Quantity"].notna()
        & data["Unit_Price"].notna()
        & data["Discount"].notna()
        & data["Quantity"].ge(0)
        & data["Unit_Price"].ge(0)
        & data["Discount"].between(0, 1)
    )

    data = data.loc[valid].copy()

    data["Revenue"] = (
        data["Quantity"]
        * data["Unit_Price"]
        * (1 - data["Discount"])
    )

    return data


# =========================================================
# 4. GROUPED REVENUE HELPER
# =========================================================

def grouped_revenue(data, column):

    if column not in data.columns:
        return {}

    result = (
        data.groupby(column)["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
    )

    return {
        str(key): float(value)
        for key, value in result.items()
    }


# =========================================================
# 5. BUSINESS METRICS
# =========================================================

def calculate_business_metrics(df):

    metrics = {
        "revenue_available": False,
        "total_revenue": 0,
        "valid_revenue_records": 0,
        "excluded_revenue_records": len(df),
        "average_revenue_per_valid_record": 0,
        "total_units_sold": 0,
        "revenue_by_product": {},
        "revenue_by_category": {},
        "revenue_by_city": {},
        "revenue_by_customer": {}
    }

    try:

        data = prepare_financial_data(df)

        if data.empty:
            return metrics

        total_revenue = float(data["Revenue"].sum())

        metrics.update({
            "revenue_available": True,
            "total_revenue": round(total_revenue, 2),
            "valid_revenue_records": len(data),
            "excluded_revenue_records": len(df) - len(data),
            "average_revenue_per_valid_record": round(
                float(data["Revenue"].mean()), 2
            ),
            "total_units_sold": round(
                float(data["Quantity"].sum()), 2
            ),
            "revenue_by_product": grouped_revenue(
                data, "Product"
            ),
            "revenue_by_category": grouped_revenue(
                data, "Category"
            ),
            "revenue_by_city": grouped_revenue(
                data, "City"
            ),
            "revenue_by_customer": grouped_revenue(
                data, "Customer"
            )
        })

        return metrics

    except Exception as e:

        metrics["error"] = str(e)
        return metrics


# =========================================================
# 6. MONTHLY REVENUE ANALYSIS
# =========================================================

def calculate_monthly_revenue(df):

    result = {
        "available": False,
        "monthly_revenue": {},
        "highest_revenue_month": None,
        "lowest_revenue_month": None,
        "monthly_contribution_percent": {},
        "valid_records": 0,
        "excluded_records": len(df)
    }

    if "Order_Date" not in df.columns:

        result["message"] = (
            "Order_Date column is missing."
        )

        return result

    try:

        data = prepare_financial_data(df)

        data["Order_Date"] = pd.to_datetime(
            data["Order_Date"],
            errors="coerce"
        )

        data = data.loc[
            data["Order_Date"].notna()
        ].copy()

        if data.empty:

            result["message"] = (
                "No valid financial records with dates."
            )

            return result

        data["Month"] = (
            data["Order_Date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly = (
            data.groupby("Month")["Revenue"]
            .sum()
            .sort_index()
            .round(2)
        )

        total = float(monthly.sum())

        monthly_values = {
            str(month): float(value)
            for month, value in monthly.items()
        }

        contributions = {}

        if total > 0:

            contributions = {
                str(month): round(
                    float(value / total * 100), 2
                )
                for month, value in monthly.items()
            }

        result.update({
            "available": True,
            "monthly_revenue": monthly_values,
            "highest_revenue_month": str(monthly.idxmax()),
            "lowest_revenue_month": str(monthly.idxmin()),
            "monthly_contribution_percent": contributions,
            "valid_records": len(data),
            "excluded_records": len(df) - len(data),
            "number_of_months": len(monthly)
        })

        return result

    except Exception as e:

        result["error"] = str(e)
        return result


# =========================================================
# 7. ADDITIONAL BUSINESS ANALYSIS
# =========================================================

def calculate_business_risks(df):

    result = {}

    try:

        data = prepare_financial_data(df)

        if data.empty:
            return result

        total = float(data["Revenue"].sum())

        if total <= 0:
            return result

        customers = grouped_revenue(data, "Customer")

        products = grouped_revenue(data, "Product")

        cities = grouped_revenue(data, "City")

        top_three_customers = list(customers.items())[:3]

        top_three_revenue = sum(
            value for _, value in top_three_customers
        )

        customer_concentration = (
            top_three_revenue / total * 100
        )

        result = {
            "top_3_customers": [
                {
                    "customer": name,
                    "revenue": value,
                    "contribution_percent": round(
                        value / total * 100, 2
                    )
                }
                for name, value in top_three_customers
            ],
            "top_3_customer_concentration_percent": round(
                customer_concentration, 2
            ),
            "lowest_revenue_product": (
                min(products, key=products.get)
                if products else None
            ),
            "highest_revenue_city": (
                max(cities, key=cities.get)
                if cities else None
            ),
            "lowest_revenue_city": (
                min(cities, key=cities.get)
                if cities else None
            ),
            "city_revenue_gap": (
                round(max(cities.values()) - min(cities.values()), 2)
                if cities else 0
            )
        }

        return result

    except Exception as e:

        return {"error": str(e)}


# =========================================================
# 8. DATASET CONTEXT
# =========================================================

def build_data_context(df):

    context = {}

    context["dataset_overview"] = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "duplicates": int(df.duplicated().sum()),
        "missing_values": int(df.isnull().sum().sum())
    }

    context["missing_values_by_column"] = {
        str(key): int(value)
        for key, value in df.isnull().sum().items()
    }

    numeric = df.select_dtypes(
        include="number"
    )

    context["numeric_statistics"] = (
        numeric.describe().round(2).to_dict()
        if not numeric.empty else {}
    )

    categorical = df.select_dtypes(
        include=["object", "category"]
    )

    categorical_summary = {}

    for column in categorical.columns:

        mode = df[column].mode()

        categorical_summary[column] = {
            "unique_values": int(
                df[column].nunique()
            ),
            "top_value": (
                str(mode.iloc[0])
                if not mode.empty else None
            )
        }

    context["categorical_summary"] = (
        categorical_summary
    )

    date_summary = {}

    for column in df.columns:

        if "date" in str(column).lower():

            dates = pd.to_datetime(
                df[column],
                errors="coerce"
            ).dropna()

            if not dates.empty:

                date_summary[column] = {
                    "minimum_date": str(dates.min().date()),
                    "maximum_date": str(dates.max().date()),
                    "valid_dates": int(len(dates))
                }

    context["date_summary"] = date_summary

    context["business_metrics"] = (
        calculate_business_metrics(df)
    )

    context["monthly_metrics"] = (
        calculate_monthly_revenue(df)
    )

    context["business_risks"] = (
        calculate_business_risks(df)
    )

    return context


# =========================================================
# 9. COMPACT CONTEXT FOR AI
# =========================================================

def build_compact_context(df):

    context = build_data_context(df)

    # Keep calculated results, not raw rows
    compact = {
        "dataset_overview": context["dataset_overview"],
        "missing_values_by_column": context[
            "missing_values_by_column"
        ],
        "date_summary": context["date_summary"],
        "business_metrics": context["business_metrics"],
        "monthly_metrics": context["monthly_metrics"],
        "business_risks": context["business_risks"]
    }

    # Limit long customer lists to top 10
    metrics = compact["business_metrics"]

    for key in [
        "revenue_by_customer",
        "revenue_by_product",
        "revenue_by_category",
        "revenue_by_city"
    ]:

        values = metrics.get(key, {})

        metrics[key] = dict(
            list(values.items())[:10]
        )

    return compact


# =========================================================
# 10. AI REQUEST
# =========================================================

def call_groq(system_prompt, user_prompt, max_tokens=900):

    client = get_groq_client()

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=0.1,

        max_tokens=min(max_tokens, MAX_OUTPUT_TOKENS)
    )

    return response.choices[0].message.content


# =========================================================
# 11. AI DATA CHAT
# =========================================================

def ask_data_question(df, question):

    if not question or not question.strip():
        return "Please enter a question."

    try:

        context = build_compact_context(df)

        context_json = json.dumps(
            context,
            ensure_ascii=False,
            default=str
        )

        system_prompt = """
You are a professional AI Data Analyst.

Analyze only the calculated dataset context.

RULES:
- Never invent numbers.
- Use actual calculated values only.
- Say when information is unavailable.
- Distinguish revenue from profit.
- Do not claim profit without cost data.
- Use monthly_metrics for monthly analysis.
- Use business_risks for customer and city analysis.
- Mention limitations of small datasets.
- Do not confuse rows with unique orders.
- Keep answers concise and structured.
- Give practical recommendations.
- Respond in the same language as the question.
- Maximum response length: concise report.
"""

        user_prompt = f"""
CALCULATED DATA:

{context_json}

QUESTION:

{question}

Provide a concise and accurate analysis.
"""

        return call_groq(
            system_prompt,
            user_prompt,
            max_tokens=900
        )

    except Exception as e:

        error = str(e)

        if "429" in error or "rate_limit" in error.lower():

            return (
                "Groq rate limit reached. "
                "Please wait before trying again, "
                "or reduce the request size."
            )

        return "AI Analysis Error: " + error


# =========================================================
# 12. AI INSIGHTS REPORT
# =========================================================

def generate_ai_insights(df):

    try:

        context = build_compact_context(df)

        context_json = json.dumps(
            context,
            ensure_ascii=False,
            default=str
        )

        system_prompt = """
You are a senior Business Intelligence Analyst.

Create a concise professional report using
only the calculated dataset context.

REPORT SECTIONS:

1. Executive Summary
2. Dataset Overview
3. Business KPIs
4. Product Performance
5. Category Performance
6. Geographic Performance
7. Monthly Revenue Analysis
8. Customer Analysis
9. Data Quality
10. Business Risks
11. Strategic Recommendations
12. Limitations

RULES:

- Never invent data.
- Use exact calculated values.
- Do not claim profit without cost data.
- Mention excluded records.
- Do not claim monthly growth with only one month.
- Use business_risks for customer concentration.
- Keep the report concise.
- Recommendations must be supported by data.
"""

        user_prompt = f"""
CALCULATED DATASET CONTEXT:

{context_json}

Generate a professional business intelligence report.
"""

        return call_groq(
            system_prompt,
            user_prompt,
            max_tokens=900
        )

    except Exception as e:

        error = str(e)

        if "429" in error or "rate_limit" in error.lower():

            return (
                "Groq rate limit reached. "
                "Please wait and try again."
            )

        return "AI Insights Error: " + error
