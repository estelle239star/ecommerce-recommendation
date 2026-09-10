# 多品类电商用户行为分析与智能推荐决策系统

本项目基于 Kaggle 多品类电商用户行为数据，围绕电商平台经营分析、用户行为分析、用户价值分层和个性化推荐展开。

原始数据覆盖 2019 年 10 月至 11 月，共约 1.10 亿条用户行为记录。项目使用 DuckDB 对大规模 CSV 数据进行清洗和查询，并转换为 Parquet 格式用于后续分析。

## 项目目标

- 分析平台整体经营表现和用户行为特征
- 构建浏览、加购、购买行为漏斗
- 分析主要商品品类和品牌表现
- 基于 RFM 方法进行用户价值分层
- 构建 Popularity Baseline 和 ItemCF 推荐模型
- 使用 Leave-One-Out 方法进行离线评估
- 使用 Streamlit 搭建交互式 Dashboard

## 技术栈

Python / Pandas / DuckDB / SQL / Parquet / SciPy / Scikit-learn / Streamlit / Plotly

## 数据处理

原始数据包括 2019 年 10 月和 11 月两个月的电商用户行为日志。

主要处理流程：

1. 使用 DuckDB 直接读取大规模 CSV
2. 检查字段类型、缺失值和价格异常
3. 合并两个月数据并删除完全重复记录
4. 过滤缺失 user_session 的记录
5. 将清洗后的数据保存为 Parquet 格式

清洗后共保留约 1.098 亿条有效用户行为记录。

原始 CSV 文件合计约 14 GB，转换后的 Parquet 文件约 3.67 GB。

## 业务分析

项目主要分析以下内容：

- PV、UV、购买用户数和购买转化率
- 每日用户行为趋势
- 浏览、加购、购买用户行为漏斗
- Top 10 商品品类
- Top 10 品牌 GMV
- RFM 用户价值分层

主要结果：

- 浏览用户中约 19.83% 发生加购
- 浏览用户中约 13.12% 发生购买
- 智能手机品类的购买量明显领先
- Samsung 的购买次数最高
- Apple 的 GMV 表现更高
- High Value 用户占购买用户约 9.29%

## 推荐系统

推荐系统部分首先构建热门商品推荐作为 Baseline，再使用 ItemCF 进行个性化推荐。

为控制计算规模，建模阶段筛选：

- 交互次数不少于 20 次的活跃用户
- 覆盖用户数不少于 400 的活跃商品
- 仅保留加购和购买两类强兴趣行为

最终得到约 168.7 万个用户-商品交互对，并使用稀疏矩阵构建 ItemCF。

## 推荐效果

使用 Leave-One-Out 方法进行离线评估，共选取 456 名有效测试用户。

| Model | Hit Rate@5 | Precision@5 | Recall@5 |
| --- | ---: | ---: | ---: |
| Popularity Baseline | 8.77% | 1.75% | 8.77% |
| ItemCF | 21.05% | 4.21% | 21.05% |

ItemCF 的 Top-5 推荐效果明显优于热门商品推荐。

## Dashboard

项目使用 Streamlit 和 Plotly 搭建可视化 Dashboard，包含：

- 经营概览
- 用户行为趋势
- 用户行为漏斗
- RFM 用户分层
- 品类和品牌分析
- 推荐模型效果对比
- ItemCF 个性化推荐案例

## 项目结构

```text
ecommerce-recommendation/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_data_overview.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_business_analysis.ipynb
│   └── 04_recommender.ipynb
├── output/
├── sql/
├── src/
├── .gitignore
├── requirements.txt
└── README.md