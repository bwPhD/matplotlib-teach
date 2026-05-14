"""
通用工具函数
"""
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from typing import Tuple
import warnings
from pathlib import Path

LOCAL_CHINESE_FONT = Path(__file__).resolve().parent.parent / "LXGWWenKai-Regular.ttf"
_local_chinese_font_name = None


def _register_local_chinese_font():
    global _local_chinese_font_name
    if _local_chinese_font_name:
        return _local_chinese_font_name

    if not LOCAL_CHINESE_FONT.exists():
        return None

    try:
        fm.fontManager.addfont(str(LOCAL_CHINESE_FONT))
        _local_chinese_font_name = fm.FontProperties(fname=str(LOCAL_CHINESE_FONT)).get_name()
        return _local_chinese_font_name
    except Exception as exc:
        warnings.warn(f"Failed to load local Chinese font: {exc}")
        return None

# 配置中文字体支持
def setup_chinese_font():
    """设置中文字体，优先使用开源字体"""
    local_font_name = _register_local_chinese_font()

    # 尝试的中文字体列表（按优先级排序）
    chinese_fonts = [
        local_font_name,
        'LXGW WenKai',
        'SimHei',           # 黑体（Windows）
        'Microsoft YaHei',  # 微软雅黑（Windows）
        'WenQuanYi Micro Hei',  # 文泉驿微米黑（Linux）
        'WenQuanYi Zen Hei',   # 文泉驿正黑（Linux）
        'Noto Sans CJK SC',    # Noto Sans（跨平台）
        'Source Han Sans CN',   # 思源黑体（跨平台）
        'STHeiti',          # 华文黑体（macOS）
        'Arial Unicode MS', # Arial Unicode（跨平台）
        'sans-serif',       # 回退到系统默认
    ]
    chinese_fonts = [font for font in chinese_fonts if font]
    
    # 获取系统可用字体
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    # 查找第一个可用的中文字体
    for font in chinese_fonts:
        if font in available_fonts:
            # 确保字体在列表最前面，避免被覆盖
            current_fonts = plt.rcParams['font.sans-serif']
            if font not in current_fonts or current_fonts[0] != font:
                plt.rcParams['font.sans-serif'] = [font] + [f for f in current_fonts if f != font]
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            return font
    
    # 如果没有找到，使用通用设置
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    return 'sans-serif'

# 初始化中文字体（全局设置）
_chinese_font_initialized = False

def ensure_chinese_font():
    """确保中文字体已配置（每次调用都会检查并设置）"""
    global _chinese_font_initialized
    # 总是调用 setup_chinese_font() 以确保字体正确设置
    # 这样可以处理字体设置被重置的情况
    setup_chinese_font()
    _chinese_font_initialized = True

@st.cache_data
def get_matplotlib_version() -> str:
    """获取 Matplotlib 版本"""
    return plt.matplotlib.__version__

def generate_sample_data(n_points: int = 50) -> Tuple[np.ndarray, np.ndarray]:
    """生成示例数据（正弦波）"""
    ensure_chinese_font()
    x = np.linspace(0, 10, n_points)
    y = np.sin(x)
    return x, y

def generate_sample_data_steps(n_points: int = 20) -> Tuple[np.ndarray, np.ndarray]:
    """生成阶梯数据（用于测试 drawstyle）"""
    ensure_chinese_font()
    x = np.linspace(0, 10, n_points)
    y = np.sin(x) + np.random.randn(n_points) * 0.1
    return x, y

