import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import altair as alt
from mpl_toolkits.mplot3d import Axes3D

# --- 配置中文字体（必须在导入后立即设置）---
from catalogs.utils import setup_chinese_font, generate_sample_data
setup_chinese_font()

# --- 页面配置 ---
st.set_page_config(page_title="计算社会学可视化教学", layout="wide", page_icon="🎨")

# --- 全局样式优化 ---
st.markdown("""
<style>
    /* ========== 全局字体和基础样式 ========== */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
    }
    
    /* ========== 主内容区域 ========== */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* ========== 标题样式 ========== */
    h1 {
        color: #1f2937;
        font-weight: 700;
        margin-bottom: 1rem;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
    }
    
    h2 {
        color: #374151;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #4b5563;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    h4 {
        color: #6b7280;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* ========== 代码块样式 ========== */
    code {
        font-size: 15px !important;
        font-family: 'Consolas', 'Courier New', 'Monaco', 'Menlo', monospace !important;
        background-color: #f3f4f6 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        color: #dc2626 !important;
    }
    
    pre {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        overflow-x: auto !important;
    }
    
    pre code {
        background-color: transparent !important;
        color: #e2e8f0 !important;
        font-size: 14px !important;
        padding: 0 !important;
    }
    
    /* ========== 侧边栏样式 ========== */
    section[data-testid="stSidebar"] {
        background-color: #f9fafb;
        border-right: 1px solid #e5e7eb;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h1 {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #1f2937 !important;
        border-bottom: 2px solid #3b82f6 !important;
        padding-bottom: 0.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 14px;
        padding: 0.5rem 0;
    }
    
    /* ========== 信息框样式 ========== */
    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid;
    }
    
    .stInfo {
        background-color: #eff6ff;
        border-left-color: #3b82f6;
    }
    
    .stSuccess {
        background-color: #f0fdf4;
        border-left-color: #22c55e;
    }
    
    .stWarning {
        background-color: #fffbeb;
        border-left-color: #f59e0b;
    }
    
    .stError {
        background-color: #fef2f2;
        border-left-color: #ef4444;
    }
    
    /* ========== 按钮样式 ========== */
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #2563eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* ========== 输入框和选择器样式 ========== */
    .stSelectbox, .stSlider, .stNumberInput {
        margin-bottom: 1rem;
    }
    
    /* ========== Tab 样式 ========== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    /* ========== 表格样式 ========== */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* ========== 图表容器 ========== */
    .stPlotlyChart, [data-testid="stPyplot"] {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* ========== 分隔线 ========== */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #e5e7eb;
    }
    
    /* ========== 间距优化 ========== */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* ========== 响应式优化 ========== */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        h1 {
            font-size: 1.75rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
    }
    
    /* ========== 滚动条样式 ========== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* ========== 隐藏 Streamlit 底部标识 ========== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* 隐藏 "Built with Streamlit" 文本 */
    footer:after {
        content: '';
        visibility: hidden;
    }
    /* 更彻底地隐藏页脚 */
    .stApp > footer {
        visibility: hidden;
        height: 0;
        position: fixed;
        bottom: 0;
    }
    /* 隐藏包含 "Built with Streamlit" 的元素 */
    [data-testid="stAppViewContainer"] > footer {
        visibility: hidden;
        height: 0;
    }
    
    /* ========== 隐藏 Streamlit 顶部菜单栏 ========== */
    /* 隐藏顶部工具栏 */
    [data-testid="stHeader"] {
        visibility: hidden;
        height: 0;
    }
    /* 隐藏顶部工具栏容器 */
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0;
    }
    /* 隐藏右上角菜单按钮 */
    [data-testid="stToolbar"] {
        visibility: hidden;
        height: 0;
    }
    /* 隐藏 Share 按钮和所有工具栏按钮 */
    button[kind="header"] {
        visibility: hidden;
        display: none;
    }
    /* 隐藏顶部所有按钮 */
    .stApp header button {
        visibility: hidden;
        display: none;
    }
    /* 隐藏顶部工具栏区域 */
    .stApp > header {
        visibility: hidden;
        height: 0;
    }
    /* 更彻底地隐藏整个顶部区域 */
    [data-testid="stHeader"] > div {
        visibility: hidden;
        height: 0;
    }
</style>
""", unsafe_allow_html=True)

# --- 侧边栏导航 ---
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem 0;'>
    <h1 style='margin: 0; color: #1f2937;'>计算社会学课程网络实验室</h1>
    <p style='color: #6b7280; font-size: 0.9rem; margin-top: 0.5rem;'>东南大学汪斌</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "课程章节",
    [
        "1. 生态全景",
        "2. Matplotlib 核心解构",
        "3. 基础笔触",
        "4. 布局与美学",
        "5. 进阶画廊",
        "6. 其他库实战",
        "7. 进阶挑战：大师之路 🚀"
    ]
)

# --- 辅助函数：生成数据 ---
@st.cache_data
def get_random_data(points=100):
    return pd.DataFrame({
        'x': np.random.randn(points),
        'y': np.random.randn(points),
        'category': np.random.choice(['A', 'B', 'C'], points),
        'value': np.random.rand(points) * 100
    })

# --- 章节 1: 生态全景 ---
if menu == "1. 生态全景":
    st.title("Python 数据可视化生态全景")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0;'>
        <h3 style='color: white; margin: 0;'>"到底该用哪个库？"</h3>
        <p style='margin: 0.5rem 0 0 0; opacity: 0.95;'>从小白到专家的第一步</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 使用Tabs组织不同类别的库
    lib_tabs = st.tabs(["🎯 核心库", "📊 统计库", "🌐 Web库", "🔧 工具库"])
    
    with lib_tabs[0]:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🛠️ Matplotlib: 基石与控制")
            st.info("""
            **核心特征：Control (控制)**
            
            Python可视化的底层引擎。只要你肯花时间，几乎可以实现任何效果。
            
            **适用场景**：
            - 出版级绘图
            - 科学论文图表
            - 高度定制化需求
            
            **优势**：完全控制，功能强大
            **劣势**：学习曲线陡峭
            """)
            
            st.subheader("📈 Pandas Plotting: 数据驱动")
            st.success("""
            **核心特征：Integration (集成)**
            
            Pandas内置的绘图接口，基于Matplotlib。
            
            **适用场景**：
            - DataFrame/Series快速可视化
            - 数据探索
            - 与Pandas无缝集成
            """)

        with col2:
            st.subheader("💅 Seaborn: 统计之美")
            st.success("""
            **核心特征：Beauty (美观)**
            
            基于Matplotlib的高级封装。适合快速探索性数据分析(EDA)。
            
            **适用场景**：
            - 统计图表
            - 数据探索
            - 美观的默认样式
            
            **优势**：美观，统计功能丰富
            **劣势**：定制化程度不如Matplotlib
            """)
    
    with lib_tabs[1]:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📊 Plotnine: ggplot2风格")
            st.info("""
            **核心特征：Grammar (语法)**
            
            Python版本的ggplot2，使用图形语法。
            
            **适用场景**：
            - R用户转Python
            - 复杂数据可视化
            - 统计图形
            
            **语法示例**：
            ```python
            (ggplot(data) + 
             aes(x='x', y='y') + 
             geom_point())
            ```
            """)
        
        with col2:
            st.subheader("📉 Bokeh: 交互式可视化")
            st.warning("""
            **核心特征：Interaction (交互)**
            
            专为Web设计的交互式可视化库。
            
            **适用场景**：
            - Web应用
            - 仪表盘
            - 实时数据可视化
            
            **优势**：强大的交互能力
            **劣势**：学习曲线较陡
            """)
    
    with lib_tabs[2]:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🖱️ Plotly: 交互为王")
            st.warning("""
            **核心特征：Interaction (交互)**
            
            独立的库，专为Web设计。支持悬停、缩放、平移等交互。
            
            **适用场景**：
            - 仪表盘
            - 网页报告
            - 交互式探索
            
            **优势**：丰富的交互功能
            **劣势**：文件较大
            """)
            
            st.subheader("📜 Altair: 声明式语法")
            st.error("""
            **核心特征：Grammar (语法)**
            
            描述"通过什么数据映射到什么视觉元素"。
            
            **适用场景**：
            - 快速构建图表逻辑
            - 数据探索
            - 简洁的代码
            
            **优势**：代码极简，逻辑清晰
            **劣势**：复杂图表可能受限
            """)
        
        with col2:
            st.subheader("🌐 Dash: Web应用框架")
            st.info("""
            **核心特征：Application (应用)**
            
            基于Plotly的Web应用框架。
            
            **适用场景**：
            - 数据仪表盘
            - 交互式Web应用
            - 实时数据展示
            
            **优势**：纯Python构建Web应用
            """)
    
    with lib_tabs[3]:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎨 Style库")
            st.info("""
            **matplotlib-stylelib**: 扩展样式库
            
            **prettyplotlib**: 美化Matplotlib图表
            
            **seaborn-style**: Seaborn样式扩展
            """)
        
        with col2:
            st.subheader("📦 其他工具")
            st.info("""
            **mplfinance**: 金融图表专用
            
            **cartopy**: 地理数据可视化
            
            **basemap**: 地图绘制（已弃用，推荐cartopy）
            """)

    st.markdown("---")
    st.markdown("""
    <div style='padding: 1rem; background-color: #f9fafb; border-radius: 8px; border-left: 4px solid #3b82f6;'>
        <h4 style='margin: 0 0 0.5rem 0; color: #1f2937;'>🎯 学习重点</h4>
        <p style='margin: 0; color: #4b5563;'>我们重点关注 <strong>Matplotlib</strong>，它是Python所有可视化的基础。</p>
    </div>
    """, unsafe_allow_html=True)

