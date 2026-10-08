"""业务指标计算模块（CLV、漏斗等）。"""
from __future__ import annotations

import numpy as np
import pandas as pd

from database import query_to_df
from queries import (
    SQL_CLV_TOP,
    SQL_FUNNEL,
    SQL_GMV_BY_CATEGORY_MONTH,
    SQL_REPEAT_PURCHASE_RATE,
    SQL_RFM,
)


def compute_core_kpis() -> dict[str, float]:
    """计算核心 KPI：GMV、AOV、订单数、用户数。"""
    df = query_to_df("""
        SELECT
            SUM(total_amount) AS gmv,
            COUNT(DISTINCT order_id) AS order_count,
            AVG(total_amount) AS aov,
            COUNT(DISTINCT user_id) AS active_users
        FROM orders WHERE status = 'completed';
    """)
    if df.empty:
        return {"gmv": 0.0, "order_count": 0, "aov": 0.0, "active_users": 0}
    row = df.iloc[0]
    return {
        "gmv": float(row["gmv"]),
        "order_count": int(row["order_count"]),
        "aov": float(row["aov"]),
        "active_users": int(row["active_users"]),
    }


def get_gmv_by_category_month() -> pd.DataFrame:
    return query_to_df(SQL_GMV_BY_CATEGORY_MONTH)


def get_funnel() -> pd.DataFrame:
    """返回漏斗各阶段的用户数 + 转化率。"""
    df = query_to_df(SQL_FUNNEL)
    if df.empty:
        return df
    base = df["user_count"].iloc[0]
    df["conversion_rate"] = df["user_count"] / base
    return df


def get_rfm() -> pd.DataFrame:
    """获取 RFM 数据，并基于分位数打 R/F/M 分数（1-5）。"""
    df = query_to_df(SQL_RFM)
    if df.empty:
        return df

    # R 分：越小越好 → 反向
    df["R_score"] = pd.qcut(df["recency_days"], q=5, labels=[5, 4, 3, 2, 1], duplicates="drop")
    df["F_score"] = pd.qcut(df["frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop")
    df["M_score"] = pd.qcut(df["monetary"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop")
    df["RFM_score"] = (
        df["R_score"].astype(str) + df["F_score"].astype(str) + df["M_score"].astype(str)
    )

    # 客户分层
    def segment(row: pd.Series) -> str:
        r, f, m = int(row["R_score"]), int(row["F_score"]), int(row["M_score"])
        if r >= 4 and f >= 4 and m >= 4:
            return "冠军客户"
        if r >= 4 and f >= 3:
            return "忠诚客户"
        if r >= 4:
            return "新客户"
        if m >= 4:
            return "高价值流失"
        return "一般客户"

    df["segment"] = df.apply(segment, axis=1)
    return df


def get_clv_top(n: int = 100) -> pd.DataFrame:
    return query_to_df(SQL_CLV_TOP)


def get_repeat_purchase_rate() -> float:
    df = query_to_df(SQL_REPEAT_PURCHASE_RATE)
    if df.empty:
        return 0.0
    return float(df.iloc[0, 0])


def predict_clv_simple(history: pd.DataFrame, predicted_months: int = 12) -> float:
    """简单 CLV 预测：
    CLV = (平均每月订单数 × 平均客单价 × 预计生命周期月数) × 毛利率
    """
    if history.empty:
        return 0.0
    n_months = max(1, (history["created_at"].max() - history["created_at"].min()).days / 30)
    monthly_orders = len(history) / n_months
    avg_order_value = history["total_amount"].mean()
    gross_margin = 0.3  # 假设毛利率 30%
    return monthly_orders * avg_order_value * predicted_months * gross_margin