
import pandas as pd
import plotly.express as px


def create_chart(
    df,
    chart_type,
    x_column,
    y_column=None,
    color_column=None,
    aggregation="Average"
):
    if x_column not in df.columns:
        raise ValueError("Invalid X-axis column.")

    if y_column and y_column not in df.columns:
        raise ValueError("Invalid Y-axis column.")

    if color_column and color_column not in df.columns:
        raise ValueError("Invalid color column.")

    required_columns = [x_column]

    if y_column:
        required_columns.append(y_column)

    chart_df = df.dropna(subset=required_columns).copy()

    if chart_df.empty:
        raise ValueError("No valid data available for this chart.")

    # Bar Chart
    if chart_type == "Bar Chart":

        if y_column is None:
            raise ValueError("Bar Chart requires a Y-axis column.")

        aggregation_functions = {
            "Average": "mean",
            "Sum": "sum",
            "Count": "count",
            "Maximum": "max",
            "Minimum": "min"
        }

        if aggregation not in aggregation_functions:
            raise ValueError("Invalid aggregation method.")

        function = aggregation_functions[aggregation]

        grouped_df = (
            chart_df.groupby(x_column, as_index=False)[y_column]
            .agg(function)
        )

        fig = px.bar(
            grouped_df,
            x=x_column,
            y=y_column,
            title=f"{aggregation} {y_column} by {x_column}",
            template="plotly_white"
        )

    # Line Chart
    elif chart_type == "Line Chart":

        if y_column is None:
            raise ValueError("Line Chart requires a Y-axis column.")

        fig = px.line(
            chart_df,
            x=x_column,
            y=y_column,
            color=color_column,
            markers=True,
            title=f"{y_column} over {x_column}",
            template="plotly_white"
        )

    # Scatter Plot
    elif chart_type == "Scatter Plot":

        if y_column is None:
            raise ValueError("Scatter Plot requires a Y-axis column.")

        fig = px.scatter(
            chart_df,
            x=x_column,
            y=y_column,
            color=color_column,
            title=f"{y_column} vs {x_column}",
            template="plotly_white"
        )

    # Histogram
    elif chart_type == "Histogram":

        fig = px.histogram(
            chart_df,
            x=x_column,
            color=color_column,
            title=f"Distribution of {x_column}",
            template="plotly_white"
        )

    # Pie Chart
    elif chart_type == "Pie Chart":

        if y_column is None:
            raise ValueError("Pie Chart requires a numerical Y-axis column.")

        pie_df = (
            chart_df.groupby(x_column, as_index=False)[y_column]
            .sum()
        )

        fig = px.pie(
            pie_df,
            names=x_column,
            values=y_column,
            title=f"{y_column} distribution by {x_column}",
            template="plotly_white"
        )

    else:
        raise ValueError("Unsupported chart type.")

    fig.update_layout(
        title_x=0.5,
        height=500
    )

    return fig
