"""
防爬虫机制模块
提供基本的爬虫检测和防护功能
"""
import streamlit as st
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import hashlib

# 常见的爬虫 User-Agent 列表
CRAWLER_USER_AGENTS = [
    'scrapy', 'requests', 'urllib', 'curl', 'wget', 'python-requests',
    'bot', 'crawler', 'spider', 'scraper', 'crawling', 'python',
    'mechanize', 'beautifulsoup', 'selenium', 'headless', 'phantom',
    'googlebot', 'bingbot', 'baiduspider', 'yandexbot', 'slurp',
    'duckduckbot', 'facebookexternalhit', 'twitterbot', 'rogerbot',
    'linkedinbot', 'embedly', 'quora', 'pinterest', 'slackbot',
    'redditbot', 'applebot', 'flipboard', 'tumblr', 'bitlybot',
    'skypeuripreview', 'nuzzel', 'discordbot', 'qwantify', 'pinterestbot',
    'bitrix link preview', 'xing-contenttabreceiver', 'chrome-lighthouse',
    'telegrambot', 'apple-preview', 'viberpreview', 'friendly', 'whatsapp',
    'flipboardproxy', 'developers.google.com/+/web/snippet', 'vkShare',
    'W3C_Validator', 'facebook', 'facebot', 'ia_archiver'
]

# 可疑的请求特征
SUSPICIOUS_PATTERNS = [
    'headless', 'phantom', 'selenium', 'webdriver', 'automation',
    'test', 'crawler', 'bot', 'spider', 'scraper'
]

# 访问频率限制配置
RATE_LIMIT_CONFIG = {
    'max_requests_per_minute': 30,  # 每分钟最大请求数
    'max_requests_per_hour': 500,   # 每小时最大请求数
    'block_duration_minutes': 60,   # 封禁时长（分钟）
}


def get_client_ip() -> Optional[str]:
    """
    获取客户端 IP 地址
    注意：Streamlit 无法直接获取真实 IP，这里返回 session_id 的哈希值作为标识
    """
    try:
        # 使用 session_id 作为唯一标识
        session_id = st.session_state.get('session_id', str(id(st.session_state)))
        return hashlib.md5(session_id.encode()).hexdigest()[:12]
    except:
        return None


def check_user_agent() -> bool:
    """
    检查 User-Agent（通过 JavaScript 注入）
    返回 True 表示可能是正常浏览器，False 表示可能是爬虫
    """
    # 由于 Streamlit 的限制，我们使用 session state 来存储检查结果
    if 'ua_check_done' not in st.session_state:
        # 注入 JavaScript 检查 User-Agent
        st.markdown("""
        <script>
        (function() {
            const ua = navigator.userAgent.toLowerCase();
            const isSuspicious = %s;
            if (isSuspicious) {
                window.parent.postMessage({type: 'suspicious_ua', ua: ua}, '*');
            }
        })();
        </script>
        """ % str([pattern for pattern in CRAWLER_USER_AGENTS if pattern.lower() in 'navigator.userAgent.toLowerCase()']).replace("'", '"'), 
        unsafe_allow_html=True)
        st.session_state['ua_check_done'] = True
        # 默认允许访问，因为无法直接获取 UA
        return True
    return True


def check_rate_limit() -> bool:
    """
    检查访问频率限制
    返回 True 表示允许访问，False 表示超过限制
    """
    client_id = get_client_ip()
    if not client_id:
        return True
    
    current_time = time.time()
    
    # 初始化访问记录
    if 'access_records' not in st.session_state:
        st.session_state['access_records'] = {}
    
    if client_id not in st.session_state['access_records']:
        st.session_state['access_records'][client_id] = {
            'requests': [],
            'blocked_until': None
        }
    
    record = st.session_state['access_records'][client_id]
    
    # 检查是否被封禁
    if record['blocked_until'] and current_time < record['blocked_until']:
        return False
    
    # 清除封禁状态
    if record['blocked_until'] and current_time >= record['blocked_until']:
        record['blocked_until'] = None
    
    # 清理过期的请求记录（保留最近1小时）
    one_hour_ago = current_time - 3600
    record['requests'] = [req_time for req_time in record['requests'] if req_time > one_hour_ago]
    
    # 检查每分钟请求数
    one_minute_ago = current_time - 60
    recent_requests = [req_time for req_time in record['requests'] if req_time > one_minute_ago]
    
    if len(recent_requests) >= RATE_LIMIT_CONFIG['max_requests_per_minute']:
        # 封禁该客户端
        record['blocked_until'] = current_time + (RATE_LIMIT_CONFIG['block_duration_minutes'] * 60)
        return False
    
    # 检查每小时请求数
    if len(record['requests']) >= RATE_LIMIT_CONFIG['max_requests_per_hour']:
        record['blocked_until'] = current_time + (RATE_LIMIT_CONFIG['block_duration_minutes'] * 60)
        return False
    
    # 记录本次请求
    record['requests'].append(current_time)
    
    return True


def check_suspicious_behavior() -> bool:
    """
    检查可疑行为模式
    """
    # 检查是否在短时间内频繁切换页面
    if 'page_switches' not in st.session_state:
        st.session_state['page_switches'] = []
    
    current_time = time.time()
    # 清理5分钟前的记录
    five_minutes_ago = current_time - 300
    st.session_state['page_switches'] = [
        switch_time for switch_time in st.session_state['page_switches'] 
        if switch_time > five_minutes_ago
    ]
    
    # 如果5分钟内切换超过20次，视为可疑
    if len(st.session_state['page_switches']) > 20:
        return False
    
    return True


def log_access(action: str = "access"):
    """
    记录访问日志
    """
    client_id = get_client_ip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if 'access_log' not in st.session_state:
        st.session_state['access_log'] = []
    
    log_entry = {
        'timestamp': timestamp,
        'client_id': client_id,
        'action': action
    }
    
    st.session_state['access_log'].append(log_entry)
    
    # 只保留最近100条日志
    if len(st.session_state['access_log']) > 100:
        st.session_state['access_log'] = st.session_state['access_log'][-100:]


def check_access() -> tuple[bool, Optional[str]]:
    """
    综合检查访问权限
    返回 (是否允许访问, 拒绝原因)
    """
    # 1. 检查频率限制
    if not check_rate_limit():
        log_access("rate_limit_exceeded")
        return False, "访问频率过高，请稍后再试"
    
    # 2. 检查可疑行为
    if not check_suspicious_behavior():
        log_access("suspicious_behavior")
        return False, "检测到异常访问模式"
    
    # 3. 记录正常访问
    log_access("normal_access")
    
    return True, None


def show_blocked_message(reason: str):
    """
    显示封禁提示页面
    """
    st.error("🚫 访问被限制")
    st.markdown(f"""
    <div style='padding: 2rem; text-align: center; background-color: #fef2f2; border-radius: 8px; border: 2px solid #ef4444;'>
        <h2 style='color: #dc2626;'>访问受限</h2>
        <p style='color: #991b1b; font-size: 1.1rem; margin: 1rem 0;'>{reason}</p>
        <p style='color: #7f1d1d;'>如果您是正常用户，请稍后再试。如持续遇到此问题，请联系管理员。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()


def init_anti_crawler():
    """
    初始化防爬虫机制
    应该在应用启动时调用
    """
    # 初始化 session_id
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(time.time()) + str(id(st.session_state))
    
    # 执行访问检查
    allowed, reason = check_access()
    
    if not allowed:
        show_blocked_message(reason)
    
    # 记录页面切换
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = None
    
    # 如果页面切换，记录时间
    # 注意：这个需要在主应用中调用时传入当前页面标识




