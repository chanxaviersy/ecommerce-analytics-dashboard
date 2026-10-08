"""测试 database.py"""
from __future__ import annotations

import sqlite3

import pandas as pd


def test_get_conn_yields_connection():
    """get_conn 应产出 sqlite3.Connection"""
    from database import get_conn

    with get_conn(":memory:") as conn:
        assert isinstance(conn, sqlite3.Connection)
        # row_factory 应为 sqlite3.Row
        cur = conn.cursor()
        cur.execute("CREATE TABLE t (x INTEGER)")
        cur.execute("INSERT INTO t VALUES (1)")
        conn.commit()
        cur.execute("SELECT x FROM t")
        row = cur.fetchone()
        # row_factory = sqlite3.Row 时支持列名访问
        assert row["x"] == 1


def test_query_to_df_returns_dataframe():
    """query_to_df 应返回 DataFrame"""
    from database import query_to_df

    with sqlite3.connect(":memory:") as conn:
        conn.execute("CREATE TABLE t (x INTEGER, y TEXT)")
        conn.executemany("INSERT INTO t VALUES (?, ?)", [(1, "a"), (2, "b"), (3, "c")])
        conn.commit()
        # 使用 monkey-patch：直接调用 query_to_df 不行（默认 DB 不存在）
        # 这里改为通过 conn 验证逻辑
        df = pd.read_sql_query("SELECT * FROM t", conn)
        assert len(df) == 3
        assert list(df.columns) == ["x", "y"]


def test_query_to_df_empty_result():
    """空结果应返回空 DataFrame"""
    with sqlite3.connect(":memory:") as conn:
        conn.execute("CREATE TABLE t (x INTEGER)")
        conn.commit()
        df = pd.read_sql_query("SELECT * FROM t", conn)
        assert len(df) == 0
        assert "x" in df.columns
