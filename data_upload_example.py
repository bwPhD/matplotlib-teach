"""
数据上传功能使用示例
展示如何使用 PlotAPI 的数据上传和绘图功能
"""

from plot_api import create_plot, DataLoader
import pandas as pd
import json

# ========== 示例 1: 从 CSV 文件加载数据 ==========
print("=" * 60)
print("示例 1: 从 CSV 文件加载数据")
print("=" * 60)

# 创建示例 CSV 数据
csv_data = """x,y
0,0
1,1
2,4
3,9
4,16
5,25"""

api1 = create_plot()
api1.load_data(csv_data, name='line_data', file_type='csv')

# 查看数据
df1 = api1.get_data('line_data')
print("加载的数据：")
print(df1)
print()

# 绘制折线图
api1.plot_from_data('line', 'line_data', x_col='x', y_col='y', 
                   linestyle='--', linewidth=2, color='#3b82f6')
print("代码生成：")
print(api1.generate_code())
print()

# ========== 示例 2: 从 JSON 文件加载数据 ==========
print("=" * 60)
print("示例 2: 从 JSON 文件加载数据")
print("=" * 60)

json_data = {
    "category": ["A", "B", "C", "D", "E"],
    "value": [23, 45, 56, 78, 32]
}

api2 = create_plot()
api2.load_data(json_data, name='bar_data', file_type='json')

# 查看数据
df2 = api2.get_data('bar_data')
print("加载的数据：")
print(df2)
print()

# 绘制条形图
api2.plot_from_data('bar', 'bar_data', x_col='category', y_col='value',
                   color='#10b981', alpha=0.8)
print("代码生成：")
print(api2.generate_code())
print()

# ========== 示例 3: 自动检测文件类型 ==========
print("=" * 60)
print("示例 3: 自动检测文件类型")
print("=" * 60)

# CSV 格式
csv_str = "x,y\n0,0\n1,1\n2,4"
api3 = create_plot()
df3 = api3.load_data(csv_str, name='auto_csv', file_type='auto')
print("自动检测为 CSV，数据：")
print(df3)
print()

# JSON 格式
json_str = '{"x": [0, 1, 2], "y": [0, 1, 4]}'
api4 = create_plot()
df4 = api4.load_data(json_str, name='auto_json', file_type='auto')
print("自动检测为 JSON，数据：")
print(df4)
print()

# ========== 示例 4: 散点图数据 ==========
print("=" * 60)
print("示例 4: 散点图数据")
print("=" * 60)

scatter_data = """x,y,size,color
0.1,0.2,50,0.3
0.3,0.4,100,0.5
0.5,0.6,150,0.7
0.7,0.8,200,0.9
0.9,0.1,250,0.2"""

api5 = create_plot()
api5.load_data(scatter_data, name='scatter_data', file_type='csv')
df5 = api5.get_data('scatter_data')
print("散点图数据：")
print(df5)
print()

# 绘制散点图
api5.plot_from_data('scatter', 'scatter_data', x_col='x', y_col='y',
                    s=df5['size'].values if 'size' in df5.columns else None,
                    c=df5['color'].values if 'color' in df5.columns else None,
                    cmap='viridis', alpha=0.6)
print("代码生成：")
print(api5.generate_code())
print()

# ========== 示例 5: 列出所有数据 ==========
print("=" * 60)
print("示例 5: 列出所有已加载的数据")
print("=" * 60)

api6 = create_plot()
api6.load_data(csv_data, name='data1')
api6.load_data(json_data, name='data2')

print("已加载的数据名称：", api6.list_data())
for name in api6.list_data():
    df = api6.get_data(name)
    print(f"\n{name}:")
    print(df.head())
print()

# ========== 示例 6: 使用 DataLoader 直接加载 ==========
print("=" * 60)
print("示例 6: 使用 DataLoader 直接加载")
print("=" * 60)

# 直接使用 DataLoader
df7 = DataLoader.load_data(csv_data, file_type='csv')
print("直接加载的数据：")
print(df7)
print()

# ========== 示例 7: 错误处理 ==========
print("=" * 60)
print("示例 7: 错误处理")
print("=" * 60)

api8 = create_plot()
try:
    # 尝试从不存在的数据绘制图表
    api8.plot_from_data('line', 'nonexistent_data')
except ValueError as e:
    print(f"预期的错误: {e}")

try:
    # 尝试加载无效的 JSON
    api8.load_data("invalid json", file_type='json')
except (ValueError, json.JSONDecodeError) as e:
    print(f"预期的错误: {e}")

print("\n所有示例完成！")