# --- 章节 2: Matplotlib 核心解构 ---
elif menu == "2. Matplotlib 核心解构":
    st.title("Matplotlib 从零到精通")
    
    st.markdown("### 1. 两种创作风格：Pyplot vs 面向对象 (OO)")
    st.markdown("""
    <div style='background-color: #eff6ff; padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6; margin: 1rem 0;'>
        <strong>💡 推荐使用面向对象（OO）模式</strong>，实现对图表的完全掌控。
    </div>
    """, unsafe_allow_html=True)
    
    col_demo, col_code = st.columns([1, 1])
    
    style_choice = st.radio("选择代码风格进行对比：", ["Pyplot (快捷模式)", "OO (面向对象模式 - 推荐)"], horizontal=True)
    
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    # 预先定义代码字符串，方便展示
    code_pyplot = """
plt.figure(figsize=(6, 4))
plt.plot(x, y, label='Sine Wave', color='blue')
plt.title("Pyplot Style")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.legend()
plt.grid(True)
"""
    code_oo = """
# 1. 创建 Figure 和 Axes (画布与坐标系)
fig, ax = plt.subplots(figsize=(6, 4))

# 2. 在 ax 对象上调用方法 (set_title, set_xlabel...)
ax.plot(x, y, label='Sine Wave', color='green')
ax.set_title("OO Style (Recommended)")
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.legend()
ax.grid(True)
"""

    with col_demo:
        if style_choice == "Pyplot (快捷模式)":
            fig = plt.figure(figsize=(6, 4))
            plt.plot(x, y, label='Sine Wave', color='blue')
            plt.title("Pyplot Style")
            plt.xlabel("X Axis")
            plt.ylabel("Y Axis")
            plt.legend()
            plt.grid(True)
        else:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(x, y, label='Sine Wave', color='green')
            ax.set_title("OO Style (Recommended)")
            ax.set_xlabel("X Axis")
            ax.set_ylabel("Y Axis")
            ax.legend()
            ax.grid(True)
        st.pyplot(fig)

    with col_code:
        st.markdown("#### 对应代码")
        st.code(code_pyplot if style_choice == "Pyplot (快捷模式)" else code_oo, language='python')
        
    st.markdown("---")
    st.markdown("### 2. 解构画布：Figure vs Axes vs Artist")
    
    # 使用Tabs组织内容
    core_tabs = st.tabs(["📐 核心概念", "🎨 Artist层级", "📊 坐标轴类型", "⚙️ 后端系统"])
    
    with core_tabs[0]:
        st.markdown("""
        <div style='background-color: #f0fdf4; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #22c55e;'>
            <ul style='margin: 0; padding-left: 1.5rem; color: #166534;'>
                <li style='margin-bottom: 0.5rem;'><strong>Figure (画布)</strong>: 整个图像的容器，可以包含多个子图。</li>
                <li style='margin-bottom: 0.5rem;'><strong>Axes (坐标系)</strong>: 实际绘图的区域（包含坐标轴、线条、标签等）。</li>
                <li style='margin-bottom: 0.5rem;'><strong>Axis (坐标轴)</strong>: 处理刻度和范围。</li>
                <li style='margin-bottom: 0;'><strong>Artist</strong>: 既然可见，皆为 Artist。</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # 可视化层级结构
        fig_hierarchy, ax_hierarchy = plt.subplots(figsize=(10, 6))
        ax_hierarchy.axis('off')
        
        # 绘制层级结构图
        hierarchy_text = """
        Figure (画布)
        └── Axes (坐标系)
            ├── Axis (X轴)
            ├── Axis (Y轴)
            ├── Line2D (线条)
            ├── Text (文本)
            ├── Patches (形状)
            └── Collections (集合)
        """
        ax_hierarchy.text(0.1, 0.5, hierarchy_text, fontsize=14, family='monospace',
                         verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax_hierarchy.set_title("Matplotlib 对象层级结构", fontsize=16, fontweight='bold', pad=20)
        st.pyplot(fig_hierarchy)
    
    with core_tabs[1]:
        st.markdown("#### Artist 层级结构")
        st.info("""
        **Artist 是 Matplotlib 中所有可见对象的基类**，包括：
        
        - **Figure**: 顶层容器
        - **Axes**: 绘图区域
        - **Line2D**: 线条对象
        - **Text**: 文本对象
        - **Rectangle, Circle**: 形状对象
        - **Collection**: 集合对象（如散点集合）
        """)
        
        # Artist 示例
        fig_artist, axes_artist = plt.subplots(2, 2, figsize=(10, 8))
        axes_flat = axes_artist.flatten()
        
        # 1. Line2D
        x = np.linspace(0, 10, 100)
        axes_flat[0].plot(x, np.sin(x), label='Line2D')
        axes_flat[0].set_title("Line2D Artist", fontweight='bold')
        axes_flat[0].legend()
        axes_flat[0].grid(True, alpha=0.3)
        
        # 2. Text
        axes_flat[1].text(0.5, 0.5, 'Text Artist', fontsize=20, ha='center', va='center',
                         bbox=dict(boxstyle='round', facecolor='lightblue'))
        axes_flat[1].set_title("Text Artist", fontweight='bold')
        axes_flat[1].set_xlim(0, 1)
        axes_flat[1].set_ylim(0, 1)
        
        # 3. Rectangle
        rect = patches.Rectangle((0.2, 0.2), 0.6, 0.6, facecolor='lightgreen', edgecolor='black', linewidth=2)
        axes_flat[2].add_patch(rect)
        axes_flat[2].set_title("Rectangle Artist", fontweight='bold')
        axes_flat[2].set_xlim(0, 1)
        axes_flat[2].set_ylim(0, 1)
        
        # 4. Collection
        x_scatter = np.random.rand(50)
        y_scatter = np.random.rand(50)
        axes_flat[3].scatter(x_scatter, y_scatter, s=100, c=x_scatter, cmap='viridis')
        axes_flat[3].set_title("Collection Artist", fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig_artist)
    
    with core_tabs[2]:
        st.markdown("#### 坐标轴类型 (Axis Scale)")
        st.info("Matplotlib 支持多种坐标轴类型，适用于不同的数据分布。")
        
        scale_type = st.selectbox("选择坐标轴类型", 
                                 ["linear (线性)", "log (对数)", "symlog (对称对数)", "logit (逻辑)", "function (函数)"],
                                 key="axis_scale_type")
        
        fig_scale, ax_scale = plt.subplots(figsize=(8, 5))
        x = np.linspace(1, 1000, 1000)
        y = np.exp(x / 100)
        
        if scale_type == "linear (线性)":
            ax_scale.plot(x, y)
            ax_scale.set_xscale('linear')
            ax_scale.set_title("Linear Scale (线性刻度)", fontweight='bold')
        elif scale_type == "log (对数)":
            ax_scale.plot(x, y)
            ax_scale.set_xscale('log')
            ax_scale.set_yscale('log')
            ax_scale.set_title("Log Scale (对数刻度)", fontweight='bold')
        elif scale_type == "symlog (对称对数)":
            x_sym = np.linspace(-100, 100, 200)
            y_sym = np.sign(x_sym) * np.log10(1 + np.abs(x_sym))
            ax_scale.plot(x_sym, y_sym)
            ax_scale.set_xscale('symlog')
            ax_scale.set_title("Symlog Scale (对称对数刻度)", fontweight='bold')
        elif scale_type == "logit (逻辑)":
            x_logit = np.linspace(0.01, 0.99, 100)
            y_logit = x_logit
            ax_scale.plot(x_logit, y_logit)
            ax_scale.set_xscale('logit')
            ax_scale.set_title("Logit Scale (逻辑刻度)", fontweight='bold')
        else:  # function
            def forward(x):
                return x ** 2
            def inverse(x):
                return np.sqrt(x)
            ax_scale.plot(x, y)
            ax_scale.set_xscale('function', functions=(forward, inverse))
            ax_scale.set_title("Function Scale (函数刻度)", fontweight='bold')
        
        ax_scale.grid(True, alpha=0.3)
        st.pyplot(fig_scale)
        
        st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(1, 1000, 1000)
y = np.exp(x / 100)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y)
ax.set_xscale('{scale_type.split('(')[0].strip()}')
ax.set_title("{scale_type.split('(')[0].strip()} Scale")
ax.grid(True, alpha=0.3)
plt.show()
        """, language='python')
    
    with core_tabs[3]:
        st.markdown("#### 后端系统 (Backend)")
        st.info("""
        Matplotlib 支持多种后端（Backend），用于渲染图形：
        
        - **TkAgg**: Tkinter 后端（桌面应用）
        - **Qt5Agg**: Qt5 后端（桌面应用）
        - **Agg**: 无显示后端（用于保存文件）
        - **PDF**: PDF 后端（生成PDF文件）
        - **SVG**: SVG 后端（生成矢量图）
        """)
        
        backend_info = f"""
        **当前后端**: {plt.get_backend()}
        
        **常用后端设置**:
        ```python
        import matplotlib
        matplotlib.use('TkAgg')  # 设置后端
        ```
        
        **注意**: 后端设置必须在导入 pyplot 之前完成。
        """
        st.markdown(backend_info)

# --- 章节 3: 基础笔触 ---
elif menu == "3. 基础笔触":
    st.title("掌握笔触：Matplotlib 的核心绘图元素")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;'>
        <p style='margin: 0; text-align: center; font-weight: 500;'>
            🎨 通过交互式参数调整，实时预览效果，快速掌握各种绘图技巧
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Line2D (线条)", "Patches (形状)", "Collections (散点)", "Images (图像)"])
    
    with tab1:
        st.subheader("线条的艺术 (Line2D)")
        st.caption("💡 调整下方参数，实时查看效果。点击参数旁的「查看选项」了解更多。")
        
        # 合并的交互式界面
        col_ctrl, col_view = st.columns([1.2, 2])
        
        with col_ctrl:
            st.markdown("#### 🎛️ 参数控制")
            
            # linestyle 参数
            with st.expander("📏 线型 (linestyle)", expanded=True):
                line_style = st.selectbox(
                    "选择线型",
                    ['-', '--', '-.', ':', 'None'],
                    index=0,
                    key="line_style",
                    help="'-' 实线 | '--' 虚线 | '-.' 点划线 | ':' 点线"
                )
                if st.button("📚 查看所有选项", key="btn_linestyle"):
                    from catalogs.line import render_linestyle_gallery
                    render_linestyle_gallery()
            
            # linewidth 参数
            with st.expander("📐 线宽 (linewidth)", expanded=True):
                line_width = st.slider(
                    "线宽",
                    1, 10, 2,
                    key="line_width",
                    help="数值越大，线条越粗"
                )
            
            # color 参数
            with st.expander("🎨 颜色 (color)", expanded=True):
                color = st.color_picker("选择颜色", "#FF5733", key="line_color")
                if st.button("📚 查看颜色选项", key="btn_color"):
                    from catalogs.color import render_color_gallery
                    render_color_gallery()
            
            # marker 参数
            with st.expander("📍 标记 (marker)", expanded=True):
                marker = st.selectbox(
                    "选择标记",
                    [None, 'o', 's', '^', 'v', '<', '>', '*', '+', 'x'],
                    key="line_marker",
                    help="None 表示不显示标记点"
                )
                if st.button("📚 查看所有标记", key="btn_marker"):
                    from catalogs.marker import render_marker_gallery
                    render_marker_gallery()
            
            # drawstyle 参数
            with st.expander("📈 绘制样式 (drawstyle)", expanded=False):
                from catalogs.line import get_drawstyle_options
                drawstyles = get_drawstyle_options()
                drawstyle = st.selectbox(
                    "选择绘制样式",
                    list(drawstyles.keys()),
                    index=0,
                    key="line_drawstyle",
                    help="控制数据点的连接方式"
                )
                if st.button("📚 查看绘制样式选项", key="btn_drawstyle"):
                    from catalogs.line import render_drawstyle_gallery
                    render_drawstyle_gallery()
            
            # capstyle 参数（仅对粗线有效）
            with st.expander("🔲 线端样式 (capstyle)", expanded=False):
                from catalogs.line import get_capstyle_options
                capstyles = get_capstyle_options()
                capstyle = st.selectbox(
                    "选择线端样式",
                    capstyles,
                    index=0,
                    key="line_capstyle",
                    help="控制线条端点的形状（仅对粗线有效）"
                )
                if st.button("📚 查看线端样式选项", key="btn_capstyle"):
                    from catalogs.line import render_capstyle_gallery
                    render_capstyle_gallery()
            
            # joinstyle 参数（仅对折线有效）
            with st.expander("🔗 连接样式 (joinstyle)", expanded=False):
                from catalogs.line import get_joinstyle_options
                joinstyles = get_joinstyle_options()
                joinstyle = st.selectbox(
                    "选择连接样式",
                    joinstyles,
                    index=0,
                    key="line_joinstyle",
                    help="控制线条转折处的连接方式（仅对折线有效）"
                )
                if st.button("📚 查看连接样式选项", key="btn_joinstyle"):
                    from catalogs.line import render_joinstyle_gallery
                    render_joinstyle_gallery()
        
        with col_view:
            st.markdown("#### 📊 实时预览")
            
            # 根据参数选择合适的数据
            # 对于 joinstyle，需要折线数据（至少3个点）才能看到效果
            use_joinstyle_data = False
            
            # 如果选择了 joinstyle，需要折线数据才能看到效果
            # 即使选择 miter（默认值），也使用折线数据以便对比
            if joinstyle:
                use_joinstyle_data = True
            
            # 根据参数选择数据
            if use_joinstyle_data:
                # 使用折线数据以便看清 joinstyle 效果
                x = np.array([1, 5, 9, 13, 17])
                y = np.array([0.2, 0.8, 0.3, 0.7, 0.4])
            elif drawstyle != 'default':
                # 对于 drawstyle，使用较少点数以便看清阶梯效果
                x = np.linspace(0, 10, 15)
                y = np.cos(x)
            else:
                # 默认数据
                x = np.linspace(0, 10, 50)
                y = np.cos(x)
            
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # 构建 plot 参数
            plot_kwargs = {
                'linestyle': line_style,
                'linewidth': line_width,
                'color': color,
                'drawstyle': drawstyle,
            }
            
            # marker 参数：只有当 marker 不为 None 时才添加
            if marker is not None:
                plot_kwargs['marker'] = marker
                # 根据线宽调整标记点大小，保持比例协调
                plot_kwargs['markersize'] = max(6, int(line_width * 3))
            
            # capstyle 和 joinstyle：总是应用，但效果在粗线上更明显
            plot_kwargs['solid_capstyle'] = capstyle
            plot_kwargs['solid_joinstyle'] = joinstyle
            
            ax.plot(x, y, **plot_kwargs)
            
            # 如果线宽较小，显示提示信息
            if line_width < 3 and (capstyle != 'butt' or joinstyle != 'miter'):
                tip_text = "💡 线宽较小时，某些效果可能不明显"
                ax.text(0.02, 0.98, tip_text, 
                       transform=ax.transAxes, fontsize=8, verticalalignment='top',
                       bbox=dict(boxstyle='round', facecolor='#fff3cd', alpha=0.8))
            
            ax.set_title("线条效果预览", fontsize=14, fontweight='bold')
            ax.set_xlabel("X 轴", fontsize=12)
            ax.set_ylabel("Y 轴", fontsize=12)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
            # 代码生成
            st.markdown("#### 💻 生成代码")
            marker_str = f"'{marker}'" if marker else "None"
            
            # 根据实际使用的数据生成代码
            if use_joinstyle_data:
                data_code = "x = np.array([1, 5, 9, 13, 17])\ny = np.array([0.2, 0.8, 0.3, 0.7, 0.4])"
            elif drawstyle != 'default':
                data_code = "x = np.linspace(0, 10, 15)\ny = np.cos(x)"
            else:
                data_code = "x = np.linspace(0, 10, 50)\ny = np.cos(x)"
            
            code_params = f"""    linestyle='{line_style}', 
    linewidth={line_width}, 
    color='{color}', 
    drawstyle='{drawstyle}',
    solid_capstyle='{capstyle}',
    solid_joinstyle='{joinstyle}'"""
            
            # 只有当 marker 不为 None 时才添加 marker 参数
            if marker is not None:
                marker_size = max(6, int(line_width * 3))
                code_params += f",\n    marker={marker_str},\n    markersize={marker_size}"
            
            st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

