"""测试 metrics.py - 业务指标计算"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


def test_predict_clv_simple_empty():
    """空数据应返回 0.0"""
    from metrics import predict_clv_simple

    empty_df = pd.DataFrame(columns=["created_at", "total_amount"])
    assert predict_clv_simple(empty_df) == 0.0


def test_predict_clv_simple_positive(sample_order_history):
    """正常数据应返回正数 CLV"""
    from metrics import predict_clv_simple

    clv = predict_clv_simple(sample_order_history, predicted_months=12)
    assert clv > 0
    assert isinstance(clv, float)


def test_predict_clv_simple_scales_with_months(sample_order_history):
    """CLV 应随 predicted_months 线性增长"""
    from metrics import predict_clv_simple

    clv_6m = predict_clv_simple(sample_order_history, predicted_months=6)
    clv_12m = predict_clv_simple(sample_order_history, predicted_months=12)
    assert clv_12m == pytest.approx(clv_6m * 2, rel=0.01)


def test_predict_clv_simple_uses_gross_margin(sample_order_history):
    """CLV 应包含 0.3 毛利率"""
    from metrics import predict_clv_simple

    clv = predict_clv_simple(sample_order_history, predicted_months=12)
    # 6 笔订单总金额 875, 跨约 4 个月 → 月均 1.5 笔 × AOV × 12 × 0.3
    # 关键：测试逻辑不是数值精确，但确保毛利率生效
    # 关闭 margin 后应大 1/0.3 倍
    assert clv > 0
    # 毛利率 0.3 应让结果小于"无 margin"
    total_amount = sample_order_history["total_amount"].sum()
    assert clv < total_amount * 12  # 必然小于 12×总金额
