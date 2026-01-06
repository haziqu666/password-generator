#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import string
import secrets
import random

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("密码生成器")
        self.root.resizable(False, False)
        self.root.geometry("480x420")
        
        self.colors = {
            'bg': '#F5F7FA', 'card_bg': '#FFFFFF', 'primary': '#4A90D9',
            'primary_hover': '#357ABD', 'success': '#5CB85C',
            'success_hover': '#449D44', 'text': '#333333', 'error': '#D9534F'
        }
        self.root.configure(bg=self.colors['bg'])
        
        self.char_sets = {
            'uppercase': string.ascii_uppercase,
            'lowercase': string.ascii_lowercase,
            'digits': string.digits,
            'special': '!@#$%^&*()_+-='
        }
        
        self.var_uppercase = tk.BooleanVar(value=True)
        self.var_lowercase = tk.BooleanVar(value=True)
        self.var_digits = tk.BooleanVar(value=True)
        self.var_special = tk.BooleanVar(value=False)
        self.length_var = tk.StringVar(value="12")
        self.password_var = tk.StringVar()
        self.last_password = ""
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="密码生成器", font=('Arial', 18, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text']).pack(pady=(0, 15))
        
        char_card = self.create_card(main_frame, "字符类型")
        cb_frame = tk.Frame(char_card, bg=self.colors['card_bg'])
        cb_frame.pack(fill='x', padx=15, pady=10)
        
        configs = [(self.var_uppercase, "大写字母 (A-Z)"), (self.var_lowercase, "小写字母 (a-z)"),
                   (self.var_digits, "数字 (0-9)"), (self.var_special, "特殊字符 (!@#$%^&*)")]
        for i, (var, text) in enumerate(configs):
            tk.Checkbutton(cb_frame, text=text, variable=var, font=('Arial', 10),
                          bg=self.colors['card_bg'], fg=self.colors['text'],
                          selectcolor=self.colors['card_bg']).grid(row=i//2, column=i%2, sticky='w', padx=10, pady=5)
        
        len_card = self.create_card(main_frame, "密码长度")
        len_frame = tk.Frame(len_card, bg=self.colors['card_bg'])
        len_frame.pack(fill='x', padx=15, pady=10)
        tk.Label(len_frame, text="长度 (8-32):", font=('Arial', 10),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(side='left')
        tk.Entry(len_frame, textvariable=self.length_var, font=('Arial', 11),
                width=8, justify='center').pack(side='left', padx=10)
        self.len_err = tk.Label(len_frame, text="", font=('Arial', 9),
                               bg=self.colors['card_bg'], fg=self.colors['error'])
        self.len_err.pack(side='left')
        
        tk.Button(main_frame, text="生成密码", font=('Arial', 12, 'bold'),
                 bg=self.colors['primary'], fg='white', width=20, height=2,
                 command=self.generate_password).pack(pady=15)
        
        res_card = self.create_card(main_frame, "生成结果")
        res_frame = tk.Frame(res_card, bg=self.colors['card_bg'])
        res_frame.pack(fill='x', padx=15, pady=10)
        tk.Entry(res_frame, textvariable=self.password_var, font=('Consolas', 14),
                state='readonly', readonlybackground='white', justify='center').pack(side='left', fill='x', expand=True, ipady=8)
        tk.Button(res_frame, text="复制", font=('Arial', 10), bg=self.colors['success'],
                 fg='white', width=8, command=self.copy_password).pack(side='left', padx=(10, 0))
        self.status = tk.Label(res_card, text="", font=('Arial', 9),
                              bg=self.colors['card_bg'], fg=self.colors['success'])
        self.status.pack(pady=(0, 5))
        
    def create_card(self, parent, title):
        card = tk.Frame(parent, bg=self.colors['card_bg'], relief='solid', bd=1)
        card.pack(fill='x', pady=8)
        tk.Label(card, text=title, font=('Arial', 11, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(anchor='w', padx=15, pady=(10, 0))
        return card
        
    def generate_password(self):
        self.status.config(text="")
        if not any([self.var_uppercase.get(), self.var_lowercase.get(),
                   self.var_digits.get(), self.var_special.get()]):
            messagebox.showwarning("提示", "请至少选择一种字符类型！")
            return
        
        try:
            length = int(self.length_var.get().strip())
            if length < 8 or length > 32:
                messagebox.showwarning("提示", "密码长度需在 8-32 之间！")
                return
        except:
            messagebox.showwarning("提示", "请输入有效的密码长度！")
            return
        
        charset = ""
        required = []
        if self.var_uppercase.get():
            charset += self.char_sets['uppercase']
            required.append(secrets.choice(self.char_sets['uppercase']))
        if self.var_lowercase.get():
            charset += self.char_sets['lowercase']
            required.append(secrets.choice(self.char_sets['lowercase']))
        if self.var_digits.get():
            charset += self.char_sets['digits']
            required.append(secrets.choice(self.char_sets['digits']))
        if self.var_special.get():
            charset += self.char_sets['special']
            required.append(secrets.choice(self.char_sets['special']))
        
        for _ in range(100):
            chars = required.copy()
            chars.extend(secrets.choice(charset) for _ in range(length - len(required)))
            random.shuffle(chars)
            password = ''.join(chars)
            if password != self.last_password:
                break
        
        self.last_password = password
        self.password_var.set(password)
        
    def copy_password(self):
        if not self.password_var.get():
            messagebox.showinfo("提示", "请先生成密码！")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.password_var.get())
        self.status.config(text="✓ 已复制到剪贴板")
        self.root.after(3000, lambda: self.status.config(text=""))

if __name__ == "__main__":
    root = tk.Tk()
    PasswordGenerator(root)
    root.mainloop()
