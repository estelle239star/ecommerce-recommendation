import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================
# 页面设置
# =========================
st.set_page_config(
    page_title="电商用户行为分析与推荐系统",
    page_icon="📊",
    layout="wide"
)

# =========================
# 路径与数据
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

daily = pd.read_csv(OUTPUT_DIR / "daily_metrics.csv")
top_categories = pd.read_csv(OUTPUT_DIR / "top_categories.csv")
top_brands = pd.read_csv(OUTPUT_DIR / "top_brands.csv")
rfm = pd.read_csv(OUTPUT_DIR / "rfm_segments.csv")
model_comparison = pd.read_csv(OUTPUT_DIR / "model_comparison.csv")
popular_products = pd.read_csv(OUTPUT_DIR / "popular_products.csv")
recommend_example = pd.read_csv(OUTPUT_DIR / "recommendation_example.csv")

daily["date"] = pd.to_datetime(daily["date"])

# =========================
# 页面标题
# =========================
st.title("📊 多品类电商用户行为分析与智能推荐决策系统")

st.caption(
    "基于 2019 年 10—11 月约 1.10 亿条电商用户行为数据，"
    "从经营表现、用户行为、商品结构、用户分层和个性化推荐等角度进行分析。"
)

st.divider()

# =========================
# 一、经营概览
# =========================
st.header("经营概览")

col1, col2, col3, col4 = st.columns(4)

col1.metric("总行为量", "1.10 亿")
col2.metric("用户数", "531.7 万")
col3.metric("购买用户", "69.7 万")
col4.metric("购买转化率", "13.12%")

st.subheader("每日用户行为趋势")

daily_long = daily.melt(
    id_vars="date",
    value_vars=["pv", "uv"],
    var_name="指标",
    value_name="数量"
)

daily_long["指标"] = daily_long["指标"].replace({
    "pv": "PV",
    "uv": "UV"
})

fig_daily = px.line(
    daily_long,
    x="date",
    y="数量",
    color="指标",
    labels={
        "date": "日期",
        "数量": "用户行为数量"
    }
)

fig_daily.update_layout(
    height=420,
    legend_title_text="",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(
    fig_daily,
    use_container_width=True
)

st.caption(
    "11 月中旬 PV 和 UV 出现明显波动，说明该时间段平台用户活跃度显著提高。"
)

st.divider()

# =========================
# 二、用户分析
# =========================
st.header("用户分析")

col1, col2 = st.columns(2)

# 用户行为漏斗
with col1:
    st.subheader("用户行为漏斗")

    funnel_data = pd.DataFrame({
        "阶段": ["浏览", "加购", "购买"],
        "用户数": [5316128, 1054127, 697470]
    })

    fig_funnel = px.funnel(
        funnel_data,
        x="用户数",
        y="阶段"
    )

    fig_funnel.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_funnel,
        use_container_width=True
    )

    st.caption(
        "浏览用户中约 19.83% 发生过加购，约 13.12% 发生过购买。"
    )

# RFM
with col2:
    st.subheader("RFM 用户分层")

    rfm_plot = rfm.sort_values(
        "user_count",
        ascending=True
    )

    fig_rfm = px.bar(
        rfm_plot,
        x="user_count",
        y="segment",
        orientation="h",
        text="percentage",
        labels={
            "user_count": "用户数",
            "segment": "用户分层"
        }
    )

    fig_rfm.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_rfm.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_rfm,
        use_container_width=True
    )

    st.caption(
        "基于 Recency、Frequency 和 Monetary 指标，将购买用户划分为 Regular、At Risk、Active 和 High Value 四类。"
    )

st.divider()

# =========================
# 三、商品分析
# =========================
st.header("商品分析")

col1, col2 = st.columns(2)

# 品类
with col1:
    st.subheader("购买量 Top 10 品类")

    category_plot = top_categories.sort_values(
        "purchases",
        ascending=True
    )

    fig_category = px.bar(
        category_plot,
        x="purchases",
        y="category_code",
        orientation="h",
        labels={
            "purchases": "购买次数",
            "category_code": "品类"
        }
    )

    fig_category.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

    st.caption(
        "智能手机品类购买量明显领先，是平台最主要的成交品类。"
    )

