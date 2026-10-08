"""测试 generate_data.py - 数据生成函数"""
from __future__ import annotations

import pandas as pd


def test_generate_products_columns():
    """生成的 products 应包含必要列"""
    from generate_data import generate_products

    df = generate_products(n_per_category=2)
    assert "product_id" in df.columns
    assert "category" in df.columns
    assert "name" in df.columns
    assert "price" in df.columns
    assert "cost" in df.columns


def test_generate_products_unique_ids():
    """product_id 应唯一"""
    from generate_data import generate_products

    df = generate_products(n_per_category=5)
    assert df["product_id"].is_unique
    # 默认数量 = sum(CATEGORIES n_products)
    assert len(df) >= 5


def test_generate_products_price_in_range():
    """价格应在品类范围内"""
    from generate_data import CATEGORIES, generate_products

    df = generate_products(n_per_category=10)
    for cat, cfg in CATEGORIES.items():
        cat_df = df[df["category"] == cat]
        if not cat_df.empty:
            assert (cat_df["price"] >= cfg["price_range"][0]).all()
            assert (cat_df["price"] <= cfg["price_range"][1]).all()


def test_generate_products_cost_less_than_price():
    """成本应低于价格（毛利率 > 0）"""
    from generate_data import generate_products

    df = generate_products(n_per_category=20)
    assert (df["cost"] < df["price"]).all()


def test_generate_users_count():
    """生成用户数应等于指定数"""
    from generate_data import generate_users

    df = generate_users(n=100)
    assert len(df) == 100
    assert df["user_id"].is_unique


def test_generate_users_columns():
    """用户表应包含必要列"""
    from generate_data import generate_users

    df = generate_users(n=50)
    assert "user_id" in df.columns
    assert "register_at" in df.columns
    assert "region" in df.columns
    assert "country" in df.columns
    assert "segment" in df.columns


def test_generate_users_segments_valid():
    """用户分群应在合法集合中"""
    from generate_data import generate_users

    df = generate_users(n=500)
    valid_segments = {"new", "regular", "vip", "churn"}
    assert set(df["segment"].unique()).issubset(valid_segments)


def test_generate_orders_count_and_shape():
    """生成的订单数和明细数应正确"""
    from generate_data import generate_orders, generate_products, generate_users

    users_df = generate_users(n=50)
    products_df = generate_products(n_per_category=5)
    orders_df, order_items_df = generate_orders(users_df, products_df, n_orders=30)

    assert len(orders_df) == 30
    assert "order_id" in orders_df.columns
    assert "user_id" in orders_df.columns
    assert "total_amount" in orders_df.columns
    assert "status" in orders_df.columns
    assert "item_id" in order_items_df.columns


def test_generate_orders_total_matches_items():
    """订单总金额应等于明细合计"""
    from generate_data import generate_orders, generate_products, generate_users

    users_df = generate_users(n=20)
    products_df = generate_products(n_per_category=5)
    orders_df, order_items_df = generate_orders(users_df, products_df, n_orders=10)

    # 按订单聚合明细金额
    items_total = order_items_df.groupby("order_id").apply(
        lambda g: (g["quantity"] * g["unit_price"]).sum()
    )
    # 检查每个订单的 total_amount 与明细一致（允许浮点误差）
    for _, row in orders_df.iterrows():
        expected = items_total.get(row["order_id"], 0)
        assert abs(row["total_amount"] - expected) < 0.01


def test_generate_orders_status_valid():
    """订单状态应在合法集合中"""
    from generate_data import generate_orders, generate_products, generate_users

    users_df = generate_users(n=20)
    products_df = generate_products(n_per_category=3)
    orders_df, _ = generate_orders(users_df, products_df, n_orders=20)
    valid_statuses = {"completed", "paid", "shipped", "cancelled"}
    assert set(orders_df["status"].unique()).issubset(valid_statuses)


def test_generate_events_count_and_types():
    """生成事件数与类型应正确"""
    from generate_data import generate_events, generate_products, generate_users, generate_orders

    users_df = generate_users(n=20)
    products_df = generate_products(n_per_category=3)
    orders_df, _ = generate_orders(users_df, products_df, n_orders=10)
    events_df = generate_events(users_df, orders_df, n_events=200)

    assert len(events_df) == 200
    valid_types = {"view", "add_to_cart", "checkout", "pay"}
    assert set(events_df["event_type"].unique()).issubset(valid_types)
