# Matplotlib 参数百科全书设计方案

## A. 现有 app.py 的页面结构总结

**当前结构（基于代码分析）：**
- **侧边栏导航**：使用 `st.sidebar.radio()` 实现 7 个章节菜单
- **路由方式**：通过 `if/elif` 判断 `menu` 变量切换页面
- **章节 3 "基础笔触"**：已有 Tab 结构（Line2D/Patches/Collections/Images），但只展示 2-3 个简单示例
- **代码展示**：使用 `st.code()` 显示代码片段
- **图表渲染**：使用 `st.pyplot(fig)` 展示图表

**关键特点：**
- 单文件架构（app.py），所有逻辑集中
- 使用 Streamlit 原生组件（radio/tabs/columns）
- 已有缓存装饰器 `@st.cache_data` 的使用示例

---

## B. 百科页面信息架构（IA）

### 顶层分类（6大类）

#### 1. **Line（线条）**
- `linestyle` - 线型（实线/虚线/点线等）
- `linewidth` - 线宽（数值范围）
- `dashes` - 自定义虚线样式（元组形式）
- `drawstyle` - 绘制样式（default/steps等）
- `capstyle` - 线端样式（butt/round/projecting）
- `joinstyle` - 连接样式（miter/round/bevel）
- `alpha` - 透明度（0-1）
- `zorder` - 图层顺序（数值）

#### 2. **Marker（标记点）**
- `marker` - 标记符号（所有合法字符/数字）
- `markersize` - 标记大小（数值）
- `markeredgewidth` - 标记边缘宽度
- `markeredgecolor` - 标记边缘颜色
- `markerfacecolor` - 标记填充颜色
- `markerfacecoloralt` - 交替填充颜色
- `fillstyle` - 填充样式（full/left/right/top/bottom/none）
- `markevery` - 标记间隔（数值/元组）

#### 3. **Color（颜色）**
- `color` - 颜色值（名称/RGB/HEX/CN等）
- `cmap` - 颜色映射（所有内置 colormap）
- `norm` - 归一化方式（Normalize 子类）
- `alpha` - 透明度（与 Line 共享）

#### 4. **Text（文本）**
- `fontsize` - 字体大小（数值/字符串）
- `fontweight` - 字体粗细（normal/bold/数值）
- `fontstyle` - 字体样式（normal/italic/oblique）
- `fontfamily` - 字体族（serif/sans-serif/monospace/自定义）
- `color` - 文本颜色
- `rotation` - 旋转角度
- `ha` / `va` - 水平/垂直对齐

#### 5. **Axes（坐标轴）**
- `xlim` / `ylim` - 坐标范围（元组）
- `xlabel` / `ylabel` - 轴标签
- `xticks` / `yticks` - 刻度位置/标签
- `grid` - 网格显示（True/False/字典）
- `spines` - 边框控制（top/bottom/left/right）
- `tick_params` - 刻度参数（方向/颜色/大小等）

#### 6. **Figure（画布）**
- `figsize` - 画布尺寸（元组）
- `dpi` - 分辨率（数值）
- `facecolor` / `edgecolor` - 背景/边框颜色
- `tight_layout` - 紧凑布局（布尔/字典）
- `constrained_layout` - 约束布局（布尔）

---

## C. 实现策略

### 1. 动态提取选项（从 Matplotlib API）

#### **linestyle**
```python
from matplotlib.lines import Line2D
line = Line2D([0,1], [0,1])
linestyles = line.lineStyles  # {'-': '_draw_solid', '--': '_draw_dashed', ...}
# 注意：还需补充元组形式 (offset, on-off-seq)
```

#### **drawstyle**
```python
drawstyles = line.drawStyles  # {'default': '_draw_lines', 'steps': ...}
```

#### **marker**
```python
markers = line.markers  # {'.': 'point', 'o': 'circle', ...}
# 包含字符串和数字键
```

#### **fillstyle**
```python
fillstyles = line.fillStyles  # ('full', 'left', 'right', 'bottom', 'top', 'none')
```

