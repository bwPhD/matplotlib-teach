"""
Figure（画布）相关参数的完整选项目录
"""
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from catalogs.utils import get_matplotlib_version, generate_sample_data, ensure_chinese_font

def render_figsize_gallery():
    """渲染 figsize 全量画廊"""
    ensure_chinese_font()
    st.title("画布尺寸 (Figsize) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：设置画布（Figure）的尺寸（宽度和高度）
    
    **适用范围**：`plt.figure()`, `plt.subplots()`, `fig.set_size_inches()`
    
    **格式**：`(width, height)` 元组，单位：英寸（inches）
    
    **默认值**：`(6.4, 4.8)` 英寸
    
    **常用尺寸**：
    - 小图：`(4, 3)`
    - 标准：`(6, 4)` 或 `(8, 6)`
    - 宽图：`(12, 4)`
    - 高图：`(6, 8)`
    """)
    
    x, y = generate_sample_data(50)
    
    # === 不同尺寸预览 ===
    st.markdown("### 🎨 不同尺寸预览")
    
    sizes = [
        ("小图 (4×3)", (4, 3)),
        ("标准 (6×4)", (6, 4)),
        ("标准 (8×6)", (8, 6)),
        ("宽图 (12×4)", (12, 4)),
        ("高图 (6×8)", (6, 8)),
        ("大图 (10×8)", (10, 8)),
    ]
    
    for title, size in sizes:
        st.markdown(f"#### {title}")
        fig, ax = plt.subplots(figsize=size)
        ax.plot(x, y, linewidth=2, color='#2c3e50')
        ax.set_title(f"figsize={size}", fontsize=10, fontweight='bold')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    # === 交互式预览 ===
    st.markdown("### 🎛️ 交互式尺寸设置")
    col1, col2 = st.columns(2)
    
    with col1:
        width = st.slider("宽度（英寸）", 2.0, 20.0, 8.0, 0.5, key='figsize_width')
    with col2:
        height = st.slider("高度（英寸）", 2.0, 20.0, 6.0, 0.5, key='figsize_height')
    
    fig_custom, ax_custom = plt.subplots(figsize=(width, height))
    ax_custom.plot(x, y, linewidth=2, color='#2c3e50')
    ax_custom.set_title(f"figsize=({width}, {height})", fontsize=11, fontweight='bold')
    ax_custom.grid(True, alpha=0.3)
    st.pyplot(fig_custom)
    
    st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)
y = np.sin(x)

fig, ax = plt.subplots(figsize=({width}, {height}))
ax.plot(x, y, linewidth=2)
ax.set_title("Figure Size Example")
ax.grid(True, alpha=0.3)
plt.show()
    """, language='python')
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **单位**：figsize 的单位是英寸（inches），不是像素
    
    2. **DPI 影响**：实际像素尺寸 = figsize × dpi
    
    3. **宽高比**：注意保持合适的宽高比，避免图形变形
    
    4. **显示大小**：在 Jupyter 中，图形会自动缩放以适应显示区域
    """)

def render_dpi_gallery():
    """渲染 dpi 全量画廊"""
    ensure_chinese_font()
    st.title("分辨率 (DPI) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：设置画布的分辨率（每英寸点数）
    
    **适用范围**：`plt.figure()`, `fig.savefig()`
    
    **默认值**：`100` DPI（显示）或 `'figure'`（保存）
    
    **常用值**：
    - 屏幕显示：`72` - `100` DPI
    - 打印质量：`300` DPI
    - 高质量：`600` DPI
    
    **注意**：DPI 影响保存图像的质量，不影响屏幕显示大小
    """)
    
    x, y = generate_sample_data(50)
    
    # === 不同 DPI 说明 ===
    st.markdown("### 📊 DPI 说明")
    
    dpi_info = [
        ("72 DPI", "屏幕显示（低质量）"),
        ("100 DPI", "默认显示质量"),
        ("150 DPI", "中等质量"),
        ("300 DPI", "打印质量（推荐）"),
        ("600 DPI", "高质量打印"),
    ]
    
    table_data = []
    for dpi_val, desc in dpi_info:
        table_data.append({
            'DPI 值': dpi_val,
            '说明': desc,
            '代码': f"dpi={dpi_val.split()[0]}"
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **显示 vs 保存**：DPI 主要影响保存图像的质量，屏幕显示通常使用默认值
    
    2. **文件大小**：DPI 越高，保存的文件越大
    
    3. **保存时设置**：可以在 `fig.savefig()` 时单独设置 DPI：`fig.savefig('file.png', dpi=300)`
    """)

def render_facecolor_gallery():
    """渲染 facecolor/edgecolor 全量画廊"""
    ensure_chinese_font()
    st.title("画布颜色 (Facecolor/Edgecolor) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：设置画布的背景颜色和边框颜色
    
    **适用范围**：`plt.figure()`, `fig.set_facecolor()`, `fig.set_edgecolor()`
    
    **默认值**：`'white'`（背景），`'black'`（边框）
    
    **支持形式**：与 `color` 参数相同（颜色名称、HEX、RGB 等）
    """)
    
    x, y = generate_sample_data(50)
    
    # === 不同颜色预览 ===
    st.markdown("### 🎨 不同背景颜色预览")
    
    colors = [
        ("白色（默认）", 'white'),
        ("浅灰色", 'lightgray'),
        ("黑色", 'black'),
        ("浅蓝色", 'lightblue'),
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()
    
    for idx, (title, color_val) in enumerate(colors):
        ax = axes[idx]
        fig_temp = ax.figure
        fig_temp.set_facecolor(color_val)
        ax.plot(x, y, linewidth=2, color='#2c3e50')
        ax.set_title(f"facecolor='{color_val}'", fontsize=10, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.code("""
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))
fig.set_facecolor('lightgray')  # 设置背景颜色
fig.set_edgecolor('blue')      # 设置边框颜色
ax.plot([1, 2, 3], [1, 2, 3])
plt.show()
    """, language='python')
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **保存时显示**：facecolor 在保存图像时会显示，但在某些显示环境中可能不可见
    
    2. **透明度**：可以使用 RGBA 格式设置半透明背景
    
    3. **全局设置**：可以通过 `plt.rcParams['figure.facecolor']` 设置全局默认背景色
    """)

def render_catalog_page(param_name: str):
    """根据参数名渲染对应的目录页面"""
    if param_name == 'figsize':
        render_figsize_gallery()
    elif param_name == 'dpi':
        render_dpi_gallery()
    elif param_name == 'facecolor' or param_name == 'edgecolor':
        render_facecolor_gallery()
    else:
        st.error(f"参数 '{param_name}' 的目录页面尚未实现")

