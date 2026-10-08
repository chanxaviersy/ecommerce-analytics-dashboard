<!-- 徽章 -->
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/chanxaviersy/ecommerce-analytics-dashboard/actions/workflows/test.yml/badge.svg)](https://github.com/chanxaviersy/ecommerce-analytics-dashboard/actions)
[![Last Commit](https://img.shields.io/github/last-commit/chanxaviersy/ecommerce-analytics-dashboard)](https://github.com/chanxaviersy/ecommerce-analytics-dashboard)

---

# 电商销售分析与交互式仪表板

> 端到端数据处理管道 + 交互式业务指标仪表板

本项目源自简历中的个人项目「E-commerce Sales Analytics and Interactive Dashboard」（2025.1 - 2025.4）。
原项目使用 Python + SQL + Tableau；本仓库将其完全 Python 化，使用 Streamlit 构建交互式仪表板，
核心指标（CLV、漏斗转化、各品类收入）保持一致。

## 项目目标

搭建一套完整的电商数据分析系统，包含：

- **数据层**：原始订单/用户/产品数据的清洗与建模
- **指标层**：CLV（客户生命周期价值）、漏斗转化、各品类表现
- **交互层**：多维筛选仪表板（日期、地区、品类、客群）

## 技术栈

- **数据处理**：Python（Pandas, NumPy）
- **数据库**：SQLite（轻量、生产可换 PostgreSQL）
- **可视化**：Streamlit + Plotly
- **打包依赖**：纯 Python，无额外服务依赖

## 目录结构

```
03-ecommerce-analytics-dashboard/
├── README.md
├── requirements.txt
├── data/                          # 数据文件（运行时自动生成模拟数据）
│   └── ecommerce.db                # SQLite 数据库（自动生成）
├── sql/
│   └── schema.sql                  # 数据库表结构定义
├── src/
│   ├── generate_data.py            # 生成模拟电商数据
│   ├── data_pipeline.py            # ETL 管道
│   ├── metrics.py                  # 业务指标计算（CLV、漏斗等）
│   ├── database.py                 # 数据库连接与查询工具
│   └── queries.py                  # SQL 查询模板
├── dashboard/
│   └── app.py                      # Streamlit 仪表板应用
└── run_demo.py                     # 一键 Demo 入口
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 一键启动：生成数据 + 启动仪表板
streamlit run dashboard/app.py
```

浏览器会自动打开 `http://localhost:8501`。

## 核心业务指标

| 指标                  | 说明                                                |
|----------------------|----------------------------------------------------|
| **GMV**              | 商品交易总额（成交金额）                              |
| **AOV**              | 客单价 = GMV / 订单数                                |
| **CLV**              | 客户生命周期价值（基于历史购买频次与金额预测）          |
| **复购率**            | 30 天内复购用户占比                                  |
| **漏斗转化率**        | 浏览 → 加购 → 下单 → 支付 全链路转化                  |
| **各品类收入贡献**    | 服装/3C/美妆 等品类的 GMV 占比                       |
| **RFM 分层**          | 按最近购买/频次/金额对客户做分层                      |

## 数据库 Schema

主要表：

- `users`：用户表（user_id, 注册时间, 地区, 客群标签）
- `products`：商品表（product_id, 品类, 价格, 成本）
- `orders`：订单表（order_id, user_id, 总金额, 时间, 状态）
- `order_items`：订单明细（order_id, product_id, 数量, 单价）

## SQL 查询示例

`src/queries.py` 内置多个高频分析 SQL：

- 各品类月度 GMV
- 漏斗各阶段用户数
- RFM 客户分层统计
- CLV 排名前 100 用户

## 仪表板功能

仪表板支持以下筛选：

- **时间范围**：自定义日期区间
- **地区**：国家/省份维度
- **品类**：服装 / 3C / 美妆 / 食品 等
- **客群**：新客 / 老客 / VIP / 流失用户

主要展示面板：

1. 核心 KPI（GMV、AOV、复购率、活跃用户数）
2. GMV 时间趋势图（按日/周/月聚合）
3. 各品类收入贡献（饼图 + 表格）
4. 转化漏斗图
5. RFM 客户分层散点图
6. CLV Top 100 客户列表

## 后续可扩展方向

- 接入真实数据源（Shopify API、MySQL 数仓）
- 加入预测模型（GMV 预测、流失预警）
- 替换为 Tableau / Power BI 真仪表板（保留 SQL 层不变）
- 加入 A/B 测试显著性分析

## License

MIT
## 📚 更多文档

- [项目架构](docs/architecture.md)
- [使用指南](docs/usage.md)
- [开发笔记](docs/dev-notes.md)
