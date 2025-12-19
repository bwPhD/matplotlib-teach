"""
Text（文本）相关参数的完整选项目录
"""
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from catalogs.utils import get_matplotlib_version, generate_sample_data, ensure_chinese_font

@st.cache_data
def get_fontsize_options() -> Dict:
    """获取 fontsize 选项"""
    return {
        'numeric': {
            'range': (1, 100),
            'default': 10,
            'common': [6, 8, 10, 12, 14, 16, 18, 20, 24, 30]
        },
        'string': {
            'xx-small': 6,
            'x-small': 7.5,
            'small': 9,
            'medium': 10,
            'large': 12,
            'x-large': 13.5,
            'xx-large': 16,
            'smaller': 'relative',
            'larger': 'relative',
        }
    }

@st.cache_data
def get_fontweight_options() -> List[str]:
    """获取 fontweight 选项"""
    return ['normal', 'bold', 'heavy', 'light', 'medium', 'regular', 'semibold', 'demibold', 'ultrabold', 'black', '100', '200', '300', '400', '500', '600', '700', '800', '900']

@st.cache_data
def get_fontstyle_options() -> List[str]:
    """获取 fontstyle 选项"""
    return ['normal', 'italic', 'oblique']

@st.cache_data
def get_fontfamily_options() -> Dict:
    """获取 fontfamily 选项"""
    # 通用字体族
    generic_families = ['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy']
    
    # 获取系统可用字体（限制数量以避免过长）
    try:
        available_fonts = sorted(set([f.name for f in fm.fontManager.ttflist]))[:50]  # 限制50个
    except:
        available_fonts = []
    
    return {
        'generic': generic_families,
        'available': available_fonts
    }