{data_code}

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, 
{code_params}
)
ax.set_title("线条效果预览", fontsize=14, fontweight='bold')
ax.set_xlabel("X 轴", fontsize=12)
ax.set_ylabel("Y 轴", fontsize=12)
ax.grid(True, alpha=0.3)
plt.show()
            """, language='python')
            
            # 添加参数说明
            if use_joinstyle_data:
                st.info("💡 **提示**：为了展示 `joinstyle` 的效果，使用了折线数据（至少3个转折点）。")
            if drawstyle != 'default':
                st.info("💡 **提示**：为了展示 `drawstyle` 的阶梯效果，使用了较少的数据点。")
            if line_width < 3 and (capstyle != 'butt' or joinstyle != 'miter'):
                st.warning(f"⚠️ **注意**：当前线宽为 {line_width}，`capstyle` 和 `joinstyle` 的效果在细线上可能不明显。建议将线宽调整为 3-5 或更大以便看清效果。")

    with tab2:
        st.subheader("塑造形态 (Patches: 形状与统计图)")
        st.markdown("""
        <div style='background-color: #f0fdf4; padding: 1rem; border-radius: 8px; border-left: 4px solid #22c55e; margin-bottom: 1.5rem;'>
            <p style='margin: 0; color: #166534;'>
                💡 <strong>提示</strong>：调整下方参数，实时查看效果。Patches 包括条形图、直方图、饼图、箱线图等多种统计图表。
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 图表类型选择
        chart_type = st.selectbox(
            "选择图表类型",
            [
                "Bar Chart (垂直条形图)",
                "Barh Chart (水平条形图)",
                "Stacked Bar (堆叠条形图)",
                "Histogram (直方图)",
                "Pie Chart (饼图)",
                "Box Plot (箱线图)",
                "Violin Plot (小提琴图)",
                "Errorbar (误差棒图)",
                "Fill Between (填充区域)",
                "Stackplot (堆叠面积图)"
            ],
            key="patches_chart_type"
        )
        
        # 合并的交互式界面
        col_ctrl, col_view = st.columns([1.2, 2])
        
        with col_ctrl:
            st.markdown("#### 🎛️ 参数控制")
            
            # 通用参数
            with st.expander("🎨 颜色 (color)", expanded=True):
                patch_color = st.color_picker("选择颜色", "#3b82f6", key="patch_color")
                if st.button("📚 查看颜色选项", key="btn_patch_color"):
                    from catalogs.color import render_color_gallery
                    render_color_gallery()
            
            with st.expander("📏 透明度 (alpha)", expanded=True):
                patch_alpha = st.slider("透明度", 0.0, 1.0, 0.8, 0.1, key="patch_alpha")
            
            with st.expander("🔲 边框 (edgecolor)", expanded=False):
                use_edge = st.checkbox("显示边框", value=True, key="patch_use_edge")
                if use_edge:
                    edge_color = st.color_picker("边框颜色", "#000000", key="patch_edgecolor")
                    edge_width = st.slider("边框宽度", 0.5, 3.0, 1.0, 0.5, key="patch_edgewidth")
        
        with col_view:
            st.markdown("#### 📊 实时预览")
            
            fig, ax = plt.subplots(figsize=(8, 5))
            code_str = ""
            plot_kwargs = {}
            
            if chart_type == "Bar Chart (垂直条形图)":
                categories = ['A', 'B', 'C', 'D', 'E']
                values = [23, 45, 56, 78, 32]
                plot_kwargs = {'color': patch_color, 'alpha': patch_alpha}
                if use_edge:
                    plot_kwargs['edgecolor'] = edge_color
                    plot_kwargs['linewidth'] = edge_width
                ax.bar(categories, values, **plot_kwargs)
                ax.set_title("Bar Chart (垂直条形图)", fontsize=14, fontweight='bold')
                ax.set_xlabel("类别", fontsize=12)
                ax.set_ylabel("数值", fontsize=12)
                code_str = f"ax.bar(categories, values, color='{patch_color}', alpha={patch_alpha}"
                if use_edge:
                    code_str += f", edgecolor='{edge_color}', linewidth={edge_width}"
                code_str += ")"
                
            elif chart_type == "Barh Chart (水平条形图)":
                categories = ['A', 'B', 'C', 'D', 'E']
                values = [23, 45, 56, 78, 32]
                plot_kwargs = {'color': patch_color, 'alpha': patch_alpha}
                if use_edge:
                    plot_kwargs['edgecolor'] = edge_color
                    plot_kwargs['linewidth'] = edge_width
                ax.barh(categories, values, **plot_kwargs)
                ax.set_title("Barh Chart (水平条形图)", fontsize=14, fontweight='bold')
                ax.set_xlabel("数值", fontsize=12)
                ax.set_ylabel("类别", fontsize=12)
                code_str = f"ax.barh(categories, values, color='{patch_color}', alpha={patch_alpha}"
                if use_edge:
                    code_str += f", edgecolor='{edge_color}', linewidth={edge_width}"
                code_str += ")"
                
            elif chart_type == "Stacked Bar (堆叠条形图)":
                categories = ['A', 'B', 'C', 'D']
                values1 = [20, 35, 30, 35]
                values2 = [25, 25, 25, 25]
                values3 = [15, 20, 15, 18]
                x = np.arange(len(categories))
                width = 0.6
                plot_kwargs1 = {'color': '#3b82f6', 'alpha': patch_alpha}
                plot_kwargs2 = {'color': '#10b981', 'alpha': patch_alpha}
                plot_kwargs3 = {'color': '#f59e0b', 'alpha': patch_alpha}
                if use_edge:
                    plot_kwargs1['edgecolor'] = edge_color
                    plot_kwargs1['linewidth'] = edge_width
                    plot_kwargs2['edgecolor'] = edge_color
                    plot_kwargs2['linewidth'] = edge_width
                    plot_kwargs3['edgecolor'] = edge_color
                    plot_kwargs3['linewidth'] = edge_width
                ax.bar(categories, values1, width, label='系列1', **plot_kwargs1)
                ax.bar(categories, values2, width, bottom=values1, label='系列2', **plot_kwargs2)
                ax.bar(categories, values3, width, bottom=np.array(values1)+np.array(values2), label='系列3', **plot_kwargs3)
                ax.set_title("Stacked Bar (堆叠条形图)", fontsize=14, fontweight='bold')
                ax.set_xlabel("类别", fontsize=12)
                ax.set_ylabel("数值", fontsize=12)
                ax.legend()
                code_str = f"""ax.bar(categories, values1, width, label='系列1', color='#3b82f6', alpha={patch_alpha})
ax.bar(categories, values2, width, bottom=values1, label='系列2', color='#10b981', alpha={patch_alpha})
ax.bar(categories, values3, width, bottom=np.array(values1)+np.array(values2), label='系列3', color='#f59e0b', alpha={patch_alpha})"""
                
            elif chart_type == "Histogram (直方图)":
                data = np.random.randn(1000)
                bins = st.slider("分组数 (bins)", 10, 50, 20, key="hist_bins")
                plot_kwargs = {'color': patch_color, 'alpha': patch_alpha, 'bins': bins}
                if use_edge:
                    plot_kwargs['edgecolor'] = edge_color
                    plot_kwargs['linewidth'] = edge_width
                ax.hist(data, **plot_kwargs)
                ax.set_title("Histogram (直方图)", fontsize=14, fontweight='bold')
                ax.set_xlabel("数值", fontsize=12)
                ax.set_ylabel("频数", fontsize=12)
                code_str = f"ax.hist(data, bins={bins}, color='{patch_color}', alpha={patch_alpha}"
                if use_edge:
                    code_str += f", edgecolor='{edge_color}', linewidth={edge_width}"
                code_str += ")"
                
            elif chart_type == "Pie Chart (饼图)":
                labels = ['类别A', '类别B', '类别C', '类别D']
                sizes = [15, 30, 45, 10]
                explode = st.multiselect("突出显示", labels, key="pie_explode")
                explode_values = [0.1 if label in explode else 0 for label in labels]
                colors_list = [patch_color, '#10b981', '#f59e0b', '#ef4444']
                wedges, texts, autotexts = ax.pie(sizes, explode=explode_values, labels=labels, colors=colors_list, 
                      autopct='%1.1f%%', shadow=True, startangle=90)
                # 设置透明度
                for w in wedges:
                    w.set_alpha(patch_alpha)
                ax.set_title("Pie Chart (饼图)", fontsize=14, fontweight='bold')
                # 保存变量供代码生成使用
                pie_explode_values = explode_values
                pie_colors_list = colors_list
                code_str = f"""wedges, texts, autotexts = ax.pie(sizes, explode={explode_values}, labels=labels, 
    colors={colors_list}, autopct='%1.1f%%', shadow=True, startangle=90)
for w in wedges:
    w.set_alpha({patch_alpha})"""
                
            elif chart_type == "Box Plot (箱线图)":
                data_box = [np.random.normal(0, std, 100) for std in range(1, 5)]
                plot_kwargs = {}
                if use_edge:
                    plot_kwargs['boxprops'] = dict(color=edge_color, linewidth=edge_width)
                    plot_kwargs['whiskerprops'] = dict(color=edge_color, linewidth=edge_width)
                    plot_kwargs['capprops'] = dict(color=edge_color, linewidth=edge_width)
                bp = ax.boxplot(data_box, patch_artist=True, **plot_kwargs)
                for patch in bp['boxes']:
                    patch.set_facecolor(patch_color)
                    patch.set_alpha(patch_alpha)
                ax.set_title("Box Plot (箱线图)", fontsize=14, fontweight='bold')
                ax.set_xticklabels(['组1', '组2', '组3', '组4'])
                ax.set_ylabel("数值", fontsize=12)
                code_str = f"""bp = ax.boxplot(data, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('{patch_color}')
    patch.set_alpha({patch_alpha})"""
                
            elif chart_type == "Violin Plot (小提琴图)":
                data_violin = [np.random.normal(0, std, 100) for std in range(1, 5)]
                parts = ax.violinplot(data_violin, positions=range(1, 5), showmeans=True)
                for pc in parts['bodies']:
                    pc.set_facecolor(patch_color)
                    pc.set_alpha(patch_alpha)
                ax.set_title("Violin Plot (小提琴图)", fontsize=14, fontweight='bold')
                ax.set_xticks(range(1, 5))
                ax.set_xticklabels(['组1', '组2', '组3', '组4'])
                ax.set_ylabel("数值", fontsize=12)
                code_str = f"""parts = ax.violinplot(data, positions=range(1, 5), showmeans=True)
for pc in parts['bodies']:
    pc.set_facecolor('{patch_color}')
    pc.set_alpha({patch_alpha})"""
                
            elif chart_type == "Errorbar (误差棒图)":
                x = np.arange(1, 6)
                y = [2, 3, 4, 3, 2]
                yerr = [0.3, 0.4, 0.5, 0.4, 0.3]
                xerr = [0.1, 0.1, 0.1, 0.1, 0.1]
                ax.errorbar(x, y, yerr=yerr, xerr=xerr, fmt='o', color=patch_color, 
                           alpha=patch_alpha, capsize=5, capthick=2)
                ax.set_title("Errorbar (误差棒图)", fontsize=14, fontweight='bold')
                ax.set_xlabel("X 轴", fontsize=12)
                ax.set_ylabel("Y 轴", fontsize=12)
                ax.grid(True, alpha=0.3)
                code_str = f"ax.errorbar(x, y, yerr=yerr, xerr=xerr, fmt='o', color='{patch_color}', alpha={patch_alpha}, capsize=5)"
                
            elif chart_type == "Fill Between (填充区域)":
                x = np.linspace(0, 10, 100)
                y1 = np.sin(x)
                y2 = np.cos(x)
                ax.plot(x, y1, color='#3b82f6', label='sin(x)')
                ax.plot(x, y2, color='#10b981', label='cos(x)')
                ax.fill_between(x, y1, y2, where=(y1 > y2), color=patch_color, alpha=patch_alpha, label='填充区域')
                ax.set_title("Fill Between (填充区域)", fontsize=14, fontweight='bold')
                ax.set_xlabel("X 轴", fontsize=12)
                ax.set_ylabel("Y 轴", fontsize=12)
                ax.legend()
                ax.grid(True, alpha=0.3)
                code_str = f"ax.fill_between(x, y1, y2, where=(y1 > y2), color='{patch_color}', alpha={patch_alpha})"
                
            elif chart_type == "Stackplot (堆叠面积图)":
                x = np.arange(0, 10, 0.1)
                y1 = np.sin(x)
                y2 = np.cos(x)
                y3 = np.sin(x) * 0.5
                ax.stackplot(x, y1, y2, y3, labels=['系列1', '系列2', '系列3'], 
                           colors=[patch_color, '#10b981', '#f59e0b'], alpha=patch_alpha)
                ax.set_title("Stackplot (堆叠面积图)", fontsize=14, fontweight='bold')
                ax.set_xlabel("X 轴", fontsize=12)
                ax.set_ylabel("Y 轴", fontsize=12)
                ax.legend()
                ax.grid(True, alpha=0.3)
                code_str = f"ax.stackplot(x, y1, y2, y3, labels=['系列1', '系列2', '系列3'], colors=['{patch_color}', '#10b981', '#f59e0b'], alpha={patch_alpha})"
            
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
            # 代码生成
            st.markdown("#### 💻 生成代码")
            
            # 根据图表类型生成完整代码
            if chart_type in ["Bar Chart (垂直条形图)", "Barh Chart (水平条形图)"]:
                full_code = f"""
import matplotlib.pyplot as plt
import numpy as np

categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]

fig, ax = plt.subplots(figsize=(8, 5))
{code_str}
ax.set_title("{chart_type.split('(')[0].strip()}", fontsize=14, fontweight='bold')
ax.set_xlabel("类别" if "垂直" in chart_type else "数值", fontsize=12)
ax.set_ylabel("数值" if "垂直" in chart_type else "类别", fontsize=12)
ax.grid(True, alpha=0.3)
plt.show()
"""
            elif chart_type == "Stacked Bar (堆叠条形图)":
                full_code = f"""
import matplotlib.pyplot as plt
import numpy as np

categories = ['A', 'B', 'C', 'D']
values1 = [20, 35, 30, 35]
values2 = [25, 25, 25, 25]
values3 = [15, 20, 15, 18]
width = 0.6

fig, ax = plt.subplots(figsize=(8, 5))
{code_str}
ax.set_title("堆叠条形图", fontsize=14, fontweight='bold')
ax.set_xlabel("类别", fontsize=12)
ax.set_ylabel("数值", fontsize=12)
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()
"""
            elif chart_type == "Histogram (直方图)":
                full_code = f"""
import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(1000)

fig, ax = plt.subplots(figsize=(8, 5))
{code_str}
ax.set_title("直方图", fontsize=14, fontweight='bold')
ax.set_xlabel("数值", fontsize=12)
ax.set_ylabel("频数", fontsize=12)
ax.grid(True, alpha=0.3)
plt.show()
"""
            elif chart_type == "Pie Chart (饼图)":
                # 使用之前保存的变量
                pie_explode_vals = pie_explode_values if 'pie_explode_values' in locals() else [0, 0, 0, 0]
                pie_colors = pie_colors_list if 'pie_colors_list' in locals() else [patch_color, '#10b981', '#f59e0b', '#ef4444']
                full_code = f"""
import matplotlib.pyplot as plt
import numpy as np

labels = ['类别A', '类别B', '类别C', '类别D']
sizes = [15, 30, 45, 10]
explode = {pie_explode_vals}
colors = {pie_colors}

fig, ax = plt.subplots(figsize=(8, 5))
wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, 
    colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
for w in wedges:
    w.set_alpha({patch_alpha})
ax.set_title("饼图", fontsize=14, fontweight='bold')
plt.show()
"""
            elif chart_type == "Box Plot (箱线图)":
                full_code = f"""
import matplotlib.pyplot as plt
import numpy as np

data = [np.random.normal(0, std, 100) for std in range(1, 5)]

fig, ax = plt.subplots(figsize=(8, 5))
{code_str}
ax.set_title("箱线图", fontsize=14, fontweight='bold')
ax.set_xticklabels(['组1', '组2', '组3', '组4'])
ax.set_ylabel("数值", fontsize=12)
ax.grid(True, alpha=0.3)
plt.show()
"""
            elif chart_type == "Violin Plot (小提琴图)":
                full_code = f"""
import matplotlib.pyplot as plt
import numpy as np

data = [np.random.normal(0, std, 100) for std in range(1, 5)]

fig, ax = plt.subplots(figsize=(8, 5))
{code_str}
ax.set_title("小提琴图", fontsize=14, fontweight='bold')
ax.set_xticks(range(1, 5))
ax.set_xticklabels(['组1', '组2', '组3', '组4'])
ax.set_ylabel("数值", fontsize=12)
ax.grid(True, alpha=0.3)
plt.show()
"""
            elif chart_type == "Errorbar (误差棒图)":
                full_code = f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 6)
