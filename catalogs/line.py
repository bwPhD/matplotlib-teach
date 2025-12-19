"""
Line（线条）相关参数的完整选项目录
"""
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.lines
import matplotlib._enums
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from catalogs.utils import get_matplotlib_version, generate_sample_data, generate_sample_data_steps, ensure_chinese_font

@st.cache_data
def get_linestyle_options() -> Dict:
    """获取所有 linestyle 选项"""
    line = matplotlib.lines.Line2D([0,1], [0,1])
    styles = dict(line.lineStyles)
    return {
        'string_styles': styles,
        'tuple_formats': [
            # 基础虚线样式
            {'value': (0, (1, 1)), 'desc': '细虚线（1点实线+1点空白）'},
            {'value': (0, (3, 1)), 'desc': '短虚线（3点实线+1点空白）'},
            {'value': (0, (5, 5)), 'desc': '等长虚线（5点实线+5点空白）'},
            {'value': (0, (10, 3)), 'desc': '长虚线（10点实线+3点空白）'},
            {'value': (0, (1, 3)), 'desc': '稀疏虚线（1点实线+3点空白）'},
            {'value': (0, (8, 2)), 'desc': '粗虚线（8点实线+2点空白）'},
            # 点划线样式
            {'value': (0, (3, 1, 1, 1)), 'desc': '点划线（3点实线+1点空白+1点实线+1点空白）'},
            {'value': (0, (5, 2, 1, 2)), 'desc': '长点划线（5点实线+2点空白+1点实线+2点空白）'},
            {'value': (0, (8, 2, 2, 2)), 'desc': '粗点划线（8点实线+2点空白+2点实线+2点空白）'},
            # 复杂模式
            {'value': (0, (10, 2, 2, 2, 2, 2)), 'desc': '长-短-短模式（10点实线+2点空白+2点实线+2点空白+2点实线+2点空白）'},
            {'value': (0, (1, 1, 3, 1)), 'desc': '点-点-长模式（1点实线+1点空白+3点实线+1点空白）'},
            # 带偏移的样式（展示 offset 参数的作用）
            {'value': (5, (5, 5)), 'desc': '带偏移虚线（偏移5点，5点实线+5点空白）'},
        ]
    }

@st.cache_data
def get_drawstyle_options() -> Dict:
    """获取 drawstyle 选项"""
    line = matplotlib.lines.Line2D([0,1], [0,1])
    return dict(line.drawStyles)

@st.cache_data
def get_capstyle_options() -> List[str]:
    """获取 capstyle 选项"""
    return [e.value for e in matplotlib._enums.CapStyle]

@st.cache_data
def get_joinstyle_options() -> List[str]:
    """获取 joinstyle 选项"""
    return [e.value for e in matplotlib._enums.JoinStyle]