def render_fontsize_gallery():
    """渲染 fontsize 全量画廊"""
    ensure_chinese_font()
    st.title("字体大小 (Fontsize) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制文本的字体大小
    
    **适用范围**：`ax.set_title()`, `ax.set_xlabel()`, `ax.text()`, `ax.annotate()` 等所有文本函数
    
    **默认值**：`10`（点）
    
    **支持形式**：
    - **数值**：`6`, `10`, `12`, `16` 等（单位：点 points）
    - **字符串**：`'xx-small'`, `'small'`, `'medium'`, `'large'`, `'x-large'`, `'xx-large'`
    - **相对大小**：`'smaller'`, `'larger'`（相对于当前大小）
    """)
    
    options = get_fontsize_options()
    x, y = generate_sample_data(50)
    
    # === 数值大小预览 ===
    st.markdown("### 🎨 数值大小预览")
    common_sizes = options['numeric']['common']
    
    fig1, axes1 = plt.subplots(len(common_sizes), 1, figsize=(10, 1.5*len(common_sizes)))
    if len(common_sizes) == 1:
        axes1 = [axes1]
    
    for idx, size in enumerate(common_sizes):
        ax = axes1[idx]
        ax.plot(x, y, linewidth=2, color='#2c3e50')
        ax.set_title(f"Fontsize = {size}", fontsize=size, fontweight='bold')
        ax.text(5, 0, f"fontsize={size}", fontsize=size, ha='center')
        ax.set_xlim(0, 10)
        ax.set_ylim(-1.5, 1.5)
        ax.axis('off')
    
    plt.tight_layout()
    st.pyplot(fig1)
    
    # === 字符串大小预览 ===
    st.markdown("### 🎨 字符串大小预览")
    string_sizes = {k: v for k, v in options['string'].items() if isinstance(v, (int, float))}
    
    fig2, axes2 = plt.subplots(len(string_sizes), 1, figsize=(10, 1.5*len(string_sizes)))
    if len(string_sizes) == 1:
        axes2 = [axes2]
    
    for idx, (size_name, size_val) in enumerate(string_sizes.items()):
        ax = axes2[idx]
        ax.plot(x, y, linewidth=2, color='#2c3e50')
        ax.set_title(f"Fontsize = '{size_name}' ({size_val}pt)", fontsize=size_val, fontweight='bold')
        ax.text(5, 0, f"fontsize='{size_name}'", fontsize=size_val, ha='center')
        ax.set_xlim(0, 10)
        ax.set_ylim(-1.5, 1.5)
        ax.axis('off')
    
    plt.tight_layout()
    st.pyplot(fig2)
    
    # === 合法值表格 ===
    st.markdown("### 📋 合法值表格")
    table_data = []
    for size in common_sizes:
        table_data.append({
            '参数值': str(size),
            '类型': '数值',
            '最小代码': f"fontsize={size}",
            '说明': f'{size} 点（points）'
        })
    for size_name, size_val in string_sizes.items():
        table_data.append({
            '参数值': f"'{size_name}'",
            '类型': '字符串',
            '最小代码': f"fontsize='{size_name}'",
            '说明': f'{size_val} 点（points）'
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # === 交互式预览 ===
    st.markdown("### 🎛️ 交互式字体大小预览")
    col1, col2 = st.columns(2)
    
    with col1:
        size_type = st.radio("大小类型", ["数值", "字符串"], key='fontsize_type')
    
    with col2:
        if size_type == "数值":
            fontsize_value = st.slider("字体大小", 6, 30, 12, key='fontsize_numeric')
        else:
            fontsize_value = st.selectbox("字体大小", list(string_sizes.keys()), key='fontsize_string')
    
    fig_custom, ax_custom = plt.subplots(figsize=(10, 4))
    x_custom, y_custom = generate_sample_data(50)
    ax_custom.plot(x_custom, y_custom, linewidth=2, color='#2c3e50')
    ax_custom.set_title(f"Title with fontsize={fontsize_value}", fontsize=fontsize_value, fontweight='bold')
    ax_custom.set_xlabel(f"X Label with fontsize={fontsize_value}", fontsize=fontsize_value)
    ax_custom.set_ylabel(f"Y Label with fontsize={fontsize_value}", fontsize=fontsize_value)
    ax_custom.text(5, 0, f"Text with fontsize={fontsize_value}", fontsize=fontsize_value, ha='center')
    ax_custom.grid(True, alpha=0.3)
    st.pyplot(fig_custom)
    
    size_code = str(fontsize_value) if size_type == "数值" else f"'{fontsize_value}'"
    st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, linewidth=2)
ax.set_title("Title", fontsize={size_code})
ax.set_xlabel("X Label", fontsize={size_code})
ax.set_ylabel("Y Label", fontsize={size_code})
plt.show()
    """, language='python')
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **单位**：fontsize 的单位是"点"（points），1 point ≈ 1/72 英寸
    
    2. **相对大小**：`'smaller'` 和 `'larger'` 是相对于当前字体大小的，不是绝对值
    
    3. **全局设置**：可以通过 `plt.rcParams['font.size']` 设置全局默认字体大小
    
    4. **不同元素**：title、label、tick label 可以分别设置不同的字体大小
    """)

def render_fontweight_gallery():
    """渲染 fontweight 全量画廊"""
    ensure_chinese_font()
    st.title("字体粗细 (Fontweight) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制文本的字体粗细
    
    **适用范围**：所有文本函数
    
    **默认值**：`'normal'`（400）
    
    **支持形式**：
    - **字符串**：`'normal'`, `'bold'`, `'light'`, `'medium'`, `'heavy'` 等
    - **数值**：`100`, `200`, ..., `900`（100的倍数）
    """)
    
    fontweights = get_fontweight_options()
    
    # 常用 fontweight
    common_weights = ['normal', 'bold', 'light', 'medium', 'heavy', '100', '400', '700', '900']
    
    fig, axes = plt.subplots(len(common_weights), 1, figsize=(10, 1.5*len(common_weights)))
    if len(common_weights) == 1:
        axes = [axes]
    
    for idx, weight in enumerate(common_weights):
        ax = axes[idx]
        ax.text(0.5, 0.5, f"Fontweight = '{weight}'", fontsize=16, fontweight=weight, 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 表格
    st.markdown("### 📋 合法值表格")
    table_data = []
    for weight in common_weights:
        table_data.append({
            '参数值': f"'{weight}'",
            '最小代码': f"fontweight='{weight}'",
            '说明': '粗体' if weight in ['bold', '700', '800', '900'] else '正常' if weight in ['normal', '400'] else '细体'
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **数值范围**：数值必须是 100 的倍数，范围 100-900
    
    2. **字体支持**：不是所有字体都支持所有粗细级别，取决于字体文件
    
    3. **等价性**：`'normal'` ≈ `'400'`, `'bold'` ≈ `'700'`
    """)

def render_fontstyle_gallery():
    """渲染 fontstyle 全量画廊"""
    ensure_chinese_font()
    st.title("字体样式 (Fontstyle) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制文本的字体样式（正常/斜体）
    
    **默认值**：`'normal'`
    
    **合法值**：`'normal'`, `'italic'`, `'oblique'`
    """)
    
    fontstyles = get_fontstyle_options()
    
    fig, axes = plt.subplots(len(fontstyles), 1, figsize=(10, 3*len(fontstyles)))
    if len(fontstyles) == 1:
        axes = [axes]
    
    for idx, style in enumerate(fontstyles):
        ax = axes[idx]
        ax.text(0.5, 0.5, f"Fontstyle = '{style}'", fontsize=20, fontstyle=style,
               ha='center', va='center', transform=ax.transAxes)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **italic vs oblique**：`'italic'` 是真正的斜体，`'oblique'` 是倾斜的正常字体
    
    2. **字体支持**：不是所有字体都有斜体版本
    """)

def render_fontfamily_gallery():
    """渲染 fontfamily 全量画廊"""
    ensure_chinese_font()
    st.title("字体族 (Fontfamily) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制文本的字体族
    
    **默认值**：`'sans-serif'`
    
    **支持形式**：
    - **通用字体族**：`'serif'`, `'sans-serif'`, `'monospace'`, `'cursive'`, `'fantasy'`
    - **具体字体名**：`'Arial'`, `'Times New Roman'`, `'Courier New'` 等
    """)
    
    options = get_fontfamily_options()
    
    # 通用字体族预览
    st.markdown("### 🎨 通用字体族预览")
    fig, axes = plt.subplots(len(options['generic']), 1, figsize=(10, 2*len(options['generic'])))
    if len(options['generic']) == 1:
        axes = [axes]
    
    for idx, family in enumerate(options['generic']):
        ax = axes[idx]
        ax.text(0.5, 0.5, f"Fontfamily = '{family}'", fontsize=18, fontfamily=family,
               ha='center', va='center', transform=ax.transAxes)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 可用字体列表（部分）
    if options['available']:
        st.markdown("### 📋 系统可用字体（部分）")
        st.info(f"系统检测到 {len(options['available'])} 个可用字体（仅显示前50个）")
        df = pd.DataFrame({'字体名称': options['available']})
        st.dataframe(df, use_container_width=True, hide_index=True, height=300)
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **字体可用性**：具体字体名可能在不同系统上不可用，建议使用通用字体族
    
    2. **字体回退**：如果指定字体不可用，Matplotlib 会使用默认字体
    
    3. **全局设置**：可以通过 `plt.rcParams['font.family']` 设置全局默认字体
    """)

def render_catalog_page(param_name: str):
    """根据参数名渲染对应的目录页面"""
    if param_name == 'fontsize':
        render_fontsize_gallery()
    elif param_name == 'fontweight':
        render_fontweight_gallery()
    elif param_name == 'fontstyle':
        render_fontstyle_gallery()
    elif param_name == 'fontfamily':
        render_fontfamily_gallery()
    else:
        st.error(f"参数 '{param_name}' 的目录页面尚未实现")