y = [2, 3, 4, 3, 2]
yerr = [0.3, 0.4, 0.5, 0.4, 0.3]
xerr = [0.1, 0.1, 0.1, 0.1, 0.1]

fig, ax = plt.subplots(figsize=(8, 5))
{code_str}
ax.set_title("误差棒图", fontsize=14, fontweight='bold')
ax.set_xlabel("X 轴", fontsize=12)
ax.set_ylabel("Y 轴", fontsize=12)
ax.grid(True, alpha=0.3)
plt.show()
"""
            elif chart_type == "Fill Between (填充区域)":
                full_code = f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y1, color='#3b82f6', label='sin(x)')
ax.plot(x, y2, color='#10b981', label='cos(x)')
{code_str}
ax.set_title("填充区域", fontsize=14, fontweight='bold')
ax.set_xlabel("X 轴", fontsize=12)
ax.set_ylabel("Y 轴", fontsize=12)
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()
"""
            elif chart_type == "Stackplot (堆叠面积图)":
                full_code = f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 10, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * 0.5

fig, ax = plt.subplots(figsize=(8, 5))
{code_str}
ax.set_title("堆叠面积图", fontsize=14, fontweight='bold')
ax.set_xlabel("X 轴", fontsize=12)
ax.set_ylabel("Y 轴", fontsize=12)
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()
"""
            else:
                full_code = f"""
import matplotlib.pyplot as plt
import numpy as np

{code_str}

ax.set_title("{chart_type.split('(')[0].strip()}", fontsize=14, fontweight='bold')
plt.show()
"""
            
            st.code(full_code, language='python')

    with tab3:
        st.subheader("点绘星空 (Collections: 集合类型)")
        st.markdown("""
        <div style='background-color: #fef3c7; padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b; margin-bottom: 1.5rem;'>
            <p style='margin: 0; color: #92400e;'>
                💡 <strong>提示</strong>：Collections 包括散点、线段集合、多边形集合等多种类型，适合高效绘制大量相似元素。
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        collection_type = st.selectbox("选择集合类型",
                                      ["Scatter (散点)", "LineCollection (线段集合)", "PolyCollection (多边形集合)", "EventCollection (事件集合)"],
                                      key="collection_type")
        
        if collection_type == "Scatter (散点)":
            st.caption("💡 调整参数查看散点图效果。点击「查看选项」了解更多参数。")
            
            col_ctrl, col_view = st.columns([1.2, 2])
            
            with col_ctrl:
                st.markdown("#### 🎛️ 参数控制")
                
                n_points = st.slider("点数量", 50, 500, 200, key="scatter_points")
                
                with st.expander("📍 标记样式 (marker)", expanded=True):
                    marker_scatter = st.selectbox(
                        "选择标记",
                        ['o', 's', '^', 'v', '*', '+', 'x'],
                        index=0,
                        key="scatter_marker"
                    )
                    if st.button("📚 查看所有标记", key="btn_scatter_marker"):
                        from catalogs.marker import render_marker_gallery
                        render_marker_gallery()
                
                # fillstyle 参数（注意：scatter 支持有限，主要用于 plot）
                with st.expander("🎨 填充样式 (fillstyle)", expanded=False):
                    st.caption("⚠️ 注意：`fillstyle` 主要用于 `plot()` 函数。`scatter()` 对 fillstyle 的支持有限。")
                    from catalogs.marker import get_fillstyle_options
                    fillstyles = get_fillstyle_options()
                    fillstyle_scatter = st.selectbox(
                        "选择填充样式",
                        fillstyles,
                        index=0,
                        key="scatter_fillstyle",
                        help="控制标记符号的填充样式。注意：scatter() 仅支持 'full' 和 'none'，其他样式主要用于 plot()"
                    )
                    if st.button("📚 查看填充样式选项", key="btn_scatter_fillstyle"):
                        from catalogs.marker import render_fillstyle_gallery
                        render_fillstyle_gallery()
                
                with st.expander("🌈 颜色映射 (cmap)", expanded=True):
                    cmap_choice = st.selectbox(
                        "选择颜色映射",
                        ['viridis', 'plasma', 'inferno', 'magma', 'coolwarm', 'RdYlBu'],
                        index=0,
                        key="scatter_cmap"
                    )
                    if st.button("📚 查看所有颜色映射", key="btn_scatter_cmap"):
                        from catalogs.color import render_colormap_gallery
                        render_colormap_gallery()
                
                alpha_scatter = st.slider("透明度 (alpha)", 0.1, 1.0, 0.5, 0.1, key="scatter_alpha")
            
            with col_view:
                st.markdown("#### 📊 实时预览")
                x = np.random.rand(n_points)
                y = np.random.rand(n_points)
                colors = np.random.rand(n_points)
                area = (30 * np.random.rand(n_points))**2 
                
                fig, ax = plt.subplots(figsize=(8, 5))
                
                # 构建 scatter 参数
                # 注意：scatter() 不支持 fillstyle 参数，fillstyle 仅适用于 plot()
                scatter_kwargs = {
                    's': area,
                    'c': colors,
                    'alpha': alpha_scatter,
                    'cmap': cmap_choice,
                    'marker': marker_scatter,
                }
                
                sc = ax.scatter(x, y, **scatter_kwargs)
                
                # scatter() 不支持 fillstyle 参数，但我们可以通过 PathCollection 的属性来模拟部分效果
                fillable_markers = ['o', 's', '^', 'v', '<', '>', 'D', 'd', 'p', 'h', 'H', '8', '*']
                if marker_scatter in fillable_markers and fillstyle_scatter == 'none':
                    # 不填充，仅显示边框
                    # 注意：scatter 的 fillstyle='none' 效果需要通过设置 facecolors 和 edgecolors 来实现
                    sc.set_facecolors('none')
                    # 确保边框可见
                    if sc.get_edgecolors().size == 0:
                        sc.set_edgecolors('black')
                    sc.set_linewidths(1.5)  # 设置边框宽度以便看清
                # 注意：'left', 'right', 'top', 'bottom' 等部分填充效果在 scatter 中无法直接实现
                # 这些效果主要用于 plot() 函数
                
                ax.set_title("散点图效果预览", fontsize=14, fontweight='bold')
                ax.set_xlabel("X 轴", fontsize=12)
                ax.set_ylabel("Y 轴", fontsize=12)
                cbar = fig.colorbar(sc, ax=ax)
                cbar.set_label("颜色映射", fontsize=10)
                st.pyplot(fig)
                
                st.markdown("#### 💻 生成代码")
                # scatter 不支持 fillstyle，但我们可以通过其他方式控制
                fillstyle_note = ""
                if marker_scatter in fillable_markers and fillstyle_scatter != 'full':
                    if fillstyle_scatter == 'none':
                        fillstyle_note = "\n# 注意：scatter() 不支持 fillstyle，但可以通过 set_facecolors('none') 实现不填充效果\nsc.set_facecolors('none')"
                    else:
                        fillstyle_note = f"\n# 注意：scatter() 不支持 fillstyle='{fillstyle_scatter}'，fillstyle 主要用于 plot() 函数"
                
                st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

# 生成随机数据
n_points = {n_points}
x = np.random.rand(n_points)
y = np.random.rand(n_points)
colors = np.random.rand(n_points)
area = (30 * np.random.rand(n_points))**2

fig, ax = plt.subplots(figsize=(8, 5))
sc = ax.scatter(x, y, s=area, c=colors, alpha={alpha_scatter}, 
                cmap='{cmap_choice}', marker='{marker_scatter}'){fillstyle_note}
ax.set_title("散点图效果预览", fontsize=14, fontweight='bold')
ax.set_xlabel("X 轴", fontsize=12)
ax.set_ylabel("Y 轴", fontsize=12)
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label("颜色映射", fontsize=10)
plt.show()
                """, language='python')
                
                # 添加说明
                if marker_scatter in fillable_markers:
                    st.info(f"💡 **提示**：`fillstyle` 参数主要用于 `plot()` 函数。对于 `scatter()`，填充样式控制有限。如需完整体验 fillstyle 效果，建议使用 `plot()` 函数配合 `marker` 参数。")
            
        elif collection_type == "LineCollection (线段集合)":
            st.caption("💡 LineCollection 用于高效绘制大量线段。")
            
            col_lc_ctrl, col_lc_view = st.columns([1.2, 2])
            
            with col_lc_ctrl:
                st.markdown("#### 🎛️ 参数控制")
                n_segments = st.slider("线段数量", 10, 100, 30, key="linecollection_n")
                line_width_lc = st.slider("线宽", 0.5, 3.0, 1.0, 0.5, key="linecollection_width")
                use_colormap = st.checkbox("使用颜色映射", value=True, key="linecollection_cmap")
            
            with col_lc_view:
                from matplotlib.collections import LineCollection
                
                fig_lc, ax_lc = plt.subplots(figsize=(8, 5))
                
                # 生成多条线段
                segments = []
                colors_list = []
                for i in range(n_segments):
                    x_seg = np.linspace(0, 10, 50)
                    y_seg = np.sin(x_seg + i * 0.2) + i * 0.1
                    segments.append(np.column_stack([x_seg, y_seg]))
                    if use_colormap:
                        colors_list.append(i)
                
                lc = LineCollection(segments, linewidths=line_width_lc)
                if use_colormap:
                    lc.set_array(np.array(colors_list))
                    lc.set_cmap('viridis')
                else:
                    lc.set_color('#3b82f6')
                
                ax_lc.add_collection(lc)
                ax_lc.autoscale()
                ax_lc.set_title("LineCollection (线段集合)", fontsize=14, fontweight='bold')
                ax_lc.set_xlabel("X 轴", fontsize=12)
                ax_lc.set_ylabel("Y 轴", fontsize=12)
                ax_lc.grid(True, alpha=0.3)
                if use_colormap:
                    plt.colorbar(lc, ax=ax_lc)
                st.pyplot(fig_lc)
                
                st.markdown("#### 💻 生成代码")
                st.code(f"""
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

# 生成线段数据
segments = []
for i in range({n_segments}):
    x = np.linspace(0, 10, 50)
    y = np.sin(x + i * 0.2) + i * 0.1
    segments.append(np.column_stack([x, y]))

# 创建 LineCollection
lc = LineCollection(segments, linewidths={line_width_lc})
{'lc.set_array(np.arange(len(segments)))' if use_colormap else "lc.set_color('#3b82f6')"}
{'lc.set_cmap("viridis")' if use_colormap else ''}

