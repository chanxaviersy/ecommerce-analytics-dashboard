"""常用 SQL 查询模板。"""
from __future__ import annotations

# 各品类月度 GMV
SQL_GMV_BY_CATEGORY_MONTH = """
SELECT
    strftime('%Y-%m', o.created_at) AS month,
    p.category                       AS category,
    SUM(oi.quantity * oi.unit_price) AS gmv
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY month, category
ORDER BY month, category;
"""

# 漏斗各阶段用户数
SQL_FUNNEL = """
SELECT
    event_type,
    COUNT(DISTINCT user_id) AS user_count
FROM events
GROUP BY event_type
ORDER BY
    CASE event_type
        WHEN 'view'         THEN 1
        WHEN 'add_to_cart'  THEN 2
        WHEN 'checkout'     THEN 3
        WHEN 'pay'          THEN 4
    END;
"""

# 用户消费 RFM 分层
SQL_RFM = """
WITH user_stats AS (
    SELECT
        user_id,
        MAX(created_at)                                 AS last_order_at,
        COUNT(DISTINCT order_id)                        AS frequency,
        SUM(total_amount)                               AS monetary
    FROM orders
    WHERE status = 'completed'
    GROUP BY user_id
),
today AS (SELECT DATE('2024-12-31') AS today)
SELECT
    us.user_id,
    CAST(julianday(today.today) - julianday(us.last_order_at) AS INTEGER) AS recency_days,
    us.frequency,
    us.monetary
FROM user_stats us, today
ORDER BY us.monetary DESC;
"""

# CLV Top 100
SQL_CLV_TOP = """
SELECT
    user_id,
    SUM(total_amount)               AS total_spent,
    COUNT(DISTINCT order_id)        AS order_count,
    AVG(total_amount)               AS avg_order_value
FROM orders
WHERE status = 'completed'
GROUP BY user_id
ORDER BY total_spent DESC
LIMIT 100;
"""

# 复购率（30 天窗口）
SQL_REPEAT_PURCHASE_RATE = """
WITH first_orders AS (
    SELECT user_id, MIN(created_at) AS first_order_at
    FROM orders WHERE status = 'completed'
    GROUP BY user_id
),
repurchasers AS (
    SELECT DISTINCT fo.user_id
    FROM first_orders fo
    JOIN orders o
      ON fo.user_id = o.user_id
     AND o.status = 'completed'
     AND julianday(o.created_at) - julianday(fo.first_order_at) BETWEEN 1 AND 30
)
SELECT
    (SELECT COUNT(*) FROM repurchasers) * 1.0
    / (SELECT COUNT(*) FROM first_orders) AS repeat_purchase_rate_30d;
"""