def render_linestyle_gallery():
    """渲染 linestyle 全量画廊"""
    ensure_chinese_font()
    st.title("线型 (Linestyle) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    # 参数说明
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制线条的样式（实线、虚线、点线等）
    
    **适用范围**：`ax.plot()`, `Line2D` 对象
    
    **默认值**：`'-'`（实线）
    
    **支持形式**：
    - 字符串：`'-'`, `'--'`, `'-.'`, `':'`, `'None'`, `' '`, `''`
    - 元组：`(offset, on-off-seq)` 用于自定义虚线样式
    """)
    
    options = get_linestyle_options()
    x, y = generate_sample_data(100)
    
    # === 字符串样式预览 ===
    st.markdown("### 🎨 字符串样式预览")
    string_styles = options['string_styles']
    
    # 创建画廊（2列布局）
    n_strings = len(string_styles)
    cols = 2
    rows = (n_strings + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(12, rows * 2.5))
    if rows == 1:
        axes = axes if isinstance(axes, np.ndarray) else [axes]
    else:
        axes = axes.flatten()
    
    style_descriptions = {
        '-': '实线，最常用，适合连续数据',
        '--': '虚线，用于区分数据系列',
        '-.': '点划线，强调趋势',
        ':': '点线，轻量级区分',
        'None': '无线条，仅显示标记点',
        ' ': '无线条（空格）',
        '': '无线条（空字符串）',
    }
    
    for idx, (name, _) in enumerate(string_styles.items()):
        if idx >= len(axes):
            break
        ax = axes[idx]
        ax.plot(x, y, linestyle=name, linewidth=2.5, label=f"'{name}'")
        ax.set_title(f"linestyle='{name}'", fontsize=11, fontweight='bold')
        ax.set_xlim(0, 10)
        ax.set_ylim(-1.2, 1.2)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right', fontsize=9)
    
    # 隐藏多余的子图
    for idx in range(n_strings, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # === 合法值表格 ===
    st.markdown("### 📋 合法值表格")
    table_data = []
    for name, _ in string_styles.items():
        code = f"linestyle='{name}'"
        desc = style_descriptions.get(name, '')
        table_data.append({
            '参数值': f"'{name}'",
            '最小代码': code,
            '说明': desc
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # === 元组形式说明 ===
    st.markdown("### 🔧 元组形式（自定义虚线）")
    st.info("""
    linestyle 还支持元组形式：`(offset, on-off-seq)`
    - **offset**: 虚线起始偏移量（点数），通常为 0
    - **on-off-seq**: 点/空序列，如 `(5, 5)` 表示 5 点实线 + 5 点空白，循环重复
    - 示例：`(0, (3, 1, 1, 1))` 表示 3点实线+1点空白+1点实线+1点空白，循环
    """)
    
    # 预设元组样式
    st.markdown("#### 预设元组样式")
    tuple_formats = options['tuple_formats']
    n_tuples = len(tuple_formats)
    
    # 使用多行布局，每行显示3个，避免过于拥挤
    cols_per_row = 3
    rows = (n_tuples + cols_per_row - 1) // cols_per_row
    
    fig2, axes2 = plt.subplots(rows, cols_per_row, figsize=(4*cols_per_row, 2.5*rows))
    if rows == 1:
        axes2 = axes2 if isinstance(axes2, np.ndarray) else [axes2]
    else:
        axes2 = axes2.flatten()
    
    for idx, fmt in enumerate(tuple_formats):
        if idx >= len(axes2):
            break
        ax = axes2[idx]
        ls_val = fmt['value']
        ax.plot(x, y, linestyle=ls_val, linewidth=2.5)
        ax.set_title(f"{ls_val}\n{fmt['desc']}", fontsize=9)
        ax.set_xlim(0, 10)
        ax.set_ylim(-1.2, 1.2)
        ax.grid(True, alpha=0.3)
    
    # 隐藏多余的子图
    for idx in range(n_tuples, len(axes2)):
        axes2[idx].axis('off')
    
    plt.tight_layout()
    st.pyplot(fig2)
    
    # === 交互式自定义 ===
    st.markdown("#### 🎛️ 交互式自定义虚线")
    col1, col2, col3 = st.columns(3)
    with col1:
        offset = st.number_input("Offset（偏移）", min_value=0, max_value=20, value=0, key='ls_offset')
    with col2:
        dash_on = st.number_input("Dash On（实线长度）", min_value=1, max_value=20, value=5, key='ls_on')
    with col3:
        dash_off = st.number_input("Dash Off（空白长度）", min_value=1, max_value=20, value=5, key='ls_off')
    
    custom_ls = (offset, (dash_on, dash_off))
    fig_custom, ax_custom = plt.subplots(figsize=(10, 3))
    ax_custom.plot(x, y, linestyle=custom_ls, linewidth=2.5, color='#2c3e50')
    ax_custom.set_title(f"linestyle={custom_ls}", fontsize=11, fontweight='bold')
    ax_custom.set_xlim(0, 10)
    ax_custom.set_ylim(-1.2, 1.2)
    ax_custom.grid(True, alpha=0.3)
    st.pyplot(fig_custom)
    
    st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, linestyle={custom_ls}, linewidth=2.5)
ax.set_title("Custom Dashed Line")
plt.show()
    """, language='python')
    
    # === 常见坑 ===
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **错误写法**：`linestyle='dashed'` → ✅ **正确**：`linestyle='--'`（注意是双短横线，不是单词）
    
    2. **元组格式**：必须包含两个元素 `(offset, sequence)`，sequence 必须是可迭代对象（列表或元组）
       - ❌ 错误：`linestyle=(5, 5)` → ✅ 正确：`linestyle=(0, (5, 5))`
    
    3. **空值等价**：`'None'`, `' '`, `''` 都表示不绘制线条，但推荐使用 `'None'` 或 `None`
    
    4. **linewidth=0**：当 linewidth=0 时，linestyle 无效（线条不可见）
    
    5. **元组序列长度**：on-off-seq 可以是任意长度，如 `(0, (3, 1, 1, 1))` 会循环使用
    """)

def render_drawstyle_gallery():
    """渲染 drawstyle 全量画廊"""
    st.title("绘制样式 (Drawstyle) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制数据点的连接方式（线性插值 vs 阶梯式）
    
    **适用范围**：`ax.plot()`（主要用于时间序列数据）
    
    **默认值**：`'default'`（线性插值）
    
    **适用场景**：阶梯图常用于表示离散事件或累积值
    """)
    
    drawstyles = get_drawstyle_options()
    x, y = generate_sample_data_steps(15)  # 较少点数便于看清阶梯效果
    
    # 预览画廊
    n_styles = len(drawstyles)
    cols = 2
    rows = (n_styles + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(12, rows * 3))
    if rows == 1:
        axes = axes if isinstance(axes, np.ndarray) else [axes]
    else:
        axes = axes.flatten()
    
    descriptions = {
        'default': '线性插值，平滑连接所有点',
        'steps': '等同于 steps-pre，在点之前保持水平',
        'steps-pre': '在点之前保持水平（左对齐）',
        'steps-mid': '在点中间保持水平（居中对齐）',
        'steps-post': '在点之后保持水平（右对齐）',
    }
    
    for idx, (name, _) in enumerate(drawstyles.items()):
        if idx >= len(axes):
            break
        ax = axes[idx]
        ax.plot(x, y, drawstyle=name, linewidth=2, marker='o', markersize=6, label=f"'{name}'")
        ax.set_title(f"drawstyle='{name}'\n{descriptions.get(name, '')}", fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
    
    for idx in range(n_styles, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 代码表格
    st.markdown("### 📋 合法值表格")
    table_data = []
    for name, _ in drawstyles.items():
        code = f"drawstyle='{name}'"
        desc = descriptions.get(name, '')
        table_data.append({
            '参数值': f"'{name}'",
            '最小代码': code,
            '说明': desc
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **steps vs steps-pre**：`'steps'` 是 `'steps-pre'` 的别名，行为相同
    
    2. **数据点数量**：阶梯图在数据点较少时效果更明显，建议配合 `marker` 使用
    
    3. **适用场景**：主要用于时间序列、累积值、直方图边缘等场景
    """)

def render_capstyle_gallery():
    """渲染 capstyle 全量画廊"""
    st.title("线端样式 (Capstyle) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制线条端点的形状（仅对虚线有效，实线通常不可见）
    
    **适用范围**：`Line2D` 对象的 `solid_capstyle` 和 `dash_capstyle`
    
    **注意**：对于实线（solid line），capstyle 通常不可见，除非 linewidth 很大
    """)
    
    capstyles = get_capstyle_options()
    x = np.array([1, 9])
    y = np.array([0.5, 0.5])
    
    # 预览（使用较粗的虚线以便看清端点）
    fig, axes = plt.subplots(1, len(capstyles), figsize=(5*len(capstyles), 3))
    if len(capstyles) == 1:
        axes = [axes]
    
    descriptions = {
        'butt': '平头（默认），端点与坐标精确对齐',
        'round': '圆头，端点超出坐标半个线宽',
        'projecting': '方头，端点超出坐标半个线宽（类似 round 但方形）',
    }
    
    for idx, cs in enumerate(capstyles):
        ax = axes[idx]
        ax.plot(x, y, linestyle='--', linewidth=15, solid_capstyle=cs, 
                color='#2c3e50', label=f"'{cs}'")
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 1)
        ax.set_title(f"solid_capstyle='{cs}'\n{descriptions.get(cs, '')}", fontsize=10)
        ax.axis('off')
        # 添加参考线
        ax.axvline(x[0], color='red', linestyle=':', alpha=0.5, label='起点')
        ax.axvline(x[1], color='red', linestyle=':', alpha=0.5, label='终点')
        ax.legend(fontsize=8)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 代码表格
    st.markdown("### 📋 合法值表格")
    table_data = []
    for cs in capstyles:
        code = f"solid_capstyle='{cs}'"
        desc = descriptions.get(cs, '')
        table_data.append({
            '参数值': f"'{cs}'",
            '最小代码': code,
            '说明': desc
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **仅对粗线有效**：linewidth 较小时，capstyle 差异不明显
    
    2. **solid_capstyle vs dash_capstyle**：
       - `solid_capstyle`：控制实线部分的端点
       - `dash_capstyle`：控制虚线部分的端点（需要设置 `dashes`）
    
    3. **round vs projecting**：视觉差异很小，通常使用 `'butt'` 或 `'round'`
    """)

def render_joinstyle_gallery():
    """渲染 joinstyle 全量画廊"""
    st.title("连接样式 (Joinstyle) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制线条转折处的连接方式（仅对折线有效）
    
    **适用范围**：`Line2D` 对象的 `solid_joinstyle` 和 `dash_joinstyle`
    
    **注意**：需要至少 3 个点才能看到连接效果
    """)
    
    joinstyles = get_joinstyle_options()
    x = np.array([1, 5, 9])
    y = np.array([0.2, 0.8, 0.3])
    
    # 预览（使用较粗的线以便看清连接）
    fig, axes = plt.subplots(1, len(joinstyles), figsize=(5*len(joinstyles), 3))
    if len(joinstyles) == 1:
        axes = [axes]
    
    descriptions = {
        'miter': '尖角连接（默认），延伸至交点',
        'round': '圆角连接，平滑过渡',
        'bevel': '斜角连接，切掉尖角',
    }
    
    for idx, js in enumerate(joinstyles):
        ax = axes[idx]
        ax.plot(x, y, linewidth=15, solid_joinstyle=js, 
                color='#2c3e50', marker='o', markersize=10, label=f"'{js}'")
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 1)
        ax.set_title(f"solid_joinstyle='{js}'\n{descriptions.get(js, '')}", fontsize=10)
        ax.axis('off')
        ax.legend(fontsize=8)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 代码表格
    st.markdown("### 📋 合法值表格")
    table_data = []
    for js in joinstyles:
        code = f"solid_joinstyle='{js}'"
        desc = descriptions.get(js, '')
        table_data.append({
            '参数值': f"'{js}'",
            '最小代码': code,
            '说明': desc
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **需要折线**：只有折线（至少 3 个点）才能看到 joinstyle 效果
    
    2. **linewidth 影响**：linewidth 较小时，joinstyle 差异不明显
    
    3. **solid_joinstyle vs dash_joinstyle**：
       - `solid_joinstyle`：控制实线部分的连接
       - `dash_joinstyle`：控制虚线部分的连接（需要设置 `dashes`）
    """)

def render_catalog_page(param_name: str):
    """根据参数名渲染对应的目录页面"""
    if param_name == 'linestyle':
        render_linestyle_gallery()
    elif param_name == 'drawstyle':
        render_drawstyle_gallery()
    elif param_name == 'capstyle':
        render_capstyle_gallery()
    elif param_name == 'joinstyle':
        render_joinstyle_gallery()
    else:
        st.error(f"参数 '{param_name}' 的目录页面尚未实现")