fig, ax = plt.subplots(figsize=(8, 5))
ax.add_collection(lc)
ax.autoscale()
{'plt.colorbar(lc, ax=ax)' if use_colormap else ''}
plt.show()
                """, language='python')
            
        elif collection_type == "PolyCollection (多边形集合)":
            st.caption("💡 PolyCollection 用于高效绘制大量多边形。")
            
            col_pc_ctrl, col_pc_view = st.columns([1.2, 2])
            
            with col_pc_ctrl:
                st.markdown("#### 🎛️ 参数控制")
                n_polygons = st.slider("多边形数量", 5, 30, 10, key="polycollection_n")
                poly_alpha = st.slider("透明度", 0.1, 1.0, 0.6, 0.1, key="polycollection_alpha")
            
            with col_pc_view:
                from matplotlib.collections import PolyCollection
                
                fig_pc, ax_pc = plt.subplots(figsize=(8, 5))
                
                # 生成多个多边形
                polygons = []
                colors_poly = []
                for i in range(n_polygons):
                    center_x = i * 1.0
                    center_y = np.sin(i * 0.5)
                    # 创建六边形
                    angles = np.linspace(0, 2*np.pi, 6, endpoint=False)
                    radius = 0.3
                    x_poly = center_x + radius * np.cos(angles)
                    y_poly = center_y + radius * np.sin(angles)
                    polygons.append(np.column_stack([x_poly, y_poly]))
                    colors_poly.append(i)
                
                pc = PolyCollection(polygons, alpha=poly_alpha, cmap='viridis')
                pc.set_array(np.array(colors_poly))
                ax_pc.add_collection(pc)
                ax_pc.autoscale()
                ax_pc.set_title("PolyCollection (多边形集合)", fontsize=14, fontweight='bold')
                ax_pc.set_xlabel("X 轴", fontsize=12)
                ax_pc.set_ylabel("Y 轴", fontsize=12)
                ax_pc.grid(True, alpha=0.3)
                plt.colorbar(pc, ax=ax_pc)
                st.pyplot(fig_pc)
                
                st.markdown("#### 💻 生成代码")
                st.code(f"""
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import numpy as np

# 生成多边形数据
polygons = []
for i in range({n_polygons}):
    center_x, center_y = i * 1.0, np.sin(i * 0.5)
    angles = np.linspace(0, 2*np.pi, 6, endpoint=False)
    radius = 0.3
    x = center_x + radius * np.cos(angles)
    y = center_y + radius * np.sin(angles)
    polygons.append(np.column_stack([x, y]))

# 创建 PolyCollection
pc = PolyCollection(polygons, alpha={poly_alpha}, cmap='viridis')
pc.set_array(np.arange(len(polygons)))

fig, ax = plt.subplots(figsize=(8, 5))
ax.add_collection(pc)
ax.autoscale()
plt.colorbar(pc, ax=ax)
plt.show()
                """, language='python')
            
        else:  # EventCollection
            st.caption("💡 EventCollection 用于标记事件时间点。")
            
            col_ec_ctrl, col_ec_view = st.columns([1.2, 2])
            
            with col_ec_ctrl:
                st.markdown("#### 🎛️ 参数控制")
                n_events = st.slider("事件数量", 5, 50, 20, key="eventcollection_n")
                orientation_ec = st.selectbox("方向", ['horizontal', 'vertical'], index=0, key="eventcollection_orient")
            
            with col_ec_view:
                from matplotlib.collections import EventCollection
                
                fig_ec, ax_ec = plt.subplots(figsize=(8, 5))
                
                # 生成事件数据
                x_data = np.linspace(0, 10, 100)
                y_data = np.sin(x_data)
                events = np.random.choice(x_data, n_events)
                
                ax_ec.plot(x_data, y_data, label='数据线')
                evt = EventCollection(events, orientation=orientation_ec, 
                                    lineoffset=0, linelength=0.5, 
                                    color='red', linewidth=2)
                ax_ec.add_collection(evt)
                ax_ec.set_title("EventCollection (事件集合)", fontsize=14, fontweight='bold')
                ax_ec.set_xlabel("X 轴", fontsize=12)
                ax_ec.set_ylabel("Y 轴", fontsize=12)
                ax_ec.legend()
                ax_ec.grid(True, alpha=0.3)
                st.pyplot(fig_ec)
                
                st.markdown("#### 💻 生成代码")
                st.code(f"""
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)
events = np.random.choice(x, {n_events})

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, label='数据线')
evt = EventCollection(events, orientation='{orientation_ec}', 
                     lineoffset=0, linelength=0.5, 
                     color='red', linewidth=2)
ax.add_collection(evt)
ax.legend()
plt.show()
                """, language='python')

    with tab4:
        st.subheader("渲染像素 (Images: 图像处理)")
        st.markdown("""
        <div style='background-color: #fef3c7; padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b; margin-bottom: 1.5rem;'>
            <p style='margin: 0; color: #92400e;'>
                💡 <strong>提示</strong>：Matplotlib 支持多种图像显示和处理方法，包括 imshow、pcolormesh 等。
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        image_type = st.selectbox("选择图像类型", 
                                 ["imshow (图像显示)", "pcolormesh (网格着色)", "matshow (矩阵显示)", "imread (读取图像)"],
                                 key="image_type")
        
        col_ctrl, col_view = st.columns([1.2, 2])
        
        with col_ctrl:
            st.markdown("#### 🎛️ 参数控制")
            
            with st.expander("🎨 颜色映射 (cmap)", expanded=True):
                cmap_img = st.selectbox("选择颜色映射", 
                                       ['viridis', 'plasma', 'inferno', 'magma', 'gray', 'hot', 'cool'],
                                       index=0, key="image_cmap")
                if st.button("📚 查看所有颜色映射", key="btn_image_cmap"):
                    from catalogs.color import render_colormap_gallery
                    render_colormap_gallery()
            
            with st.expander("🔄 插值方式 (interpolation)", expanded=True):
                interpolation = st.selectbox("插值方式", 
                                           ['nearest', 'bilinear', 'bicubic', 'spline16', 'spline36', 'hanning', 'hamming'],
                                           index=1, key="image_interpolation")
            
            with st.expander("📐 其他参数", expanded=False):
                aspect_ratio = st.selectbox("宽高比", ['auto', 'equal', 1.0, 0.5, 2.0], index=0, key="image_aspect")
                origin_pos = st.selectbox("原点位置", ['upper', 'lower'], index=0, key="image_origin")
        
        with col_view:
            st.markdown("#### 📊 实时预览")
            
            if image_type == "imshow (图像显示)":
                data = np.random.rand(30, 30)
                fig, ax = plt.subplots(figsize=(8, 6))
                im = ax.imshow(data, interpolation=interpolation, cmap=cmap_img, 
                             aspect=aspect_ratio, origin=origin_pos)
                fig.colorbar(im, ax=ax)
                ax.set_title("imshow (图像显示)", fontsize=14, fontweight='bold')
                st.pyplot(fig)
                
                st.markdown("#### 💻 生成代码")
                st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

data = np.random.rand(30, 30)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(data, interpolation='{interpolation}', cmap='{cmap_img}', 
               aspect='{aspect_ratio}', origin='{origin_pos}')
fig.colorbar(im, ax=ax)
ax.set_title("imshow (图像显示)")
plt.show()
                """, language='python')
            
            elif image_type == "pcolormesh (网格着色)":
                x = np.linspace(0, 10, 20)
                y = np.linspace(0, 10, 20)
                X, Y = np.meshgrid(x, y)
                Z = np.sin(X) * np.cos(Y)
                fig, ax = plt.subplots(figsize=(8, 6))
                mesh = ax.pcolormesh(X, Y, Z, cmap=cmap_img, shading='auto')
                fig.colorbar(mesh, ax=ax)
                ax.set_title("pcolormesh (网格着色)", fontsize=14, fontweight='bold')
                ax.set_xlabel("X 轴", fontsize=12)
                ax.set_ylabel("Y 轴", fontsize=12)
                st.pyplot(fig)
                
                st.markdown("#### 💻 生成代码")
                st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 20)
y = np.linspace(0, 10, 20)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

fig, ax = plt.subplots(figsize=(8, 6))
mesh = ax.pcolormesh(X, Y, Z, cmap='{cmap_img}', shading='auto')
fig.colorbar(mesh, ax=ax)
ax.set_title("pcolormesh (网格着色)")
plt.show()
                """, language='python')
            
            elif image_type == "matshow (矩阵显示)":
                data = np.random.rand(10, 10)
                fig, ax = plt.subplots(figsize=(8, 6))
                mat = ax.matshow(data, cmap=cmap_img)
                fig.colorbar(mat, ax=ax)
                ax.set_title("matshow (矩阵显示)", fontsize=14, fontweight='bold')
                st.pyplot(fig)
                
                st.markdown("#### 💻 生成代码")
                st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

data = np.random.rand(10, 10)

fig, ax = plt.subplots(figsize=(8, 6))
mat = ax.matshow(data, cmap='{cmap_img}')
fig.colorbar(mat, ax=ax)
ax.set_title("matshow (矩阵显示)")
plt.show()
                """, language='python')
            
            else:  # imread
                st.info("""
                **imread 用于读取图像文件**：
                
                ```python
                from matplotlib.image import imread
                img = imread('image.png')  # 读取图像
                ax.imshow(img)  # 显示图像
                ```
                
                **支持的格式**: PNG, JPEG, TIFF, BMP 等
                """)
                
                # 创建一个示例图像数据
                fig, ax = plt.subplots(figsize=(8, 6))
                # 模拟一个图像（使用随机数据）
                img_data = np.random.rand(100, 100, 3)  # RGB图像
                ax.imshow(img_data)
                ax.set_title("imread 示例 (模拟RGB图像)", fontsize=14, fontweight='bold')
                st.pyplot(fig)
                
                st.markdown("#### 💻 生成代码")
                st.code("""
import matplotlib.pyplot as plt
from matplotlib.image import imread

# 读取图像文件
img = imread('your_image.png')  # 替换为实际图像路径

fig, ax = plt.subplots(figsize=(8, 6))
ax.imshow(img)
ax.set_title("读取的图像")
plt.show()
                """, language='python')

# --- 章节 4: 布局与美学 ---
elif menu == "4. 布局与美学":
    st.title("谋篇布局与画龙点睛")
    st.markdown("""
    <div style='background-color: #fffbeb; padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b; margin-bottom: 1.5rem;'>
        <p style='margin: 0; color: #92400e;'>
            💡 <strong>提示</strong>：学习如何控制图表的外观和布局。点击参数旁的「查看选项」了解更多。
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 使用 Tab 组织不同类别
    style_tabs = st.tabs(["📐 子图布局", "🎨 样式与颜色", "📝 文本样式", "📊 坐标轴设置"])
    
    with style_tabs[0]:
        st.subheader("子图布局 (Subplots)")
        st.caption("学习如何创建多个子图")
        
        c1, c2 = st.columns(2)
        rows = c1.number_input("行数 (Rows)", min_value=1, max_value=5, value=2, key="subplot_rows")
        cols = c2.number_input("列数 (Columns)", min_value=1, max_value=5, value=2, key="subplot_cols")

        col_img, col_code = st.columns([3, 2])
        
        with col_img:
            fig, axes = plt.subplots(rows, cols, figsize=(8, 6), constrained_layout=True)
            
            if rows == 1 and cols == 1:
                axes_flat = [axes]
            else:
                axes_flat = axes.flatten()
                
            for i, ax in enumerate(axes_flat):
                ax.plot(np.random.rand(10), label=f"线条 {i+1}")
                ax.set_title(f"子图 {i+1}", fontsize=12, fontweight='bold')
                ax.legend(loc='upper right', fontsize='small')
                ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
        with col_code:
            st.markdown("#### 💻 实现代码")
            code_str = f"""
import matplotlib.pyplot as plt
import numpy as np

# {rows}行{cols}列布局
fig, axes = plt.subplots({rows}, {cols}, 
    figsize=(8, 6), 
    constrained_layout=True)

# 统一处理 axes
if {rows} * {cols} > 1:
    axes_flat = axes.flatten()
else:
    axes_flat = [axes]

for i, ax in enumerate(axes_flat):
    ax.plot(data)
    ax.set_title(f"子图 {{i+1}}", fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
plt.show()
"""
            st.code(code_str, language='python')
    
    with style_tabs[1]:
        st.subheader("样式与颜色")
        
        col_ctrl, col_view = st.columns([1.2, 2])
        
        with col_ctrl:
            st.markdown("#### 🎨 全局样式")
            style_select = st.selectbox(
                "选择样式 (Style Sheets)", 
                plt.style.available, 
                index=plt.style.available.index('ggplot') if 'ggplot' in plt.style.available else 0,
                key="style_select"
            )
            
            if st.button("📚 查看颜色选项", key="btn_style_color"):
                from catalogs.color import render_color_gallery
                render_color_gallery()
            
            if st.button("📚 查看颜色映射", key="btn_style_cmap"):
                from catalogs.color import render_colormap_gallery
                render_colormap_gallery()
        
        with col_view:
            with plt.style.context(style_select):
                fig, ax = plt.subplots(figsize=(8, 5))
                x = np.linspace(0, 10, 100)
                for i in range(1, 4):
                    ax.plot(x, np.sin(x + i * .5) * (7 - i), label=f"波形 {i}")
                ax.set_title(f"样式预览: {style_select}", fontsize=14, fontweight='bold')
                ax.set_xlabel("X 轴", fontsize=12)
                ax.set_ylabel("Y 轴", fontsize=12)
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
    
    with style_tabs[2]:
        st.subheader("文本样式")
        st.caption("💡 学习如何设置标题、标签等文本的样式")
        
        col_ctrl, col_view = st.columns([1.2, 2])
        
        with col_ctrl:
            st.markdown("#### 📝 文本参数")
            
            with st.expander("📏 字体大小 (fontsize)", expanded=True):
                fontsize_val = st.slider("字体大小", 8, 24, 12, key="text_fontsize")
                if st.button("📚 查看字体大小选项", key="btn_fontsize"):
                    from catalogs.text import render_fontsize_gallery
                    render_fontsize_gallery()
            
            with st.expander("💪 字体粗细 (fontweight)", expanded=True):
                fontweight_val = st.selectbox("字体粗细", ['normal', 'bold', 'light'], index=1, key="text_fontweight")
                if st.button("📚 查看字体粗细选项", key="btn_fontweight"):
                    from catalogs.text import render_fontweight_gallery
                    render_fontweight_gallery()
            
            with st.expander("🔤 字体族 (fontfamily)", expanded=True):
                fontfamily_val = st.selectbox("字体族", ['sans-serif', 'serif', 'monospace'], index=0, key="text_fontfamily")
                if st.button("📚 查看字体族选项", key="btn_fontfamily"):
                    from catalogs.text import render_fontfamily_gallery
                    render_fontfamily_gallery()
        
        with col_view:
            fig, ax = plt.subplots(figsize=(8, 5))
            x = np.linspace(0, 10, 50)
            y = np.sin(x)
            ax.plot(x, y, linewidth=2, color='#2c3e50')
            ax.set_title("标题示例", fontsize=fontsize_val, fontweight=fontweight_val, fontfamily=fontfamily_val)
            ax.set_xlabel("X 轴标签", fontsize=fontsize_val-2, fontfamily=fontfamily_val)
            ax.set_ylabel("Y 轴标签", fontsize=fontsize_val-2, fontfamily=fontfamily_val)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
            st.markdown("#### 💻 生成代码")
            st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, linewidth=2)