#### **capstyle / joinstyle**
```python
import matplotlib._enums
capstyles = [e.value for e in matplotlib._enums.CapStyle]  # ['butt', 'round', 'projecting']
joinstyles = [e.value for e in matplotlib._enums.JoinStyle]  # ['miter', 'round', 'bevel']
```

#### **cmap（颜色映射）**
```python
import matplotlib.pyplot as plt
cmaps = plt.colormaps()  # 返回所有注册的 colormap 名称列表
```

#### **fontfamily**
```python
from matplotlib import font_manager
font_families = sorted(set([f.name for f in font_manager.fontManager.ttflist]))
```

### 2. 按文档规则补齐

#### **linestyle 元组形式**
- 文档规则：`(offset, on-off-seq)` 其中 `on-off-seq` 是点/空序列
- 预设示例：`(0, (5, 5))`, `(0, (3, 1, 1, 1))`, `(0, (1, 1))` 等
- 提供交互式输入框让用户自定义

#### **dashes**
- 与 linestyle 元组形式相同，但通过 `set_dashes()` 方法设置
- 提供预设 + 自定义输入

#### **color**
- 颜色名称：从 `matplotlib.colors` 的 `CSS4_COLORS`, `BASE_COLORS`, `TAB10_COLORS` 等获取
- RGB/RGBA：`(r, g, b)` 或 `(r, g, b, a)` 元组，值范围 0-1
- HEX：`#RRGGBB` 或 `#RRGGBBAA`
- CN 颜色：`'C0'`, `'C1'`, ... `'C9'`（循环使用）

#### **linewidth / markersize / alpha**
- 数值范围：根据文档和实际测试确定合理范围
- linewidth: 通常 0.5-10，默认 1.5
- markersize: 通常 1-100，默认 6
- alpha: 0.0-1.0，默认 1.0

### 3. 缓存策略

```python
@st.cache_data
def get_linestyles():
    """缓存 linestyle 选项"""
    from matplotlib.lines import Line2D
    line = Line2D([0,1], [0,1])
    return dict(line.lineStyles)

@st.cache_data
def get_markers():
    """缓存 marker 选项"""
    from matplotlib.lines import Line2D
    line = Line2D([0,1], [0,1])
    return dict(line.markers)

@st.cache_data
def get_colormaps():
    """缓存 colormap 列表"""
    import matplotlib.pyplot as plt
    return sorted(plt.colormaps())
```

**缓存原则：**
- 所有从 Matplotlib API 提取的选项都使用 `@st.cache_data`
- 避免每次页面加载都重新查询
- 如果 Matplotlib 版本变化，可通过版本号作为缓存键的一部分

---

## D. 代码级补丁方案

### 目录结构

```
matplotlib-teach/
├── app.py                    # 主应用（保留现有结构）
├── catalogs/                 # 新增：参数目录模块
│   ├── __init__.py
│   ├── line.py              # Line 相关参数
│   ├── marker.py            # Marker 相关参数
│   ├── color.py             # Color 相关参数
│   ├── text.py              # Text 相关参数
│   ├── axes.py              # Axes 相关参数
│   ├── figure.py            # Figure 相关参数
│   └── utils.py             # 通用工具函数
└── requirements.txt
```

### 模块接口设计

#### **catalogs/utils.py**（通用工具）
```python
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Any

@st.cache_data
def get_matplotlib_version():
    """获取 Matplotlib 版本"""
    return plt.matplotlib.__version__

def generate_sample_data(n_points=50):
    """生成示例数据"""
    x = np.linspace(0, 10, n_points)
    y = np.sin(x)
    return x, y

def render_preview_figure(fig, title=""):
    """统一渲染预览图"""
    if title:
        fig.suptitle(title, fontsize=10)
    return fig
```

