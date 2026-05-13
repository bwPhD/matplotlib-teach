# PlotAPI 使用文档

## 📖 概述

`plot_api.py` 是一个统一的图表绘制 API 模块，参考 FigureForge 的设计理念，提供科学、完整的图表绘制接口。

## 🎯 设计原则

1. **统一的图表类型注册机制**：所有图表类型通过注册表管理
2. **参数验证和默认值管理**：自动验证参数类型和有效性
3. **科学的代码生成逻辑**：生成可读性高、格式规范的代码
4. **可扩展的图表类型支持**：易于添加新的图表类型
5. **完整的参数文档**：每个参数都有详细的说明和验证规则

## 🚀 快速开始

### 基本使用

```python
from plot_api import create_plot

# 创建绘图 API 实例
api = create_plot(figsize=(8, 5))

# 绘制折线图
api.plot("line", linestyle='--', linewidth=2, color='#3b82f6')

# 生成代码
code = api.generate_code()
print(code)

# 显示图表
fig = api.show()
```

### 支持的图表类型

#### 线条类 (LINE)
- `line`: 折线图

#### 形状与统计图 (PATCH)
- `bar`: 垂直条形图
- `barh`: 水平条形图
- `hist`: 直方图
- `pie`: 饼图

#### 集合类 (COLLECTION)
- `scatter`: 散点图

## 📚 API 参考

### `create_plot(figsize=(8, 5))`

创建绘图 API 实例。

**参数：**
- `figsize`: 图表尺寸，默认 `(8, 5)`

**返回：** `PlotAPI` 实例

### `PlotAPI.plot(chart_type, **params)`

绘制图表。

**参数：**
- `chart_type`: 图表类型名称（字符串）
- `**params`: 图表参数

**返回：** matplotlib 绘图函数的返回值

**示例：**
```python
api.plot("line", x=[1, 2, 3], y=[1, 4, 9], linestyle='--', linewidth=2)
api.plot("bar", x=['A', 'B', 'C'], height=[10, 20, 30], color='blue')
```

### `PlotAPI.generate_code(include_imports=True, include_setup=True)`

生成完整的 Python 代码。

**参数：**
- `include_imports`: 是否包含导入语句，默认 `True`
- `include_setup`: 是否包含图表设置代码，默认 `True`

**返回：** 生成的代码字符串

**示例：**
```python
code = api.generate_code()
print(code)
```

### `PlotAPI.show()`

显示图表。

**返回：** matplotlib Figure 对象

### `PlotAPI.save(filename, **kwargs)`

保存图表。

**参数：**
- `filename`: 保存的文件名
- `**kwargs`: matplotlib `savefig` 的其他参数

### `get_chart_types(category=None)`

获取图表类型列表。

**参数：**
- `category`: 图表类别（可选），`ChartCategory` 枚举值

**返回：** 图表类型列表

**示例：**
```python
from plot_api import get_chart_types, ChartCategory

# 获取所有图表类型
all_charts = get_chart_types()

# 获取特定类别的图表
line_charts = get_chart_types(ChartCategory.LINE)
```

### `get_chart_info(chart_type)`

获取图表类型信息。

**参数：**
- `chart_type`: 图表类型名称

**返回：** `ChartType` 对象或 `None`

## 📋 参数说明

### Line Plot (折线图)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `x` | list/tuple/ndarray | None | X 轴数据 |
| `y` | list/tuple/ndarray | None | Y 轴数据 |
| `linestyle` | str | '-' | 线型：'-', '--', '-.', ':', 'None' |
| `linewidth` | float | 1.5 | 线宽 |
| `color` | str | '#2c3e50' | 颜色 |
| `marker` | str | None | 标记符号 |
| `markersize` | float | 6 | 标记大小 |
| `alpha` | float | 1.0 | 透明度 (0-1) |
| `label` | str | None | 标签 |

### Bar Chart (垂直条形图)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `x` | list/tuple/ndarray | None | X 轴类别 |
| `height` | list/tuple/ndarray | None | 条形高度 |
| `width` | float | 0.8 | 条形宽度 |
| `color` | str | '#3b82f6' | 颜色 |
| `alpha` | float | 0.8 | 透明度 (0-1) |
| `edgecolor` | str | None | 边框颜色 |
| `linewidth` | float | 1.0 | 边框宽度 |
| `label` | str | None | 标签 |

### Scatter Plot (散点图)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `x` | list/tuple/ndarray | None | X 轴数据 |
| `y` | list/tuple/ndarray | None | Y 轴数据 |
| `s` | int/float/list/ndarray | None | 点的大小 |
| `c` | str/list/ndarray | None | 颜色 |
| `marker` | str | 'o' | 标记符号 |
| `alpha` | float | 0.5 | 透明度 (0-1) |
| `cmap` | str | 'viridis' | 颜色映射 |
| `label` | str | None | 标签 |

## 🔧 扩展图表类型

### 添加新的图表类型

1. **定义绘图函数**：
```python
def plot_my_chart(ax: matplotlib.axes.Axes, x=None, y=None, **kwargs):
    if x is None:
        x = np.linspace(0, 10, 50)
    if y is None:
        y = np.sin(x)
    return ax.plot(x, y, **kwargs)
```

2. **定义参数**：
```python
parameters = {
    'x': ParameterDefinition('x', (list, tuple, np.ndarray), None, "X 轴数据"),
    'y': ParameterDefinition('y', (list, tuple, np.ndarray), None, "Y 轴数据"),
    'color': ParameterDefinition('color', str, '#3b82f6', "颜色"),
    # ... 更多参数
}
```

3. **注册图表类型**：
```python
ChartRegistry.register(ChartType(
    name="my_chart",
    display_name="My Chart (我的图表)",
    category=ChartCategory.LINE,
    plot_func=plot_my_chart,
    parameters=parameters,
    description="我的自定义图表"
))
```

## ⚠️ 注意事项

1. **参数验证**：所有参数都会自动验证，无效参数会抛出 `ValueError`
2. **默认值**：如果参数未提供，会使用定义的默认值
3. **代码生成**：生成的代码可以直接运行，但需要确保数据已定义
4. **图表叠加**：可以在同一个 `PlotAPI` 实例上绘制多个图表

## 📝 示例代码

完整示例请参考 `plot_api_example.py`。

## 🔗 相关资源

- [FigureForge GitHub](https://github.com/nogula/FigureForge)
- [Matplotlib 官方文档](https://matplotlib.org/)
- [项目 README](README_CATALOG.md)

