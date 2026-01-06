#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 将密码生成器打包为独立 exe
使用 PyInstaller 打包，支持 Windows 7/10/11
"""

import subprocess
import sys
import os


def install_pyinstaller():
    """安装 PyInstaller"""
    print("正在安装 PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def build_exe():
    """打包为 exe"""
    print("开始打包...")
    
    # PyInstaller 参数
    args = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # 打包成单个 exe
        "--windowed",          # 无控制台窗口
        "--name=密码生成器",    # exe 名称
        "--clean",             # 清理临时文件
        "--noconfirm",         # 覆盖已有文件
        "password_generator.py"
    ]
    
    subprocess.check_call(args)
    
    print("\n" + "="*50)
    print("打包完成！")
    print("exe 文件位置: dist/密码生成器.exe")
    print("="*50)


def main():
    try:
        import PyInstaller
    except ImportError:
        install_pyinstaller()
    
    build_exe()


if __name__ == "__main__":
    main()
