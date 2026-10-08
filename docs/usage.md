# 详细使用指南

## 安装

```bash
git clone https://github.com/chanxaviersy/ecommerce-analytics-dashboard.git
cd ecommerce-analytics-dashboard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 运行

### 一键 Demo

```bash
python run_demo.py
```

流程：
1. 生成 5000 用户 + 20000 订单 + 10万行为
2. 写入 SQLite
3. 跑 ETL 校验
4. 启动 Streamlit 仪表板（http://localhost:8501）

### 分步运行

```bash
# 1. 仅生成数据
python src/generate_data.py

# 2. 跑 ETL
python src/data_pipeline.py

# 3. 启动仪表板
streamlit run dashboard/app.py
```

## 配置

```bash
cp .env.example .env
# 修改 DATABASE_PATH / STREAMLIT_PORT 等
```

## 仪表板模块

| 模块 | 入口 | 说明 |
|------|------|------|
| 核心 KPI | 首页 | GMV / AOV / 订单数 / 用户数 |
| 转化漏斗 | 侧边栏 → 漏斗 | view → add_to_cart → checkout → pay |
| RFM 分层 | 侧边栏 → RFM | 8 客户分层 + 分布图 |
| 品类 GMV | 侧边栏 → 品类 | 5 大品类月度趋势 |
| CLV Top | 侧边栏 → CLV | Top 100 高价值用户 |

## 常见问题

**Q: 仪表板打开是空白？**
A: 检查 Streamlit 终端日志，确认端口 8501 未被占用。

**Q: 数据生成太慢？**
A: 减小 `n_orders=20000` 或 `n_events=100000`。

**Q: 怎么接真实数据？**
A: 替换 `src/data_pipeline.py` 的 SQL，用 `pd.read_sql()` 即可。

## 扩展

- **加新指标**：在 `src/metrics.py` 加函数 + `src/queries.py` 加 SQL
- **加新页面**：在 `dashboard/` 下建新 `.py`，用 `st.page_link` 接入
- **换数据库**：改 `src/database.py` 的 `get_conn` 即可