#### **catalogs/line.py**（示例：完整实现）
```python
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.lines
import matplotlib._enums
import numpy as np
from typing import Dict, List, Tuple

@st.cache_data
def get_linestyle_options():
    """获取所有 linestyle 选项"""
    line = matplotlib.lines.Line2D([0,1], [0,1])
    styles = dict(line.lineStyles)
    # 补充元组形式的说明
    return {
        'string_styles': styles,
        'tuple_formats': [
            {'value': (0, (5, 5)), 'desc': '等长虚线'},
            {'value': (0, (3, 1, 1, 1)), 'desc': '点划线'},
            {'value': (0, (1, 1)), 'desc': '细虚线'},
        ]
    }

@st.cache_data
def get_drawstyle_options():
    """获取 drawstyle 选项"""
    line = matplotlib.lines.Line2D([0,1], [0,1])
    return dict(line.drawStyles)

@st.cache_data
def get_capstyle_options():
    """获取 capstyle 选项"""
    return [e.value for e in matplotlib._enums.CapStyle]

@st.cache_data
def get_joinstyle_options():
    """获取 joinstyle 选项"""
    return [e.value for e in matplotlib._enums.JoinStyle]

def render_linestyle_gallery():
    """渲染 linestyle 全量画廊"""
    options = get_linestyle_options()
    x, y = np.linspace(0, 10, 100), np.sin(np.linspace(0, 10, 100))
    
    # 字符串样式
    string_styles = options['string_styles']
    n_strings = len(string_styles)
    
    # 创建画廊
    cols = 2
    rows = (n_strings + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(10, rows * 2))
    axes = axes.flatten() if rows > 1 else [axes] if cols == 1 else axes
    
    for idx, (name, _) in enumerate(string_styles.items()):
        if idx >= len(axes):
            break
        ax = axes[idx]
        ax.plot(x, y, linestyle=name, linewidth=2, label=f"'{name}'")
        ax.set_title(f"linestyle='{name}'", fontsize=9)
        ax.axis('off')
        ax.legend(loc='upper right', fontsize=7)
    
    # 隐藏多余的子图
    for idx in range(n_strings, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 显示代码表格
    st.markdown("### 合法值表格")
    import pandas as pd
    data = []
    for name, _ in string_styles.items():
        code = f"linestyle='{name}'"
        desc = {
            '-': '实线，最常用',
            '--': '虚线，用于区分数据系列',
            '-.': '点划线，强调趋势',
            ':': '点线，轻量级区分',
            'None': '无线条，仅显示标记点',
        }.get(name, '')
        data.append({
            '参数值': f"'{name}'",
            '最小代码': code,
            '说明': desc
        })
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 元组形式说明
    st.markdown("### 元组形式（自定义虚线）")
    st.info("""
    linestyle 还支持元组形式：`(offset, on-off-seq)`
    - `offset`: 虚线起始偏移量（点数）
    - `on-off-seq`: 点/空序列，如 `(5, 5)` 表示 5 点实线 + 5 点空白
    """)
    
    # 交互式自定义
    col1, col2 = st.columns(2)
    with col1:
        offset = st.number_input("Offset", min_value=0, max_value=20, value=0)
        dash_on = st.number_input("Dash On", min_value=1, max_value=20, value=5)
    with col2:
        dash_off = st.number_input("Dash Off", min_value=1, max_value=20, value=5)
    
    custom_ls = (offset, (dash_on, dash_off))
    fig_custom, ax_custom = plt.subplots(figsize=(8, 2))
    ax_custom.plot(x, y, linestyle=custom_ls, linewidth=2)
    ax_custom.set_title(f"linestyle={custom_ls}")
    st.pyplot(fig_custom)
    st.code(f"ax.plot(x, y, linestyle={custom_ls})", language='python')

def render_catalog_page(param_name: str):
    """根据参数名渲染对应的目录页面"""
    if param_name == 'linestyle':
        render_linestyle_gallery()
    # ... 其他参数
```

### 主应用集成（app.py 修改）

在现有章节 3 的 Tab1 中，添加"参数百科"选项：

