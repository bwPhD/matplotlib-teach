"""
PlotAPI 使用示例
展示如何使用统一的图表绘制 API
"""

from plot_api import create_plot, get_chart_types, ChartCategory
import numpy as np

# ========== 示例 1: 基本使用 ==========
print("=" * 60)
print("示例 1: 基本折线图")
print("=" * 60)

api = create_plot(figsize=(8, 5))
api.plot("line", linestyle='--', linewidth=2, color='#3b82f6', marker='o', markersize=8)
code = api.generate_code()
print(code)
print()

# ========== 示例 2: 条形图 ==========
print("=" * 60)
print("示例 2: 条形图")
print("=" * 60)

api2 = create_plot(figsize=(8, 5))
api2.plot("bar", 
          x=['A', 'B', 'C', 'D', 'E'],
          height=[23, 45, 56, 78, 32],
          color='#10b981',
          alpha=0.8,
          edgecolor='black',
          linewidth=1.5)
code2 = api2.generate_code()
print(code2)
print()

# ========== 示例 3: 散点图 ==========
print("=" * 60)
print("示例 3: 散点图")
print("=" * 60)

api3 = create_plot(figsize=(8, 5))
x = np.random.rand(200)
y = np.random.rand(200)
sizes = (30 * np.random.rand(200))**2
colors = np.random.rand(200)

api3.plot("scatter", x=x, y=y, s=sizes, c=colors, cmap='viridis', alpha=0.6)
code3 = api3.generate_code()
print(code3)
print()

# ========== 示例 4: 查看所有图表类型 ==========
print("=" * 60)
print("示例 4: 查看所有图表类型")
print("=" * 60)

all_charts = get_chart_types()
print(f"总共注册了 {len(all_charts)} 种图表类型：\n")
for chart in all_charts:
    print(f"  - {chart.display_name} ({chart.name})")
    print(f"    类别: {chart.category.value}")
    print(f"    描述: {chart.description}")
    print(f"    参数数量: {len(chart.parameters)}")
    print()

# ========== 示例 5: 按类别查看图表 ==========
print("=" * 60)
print("示例 5: 按类别查看图表")
print("=" * 60)

line_charts = get_chart_types(ChartCategory.LINE)
print(f"线条类图表 ({len(line_charts)} 种):")
for chart in line_charts:
    print(f"  - {chart.display_name}")

patch_charts = get_chart_types(ChartCategory.PATCH)
print(f"\n形状与统计图表 ({len(patch_charts)} 种):")
for chart in patch_charts:
    print(f"  - {chart.display_name}")

collection_charts = get_chart_types(ChartCategory.COLLECTION)
print(f"\n集合类图表 ({len(collection_charts)} 种):")
for chart in collection_charts:
    print(f"  - {chart.display_name}")

# ========== 示例 6: 参数验证 ==========
print("\n" + "=" * 60)
print("示例 6: 参数验证")
print("=" * 60)

api4 = create_plot()
try:
    # 尝试使用无效的参数值
    api4.plot("line", linestyle='invalid_style')
except ValueError as e:
    print(f"参数验证失败（预期行为）: {e}")

try:
    # 尝试使用无效的 alpha 值
    api4.plot("line", alpha=1.5)  # alpha 应该在 0-1 之间
except ValueError as e:
    print(f"参数验证失败（预期行为）: {e}")

# 使用有效的参数
api4.plot("line", linestyle='--', alpha=0.7, linewidth=2.5)
print("参数验证通过，图表绘制成功！")

