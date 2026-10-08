# 开发笔记

## 踩过的坑

### 1. RFM 分位数切分报错

- **问题**：`pd.qcut` 在重复值多时报错
- **解决**：`duplicates="drop"`
- **代码**：`src/metrics.py:get_rfm`

### 2. SQL 注入风险

- **问题**：直接拼接用户输入到 SQL
- **解决**：用参数化查询 `?` 占位符
- **代码**：`src/database.py:query_to_df` 的 `params` 参数

### 3. Streamlit 缓存失效

- **问题**：数据更新后仪表板不刷新
- **解决**：`@st.cache_data(ttl=3600)` 设置 TTL，或加手动刷新按钮
- **代码**：`dashboard/app.py`

### 4. 大数据量渲染卡顿

- **问题**：10万事件一次性 Plotly 渲染很慢
- **解决**：
  - 预聚合到日 / 周 / 月
  - 用 `st.plotly_chart` 的 `use_container_width=True`
  - 必要时采样（`df.sample(n=1000)`）

## 性能优化

- **数据库索引**：在 `user_id` / `created_at` 上建索引
- **预计算**：把 RFM、漏斗等预计算后存为物化视图
- **异步加载**：Streamlit 的 `@st.cache_resource` 缓存数据库连接
- **分页**：大表格用 `st.dataframe` 的分页

## 业务理解

### RFM 阈值

- **R ≤ 30 天**：活跃
- **R 30-90 天**：沉睡
- **R > 90 天**：流失
- **F ≥ 5 次**：高频
- **M ≥ 500 元**：高价值

### CLV 公式

```
CLV = (月均订单数 × AOV × 预计生命周期) × 毛利率
```

实际生产会更复杂（用 BG/NBD + Gamma-Gamma 模型），这里简化演示。