```python
# 在章节 3 的 tab1 中
with tab1:
    view_mode = st.radio(
        "查看模式",
        ["交互式调整", "参数百科 (Catalog)"],
        horizontal=True
    )
    
    if view_mode == "参数百科 (Catalog)":
        from catalogs.line import render_catalog_page
        param_select = st.selectbox(
            "选择参数",
            ["linestyle", "linewidth", "drawstyle", "capstyle", "joinstyle"]
        )
        render_catalog_page(param_select)
    else:
        # 原有的交互式代码
        ...
```

---

## E. 内容模板（Catalog Page Template）

### 标准页面结构

```python
def render_catalog_template(param_name: str, param_info: Dict):
    """
    参数：
    - param_name: 参数名称（如 'linestyle'）
    - param_info: 包含以下键的字典：
        - title: 页面标题
        - description: 参数说明
        - valid_values: 合法值列表
        - examples: 示例代码列表
        - common_pitfalls: 常见坑列表
    """
    # 1. 标题
    st.title(f"{param_info['title']} ({param_name})")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    # 2. 参数说明
    st.markdown("### 📖 参数说明")
    st.info(param_info['description'])
    
    # 3. 合法值表格
    st.markdown("### 📋 合法值表格")
    # 渲染表格（包含预览图、参数值、代码、说明）
    
    # 4. 预览画廊
    st.markdown("### 🎨 预览画廊")
    render_gallery(param_name)
    
    # 5. 代码生成器
    st.markdown("### 💻 代码生成器")
    render_code_generator(param_name)
    
    # 6. 常见坑
    st.markdown("### ⚠️ 常见坑")
    for pitfall in param_info['common_pitfalls']:
        st.warning(pitfall)
```

### linestyle 完整示例模板

```python
LINESTYLE_TEMPLATE = {
    'title': '线型 (Linestyle)',
    'description': """
    **作用**：控制线条的样式（实线、虚线、点线等）
    
    **适用范围**：`ax.plot()`, `ax.scatter()`（当设置 linewidth 时）
    
    **默认值**：`'-'`（实线）
    
    **注意事项**：
    - 字符串形式：`'-'`, `'--'`, `'-.'`, `':'`, `'None'`, `' '`, `''`
    - 元组形式：`(offset, on-off-seq)` 用于自定义虚线样式
    - `'None'`, `' '`, `''` 都表示不绘制线条（仅显示标记点）
    """,
    'valid_values': [
        {
            'value': '-',
            'code': "ax.plot(x, y, linestyle='-')",
            'preview': '实线预览图',
            'desc': '实线，最常用，适合连续数据'
        },
        # ... 其他值
    ],
    'common_pitfalls': [
        "❌ 错误：`linestyle='dashed'` → ✅ 正确：`linestyle='--'`（注意是双短横线）",
        "❌ 元组形式必须两个元素：`(offset, sequence)`，sequence 必须是可迭代对象",
        "⚠️ 当 linewidth=0 时，linestyle 无效（线条不可见）"
    ]
}
```

---

## 实施优先级建议

1. **Phase 1（MVP）**：Line 类下的 `linestyle`（完整实现作为模板）
2. **Phase 2**：Line 类下的其他参数（`drawstyle`, `capstyle`, `joinstyle`）
3. **Phase 3**：Marker 类（`marker`, `fillstyle`）
4. **Phase 4**：Color 类（`color`, `cmap`）
5. **Phase 5**：Text / Axes / Figure 类

---

## 技术注意事项

1. **版本兼容性**：所有动态提取的选项都应显示 Matplotlib 版本号
2. **错误处理**：如果某个 API 调用失败，应回退到硬编码的已知选项列表
3. **性能优化**：大量预览图使用 `st.columns()` 网格布局，避免单列过长
4. **代码可复制性**：所有代码示例都使用 `st.code()` 并设置 `language='python'`
5. **响应式设计**：使用 `use_container_width=True` 确保表格和图表自适应

