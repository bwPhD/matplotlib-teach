#!/usr/bin/env python3
"""
Streamlit 应用唤醒脚本

使用 Selenium 自动访问 Streamlit Cloud 应用，防止应用休眠。
适用于 Streamlit Cloud 的免费层应用会自动休眠的情况。

使用方法：
1. 在 GitHub Secrets 中设置 STREAMLIT_URL
2. 配置 GitHub Actions 定时运行此脚本
"""

import os
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('.github/logs/wake_up.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def setup_driver():
    """设置 Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')

    # 使用 webdriver-manager 自动管理 ChromeDriver
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)

    return driver

def wait_for_app_load(driver, timeout=30):
    """等待应用加载完成"""
    try:
        # 等待 Streamlit 应用的主要内容加载
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

        # 等待 Streamlit 特有的元素出现
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main"))
        )

        logger.info("应用页面加载完成")
        return True

    except Exception as e:
        logger.error(f"等待应用加载超时: {e}")
        return False

def interact_with_app(driver):
    """与应用进行简单交互以确保唤醒"""
    try:
        # 等待一下让页面完全加载
        time.sleep(2)

        # 尝试点击一些元素来唤醒应用
        # 对于 Streamlit 应用，通常点击侧边栏或主要内容区域

        # 查找并点击第一个可点击的元素
        try:
            # 尝试点击 Streamlit 的主要内容区域
            main_content = driver.find_element(By.CLASS_NAME, "main")
            main_content.click()
            logger.info("点击了主内容区域")
            time.sleep(1)
        except Exception:
            pass

        # 尝试滚动页面
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        logger.info("成功与应用进行交互")
        return True

    except Exception as e:
        logger.error(f"与应用交互失败: {e}")
        return False

def wake_up_streamlit_app(app_url, max_retries=3):
    """
    唤醒 Streamlit 应用

    Args:
        app_url: Streamlit 应用的 URL
        max_retries: 最大重试次数
    """
    driver = None

    for attempt in range(max_retries):
        try:
            logger.info(f"尝试唤醒应用 (第 {attempt + 1} 次): {app_url}")

            # 设置 WebDriver
            driver = setup_driver()

            # 访问应用
            driver.get(app_url)
            logger.info(f"已访问 URL: {app_url}")

            # 等待应用加载
            if not wait_for_app_load(driver):
                logger.warning(f"应用加载失败 (尝试 {attempt + 1})")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                else:
                    return False

            # 与应用交互
            if interact_with_app(driver):
                logger.info(f"✅ 应用唤醒成功: {app_url}")
                return True
            else:
                logger.warning(f"应用交互失败 (尝试 {attempt + 1})")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                else:
                    return False

        except Exception as e:
            logger.error(f"唤醒应用时出错 (尝试 {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            else:
                return False

        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass

    return False

def main():
    """主函数"""
    # 获取环境变量
    app_url = os.getenv('STREAMLIT_URL')

    if not app_url:
        logger.error("❌ 未设置 STREAMLIT_URL 环境变量")
        print("请在 GitHub Secrets 中设置 STREAMLIT_URL")
        sys.exit(1)

    logger.info("🚀 开始唤醒 Streamlit 应用...")
    logger.info(f"目标 URL: {app_url}")

    # 唤醒应用
    success = wake_up_streamlit_app(app_url)

    if success:
        logger.info("🎉 应用唤醒任务完成")
        print("✅ 应用唤醒成功")
        sys.exit(0)
    else:
        logger.error("❌ 应用唤醒失败")
        print("❌ 应用唤醒失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