# 品牌
with col2:
    st.subheader("GMV Top 10 品牌")

    brand_plot = top_brands.copy()
    brand_plot["gmv_million"] = (
        brand_plot["gmv"] / 1_000_000
    )

    brand_plot = brand_plot.sort_values(
        "gmv_million",
        ascending=True
    )

    fig_brand = px.bar(
        brand_plot,
        x="gmv_million",
        y="brand",
        orientation="h",
        labels={
            "gmv_million": "GMV（百万）",
            "brand": "品牌"
        }
    )

    fig_brand.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_brand,
        use_container_width=True
    )

    st.caption(
        "Apple 与 Samsung 的 GMV 位居前列，其中 Apple 的平均购买记录金额更高。"
    )

st.divider()

# =========================
# 四、推荐系统
# =========================
st.header("推荐系统")

col1, col2 = st.columns(2)

# 模型效果
with col1:
    st.subheader("模型效果对比")

    comparison_plot = model_comparison.copy()
    comparison_plot["Hit Rate@5 (%)"] = (
        comparison_plot["Hit Rate@5"] * 100
    )

    fig_model = px.bar(
        comparison_plot,
        x="Model",
        y="Hit Rate@5 (%)",
        text="Hit Rate@5 (%)",
        labels={
            "Model": "模型"
        }
    )

    fig_model.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_model.update_layout(
        height=420,
        yaxis_range=[0, 25],
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_model,
        use_container_width=True
    )

    st.caption(
        "ItemCF 的 Hit Rate@5 为 21.05%，明显高于 Popularity Baseline 的 8.77%。"
    )

# 热门商品
with col2:
    st.subheader("热门商品 Top 10")

    popular_plot = popular_products.copy()

    # 商品 ID 转为字符串
    popular_plot["product_id"] = (
        popular_plot["product_id"]
        .astype(str)
    )

    popular_plot = popular_plot.sort_values(
        "popularity_score",
        ascending=True
    )

    fig_popular = px.bar(
        popular_plot,
        x="popularity_score",
        y="product_id",
        orientation="h",
        labels={
            "popularity_score": "热度得分",
            "product_id": "商品 ID"
        },
        hover_data={
            "category_code": True,
            "brand": True,
            "avg_price": ":.2f"
        }
    )

    fig_popular.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis_type="category"
    )

    st.plotly_chart(
        fig_popular,
        use_container_width=True
    )

    st.caption(
        "热门商品主要集中在智能手机及相关电子产品品类。"
    )

# 个性化推荐案例
st.subheader("ItemCF 个性化推荐案例")

display_recommend = recommend_example[
    [
        "product_id",
        "recommend_score",
        "category_code",
        "brand",
        "avg_price"
    ]
].copy()

display_recommend["recommend_score"] = (
    display_recommend["recommend_score"]
    .round(4)
)

display_recommend["avg_price"] = (
    display_recommend["avg_price"]
    .round(2)
)

display_recommend.columns = [
    "商品 ID",
    "推荐得分",
    "品类",
    "品牌",
    "平均价格"
]

st.dataframe(
    display_recommend,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "示例推荐结果基于用户历史加购和购买行为，通过 ItemCF 计算商品相似关系后生成 Top-5 个性化推荐。"
)

st.divider()

# =========================
# 五、项目说明
# =========================
st.header("项目说明")

st.markdown(
    """
**技术栈：** Python / Pandas / DuckDB / SQL / Parquet / SciPy / Scikit-learn / Streamlit / Plotly

**核心流程：**

原始 CSV  
→ DuckDB 数据清洗  
→ Parquet 存储优化  
→ 业务指标分析  
→ RFM 用户分层  
→ Popularity Baseline  
→ ItemCF 个性化推荐  
→ Leave-One-Out 离线评估  
→ Streamlit Dashboard
"""
)