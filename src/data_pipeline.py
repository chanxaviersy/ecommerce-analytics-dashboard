"""ETL 流水线（提取 → 校验 → 加载）。"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from database import DEFAULT_DB, get_conn
from generate_data import main as generate_data_main


def run_etl(force: bool = False) -> None:
    """运行 ETL：
    1. 提取：从 SQLite 提取数据
    2. 校验：数据完整性检查
    3. 加载：返回清洗后的 DataFrame
    """
    db_path = DEFAULT_DB
    if force or not db_path.exists():
        print("[ETL] 生成数据...")
        generate_data_main()

    print("[ETL] 提取数据...")
    with get_conn(db_path) as conn:
        orders = pd.read_sql_query("SELECT * FROM orders", conn)
        users = pd.read_sql_query("SELECT * FROM users", conn)
        products = pd.read_sql_query("SELECT * FROM products", conn)
        order_items = pd.read_sql_query("SELECT * FROM order_items", conn)
        events = pd.read_sql_query("SELECT * FROM events", conn)

    print("[ETL] 数据校验...")
    assert orders["order_id"].is_unique, "order_id 不唯一"
    assert users["user_id"].is_unique, "user_id 不唯一"
    assert products["product_id"].is_unique, "product_id 不唯一"
    # 检查订单完整性
    assert order_items["order_id"].isin(orders["order_id"]).all(), "存在孤儿订单明细"
    print("[ETL] 校验通过 ✅")

    # 加载：时间格式转换
    orders["created_at"] = pd.to_datetime(orders["created_at"])
    events["occurred_at"] = pd.to_datetime(events["occurred_at"])

    print(f"[ETL] 完成：orders={len(orders)}, users={len(users)}, "
          f"products={len(products)}, order_items={len(order_items)}, events={len(events)}")

    return {
        "orders": orders,
        "users": users,
        "products": products,
        "order_items": order_items,
        "events": events,
    }


if __name__ == "__main__":
    run_etl(force=True)