ax.set_title("标题示例", fontsize={fontsize_val}, 
             fontweight='{fontweight_val}', 
             fontfamily='{fontfamily_val}')
ax.set_xlabel("X 轴标签", fontsize={fontsize_val-2}, 
              fontfamily='{fontfamily_val}')
ax.set_ylabel("Y 轴标签", fontsize={fontsize_val-2}, 
              fontfamily='{fontfamily_val}')
ax.grid(True, alpha=0.3)
plt.show()
            """, language='python')
    
    with style_tabs[3]:
        st.subheader("坐标轴设置")
        st.caption("💡 学习如何控制坐标轴的范围、网格和边框")
        
        col_ctrl, col_view = st.columns([1.2, 2])
        
        with col_ctrl:
            st.markdown("#### 📊 坐标轴参数")
            
            with st.expander("📏 坐标范围 (xlim/ylim)", expanded=True):
                x_min = st.number_input("X 最小值", value=0.0, key="axes_xmin")
                x_max = st.number_input("X 最大值", value=10.0, key="axes_xmax")
                y_min = st.number_input("Y 最小值", value=-1.5, key="axes_ymin")
                y_max = st.number_input("Y 最大值", value=1.5, key="axes_ymax")
                if st.button("📚 查看坐标范围选项", key="btn_xlim"):
                    from catalogs.axes import render_xlim_ylim_gallery
                    render_xlim_ylim_gallery()
            
            with st.expander("🔲 网格 (grid)", expanded=True):
                show_grid = st.checkbox("显示网格", value=True, key="axes_grid")
                grid_alpha = st.slider("网格透明度", 0.1, 1.0, 0.3, 0.1, key="grid_alpha")
                if st.button("📚 查看网格选项", key="btn_grid"):
                    from catalogs.axes import render_grid_gallery
                    render_grid_gallery()
            
            with st.expander("📐 边框 (spines)", expanded=True):
                hide_top = st.checkbox("隐藏上边框", key="spine_top")
                hide_right = st.checkbox("隐藏右边框", key="spine_right")
                if st.button("📚 查看边框选项", key="btn_spines"):
                    from catalogs.axes import render_spines_gallery
                    render_spines_gallery()
        
        with col_view:
            x, y = generate_sample_data(50)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(x, y, linewidth=2, color='#2c3e50')
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
            if show_grid:
                ax.grid(True, alpha=grid_alpha)
            if hide_top:
                ax.spines['top'].set_visible(False)
            if hide_right:
                ax.spines['right'].set_visible(False)
            ax.set_title("坐标轴设置预览", fontsize=14, fontweight='bold')
            ax.set_xlabel("X 轴", fontsize=12)
            ax.set_ylabel("Y 轴", fontsize=12)
            st.pyplot(fig)
            
            st.markdown("#### 💻 生成代码")
            st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, linewidth=2)
ax.set_xlim({x_min}, {x_max})
ax.set_ylim({y_min}, {y_max})
{'ax.grid(True, alpha=' + str(grid_alpha) + ')' if show_grid else '# ax.grid(False)'}
{'ax.spines[\'top\'].set_visible(False)' if hide_top else ''}
{'ax.spines[\'right\'].set_visible(False)' if hide_right else ''}
ax.set_title("坐标轴设置预览", fontsize=14, fontweight='bold')
ax.set_xlabel("X 轴", fontsize=12)
ax.set_ylabel("Y 轴", fontsize=12)
plt.show()
            """, language='python')
        st.caption("调整下方的滑块，查看代码如何动态变化以适应不同的子图布局。")
        
        # 增加自由设置行列的功能
        c1, c2 = st.columns(2)
        rows = c1.number_input("行数 (Rows)", min_value=1, max_value=5, value=2)
        cols = c2.number_input("列数 (Columns)", min_value=1, max_value=5, value=2)

        col_img, col_code = st.columns([3, 2])
        
        with col_img:
            fig, axes = plt.subplots(rows, cols, figsize=(8, 6), constrained_layout=True)
            
            # 统一处理 axes，因为当 rows=1, cols=1 时，axes 不是数组
            if rows == 1 and cols == 1:
                axes_flat = [axes]
            else:
                axes_flat = axes.flatten()
                
            for i, ax in enumerate(axes_flat):
                ax.plot(np.random.rand(10), label=f"Line {i}")
                ax.set_title(f"Subplot {i+1}")
                ax.legend(loc='upper right', fontsize='small')
            st.pyplot(fig)
            
        with col_code:
            st.markdown("**实现代码：**")
            code_str = f"""
# {rows}行{cols}列布局，自动调整间距
fig, axes = plt.subplots({rows}, {cols}, 
    constrained_layout=True)

# 注意：当行列数变化时，axes 的形状会变化
# 推荐统一展平处理：
if {rows} * {cols} > 1:
    axes_flat = axes.flatten()
else:
    axes_flat = [axes]

for i, ax in enumerate(axes_flat):
    ax.plot(data)
    ax.set_title(f"Subplot {{i+1}}")
"""
            st.code(code_str, language='python')

        st.markdown("---")
        st.subheader("2. 全局样式 (Style Sheets)")
        
        style_select = st.selectbox("选择样式 (rcParams预设)", plt.style.available, index=plt.style.available.index('ggplot') if 'ggplot' in plt.style.available else 0)
        
        col1, col2 = st.columns([1,1])
        with col1:
            with plt.style.context(style_select):
                fig, ax = plt.subplots(figsize=(6,4))
                x = np.linspace(0, 10, 100)
                for i in range(1, 4):
                    ax.plot(x, np.sin(x + i * .5) * (7 - i), label=f"Wave {i}")
                ax.set_title(f"Style: {style_select}")
                ax.legend()
                st.pyplot(fig)
        with col2:
            st.markdown("**上下文管理器代码：**")
            st.code(f"""
# 临时应用样式，不影响全局
with plt.style.context('{style_select}'):
    fig, ax = plt.subplots()
    ax.plot(x, y)
            """, language='python')
                
        st.markdown("### 3. 图例 (Legend)")
        st.caption("💡 学习如何创建和自定义图例")
        
        legend_tabs = st.tabs(["基础图例", "图例位置", "图例样式"])
        
        with legend_tabs[0]:
            col_legend_demo, col_legend_code = st.columns([1, 1])
            with col_legend_demo:
                fig_legend, ax_legend = plt.subplots(figsize=(6, 4))
                x = np.linspace(0, 10, 100)
                ax_legend.plot(x, np.sin(x), label='sin(x)')
                ax_legend.plot(x, np.cos(x), label='cos(x)')
                ax_legend.plot(x, np.sin(x)*0.5, label='0.5*sin(x)')
                ax_legend.legend()
                ax_legend.grid(True, alpha=0.3)
                st.pyplot(fig_legend)
            with col_legend_code:
                st.code("""
ax.plot(x, y1, label='sin(x)')
ax.plot(x, y2, label='cos(x)')
ax.legend()  # 自动创建图例
                """, language='python')
        
        with legend_tabs[1]:
            legend_loc = st.selectbox("图例位置", 
                                    ['best', 'upper right', 'upper left', 'lower left', 'lower right',
                                     'right', 'center left', 'center right', 'lower center', 'upper center', 'center'],
                                    index=0, key="legend_loc_demo")
            fig_legend_loc, ax_legend_loc = plt.subplots(figsize=(6, 4))
            x = np.linspace(0, 10, 100)
            ax_legend_loc.plot(x, np.sin(x), label='sin(x)')
            ax_legend_loc.plot(x, np.cos(x), label='cos(x)')
            ax_legend_loc.legend(loc=legend_loc)
            ax_legend_loc.grid(True, alpha=0.3)
            st.pyplot(fig_legend_loc)
            st.code(f"ax.legend(loc='{legend_loc}')", language='python')
        
        with legend_tabs[2]:
            col_legend_style, col_legend_style_code = st.columns([1, 1])
            with col_legend_style:
                fig_legend_style, ax_legend_style = plt.subplots(figsize=(6, 4))
                x = np.linspace(0, 10, 100)
                ax_legend_style.plot(x, np.sin(x), label='sin(x)', linewidth=2)
                ax_legend_style.plot(x, np.cos(x), label='cos(x)', linewidth=2)
                ax_legend_style.legend(frameon=True, fancybox=True, shadow=True, 
                                     framealpha=0.9, ncol=2, fontsize=10)
                ax_legend_style.grid(True, alpha=0.3)
                st.pyplot(fig_legend_style)
            with col_legend_style_code:
                st.code("""
ax.legend(frameon=True,      # 显示边框
          fancybox=True,      # 圆角边框
          shadow=True,        # 阴影
          framealpha=0.9,     # 透明度
          ncol=2,            # 列数
          fontsize=10)       # 字体大小
                """, language='python')
        
        st.markdown("---")
        st.markdown("### 4. 注解 (Annotations)")
        st.caption("💡 学习如何添加箭头、文本标注等注解")
        
        annotation_tabs = st.tabs(["基础注解", "箭头样式", "高级注解"])
        
        with annotation_tabs[0]:
            col_anno_demo, col_anno_code = st.columns([1, 1])
            with col_anno_demo:
                fig_anno, ax_anno = plt.subplots(figsize=(6, 4))
                x = np.linspace(0, 10, 100)
                y = np.sin(x)
                ax_anno.plot(x, y)
                # 找到最大值点
                max_idx = np.argmax(y)
                max_x, max_y = x[max_idx], y[max_idx]
                ax_anno.annotate('最大值', xy=(max_x, max_y), xytext=(max_x+2, max_y+0.3),
                               arrowprops=dict(arrowstyle='->', color='red', lw=2))
                ax_anno.plot(max_x, max_y, 'ro', markersize=10)
                ax_anno.grid(True, alpha=0.3)
                st.pyplot(fig_anno)
            with col_anno_code:
                st.code("""
ax.annotate('最大值', 
            xy=(max_x, max_y),      # 箭头指向的点
            xytext=(max_x+2, max_y+0.3),  # 文字位置
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
                """, language='python')
        
        with annotation_tabs[1]:
            arrow_style = st.selectbox("箭头样式",
                                     ['->', '->>', '-', '-|>', '<-', '<->', '<|-', '<|-|>'],
                                     index=0, key="arrow_style_demo")
            fig_arrow, ax_arrow = plt.subplots(figsize=(6, 4))
            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            ax_arrow.plot(x, y)
            max_idx = np.argmax(y)
            max_x, max_y = x[max_idx], y[max_idx]
            ax_arrow.annotate(f'样式: {arrow_style}', xy=(max_x, max_y), 
                            xytext=(max_x+2, max_y+0.3),
                            arrowprops=dict(arrowstyle=arrow_style, color='red', lw=2))
            ax_arrow.plot(max_x, max_y, 'ro', markersize=10)
            ax_arrow.grid(True, alpha=0.3)
            st.pyplot(fig_arrow)
            st.code(f"arrowprops=dict(arrowstyle='{arrow_style}', color='red', lw=2)", language='python')
        
        with annotation_tabs[2]:
            col_anno_adv, col_anno_adv_code = st.columns([1, 1])
            with col_anno_adv:
                fig_anno_adv, ax_anno_adv = plt.subplots(figsize=(6, 4))
                x = np.linspace(0, 10, 100)
                y = np.sin(x)
                ax_anno_adv.plot(x, y, label='sin(x)')
                # 多个注解
                ax_anno_adv.annotate('起点', xy=(0, 0), xytext=(1, 0.5),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3'),
                                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
                ax_anno_adv.annotate('中点', xy=(5, np.sin(5)), xytext=(6, 0.5),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3'),
                                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
                ax_anno_adv.grid(True, alpha=0.3)
                st.pyplot(fig_anno_adv)
            with col_anno_adv_code:
                st.code("""
# 连接样式示例
ax.annotate('起点', xy=(0, 0), xytext=(1, 0.5),
           arrowprops=dict(arrowstyle='->', 
                          connectionstyle='arc3'),
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

# 弯曲连接
ax.annotate('中点', xy=(5, y[50]), xytext=(6, 0.5),
           arrowprops=dict(arrowstyle='->', 
                          connectionstyle='arc3,rad=0.3'))
                """, language='python')

# --- 章节 5: 进阶画廊 ---
elif menu == "5. 进阶画廊":
    st.title("Matplotlib 官方画廊复刻 (Advanced)")
    st.markdown("""
    <div style='background-color: #f3f4f6; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;'>
        <p style='margin: 0; color: #374151; text-align: center;'>
            🚀 探索 Matplotlib 的高级功能，复刻官方画廊经典案例
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    gallery_type = st.selectbox("选择画廊类别", [
        "3D Plotting (3D曲线)",
        "3D Surface (3D曲面)",
        "3D Scatter (3D散点)",
        "Polar Coordinates (极坐标)",
        "Vector Fields (Quiver矢量场)",
        "Streamplot (流线图)",
        "Contour (等高线)",
        "Heatmap (热力图)"
    ])
    
    col_viz, col_code = st.columns([3, 2])
    
    fig = plt.figure(figsize=(8, 6))
    code_display = ""
    
    if gallery_type == "3D Plotting (3D曲线)":
        ax = fig.add_subplot(111, projection='3d')
        n = 100
        theta = np.linspace(-4 * np.pi, 4 * np.pi, n)
        z = np.linspace(-2, 2, n)
        r = z**2 + 1
        x = r * np.sin(theta)
        y = r * np.cos(theta)
        ax.plot(x, y, z, label='3D Curve', linewidth=2)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title("3D Plotting (3D曲线)")
        code_display = """
from mpl_toolkits.mplot3d import Axes3D
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, linewidth=2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
"""

    elif gallery_type == "3D Surface (3D曲面)":
        ax = fig.add_subplot(111, projection='3d')
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(np.sqrt(X**2 + Y**2))
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9)
        fig.colorbar(surf, ax=ax)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title("3D Surface (3D曲面)")
        code_display = """
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))
surf = ax.plot_surface(X, Y, Z, cmap='viridis')
fig.colorbar(surf, ax=ax)
"""

    elif gallery_type == "3D Scatter (3D散点)":
        ax = fig.add_subplot(111, projection='3d')
        n = 100
        x = np.random.rand(n)
        y = np.random.rand(n)
        z = np.random.rand(n)
        colors = np.random.rand(n)
        ax.scatter(x, y, z, c=colors, cmap='viridis', s=50)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title("3D Scatter (3D散点)")
        code_display = """
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c=colors, cmap='viridis', s=50)
"""

    elif gallery_type == "Polar Coordinates (极坐标)":
        ax = fig.add_subplot(111, projection='polar')
        theta = np.linspace(0, 2*np.pi, 100)
        r = 2 * np.sin(4*theta)
        ax.plot(theta, r, color='crimson', linewidth=2)
        ax.set_title("Polar Plot (极坐标 - 玫瑰曲线)", pad=20)
        code_display = """
