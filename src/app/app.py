import os

import pandas as pd
import streamlit as st

from utils.database import query_table
from utils.ui import apply_theme, page_header, render_header, section_header

LOW_OCCUPANCY_PCT = 80.0
TOP_N = 10

st.set_page_config(
    page_title="Property Intelligence Platform",
    page_icon="🏢",
    layout="wide"
)

apply_theme()
render_header("Portfolio")

page_header(
    "Portfolio Overview",
    "Executive view of occupancy, rental revenue, net operating income and maintenance pressure.",
    eyebrow="Portfolio",
)


def to_numeric(df, columns):
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)
    return df


def percent(numerator, denominator):
    return (numerator / denominator.where(denominator > 0) * 100).fillna(0)


try:
    with st.spinner("Loading executive dashboard..."):
        kpis = query_table(os.getenv("PORTFOLIO_KPIS_TABLE"), limit=12)
        markets = query_table(os.getenv("MARKET_MONTHLY_TABLE"), limit=1000)
        properties = query_table(os.getenv("PROPERTY_PERFORMANCE_TABLE"), limit=1000)
        maintenance = query_table(os.getenv("MAINTENANCE_TABLE"), limit=1000)

    if kpis.empty or markets.empty or properties.empty:
        st.warning("Dashboard data is not available yet.")
        st.stop()

    kpis = to_numeric(kpis, [
        "total_properties",
        "total_occupied_days",
        "total_service_days",
        "total_rental_revenue",
        "total_noi",
    ])
    kpis = kpis.sort_values("month_year").reset_index(drop=True)
    kpis["occupancy_pct"] = percent(kpis["total_occupied_days"], kpis["total_service_days"])

    latest = kpis.iloc[-1]
    prior = kpis.iloc[-2] if len(kpis) > 1 else None

    maintenance = to_numeric(maintenance, ["total_maintenance_cost", "open_work_orders"])

    markets["month"] = pd.to_datetime(markets["month"])
    markets = to_numeric(markets, [
        "property_count",
        "total_occupied_days",
        "total_service_days",
        "total_rental_revenue",
        "total_noi",
    ])
    market_latest = markets[markets["month"] == markets["month"].max()]
    market_table = market_latest.groupby("market_name", as_index=False).agg(
        properties=("property_count", "sum"),
        occupied=("total_occupied_days", "sum"),
        service=("total_service_days", "sum"),
        revenue=("total_rental_revenue", "sum"),
        noi=("total_noi", "sum"),
    )
    market_table["occupancy_pct"] = percent(market_table["occupied"], market_table["service"])
    market_table["noi_margin_pct"] = percent(market_table["noi"], market_table["revenue"])
    market_table = market_table.sort_values("noi", ascending=False).reset_index(drop=True)

    market_service_total = market_table["service"].sum()
    portfolio_occupancy = (
        market_table["occupied"].sum() / market_service_total * 100
        if market_service_total else 0
    )

    properties = to_numeric(properties, [
        "total_occupied_days",
        "total_service_days",
        "total_rental_revenue",
        "total_noi",
    ])
    property_table = properties.groupby("property_id", as_index=False).agg(
        market_name=("market_name", "first"),
        property_type=("property_type", "first"),
        occupied=("total_occupied_days", "sum"),
        service=("total_service_days", "sum"),
        revenue=("total_rental_revenue", "sum"),
        noi=("total_noi", "sum"),
    )
    maintenance_by_property = maintenance.groupby("property_id", as_index=False).agg(
        maintenance_cost=("total_maintenance_cost", "sum"),
        open_work_orders=("open_work_orders", "sum"),
    )
    property_table = property_table.merge(maintenance_by_property, on="property_id", how="left")
    property_table[["maintenance_cost", "open_work_orders"]] = (
        property_table[["maintenance_cost", "open_work_orders"]].fillna(0)
    )
    property_table["occupancy_pct"] = percent(property_table["occupied"], property_table["service"])

    low_occupancy = property_table[
        property_table["occupancy_pct"] < LOW_OCCUPANCY_PCT
    ].sort_values("occupancy_pct")
    negative_noi = property_table[property_table["noi"] < 0]
    attention_markets = market_table[
        market_table["occupancy_pct"] < portfolio_occupancy
    ].sort_values("occupancy_pct")

    st.caption(
        f"Reporting month: {latest['month_year']}  ·  Source: Databricks Gold layer  ·  "
        f"{len(kpis)} months loaded"
    )

    occupancy_delta = (
        f"{latest['occupancy_pct'] - prior['occupancy_pct']:+.2f} pts vs prior month"
        if prior is not None else None
    )
    revenue_delta = (
        f"{(latest['total_rental_revenue'] - prior['total_rental_revenue']) / prior['total_rental_revenue'] * 100:+.1f}% vs prior month"
        if prior is not None and prior["total_rental_revenue"] else None
    )
    noi_delta = (
        f"{(latest['total_noi'] - prior['total_noi']) / abs(prior['total_noi']) * 100:+.1f}% vs prior month"
        if prior is not None and prior["total_noi"] else None
    )

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Total Properties", f"{int(latest['total_properties']):,}")
    k2.metric("Occupancy", f"{latest['occupancy_pct']:.2f}%", occupancy_delta)
    k3.metric("Rental Revenue", f"${latest['total_rental_revenue']:,.0f}", revenue_delta)
    k4.metric("Net Operating Income", f"${latest['total_noi']:,.0f}", noi_delta)
    k5.metric("Maintenance Cost", f"${maintenance['total_maintenance_cost'].sum():,.0f}")
    k6.metric("Open Work Orders", f"{int(maintenance['open_work_orders'].sum()):,}")

    st.divider()

    section_header("Portfolio Performance", "Monthly trends across the portfolio.")

    trend = kpis.assign(month_label=kpis["month_year"].astype(str)).set_index("month_label")

    chart1, chart2 = st.columns(2)

    with chart1:
        st.markdown("**Rental Revenue vs NOI**")
        st.line_chart(trend[["total_rental_revenue", "total_noi"]])

    with chart2:
        st.markdown("**Occupancy Trend (%)**")
        st.line_chart(trend[["occupancy_pct"]])

    section_header("Market Performance", "Latest reporting month by market, ranked by NOI.")

    st.dataframe(
        market_table.rename(columns={
            "market_name": "Market",
            "properties": "Properties",
            "occupancy_pct": "Occupancy %",
            "revenue": "Rental Revenue",
            "noi": "NOI",
            "noi_margin_pct": "NOI Margin %",
        })[["Market", "Properties", "Occupancy %", "Rental Revenue", "NOI", "NOI Margin %"]].style.format({
            "Occupancy %": "{:.2f}%",
            "Rental Revenue": "${:,.0f}",
            "NOI": "${:,.0f}",
            "NOI Margin %": "{:.2f}%",
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    section_header(
        "Decision Queue",
        f"Rules: occupancy below {LOW_OCCUPANCY_PCT:.0f}%, negative NOI, highest maintenance cost, "
        "and markets below the portfolio occupancy average.",
    )

    low_tab, noi_tab, cost_tab, market_tab = st.tabs([
        f"Low occupancy ({len(low_occupancy)})",
        f"Negative NOI ({len(negative_noi)})",
        "High maintenance cost",
        f"Markets to review ({len(attention_markets)})",
    ])

    with low_tab:
        if low_occupancy.empty:
            st.info("No properties are below the occupancy threshold.")
        else:
            st.dataframe(
                low_occupancy.head(TOP_N).rename(columns={
                    "property_id": "Property",
                    "market_name": "Market",
                    "property_type": "Type",
                    "occupancy_pct": "Occupancy %",
                    "noi": "NOI",
                })[["Property", "Market", "Type", "Occupancy %", "NOI"]].style.format({
                    "Occupancy %": "{:.2f}%",
                    "NOI": "${:,.0f}",
                }),
                use_container_width=True,
                hide_index=True,
            )

    with noi_tab:
        if negative_noi.empty:
            st.info("No properties have negative NOI.")
        else:
            st.dataframe(
                negative_noi.nsmallest(TOP_N, "noi").rename(columns={
                    "property_id": "Property",
                    "market_name": "Market",
                    "revenue": "Rental Revenue",
                    "noi": "NOI",
                })[["Property", "Market", "Rental Revenue", "NOI"]].style.format({
                    "Rental Revenue": "${:,.0f}",
                    "NOI": "${:,.0f}",
                }),
                use_container_width=True,
                hide_index=True,
            )

    with cost_tab:
        st.dataframe(
            property_table.nlargest(TOP_N, "maintenance_cost").rename(columns={
                "property_id": "Property",
                "market_name": "Market",
                "maintenance_cost": "Maintenance Cost",
                "open_work_orders": "Open Work Orders",
                "noi": "NOI",
            })[["Property", "Market", "Maintenance Cost", "Open Work Orders", "NOI"]].style.format({
                "Maintenance Cost": "${:,.0f}",
                "NOI": "${:,.0f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

    with market_tab:
        if attention_markets.empty:
            st.info("No markets are below the portfolio occupancy average.")
        else:
            st.dataframe(
                attention_markets.rename(columns={
                    "market_name": "Market",
                    "occupancy_pct": "Occupancy %",
                    "noi": "NOI",
                    "noi_margin_pct": "NOI Margin %",
                })[["Market", "Occupancy %", "NOI", "NOI Margin %"]].style.format({
                    "Occupancy %": "{:.2f}%",
                    "NOI": "${:,.0f}",
                    "NOI Margin %": "{:.2f}%",
                }),
                use_container_width=True,
                hide_index=True,
            )

    st.divider()

    section_header(
        "Calculated Insights",
        "Derived directly from the Gold tables. No AI is used in this section.",
    )

    insights = []

    if prior is not None:
        occupancy_move = latest["occupancy_pct"] - prior["occupancy_pct"]
        direction = "up" if occupancy_move >= 0 else "down"
        insights.append(
            f"Occupancy is {direction} {abs(occupancy_move):.2f} points from the prior month "
            f"({latest['occupancy_pct']:.2f}% vs {prior['occupancy_pct']:.2f}%)."
        )

    insights.append(
        f"{len(low_occupancy)} of {len(property_table)} properties are below "
        f"{LOW_OCCUPANCY_PCT:.0f}% occupancy."
    )
    insights.append(f"{len(negative_noi)} properties report negative NOI across the loaded records.")

    if not attention_markets.empty:
        insights.append(
            f"{len(attention_markets)} markets sit below the portfolio occupancy average of "
            f"{portfolio_occupancy:.2f}%; {attention_markets.iloc[0]['market_name']} is lowest."
        )

    top_cost = property_table.nlargest(1, "maintenance_cost")
    if not top_cost.empty and top_cost.iloc[0]["maintenance_cost"] > 0:
        insights.append(
            f"Property {top_cost.iloc[0]['property_id']} has the highest maintenance cost "
            f"at ${top_cost.iloc[0]['maintenance_cost']:,.0f}."
        )

    st.markdown("\n".join(f"- {text}" for text in insights))

    section_header(
        "Suggested Actions",
        "Rule-based recommendations generated from the calculated insights, not AI output.",
    )

    actions = []

    if not low_occupancy.empty:
        actions.append("Review leasing and pricing for the properties in the low-occupancy queue.")
    if not negative_noi.empty:
        actions.append("Review rents and operating expenses for properties with negative NOI.")
    if not top_cost.empty and top_cost.iloc[0]["maintenance_cost"] > 0:
        actions.append("Check open work orders at the highest-cost properties.")
    if not attention_markets.empty:
        actions.append("Prepare occupancy recovery plans for the markets flagged for review.")
    if not actions:
        actions.append("No threshold breaches in the loaded data. Continue monitoring.")

    st.markdown("\n".join(f"- {text}" for text in actions))

    with st.expander("View monthly portfolio data"):
        st.dataframe(
            kpis.sort_values("month_year", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

except Exception as e:
    st.error("Unable to load portfolio data.")
    st.exception(e)
