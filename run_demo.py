"""一键运行 Demo：生成数据 → 输出关键指标。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from metrics import (  # noqa: E402
    compute_core_kpis,
    get_clv_top,
    get_funnel,
    get_gmv_by_category_month,
    get_repeat_purchase_rate,
    get_rfm,
)
from data_pipeline import run_etl  # noqa: E402


def main() -> None:
    print("=" * 60)
    print("  电商销售分析与交互式仪表板 - 一键 Demo")
    print("=" * 60)

    # 1. ETL
    print("\n[DEMO] 加载数据...")
    run_etl(force=False)

    # 2. KPI
    print("\n[DEMO] 核心 KPI：")
    kpis = compute_core_kpis()
    for k, v in kpis.items():
        if isinstance(v, float):
            print(f"  {k:15s}: {v:,.2f}")
        else:
            print(f"  {k:15s}: {v:,}")

    print(f"\n[DEMO] 30 天复购率：{get_repeat_purchase_rate():.2%}")

    # 3. 各品类 GMV
    print("\n[DEMO] 各品类累计 GMV：")
    cat_gmv = get_gmv_by_category_month()
    if not cat_gmv.empty:
        total = cat_gmv.groupby("category")["gmv"].sum().sort_values(ascending=False)
        for cat, gmv in total.items():
            share = gmv / total.sum()
            print(f"  {cat:8s}: ¥{gmv:>12,.2f}  ({share:>6.2%})")

    # 4. 漏斗
    print("\n[DEMO] 转化漏斗：")
    funnel = get_funnel()
    if not funnel.empty:
        for _, row in funnel.iterrows():
            print(f"  {row['event_type']:12s}: {row['user_count']:>6,} 用户  "
                  f"({row['conversion_rate']:>6.2%})")

    # 5. RFM 分层
    print("\n[DEMO] RFM 客户分层：")
    rfm = get_rfm()
    if not rfm.empty:
        for seg, cnt in rfm["segment"].value_counts().items():
            print(f"  {seg:10s}: {cnt:>5,} 人")

    print("\n[DEMO] ✅ 完成！")
    print("[DEMO] 启动仪表板：streamlit run dashboard/app.py")


if __name__ == "__main__":
    main()