ax = fig.add_subplot(111, projection='polar')
ax.plot(theta, r) # 极坐标绘图
"""
        
    elif gallery_type == "Vector Fields (Quiver矢量场)":
        ax = fig.add_subplot(111)
        x, y = np.meshgrid(np.arange(0, 2 * np.pi, .2), np.arange(0, 2 * np.pi, .2))
        u = np.cos(x)
        v = np.sin(y)
        q = ax.quiver(x, y, u, v, scale=20)
        ax.set_title("Quiver Plot (矢量场)")
        code_display = """
x, y = np.meshgrid(np.arange(0, 2*np.pi, .2), np.arange(0, 2*np.pi, .2))
u, v = np.cos(x), np.sin(y)
ax.quiver(x, y, u, v, scale=20)
"""

    elif gallery_type == "Streamplot (流线图)":
        ax = fig.add_subplot(111)
        x = np.linspace(0, 2*np.pi, 20)
        y = np.linspace(0, 2*np.pi, 20)
        X, Y = np.meshgrid(x, y)
        U = np.cos(X)
        V = np.sin(Y)
        ax.streamplot(X, Y, U, V, density=1.5, color=U, linewidth=2, cmap='viridis')
        ax.set_title("Streamplot (流线图)")
        code_display = """
X, Y = np.meshgrid(x, y)
U, V = np.cos(X), np.sin(Y)
ax.streamplot(X, Y, U, V, density=1.5, color=U, cmap='viridis')
"""

    elif gallery_type == "Contour (等高线)":
        ax = fig.add_subplot(111)
        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X**2 + Y**2))
        contour = ax.contour(X, Y, Z, levels=10, cmap='viridis')
        ax.clabel(contour, inline=True, fontsize=8)
        ax.set_title("Contour Plot (等高线)")
        code_display = """
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2))
contour = ax.contour(X, Y, Z, levels=10, cmap='viridis')
ax.clabel(contour, inline=True, fontsize=8)
"""

    elif gallery_type == "Heatmap (热力图)":
        ax = fig.add_subplot(111)
        data = np.random.rand(10, 10)
        im = ax.imshow(data, cmap='viridis', aspect='auto')
        fig.colorbar(im, ax=ax)
        ax.set_title("Heatmap (热力图)")
        code_display = """
data = np.random.rand(10, 10)
im = ax.imshow(data, cmap='viridis', aspect='auto')
fig.colorbar(im, ax=ax)
"""

    with col_viz:
        st.pyplot(fig)
    with col_code:
        st.code(code_display, language='python')

# --- 章节 6: 其他库实战 ---
elif menu == "6. 其他库实战":
    st.title("超越 Matplotlib：现代库体验")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;'>
        <p style='margin: 0; text-align: center; font-weight: 500;'>
            🌟 体验现代可视化库的强大功能：Seaborn、Plotly、Altair、Bokeh等
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    lib_choice = st.selectbox("选择可视化库", [
        "Seaborn (统计)", 
        "Plotly (交互)", 
        "Altair (声明式)",
        "Pandas Plotting (数据驱动)",
        "Bokeh (Web交互)"
    ])
    df = px.data.iris() 
    
    if lib_choice == "Seaborn (统计)":
        st.subheader("Seaborn: 极简统计图")
        st.info("Seaborn 基于 Matplotlib，提供更美观的统计图表。")
        
        seaborn_tabs = st.tabs(["联合分布图", "分类图", "关系图"])
        
        with seaborn_tabs[0]:
            col_x = st.selectbox("X 轴", df.columns[:-2], key="sns_x")
            col_y = st.selectbox("Y 轴", df.columns[:-2], index=1, key="sns_y")
            
            fig = sns.jointplot(data=df, x=col_x, y=col_y, hue="species", kind="scatter")
            st.pyplot(fig)
            st.code(f"sns.jointplot(data=df, x='{col_x}', y='{col_y}', hue='species', kind='scatter')", language='python')
        
        with seaborn_tabs[1]:
            fig_cat, ax_cat = plt.subplots(figsize=(8, 5))
            sns.boxplot(data=df, x='species', y='sepal_length', ax=ax_cat)
            ax_cat.set_title("Seaborn Boxplot", fontweight='bold')
            st.pyplot(fig_cat)
            st.code("sns.boxplot(data=df, x='species', y='sepal_length')", language='python')
        
        with seaborn_tabs[2]:
            fig_rel, ax_rel = plt.subplots(figsize=(8, 5))
            sns.scatterplot(data=df, x='sepal_length', y='sepal_width', hue='species', style='species', ax=ax_rel)
            ax_rel.set_title("Seaborn Scatterplot", fontweight='bold')
            st.pyplot(fig_rel)
            st.code("sns.scatterplot(data=df, x='sepal_length', y='sepal_width', hue='species', style='species')", language='python')

    elif lib_choice == "Plotly (交互)":
        st.subheader("Plotly: 网页原生交互")
        st.info("Plotly 提供丰富的交互功能，适合Web应用。")
        
        plotly_tabs = st.tabs(["3D散点", "交互式线图", "热力图"])
        
        with plotly_tabs[0]:
            fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
                          color='species', size='petal_length', opacity=0.7)
            st.plotly_chart(fig, use_container_width=True)
            st.code("px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width', color='species')", language='python')
        
        with plotly_tabs[1]:
            fig_line = px.line(df.head(20), x='sepal_length', y='sepal_width', color='species')
            st.plotly_chart(fig_line, use_container_width=True)
            st.code("px.line(df, x='sepal_length', y='sepal_width', color='species')", language='python')
        
        with plotly_tabs[2]:
            fig_heat = px.density_heatmap(df, x='sepal_length', y='sepal_width', nbinsx=20, nbinsy=20)
            st.plotly_chart(fig_heat, use_container_width=True)
            st.code("px.density_heatmap(df, x='sepal_length', y='sepal_width')", language='python')

    elif lib_choice == "Altair (声明式)":
        st.subheader("Altair: 语法驱动")
        st.info("Altair 使用声明式语法，代码简洁优雅。")
        
        altair_tabs = st.tabs(["基础图表", "交互式图表", "组合图表"])
        
        with altair_tabs[0]:
            chart = alt.Chart(df).mark_point().encode(
                x='sepal_length',
                y='sepal_width',
                color='species',
                size='petal_length'
            )
            st.altair_chart(chart, use_container_width=True)
            st.code("""
alt.Chart(df).mark_point().encode(
    x='sepal_length',
    y='sepal_width',
    color='species',
    size='petal_length'
)
            """, language='python')
        
        with altair_tabs[1]:
            brush = alt.selection_interval()
            points = alt.Chart(df).mark_point().encode(
                x='sepal_length', y='sepal_width',
                color=alt.condition(brush, 'species', alt.value('lightgray'))
            ).add_params(brush)
            bars = alt.Chart(df).mark_bar().encode(
                y='species', color='species', x='count(species)'
            ).transform_filter(brush)
            
            st.altair_chart(points & bars, use_container_width=True)
            st.code("""
brush = alt.selection_interval()
points = alt.Chart(df).mark_point().encode(...).add_params(brush)
bars = alt.Chart(df).mark_bar().encode(...).transform_filter(brush)
chart = points & bars
            """, language='python')
        
        with altair_tabs[2]:
            chart1 = alt.Chart(df).mark_bar().encode(x='species', y='mean(sepal_length)')
            chart2 = alt.Chart(df).mark_point().encode(x='sepal_length', y='sepal_width', color='species')
            combined = chart1 | chart2
            st.altair_chart(combined, use_container_width=True)
            st.code("""
chart1 = alt.Chart(df).mark_bar().encode(...)
chart2 = alt.Chart(df).mark_point().encode(...)
combined = chart1 | chart2  # 水平组合
            """, language='python')
    
    elif lib_choice == "Pandas Plotting (数据驱动)":
        st.subheader("Pandas Plotting: 数据驱动可视化")
        st.info("Pandas 内置的绘图接口，与DataFrame无缝集成。")
        
        pandas_tabs = st.tabs(["线图", "柱状图", "散点图", "直方图"])
        
        with pandas_tabs[0]:
            fig_pd_line, ax_pd_line = plt.subplots(figsize=(8, 5))
            df.head(20).plot(x='sepal_length', y='sepal_width', ax=ax_pd_line, kind='line')
            ax_pd_line.set_title("Pandas Line Plot", fontweight='bold')
            st.pyplot(fig_pd_line)
            st.code("df.plot(x='sepal_length', y='sepal_width', kind='line')", language='python')
        
        with pandas_tabs[1]:
            fig_pd_bar, ax_pd_bar = plt.subplots(figsize=(8, 5))
            df.groupby('species')['sepal_length'].mean().plot(kind='bar', ax=ax_pd_bar)
            ax_pd_bar.set_title("Pandas Bar Plot", fontweight='bold')
            ax_pd_bar.set_ylabel("平均 Sepal Length")
            st.pyplot(fig_pd_bar)
            st.code("df.groupby('species')['sepal_length'].mean().plot(kind='bar')", language='python')
        
        with pandas_tabs[2]:
            fig_pd_scatter, ax_pd_scatter = plt.subplots(figsize=(8, 5))
            df.plot(x='sepal_length', y='sepal_width', kind='scatter', ax=ax_pd_scatter, c=df['species'].astype('category').cat.codes, cmap='viridis')
            ax_pd_scatter.set_title("Pandas Scatter Plot", fontweight='bold')
            st.pyplot(fig_pd_scatter)
            st.code("df.plot(x='sepal_length', y='sepal_width', kind='scatter')", language='python')
        
        with pandas_tabs[3]:
            fig_pd_hist, ax_pd_hist = plt.subplots(figsize=(8, 5))
            df['sepal_length'].plot(kind='hist', bins=20, ax=ax_pd_hist)
            ax_pd_hist.set_title("Pandas Histogram", fontweight='bold')
            st.pyplot(fig_pd_hist)
            st.code("df['sepal_length'].plot(kind='hist', bins=20)", language='python')
    
    else:  # Bokeh
        st.subheader("Bokeh: Web交互式可视化")
        st.info("Bokeh 专为Web设计，提供强大的交互功能。")
        st.warning("⚠️ 注意：Bokeh 在网页中需要特殊处理，这里展示代码示例。")
        
        st.code("""
