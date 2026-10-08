<!-- ============= 顶部徽章 ============= -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Plotly-5.0%2B-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly"/>
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge" alt="License"/>
</p>

<p align="center">
  <a href="https://github.com/chanxaviersy/ecommerce-analytics-dashboard/actions/workflows/test.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/chanxaviersy/ecommerce-analytics-dashboard/test.yml?label=CI&style=flat-square" alt="CI"/>
  </a>
  <a href="https://github.com/chanxaviersy/ecommerce-analytics-dashboard">
    <img src="https://img.shields.io/github/last-commit/chanxaviersy/ecommerce-analytics-dashboard?style=flat-square" alt="Last Commit"/>
  </a>
  <a href="https://github.com/chanxaviersy/ecommerce-analytics-dashboard/stargazers">
    <img src="https://img.shields.io/github/stars/chanxaviersy/ecommerce-analytics-dashboard?style=flat-square" alt="Stars"/>
  </a>
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome"/>
</p>

<!-- ============= 标题区 ============= -->
<br/>
<div align="center">

# 🛒 电商销售分析与交互式仪表板

### 端到端数据处理管道 + Streamlit 交互式业务指标仪表板

[🚀 快速开始](#-快速开始) · [📖 文档](docs/architecture.md) · [🐛 报告 Bug](https://github.com/chanxaviersy/ecommerce-analytics-dashboard/issues) · [💡 提出新特性](https://github.com/chanxaviersy/ecommerce-analytics-dashboard/issues)

</div>

<!-- ============= 项目亮点卡片 ============= -->
<p align="center">
  <table>
    <tr>
      <td align="center" width="200">
        <h3>📊</h3>
        <b>4 大模块</b><br/>
        <sub><code>CLV / 漏斗 / RFM / GMV</code></sub>
      </td>
      <td align="center" width="200">
        <h3>🎯</h3>
        <b>5000 用户</b><br/>
        <sub><code>20000 订单 / 10万 行为</code></sub>
      </td>
      <td align="center" width="200">
        <h3>🌪</h3>
        <b>全链路漏斗</b><br/>
        <sub><code>view → cart → pay</code></sub>
      </td>
      <td align="center" width="200">
        <h3>💎</h3>
        <b>RFM 8 客户分层</b><br/>
        <sub><code>冠军 / 忠诚 / 新客</code></sub>
      </td>
    </tr>
  </table>
</p>

---

<!-- ============= 目录 ============= -->
## 📑 目录

- [🎯 项目目标](#-项目目标)
- [🛠 技术栈](#-技术栈)
- [📂 目录结构](#-目录结构)
- [🚀 快速开始](#-快速开始)
- [📊 核心业务指标](#-核心业务指标)
- [🗄 数据库 Schema](#-数据库-schema)
- [🎨 仪表板功能](#-仪表板功能)
- [🚀 后续可扩展方向](#-后续可扩展方向)
- [📚 更多文档](#-更多文档)
- [📄 License](#-license)

---

## 🎯 项目目标

搭建一套完整的电商数据分析系统，包含：

- **数据层**：原始订单/用户/产品数据的清洗与建模
- **指标层**：CLV（客户生命周期价值）、漏斗转化、各品类表现
- **交互层**：多维筛选仪表板（日期、地区、品类、客群）

> 本项目源自简历中的个人项目「E-commerce Sales Analytics and Interactive Dashboard」（2025.1 - 2025.4）。原项目使用 Python + SQL + Tableau；本仓库将其完全 Python 化，使用 Streamlit 构建交互式仪表板，核心指标（CLV、漏斗转化、各品类收入）保持一致。

---

## 🛠 技术栈

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,pandas,numpy,sqlite,git,github,vscode" alt="Tech Stack"/>
</p>

| 类别       | 技术                                       |
| ---------- | ------------------------------------------ |
| **数据处理** | Python · Pandas · NumPy                  |
| **数据库**  | SQLite（轻量、生产可换 PostgreSQL）        |
| **可视化**  | Streamlit · Plotly                        |
| **打包依赖** | 纯 Python，无额外服务依赖                |

---

## 📂 目录结构

```
03-ecommerce-analytics-dashboard/
├── 📄 README.md
├── 📋 requirements.txt
├── 📂 data/
│   └── ecommerce.db                # SQLite 数据库（自动生成）
├── 📂 sql/
│   └── schema.sql                  # 数据库表结构定义
├── 🐍 src/
│   ├── generate_data.py            # 生成模拟电商数据
│   ├── data_pipeline.py            # ETL 管道
│   ├── metrics.py                  # 业务指标计算（CLV、漏斗等）
│   ├── database.py                 # 数据库连接与查询工具
│   └── queries.py                  # SQL 查询模板
├── 🎨 dashboard/
│   └── app.py                      # Streamlit 仪表板应用
├── 🧪 tests/                       # 单元测试
├── 📚 docs/                        # 详细文档
│   ├── architecture.md
│   ├── usage.md
│   └── dev-notes.md
└── 🎬 run_demo.py                  # 一键 Demo 入口
```

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/chanxaviersy/ecommerce-analytics-dashboard.git
cd ecommerce-analytics-dashboard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 一键启动

```bash
# 方式 1：自动生成数据 + 启动仪表板
python run_demo.py

# 方式 2：手动启动
python src/generate_data.py    # 生成模拟数据
streamlit run dashboard/app.py # 启动仪表板
```

浏览器会自动打开 `http://localhost:8501` 🎉

---

## 📊 核心业务指标

| 指标                  | 说明                                                |
| --------------------- | --------------------------------------------------- |
| **GMV**              | 商品交易总额（成交金额）                              |
| **AOV**              | 客单价 = GMV / 订单数                                |
| **CLV**              | 客户生命周期价值（基于历史购买频次与金额预测）          |
| **复购率**            | 30 天内复购用户占比                                  |
| **漏斗转化率**        | 浏览 → 加购 → 下单 → 支付 全链路转化                  |
| **各品类收入贡献**    | 服装/3C/美妆 等品类的 GMV 占比                       |
| **RFM 分层**          | 按最近购买/频次/金额对客户做分层                      |

---

## 🗄 数据库 Schema

主要表：

| 表名            | 字段                                                                 |
| --------------- | -------------------------------------------------------------------- |
| `users`         | user_id, 注册时间, 地区, 客群标签                                     |
| `products`      | product_id, 品类, 价格, 成本                                          |
| `orders`        | order_id, user_id, 总金额, 时间, 状态                                 |
| `order_items`   | order_id, product_id, 数量, 单价                                      |
| `events`        | event_id, user_id, session_id, event_type (view/cart/checkout/pay)    |

---

## 🎨 仪表板功能

### 筛选维度

- 📅 **时间范围**：自定义日期区间
- 🌍 **地区**：国家/省份维度
- 🛍 **品类**：服装 / 3C / 美妆 / 食品 等
- 👥 **客群**：新客 / 老客 / VIP / 流失用户

### 主要面板

1. 📊 **核心 KPI**（GMV、AOV、复购率、活跃用户数）
2. 📈 **GMV 时间趋势图**（按日/周/月聚合）
3. 🥧 **各品类收入贡献**（饼图 + 表格）
4. 🌪 **转化漏斗图**
5. 👥 **RFM 客户分层散点图**
6. 💎 **CLV Top 100 客户列表**

### 📸 仪表板截图

> 截图待补充：运行 `streamlit run dashboard/app.py` 后截图保存到 [`assets/`](assets/)。

---

## 🚀 后续可扩展方向

- 接入真实数据源（Shopify API、MySQL 数仓）
- 加入预测模型（GMV 预测、流失预警）
- 替换为 Tableau / Power BI 真仪表板（保留 SQL 层不变）
- 加入 A/B 测试显著性分析
- 接入 dbt 做数据建模

---

## 📚 更多文档

| 文档 | 说明 |
|------|------|
| [📐 项目架构](docs/architecture.md) | 整体设计、模块关系、数据流 |
| [📖 使用指南](docs/usage.md) | 详细安装、配置、自定义 |
| [🔧 开发笔记](docs/dev-notes.md) | 踩过的坑、性能优化、业务理解 |
| [📝 CHANGELOG](CHANGELOG.md) | 版本变更记录 |
| [🤝 CONTRIBUTING](CONTRIBUTING.md) | 如何参与贡献 |

---

## 📄 License

本项目基于 [MIT](LICENSE) 协议开源。

---

<div align="center">

**[⬆ 回到顶部](#-电商销售分析与交互式仪表板)**

Made with ❤️ by [Xavier Chen](https://github.com/chanxaviersy)

</div>
