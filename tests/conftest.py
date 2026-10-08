"""pytest 共享 fixtures"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest
import sqlite3

# 把 src/ 加入路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def in_memory_db():
    """创建内存 SQLite 数据库，含示例数据"""
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE order_items (
            order_id INTEGER,
            product_id INTEGER,
            category TEXT,
            quantity INTEGER,
            price REAL
        )
    """)
    cur.execute("""
        CREATE TABLE user_events (
            user_id INTEGER,
            event_type TEXT,  -- view / add_to_cart / checkout / purchase
            created_at TEXT
        )
    """)
    # 插入示例数据
    cur.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
        [
            (1, 101, 100.0, "completed", "2024-01-15"),
            (2, 101, 150.0, "completed", "2024-02-20"),
            (3, 102, 200.0, "completed", "2024-01-25"),
            (4, 103, 50.0, "completed", "2024-03-01"),
            (5, 102, 300.0, "completed", "2024-04-10"),
        ],
    )
    cur.executemany(
        "INSERT INTO order_items VALUES (?, ?, ?, ?, ?)",
        [
            (1, 1, "电子产品", 1, 100.0),
            (2, 2, "服装", 2, 75.0),
            (3, 3, "家居", 1, 200.0),
            (4, 4, "服装", 1, 50.0),
            (5, 5, "电子产品", 1, 300.0),
        ],
    )
    cur.executemany(
        "INSERT INTO user_events VALUES (?, ?, ?)",
        [
            (101, "view", "2024-01-10"),
            (101, "add_to_cart", "2024-01-12"),
            (101, "checkout", "2024-01-14"),
            (101, "purchase", "2024-01-15"),
            (102, "view", "2024-01-20"),
            (102, "purchase", "2024-01-25"),
            (103, "view", "2024-02-25"),
            (103, "add_to_cart", "2024-02-28"),
            (103, "checkout", "2024-02-29"),
            (103, "purchase", "2024-03-01"),
        ],
    )
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def sample_order_history():
    """示例订单历史 DataFrame"""
    return pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5, 6],
            "user_id": [101, 101, 101, 102, 102, 103],
            "total_amount": [100.0, 150.0, 200.0, 50.0, 300.0, 75.0],
            "created_at": pd.to_datetime(
                [
                    "2024-01-15",
                    "2024-02-20",
                    "2024-03-15",
                    "2024-01-25",
                    "2024-04-10",
                    "2024-05-05",
                ]
            ),
        }
    )


@pytest.fixture
def patch_database(monkeypatch, in_memory_db):
    """把 database.query_to_df 替换为使用 in-memory 数据库"""

    def mock_query_to_df(sql: str, params: tuple = ()) -> pd.DataFrame:
        return pd.read_sql_query(sql, in_memory_db, params=params)

    import database

    monkeypatch.setattr(database, "query_to_df", mock_query_to_df)
    yield