from bokeh.plotting import figure, show
from bokeh.io import output_notebook

# 创建图表
p = figure(width=400, height=300)
p.circle(df['sepal_length'], df['sepal_width'], 
         size=10, color='blue', alpha=0.5)

# 添加工具
p.toolbar_location = "above"
p.toolbar.active_drag = None

show(p)
        """, language='python')
        
        st.markdown("""
        **Bokeh 特点**：
        - 专为Web设计
        - 丰富的交互工具（缩放、平移、悬停等）
        - 支持服务器端应用
        - 可以导出为HTML文件
        """)

# --- 章节 7: 进阶挑战 (大师之路) ---
elif menu == "7. 进阶挑战：大师之路 🚀":
    st.title("🏆 Matplotlib 大神进阶之路")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                color: white; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0;'>
        <h3 style='color: white; margin: 0 0 0.5rem 0;'>🎯 挑战目标</h3>
        <p style='margin: 0; opacity: 0.95;'>本章节复刻了专业数据分析中<strong>最高频、最难</strong>的三个场景。请点击 Tab 切换学习。</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab_layout, tab_dual, tab_fmt, tab_gspec, tab_anim = st.tabs([
        "1. 复杂仪表盘 (Mosaic Layout)", 
        "2. 双轴帕累托图 (Dual Axis)", 
        "3. 专业格式化 (Formatter)",
        "4. GridSpec 高级布局",
        "5. 动画制作 (Animation)"
    ])
    
    # --- 挑战 1: 语义化布局 ---
    with tab_layout:
        st.header("利用 subplot_mosaic 进行语义化布局")
        st.markdown("放弃 `GridSpec` 的复杂索引，使用 ASCII 字符画来定义你的仪表盘布局。")
        
        col_viz, col_code = st.columns([1.5, 1])
        
        # 修正：移除空格，确保 contiguous 连续性
        layout_str = """
        AAB
        AAC
        DDD
        """
        
        with col_viz:
            fig, axd = plt.subplot_mosaic(layout_str, figsize=(10, 6), constrained_layout=True)
            
            # 模拟绘图
            axd['A'].plot(np.cumsum(np.random.randn(100)), color='#2c3e50')
            axd['A'].set_title("Main Trend (A)")
            
            axd['B'].hist(np.random.randn(100), color='#e74c3c')
            axd['B'].set_title("Dist (B)")
            
            axd['C'].scatter(np.random.rand(20), np.random.rand(20), color='#f1c40f')
            axd['C'].set_title("Scatter (C)")
            
            axd['D'].bar(['Q1','Q2','Q3','Q4'], [10,20,15,25], color='#3498db')
            axd['D'].set_title("Quarterly (D)")
            
            st.pyplot(fig)
            
        with col_code:
            st.code("""
# 1. 定义布局 (ASCII Art)
# 修正：移除中间空格，确保D是连续的
layout = \"\"\"
AAB
AAC
DDD
\"\"\"

# 2. 生成 Axes 字典 (axd)
fig, axd = plt.subplot_mosaic(layout, 
    figsize=(10, 6), 
    constrained_layout=True)

# 3. 像字典一样访问
axd['A'].plot(data)
axd['B'].hist(data)
            """, language='python')
            
    # --- 挑战 2: 双轴图 ---
    with tab_dual:
        st.header("双轴图 (Twin Axis) 与 帕累托图")
        st.markdown("在同一个 X 轴上展示两个不同量纲的数据（例如：销售额 vs 累计百分比）。")
        
        col_viz, col_code = st.columns([1.5, 1])
        
        data = pd.DataFrame({'Sales': [100, 80, 50, 30, 10]}, index=['Product A', 'B', 'C', 'D', 'E'])
        data['CumPct'] = data['Sales'].cumsum() / data['Sales'].sum() * 100
        
        with col_viz:
            fig, ax1 = plt.subplots(figsize=(10, 5))
            
            # 轴1：柱状图
            color = 'tab:blue'
            ax1.set_xlabel('Product')
            ax1.set_ylabel('Sales Volume', color=color)
            ax1.bar(data.index, data['Sales'], color=color, alpha=0.6)
            ax1.tick_params(axis='y', labelcolor=color)
            
            # 轴2：共享 X 轴
            ax2 = ax1.twinx()  
            color = 'tab:red'
            ax2.set_ylabel('Cumulative %', color=color)
            ax2.plot(data.index, data['CumPct'], color=color, marker='o', linewidth=2)
            ax2.tick_params(axis='y', labelcolor=color)
            ax2.set_ylim(0, 110)
            
            st.pyplot(fig)
            
        with col_code:
            st.code("""
fig, ax1 = plt.subplots()

# 绘制左轴
ax1.bar(x, sales, color='blue')
ax1.set_ylabel('Sales', color='blue')

# 关键：实例化共享 X 轴的第二个轴
ax2 = ax1.twinx()

# 绘制右轴
ax2.plot(x, pct, color='red')
ax2.set_ylabel('Percentage', color='red')
            """, language='python')

    # --- 挑战 3: 格式化 ---
    with tab_fmt:
        st.header("专业格式化 (FuncFormatter)")
        st.markdown("将丑陋的科学计数法（1e6）转换为可读性强的商业格式（$1M）。")
        
        col_viz, col_code = st.columns([1.5, 1])
        
        with col_viz:
            money = [1500000, 2500000, 3800000]
            names = ['A Corp', 'B Corp', 'C Corp']
            
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(names, money, color='#16a085')
            
            # 定义格式化函数
            def currency(x, pos):
                if x >= 1e6:
                    return f'${x*1e-6:.1f}M'
                return f'${x:.0f}'
            
            # 应用 Formatter
            formatter = FuncFormatter(currency)
            ax.xaxis.set_major_formatter(formatter)
            ax.set_title("Revenue (Formatted)")
            
            st.pyplot(fig)
            
        with col_code:
            st.code("""
from matplotlib.ticker import FuncFormatter

def currency(x, pos):
    if x >= 1e6:
        return f'${x*1e-6:.1f}M'
    return f'${x:.0f}'

formatter = FuncFormatter(currency)
ax.xaxis.set_major_formatter(formatter)
            """, language='python')
    
    # --- 挑战 4: GridSpec 高级布局 ---
    with tab_gspec:
        st.header("GridSpec: 灵活的子图布局")
        st.markdown("使用 `GridSpec` 创建非均匀、跨行列的复杂布局。")
        
        col_gspec_demo, col_gspec_code = st.columns([1.5, 1])
        
        with col_gspec_demo:
            from matplotlib.gridspec import GridSpec
            
            fig_gspec = plt.figure(figsize=(10, 6))
            gs = GridSpec(3, 3, figure=fig_gspec, hspace=0.3, wspace=0.3)
            
            # 大图占据左侧2x2
            ax_main = fig_gspec.add_subplot(gs[0:2, 0:2])
            x = np.linspace(0, 10, 100)
            ax_main.plot(x, np.sin(x), label='sin(x)')
            ax_main.plot(x, np.cos(x), label='cos(x)')
            ax_main.set_title("主图 (2x2)", fontweight='bold')
            ax_main.legend()
            ax_main.grid(True, alpha=0.3)
            
            # 右上角小图
            ax_top = fig_gspec.add_subplot(gs[0, 2])
            ax_top.hist(np.random.randn(100), bins=20)
            ax_top.set_title("直方图", fontsize=9)
            
            # 右中小图
            ax_mid = fig_gspec.add_subplot(gs[1, 2])
            ax_mid.scatter(np.random.rand(50), np.random.rand(50))
            ax_mid.set_title("散点图", fontsize=9)
            
            # 底部横跨3列
            ax_bottom = fig_gspec.add_subplot(gs[2, :])
            ax_bottom.bar(['A', 'B', 'C', 'D'], [10, 20, 15, 25])
            ax_bottom.set_title("底部条形图 (跨3列)", fontweight='bold')
            
            st.pyplot(fig_gspec)
        
        with col_gspec_code:
            st.code("""
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(10, 6))
gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

# 主图：占据 [0:2, 0:2] (左上2x2)
ax_main = fig.add_subplot(gs[0:2, 0:2])
ax_main.plot(x, y)

# 右上角：占据 [0, 2]
ax_top = fig.add_subplot(gs[0, 2])
ax_top.hist(data)

# 底部：占据 [2, :] (跨所有列)
ax_bottom = fig.add_subplot(gs[2, :])
ax_bottom.bar(categories, values)
            """, language='python')
        
        st.markdown("---")
        st.markdown("#### GridSpec vs subplot_mosaic")
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            st.markdown("**GridSpec (传统方法)**")
            st.code("""
from matplotlib.gridspec import GridSpec
gs = GridSpec(2, 2)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
            """, language='python')
            st.caption("✅ 灵活但需要手动计算索引")
        
        with col_comp2:
            st.markdown("**subplot_mosaic (推荐)**")
            st.code("""
layout = \"\"\"
AAB
AAC
DDD
\"\"\"
fig, axd = plt.subplot_mosaic(layout)
axd['A'].plot(x, y)
            """, language='python')
            st.caption("✅ 直观，使用ASCII字符画布局")
    
    # --- 挑战 5: 动画制作 ---
    with tab_anim:
        st.header("动画制作 (Animation)")
        st.markdown("使用 Matplotlib 的 `animation` 模块创建动态图表。")
        
        st.info("""
        **注意**：网页中无法直接显示动画，这里展示代码示例和静态预览。
        实际运行时需要使用 `plt.show()` 或保存为 GIF/MP4 文件。
        """)
        
        anim_type = st.selectbox("选择动画类型", 
                                ["动态线图", "动态散点", "3D动画", "保存动画"],
                                key="anim_type")
        
        if anim_type == "动态线图":
            st.code("""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(0, 2*np.pi, 100)
line, = ax.plot([], [], lw=2)
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1, 1)
ax.grid(True)

def animate(frame):
    y = np.sin(x + frame * 0.1)
    line.set_data(x, y)
    return line,

ani = animation.FuncAnimation(fig, animate, frames=100, 
                              interval=50, blit=True)
plt.show()
            """, language='python')
            
            # 静态预览
            fig_anim_preview, ax_anim_preview = plt.subplots(figsize=(8, 5))
            x_preview = np.linspace(0, 2*np.pi, 100)
            y_preview = np.sin(x_preview)
            ax_anim_preview.plot(x_preview, y_preview, lw=2)
            ax_anim_preview.set_xlim(0, 2*np.pi)
            ax_anim_preview.set_ylim(-1, 1)
            ax_anim_preview.set_title("动画预览（静态帧）", fontweight='bold')
            ax_anim_preview.grid(True, alpha=0.3)
            st.pyplot(fig_anim_preview)
        
        elif anim_type == "动态散点":
            st.code("""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots(figsize=(8, 5))
scatter = ax.scatter([], [], s=100)
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

def animate(frame):
    n = 50
    x = np.random.rand(n) * 2 - 1
    y = np.random.rand(n) * 2 - 1
    scatter.set_offsets(np.c_[x, y])
    return scatter,

ani = animation.FuncAnimation(fig, animate, frames=100, 
                              interval=100, blit=True)
plt.show()
            """, language='python')
        
        elif anim_type == "3D动画":
            st.code("""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def animate(frame):
    ax.clear()
    theta = np.linspace(0, 2*np.pi, 100)
    z = np.linspace(0, 10, 100)
    r = 1 + np.sin(frame * 0.1)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    ax.plot(x, y, z)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(0, 10)

ani = animation.FuncAnimation(fig, animate, frames=100, interval=50)
plt.show()
            """, language='python')
        
        else:  # 保存动画
            st.code("""
import matplotlib.animation as animation

# 创建动画
ani = animation.FuncAnimation(fig, animate, frames=100, interval=50)

# 保存为GIF（需要pillow）
ani.save('animation.gif', writer='pillow', fps=20)

# 保存为MP4（需要ffmpeg）
ani.save('animation.mp4', writer='ffmpeg', fps=20)

# 保存为HTML（JavaScript动画）
from matplotlib.animation import HTMLWriter
ani.save('animation.html', writer=HTMLWriter())
            """, language='python')
            
            st.markdown("""
            **保存格式说明**：
            - **GIF**: 需要 `pillow` 库，适合简单动画
            - **MP4**: 需要 `ffmpeg`，适合复杂动画
            - **HTML**: JavaScript动画，可在浏览器中播放
            """)

# --- 页脚 ---
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem 0; color: #6b7280; font-size: 0.85rem;'>
    <p style='margin: 0;'>📚 计算社会学可视化教学</p>
    <p style='margin: 0.5rem 0 0 0;'>Bin Wang, SEU</p>
</div>
""", unsafe_allow_html=True)