-- 电商数据仓库 Schema（SQLite 语法，生产可换 PostgreSQL）

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    user_id       INTEGER PRIMARY KEY,
    register_at   TEXT NOT NULL,
    region        TEXT NOT NULL,
    country       TEXT NOT NULL,
    segment       TEXT NOT NULL  -- 'new' / 'regular' / 'vip' / 'churn'
);

-- 商品表
CREATE TABLE IF NOT EXISTS products (
    product_id    INTEGER PRIMARY KEY,
    category      TEXT NOT NULL,
    name          TEXT NOT NULL,
    price         REAL NOT NULL,
    cost          REAL NOT NULL
);

-- 订单表
CREATE TABLE IF NOT EXISTS orders (
    order_id      INTEGER PRIMARY KEY,
    user_id       INTEGER NOT NULL,
    created_at    TEXT NOT NULL,
    status        TEXT NOT NULL,   -- 'placed' / 'paid' / 'shipped' / 'completed' / 'cancelled'
    total_amount  REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 订单明细表
CREATE TABLE IF NOT EXISTS order_items (
    item_id       INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL,
    product_id    INTEGER NOT NULL,
    quantity      INTEGER NOT NULL,
    unit_price    REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 行为日志（用于漏斗分析）
CREATE TABLE IF NOT EXISTS events (
    event_id      INTEGER PRIMARY KEY,
    user_id       INTEGER NOT NULL,
    session_id    TEXT NOT NULL,
    event_type    TEXT NOT NULL,  -- 'view' / 'add_to_cart' / 'checkout' / 'pay'
    product_id    INTEGER,
    occurred_at   TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_created ON orders(created_at);
CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);