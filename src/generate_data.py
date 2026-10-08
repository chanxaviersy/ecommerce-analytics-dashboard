"""生成模拟电商数据。"""
from __future__ import annotations

import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


CATEGORIES = {
    "服装": {"price_range": (20, 200), "n_products": 80},
    "3C数码": {"price_range": (200, 5000), "n_products": 60},
    "美妆": {"price_range": (30, 500), "n_products": 70},
    "食品": {"price_range": (10, 100), "n_products": 90},
    "家居": {"price_range": (50, 1500), "n_products": 50},
}

REGIONS = ["华东", "华北", "华南", "西南", "西北", "东北"]
COUNTRIES_BY_REGION = {
    "华东": ["上海", "江苏", "浙江"],
    "华北": ["北京", "天津", "河北"],
    "华南": ["广东", "福建", "广西"],
    "西南": ["四川", "云南", "贵州"],
    "西北": ["陕西", "甘肃", "新疆"],
    "东北": ["辽宁", "吉林", "黑龙江"],
}


def generate_products(n_per_category: int | None = None) -> pd.DataFrame:
    products = []
    pid = 1
    for cat, cfg in CATEGORIES.items():
        n = n_per_category or cfg["n_products"]
        for _ in range(n):
            price = round(random.uniform(*cfg["price_range"]), 2)
            cost = round(price * random.uniform(0.4, 0.7), 2)
            products.append(
                {
                    "product_id": pid,
                    "category": cat,
                    "name": f"{cat}_Product_{pid}",
                    "price": price,
                    "cost": cost,
                }
            )
            pid += 1
    return pd.DataFrame(products)


def generate_users(n: int = 5000) -> pd.DataFrame:
    users = []
    base_date = datetime(2024, 1, 1)
    for uid in range(1, n + 1):
        register_at = base_date + timedelta(days=random.randint(0, 365))
        region = random.choice(REGIONS)
        country = random.choice(COUNTRIES_BY_REGION[region])
        # 客群分布：new 30%, regular 50%, vip 10%, churn 10%
        segment = random.choices(
            ["new", "regular", "vip", "churn"], weights=[30, 50, 10, 10]
        )[0]
        users.append(
            {
                "user_id": uid,
                "register_at": register_at.strftime("%Y-%m-%d"),
                "region": region,
                "country": country,
                "segment": segment,
            }
        )
    return pd.DataFrame(users)


def generate_orders(
    users_df: pd.DataFrame, products_df: pd.DataFrame, n_orders: int = 20000
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """生成订单表与订单明细表。"""
    orders = []
    order_items = []
    item_id = 1

    # 用户购买频次近似幂律分布（少数用户贡献大量订单）
    user_purchase_power = np.random.pareto(a=1.5, size=len(users_df)) + 1
    user_purchase_prob = user_purchase_power / user_purchase_power.sum()

    base_date = datetime(2024, 1, 1)
    for oid in range(1, n_orders + 1):
        user_id = int(np.random.choice(users_df["user_id"].values, p=user_purchase_prob))
        days_offset = random.randint(0, 365)
        order_date = base_date + timedelta(days=days_offset)
        # 状态分布：90% completed, 5% shipped/paid, 5% cancelled
        status = random.choices(
            ["completed", "paid", "shipped", "cancelled"],
            weights=[85, 5, 5, 5],
        )[0]

        # 1-5 个商品
        n_items = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 15, 7, 3])[0]
        product_ids = np.random.choice(
            products_df["product_id"].values, size=n_items, replace=False
        )
        total = 0.0
        for pid in product_ids:
            prod = products_df[products_df["product_id"] == pid].iloc[0]
            qty = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
            unit_price = prod["price"]
            total += qty * unit_price
            order_items.append(
                {
                    "item_id": item_id,
                    "order_id": oid,
                    "product_id": int(pid),
                    "quantity": qty,
                    "unit_price": unit_price,
                }
            )
            item_id += 1

        orders.append(
            {
                "order_id": oid,
                "user_id": user_id,
                "created_at": order_date.strftime("%Y-%m-%d %H:%M:%S"),
                "status": status,
                "total_amount": round(total, 2),
            }
        )

    return pd.DataFrame(orders), pd.DataFrame(order_items)


def generate_events(users_df: pd.DataFrame, orders_df: pd.DataFrame, n_events: int = 100000) -> pd.DataFrame:
    """生成行为日志（用于漏斗分析）。"""
    events = []
    eid = 1
    # 行为分布：view (60%), add_to_cart (20%), checkout (15%), pay (5%)
    event_weights = [60, 20, 15, 5]
    event_types = ["view", "add_to_cart", "checkout", "pay"]

    for _ in range(n_events):
        uid = int(np.random.choice(users_df["user_id"].values))
        et = random.choices(event_types, weights=event_weights)[0]
        days_offset = random.randint(0, 365)
        occurred = datetime(2024, 1, 1) + timedelta(days=days_offset, seconds=random.randint(0, 86400))
        events.append(
            {
                "event_id": eid,
                "user_id": uid,
                "session_id": f"s_{random.randint(1, 50000)}",
                "event_type": et,
                "product_id": None,
                "occurred_at": occurred.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        eid += 1
    return pd.DataFrame(events)


def save_to_sqlite(
    db_path: str | Path,
    users_df: pd.DataFrame,
    products_df: pd.DataFrame,
    orders_df: pd.DataFrame,
    order_items_df: pd.DataFrame,
    events_df: pd.DataFrame,
) -> None:
    """把生成的数据写入 SQLite。"""
    schema_path = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_sql)
        users_df.to_sql("users", conn, if_exists="replace", index=False)
        products_df.to_sql("products", conn, if_exists="replace", index=False)
        orders_df.to_sql("orders", conn, if_exists="replace", index=False)
        order_items_df.to_sql("order_items", conn, if_exists="replace", index=False)
        events_df.to_sql("events", conn, if_exists="replace", index=False)
        conn.commit()
    print(f"[INFO] 数据已写入 SQLite: {db_path}")


def main() -> None:
    db_path = Path(__file__).resolve().parent.parent / "data" / "ecommerce.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    print("[INFO] 生成模拟数据...")
    users_df = generate_users(n=5000)
    products_df = generate_products()
    orders_df, order_items_df = generate_orders(users_df, products_df, n_orders=20000)
    events_df = generate_events(users_df, orders_df, n_events=100000)

    save_to_sqlite(db_path, users_df, products_df, orders_df, order_items_df, events_df)
    print(f"[INFO] users: {len(users_df)}, products: {len(products_df)}, "
          f"orders: {len(orders_df)}, order_items: {len(order_items_df)}, events: {len(events_df)}")


if __name__ == "__main__":
    main()