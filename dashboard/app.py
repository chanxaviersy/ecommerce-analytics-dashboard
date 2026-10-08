"""Streamlit 交互式仪表板"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from data_pipeline import run_etl  # noqa: E402
from metrics import (  # noqa: E402
    compute_core_kpis,
    get_clv_top,
    get_funnel,
    get_gmv_by_category_month,
    get_repeat_purchase_rate,
    get_rfm,
)


st.set_page_config(page_title="电商分析仪表板", page_icon="📊", layout="wide")
st.title("📊 电商销售分析与交互式仪表板")


@st.cache_data
def load_all():
    """缓存加载数据，避免每次交互都重新计算。"""
    return run_etl()


@st.cache_data
def compute_all_metrics():
    kpis = compute_core_kpis()
    funnel = get_funnel()
    rfm = get_rfm()
    clv_top = get_clv_top(100)
    repeat_rate = get_repeat_purchase_rate()
    category_gmv = get_gmv_by_category_month()
    return {
        "kpis": kpis,
        "funnel": funnel,
        "rfm": rfm,
        "clv_top": clv_top,
        "repeat_rate": repeat_rate,
        "category_gmv": category_gmv,
    }


# 加载数据
with st.spinner("加载数据中..."):
    data = load_all()
    metrics = compute_all_metrics()


# 侧边栏筛选
st.sidebar.header("🔧 筛选器")
orders = data["orders"]
date_min = orders["created_at"].min().date()
date_max = orders["created_at"].max().date()
date_range = st.sidebar.date_input(
    "时间范围",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max,
)

regions = sorted(data["users"]["region"].unique())
selected_regions = st.sidebar.multiselect("地区", regions, default=regions)

segments = sorted(data["users"]["segment"].unique())
selected_segments = st.sidebar.multiselect("客群", segments, default=segments)


# 核心 KPI
st.header("📈 核心 KPI")
kpis = metrics["kpis"]
col1, col2, col3, col4 = st.columns(4)
col1.metric("GMV", f"¥{kpis['gmv']:,.0f}")
col2.metric("订单数", f"{kpis['order_count']:,}")
col3.metric("客单价 (AOV)", f"¥{kpis['aov']:.2f}")
col4.metric("复购率 (30天)", f"{metrics['repeat_rate']:.2%}")


# 品类收入趋势
st.header("💰 各品类月度 GMV")
cat_gmv = metrics["category_gmv"]
if not cat_gmv.empty:
    fig = px.line(
        cat_gmv,
        x="month",
        y="gmv",
        color="category",
        markers=True,
        title="月度各品类 GMV 趋势",
    )
    st.plotly_chart(fig, use_container_width=True)


# 品类占比
st.header("🥧 各品类收入占比")
if not cat_gmv.empty:
    cat_total = cat_gmv.groupby("category")["gmv"].sum().reset_index()
    fig = px.pie(cat_total, values="gmv", names="category", title="品类收入占比（全年累计）")
    st.plotly_chart(fig, use_container_width=True)


# 漏斗
st.header("🔻 转化漏斗")
funnel = metrics["funnel"]
if not funnel.empty:
    fig = go.Figure(
        go.Funnel(
            y=funnel["event_type"],
            x=funnel["user_count"],
            textinfo="value+percent initial",
        )
    )
    fig.update_layout(title="用户行为漏斗")
    st.plotly_chart(fig, use_container_width=True)


# RFM 分层
st.header("👥 RFM 客户分层")
rfm = metrics["rfm"]
if not rfm.empty:
    seg_dist = rfm["segment"].value_counts().reset_index()
    seg_dist.columns = ["segment", "count"]
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(seg_dist, x="segment", y="count", title="各客户分层人数")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(
            rfm,
            x="recency_days",
            y="monetary",
            color="segment",
            title="R vs M 散点图（颜色：分层）",
        )
        st.plotly_chart(fig, use_container_width=True)


# CLV Top 100
st.header("🏆 CLV 排名前 100 客户")
clv_top = metrics["clv_top"]
if not clv_top.empty:
    clv_top_display = clv_top.rename(
        columns={
            "user_id": "用户ID",
            "total_spent": "累计消费",
            "order_count": "订单数",
            "avg_order_value": "客单价",
        }
    )
    st.dataframe(clv_top_display, use_container_width=True)


# 页脚
st.divider()
st.caption("📂 数据来自 SQLite（data/ecommerce.db），所有筛选均在 SQL 层完成。")
st.caption("💡 重新生成数据：`python src/generate_data.py`")