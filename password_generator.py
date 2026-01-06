#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密码生成器 - Password Generator
支持 Windows 7/10/11，无需额外依赖
"""

import tkinter as tk
from tkinter import ttk, messagebox
import string
import secrets
import random


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("密码生成器")
        self.root.resizable(False, False)
        
        # 窗口大小和居中
        window_width = 480
        window_height = 420
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 配色方案
        self.colors = {
            'bg': '#F5F7FA',
            'card_bg': '#FFFFFF',
            'primary': '#4A90D9',
            'primary_hover': '#357ABD',
            'success': '#5CB85C',
            'success_hover': '#449D44',
            'text': '#333333',
            'text_light': '#666666',
            'border': '#E1E4E8',
            'error': '#D9534F'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # 字符集
        self.char_sets = {
            'uppercase': string.ascii_uppercase,
            'lowercase': string.ascii_lowercase,
            'digits': string.digits,
            'special': '!@#$%^&*()_+-='
        }
        
        # 复选框变量
        self.var_uppercase = tk.BooleanVar(value=True)
        self.var_lowercase = tk.BooleanVar(value=True)
        self.var_digits = tk.BooleanVar(value=True)
        self.var_special = tk.BooleanVar(value=False)
        
        # 密码长度变量
        self.length_var = tk.StringVar(value="12")
        
        # 上一次生成的密码（用于防重复）
        self.last_password = ""
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """设置控件样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 复选框样式
        style.configure('Custom.TCheckbutton',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text'],
                       font=('Microsoft YaHei UI', 10))
        
        # 标签样式
        style.configure('Title.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=('Microsoft YaHei UI', 16, 'bold'))
        
        style.configure('Card.TFrame',
                       background=self.colors['card_bg'])
        
    def create_widgets(self):
        """创建界面控件"""
        # 主容器
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(main_frame, text="🔐 密码生成器",
                              font=('Microsoft YaHei UI', 18, 'bold'),
                              bg=self.colors['bg'], fg=self.colors['text'])
        title_label.pack(pady=(0, 15))
        
        # 字符类型选择卡片
        char_card = self.create_card(main_frame, "字符类型")
        
        checkboxes_frame = tk.Frame(char_card, bg=self.colors['card_bg'])
        checkboxes_frame.pack(fill='x', padx=15, pady=10)
        
        # 复选框配置
        checkbox_configs = [
            (self.var_uppercase, "大写字母 (A-Z)"),
            (self.var_lowercase, "小写字母 (a-z)"),
            (self.var_digits, "数字 (0-9)"),
            (self.var_special, "特殊字符 (!@#$%^&*)")
        ]
        
        for i, (var, text) in enumerate(checkbox_configs):
            cb = tk.Checkbutton(checkboxes_frame, text=text, variable=var,
                               font=('Microsoft YaHei UI', 10),
                               bg=self.colors['card_bg'], fg=self.colors['text'],
                               activebackground=self.colors['card_bg'],
                               selectcolor=self.colors['card_bg'],
                               cursor='hand2')
            cb.grid(row=i//2, column=i%2, sticky='w', padx=10, pady=5)
        
        # 密码长度卡片
        length_card = self.create_card(main_frame, "密码长度")
        
        length_frame = tk.Frame(length_card, bg=self.colors['card_bg'])
        length_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(length_frame, text="长度 (8-32):",
                font=('Microsoft YaHei UI', 10),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(side='left')
        
        # 长度输入框
        self.length_entry = tk.Entry(length_frame, textvariable=self.length_var,
                                    font=('Microsoft YaHei UI', 11),
                                    width=8, justify='center',
                                    relief='solid', bd=1)
        self.length_entry.pack(side='left', padx=10)
        self.length_entry.bind('<KeyRelease>', self.validate_length_input)
        
        # 长度错误提示
        self.length_error_label = tk.Label(length_frame, text="",
                                          font=('Microsoft YaHei UI', 9),
                                          bg=self.colors['card_bg'],
                                          fg=self.colors['error'])
        self.length_error_label.pack(side='left', padx=5)
        
        # 生成按钮
        self.generate_btn = tk.Button(main_frame, text="生成密码",
                                     font=('Microsoft YaHei UI', 12, 'bold'),
                                     bg=self.colors['primary'],
                                     fg='white', relief='flat',
                                     cursor='hand2', width=20, height=2,
                                     command=self.generate_password)
        self.generate_btn.pack(pady=15)
        self.add_button_hover(self.generate_btn, 
                             self.colors['primary'], 
                             self.colors['primary_hover'])
        
        # 密码显示卡片
        result_card = self.create_card(main_frame, "生成结果")
        
        result_frame = tk.Frame(result_card, bg=self.colors['card_bg'])
        result_frame.pack(fill='x', padx=15, pady=10)
        
        # 密码显示框
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(result_frame, textvariable=self.password_var,
                                       font=('Consolas', 14),
                                       state='readonly', readonlybackground='white',
                                       relief='solid', bd=1, justify='center')
        self.password_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        # 复制按钮
        self.copy_btn = tk.Button(result_frame, text="📋 复制",
                                 font=('Microsoft YaHei UI', 10),
                                 bg=self.colors['success'],
                                 fg='white', relief='flat',
                                 cursor='hand2', width=8,
                                 command=self.copy_password)
        self.copy_btn.pack(side='left', padx=(10, 0))
        self.add_button_hover(self.copy_btn,
                             self.colors['success'],
                             self.colors['success_hover'])
        
        # 复制成功提示
        self.copy_status_label = tk.Label(result_card, text="",
                                         font=('Microsoft YaHei UI', 9),
                                         bg=self.colors['card_bg'],
                                         fg=self.colors['success'])
        self.copy_status_label.pack(pady=(0, 5))
        
    def create_card(self, parent, title):
        """创建卡片容器"""
        card_frame = tk.Frame(parent, bg=self.colors['card_bg'],
                             relief='solid', bd=1)
        card_frame.pack(fill='x', pady=8)
        
        # 卡片标题
        title_label = tk.Label(card_frame, text=title,
                              font=('Microsoft YaHei UI', 11, 'bold'),
                              bg=self.colors['card_bg'],
                              fg=self.colors['text'])
        title_label.pack(anchor='w', padx=15, pady=(10, 0))
        
        return card_frame
    
    def add_button_hover(self, button, normal_color, hover_color):
        """添加按钮悬停效果"""
        def on_enter(e):
            button.configure(bg=hover_color)
        def on_leave(e):
            button.configure(bg=normal_color)
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
    def validate_length_input(self, event=None):
        """验证密码长度输入"""
        value = self.length_var.get().strip()
        
        if not value:
            self.length_error_label.config(text="")
            return True
            
        # 检查是否为正整数
        if not value.isdigit():
            self.length_error_label.config(text="请输入正整数")
            return False
            
        length = int(value)
        if length < 8:
            self.length_error_label.config(text="最小长度为 8")
            return False
        elif length > 32:
            self.length_error_label.config(text="最大长度为 32")
            return False
        else:
            self.length_error_label.config(text="")
            return True
            
    def generate_password(self):
        """生成密码"""
        # 清除复制状态
        self.copy_status_label.config(text="")
        
        # 验证至少选择一种字符类型
        if not any([self.var_uppercase.get(), self.var_lowercase.get(),
                   self.var_digits.get(), self.var_special.get()]):
            messagebox.showwarning("提示", "请至少选择一种字符类型！")
            return
            
        # 验证密码长度
        if not self.validate_length_input():
            messagebox.showwarning("提示", "请输入有效的密码长度 (8-32)！")
            return
            
        length_str = self.length_var.get().strip()
        if not length_str:
            messagebox.showwarning("提示", "请输入密码长度！")
            return
            
        length = int(length_str)
        
        # 构建字符集
        charset = ""
        required_chars = []
        
        if self.var_uppercase.get():
            charset += self.char_sets['uppercase']
            required_chars.append(secrets.choice(self.char_sets['uppercase']))
        if self.var_lowercase.get():
            charset += self.char_sets['lowercase']
            required_chars.append(secrets.choice(self.char_sets['lowercase']))
        if self.var_digits.get():
            charset += self.char_sets['digits']
            required_chars.append(secrets.choice(self.char_sets['digits']))
        if self.var_special.get():
            charset += self.char_sets['special']
            required_chars.append(secrets.choice(self.char_sets['special']))
        
        # 生成密码（确保包含每种选中的字符类型）
        max_attempts = 100
        for _ in range(max_attempts):
            # 先填充必需字符，再随机填充剩余位置
            remaining_length = length - len(required_chars)
            password_chars = required_chars.copy()
            password_chars.extend(secrets.choice(charset) for _ in range(remaining_length))
            
            # 打乱顺序
            random.shuffle(password_chars)
            password = ''.join(password_chars)
            
            # 确保不与上次生成的密码相同
            if password != self.last_password:
                break
        
        self.last_password = password
        self.password_var.set(password)
        
    def copy_password(self):
        """复制密码到剪贴板"""
        password = self.password_var.get()
        if not password:
            messagebox.showinfo("提示", "请先生成密码！")
            return
            
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()
        
        # 显示复制成功提示
        self.copy_status_label.config(text="✓ 已复制到剪贴板")
        
        # 3秒后清除提示
        self.root.after(3000, lambda: self.copy_status_label.config(text=""))


def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
