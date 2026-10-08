"""数据库连接与查询工具。"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import pandas as pd


DEFAULT_DB = Path(__file__).resolve().parent.parent / "data" / "ecommerce.db"


@contextmanager
def get_conn(db_path: str | Path = DEFAULT_DB):
    """获取数据库连接（自动关闭）。"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def query_to_df(sql: str, params: tuple[Any, ...] | None = None, db_path: str | Path = DEFAULT_DB) -> pd.DataFrame:
    """执行 SQL 查询并返回 DataFrame。"""
    with get_conn(db_path) as conn:
        if params:
            return pd.read_sql_query(sql, conn, params=params)
        return pd.read_sql_query(sql, conn)