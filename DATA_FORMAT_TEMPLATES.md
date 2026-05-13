# 数据格式模板说明

## 📋 概述

本文档提供了各种图表类型所需的数据格式模板，帮助您准备和上传数据文件。

## 📁 模板文件位置

所有模板文件位于 `data_templates/` 目录下，包括：
- CSV 格式模板
- JSON 格式模板

## 📊 支持的图表类型和数据格式

### 1. 折线图 (Line Chart)

#### CSV 格式
```csv
x,y
0,0
1,1
2,4
3,9
4,16
```

**要求：**
- 第一行为列名（x, y）
- x 列：X 轴数据（数值）
- y 列：Y 轴数据（数值）

#### JSON 格式
```json
[
  {"x": 0, "y": 0},
  {"x": 1, "y": 1},
  {"x": 2, "y": 4}
]
```

**要求：**
- JSON 数组格式
- 每个对象包含 x 和 y 字段

### 2. 条形图 (Bar Chart)

#### CSV 格式
```csv
category,value
A,23
B,45
C,56
D,78
```

**要求：**
- 第一行为列名（category, value）
- category 列：类别名称（字符串）
- value 列：数值（数值）

#### JSON 格式
```json
{
  "category": ["A", "B", "C", "D"],
  "value": [23, 45, 56, 78]
}
```

**要求：**
- JSON 对象格式
- category：类别数组
- value：数值数组

### 3. 散点图 (Scatter Plot)

#### CSV 格式
```csv
x,y,size,color
0.1,0.2,50,0.3
0.3,0.4,100,0.5
0.5,0.6,150,0.7
```

**要求：**
- 第一行为列名（x, y, size, color）
- x 列：X 轴数据（数值）
- y 列：Y 轴数据（数值）
- size 列（可选）：点的大小（数值）
- color 列（可选）：点的颜色值（数值，用于颜色映射）

#### JSON 格式
```json
[
  {"x": 0.1, "y": 0.2, "size": 50, "color": 0.3},
  {"x": 0.3, "y": 0.4, "size": 100, "color": 0.5}
]
```

### 4. 直方图 (Histogram)

#### CSV 格式
```csv
value
2.3
1.8
3.2
2.5
1.9
```

**要求：**
- 第一行为列名（value）
- value 列：数据值（数值）

#### JSON 格式
```json
{
  "value": [2.3, 1.8, 3.2, 2.5, 1.9]
}
```

### 5. 饼图 (Pie Chart)

#### CSV 格式
```csv
label,size
类别A,15
类别B,30
类别C,45
类别D,10
```

**要求：**
- 第一行为列名（label, size）
- label 列：标签名称（字符串）
- size 列：扇形大小（数值）

#### JSON 格式
```json
{
  "label": ["类别A", "类别B", "类别C", "类别D"],
  "size": [15, 30, 45, 10]
}
```

### 6. 误差棒图 (Errorbar)

#### CSV 格式
```csv
x,y,yerr,xerr
1,2,0.3,0.1
2,3,0.4,0.1
3,4,0.5,0.1
```

**要求：**
- 第一行为列名（x, y, yerr, xerr）
- x 列：X 轴数据（数值）
- y 列：Y 轴数据（数值）
- yerr 列：Y 轴误差（数值）
- xerr 列：X 轴误差（数值，可选）

#### JSON 格式
```json
[
  {"x": 1, "y": 2, "yerr": 0.3, "xerr": 0.1},
  {"x": 2, "y": 3, "yerr": 0.4, "xerr": 0.1}
]
```

## 🔧 使用示例

### Python 代码示例

```python
from plot_api import create_plot

# 创建 API 实例
api = create_plot()

# 方法 1: 从文件加载数据
with open('data_templates/line_chart_template.csv', 'r') as f:
    api.load_data(f.read(), name='line_data', file_type='csv')

# 方法 2: 从字符串加载数据
csv_data = """x,y
0,0
1,1
2,4"""
api.load_data(csv_data, name='line_data', file_type='csv')

# 方法 3: 从 JSON 加载数据
json_data = '{"x": [0, 1, 2], "y": [0, 1, 4]}'
api.load_data(json_data, name='line_data', file_type='json')

# 从数据绘制图表
api.plot_from_data('line', data_name='line_data', x_col='x', y_col='y')

# 显示图表
fig = api.show()
```

### Streamlit 使用示例

```python
import streamlit as st
from plot_api import create_plot

# 文件上传
uploaded_file = st.file_uploader("上传数据文件", type=['csv', 'json'])

if uploaded_file is not None:
    # 读取文件内容
    file_content = uploaded_file.read()
    
    # 创建 API 实例
    api = create_plot()
    
    # 加载数据
    file_type = uploaded_file.name.split('.')[-1]
    api.load_data(file_content, name='uploaded_data', file_type=file_type)
    
    # 显示数据预览
    df = api.get_data('uploaded_data')
    st.dataframe(df)
    
    # 选择列
    if len(df.columns) >= 2:
        x_col = st.selectbox("选择 X 轴列", df.columns)
        y_col = st.selectbox("选择 Y 轴列", df.columns)
        
        # 绘制图表
        chart_type = st.selectbox("选择图表类型", ['line', 'bar', 'scatter'])
        api.plot_from_data(chart_type, 'uploaded_data', x_col=x_col, y_col=y_col)
        
        # 显示图表
        st.pyplot(api.show())
```

## ⚠️ 注意事项

1. **编码格式**：CSV 文件应使用 UTF-8 编码
2. **分隔符**：CSV 文件默认使用逗号分隔，如需使用其他分隔符，请在加载时指定
3. **缺失值**：缺失值应使用空字符串或 NaN 表示
4. **数据类型**：
   - 数值列应包含纯数字
   - 字符串列可以包含任何文本
   - 日期时间列建议使用 ISO 格式（YYYY-MM-DD HH:MM:SS）
5. **文件大小**：建议单个文件不超过 10MB

## 📝 数据验证

上传数据后，系统会自动进行以下验证：

1. **格式验证**：检查文件格式是否正确
2. **列名验证**：检查必需的列是否存在
3. **数据类型验证**：检查数值列是否包含有效数字
4. **数据完整性验证**：检查是否有缺失值

## 🔗 相关资源

- [Pandas 文档](https://pandas.pydata.org/docs/) - 数据处理库
- [CSV 格式规范](https://tools.ietf.org/html/rfc4180) - CSV 标准
- [JSON 格式规范](https://www.json.org/) - JSON 标准

