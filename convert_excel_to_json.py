import pandas as pd
import json

# 文件路径
file1 = "/Users/linashley/Library/CloudStorage/OneDrive-波士顿咨询公司/Desktop/convert_excel_to_json/Product Data.xlsx"
file2 = "/Users/linashley/Library/CloudStorage/OneDrive-波士顿咨询公司/Desktop/convert_excel_to_json/chart.xlsx"

# === 图表 1：Clustered Bar Chart ===
df1 = pd.read_excel(file1)

# 清洗列名
df1.columns = [col.strip() for col in df1.columns]

# 提取需要的字段
df_cluster = df1[['Product name', 'List Price per unit', 'Production costs per unit']].copy()

# 去掉 $ 符号并转为 float
df_cluster['List Price per unit'] = df_cluster['List Price per unit'].replace('[\$,]', '', regex=True).astype(float)
df_cluster['Production costs per unit'] = df_cluster['Production costs per unit'].replace('[\$,]', '', regex=True).astype(float)

# 分组（有重复产品名的求平均）
df_cluster_grouped = df_cluster.groupby('Product name', as_index=False).mean()

# 保存为 JSON 文件
df_cluster_grouped.to_json("clustered_chart_data.json", orient="records")

# === 图表 2：Bar + Line Chart ===
df2 = pd.read_excel(file2)
df2.columns = [col.strip() for col in df2.columns]

# 分组聚合
df_combo = df2.groupby('Product Name', as_index=False).agg({
    'Quantity': 'sum',
    'Price Paid': 'mean'  # 折线图就用平均价格
})

# 保存为 JSON
df_combo.to_json("combo_chart_data.json", orient="records")

print("✅ 转换完成，生成了 clustered_chart_data.json 和 combo_chart_data.json")
