import tkinter as tk
from tkinter import messagebox
import string
import random

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("晶环科数出品")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#0d1117")
        
        self.history = set()
        
        # 标题
        title = tk.Label(self.root, text="✦ 复杂口令生成工具 ✦", font=("Microsoft YaHei UI", 18, "bold"),
                        bg="#0d1117", fg="#58a6ff")
        title.pack(pady=20)
        
        # 字符类型卡片
        card1 = tk.Frame(self.root, bg="#161b22", padx=20, pady=15)
        card1.pack(padx=30, pady=10, fill="x")
        
        tk.Label(card1, text="◆ 字符类型", font=("Microsoft YaHei UI", 11, "bold"),
                bg="#161b22", fg="#58a6ff").pack(anchor="w", pady=(0, 10))
        
        cb_frame = tk.Frame(card1, bg="#161b22")
        cb_frame.pack(fill="x")
        
        self.v1 = tk.IntVar(value=1)
        self.v2 = tk.IntVar(value=1)
        self.v3 = tk.IntVar(value=1)
        self.v4 = tk.IntVar(value=0)
        
        style = {"font": ("Microsoft YaHei UI", 10), "bg": "#161b22", "fg": "#c9d1d9",
                "selectcolor": "#21262d", "activebackground": "#161b22", "activeforeground": "#58a6ff"}
        
        tk.Checkbutton(cb_frame, text="大写字母 A-Z", variable=self.v1, **style).grid(row=0, column=0, sticky="w", padx=8, pady=4)
        tk.Checkbutton(cb_frame, text="小写字母 a-z", variable=self.v2, **style).grid(row=0, column=1, sticky="w", padx=8, pady=4)
        tk.Checkbutton(cb_frame, text="数字 0-9", variable=self.v3, **style).grid(row=1, column=0, sticky="w", padx=8, pady=4)
        tk.Checkbutton(cb_frame, text="特殊字符 !@#$%", variable=self.v4, **style).grid(row=1, column=1, sticky="w", padx=8, pady=4)
        
        # 密码长度卡片
        card2 = tk.Frame(self.root, bg="#161b22", padx=20, pady=15)
        card2.pack(padx=30, pady=10, fill="x")
        
        len_row = tk.Frame(card2, bg="#161b22")
        len_row.pack(fill="x")
        
        tk.Label(len_row, text="◆ 密码长度 (8-32):", font=("Microsoft YaHei UI", 11, "bold"),
                bg="#161b22", fg="#58a6ff").pack(side="left")
        
        self.len_entry = tk.Entry(len_row, font=("Consolas", 12), width=8, justify="center",
                                 bg="#21262d", fg="#c9d1d9", insertbackground="#58a6ff",
                                 relief="flat", highlightthickness=0)
        self.len_entry.insert(0, "12")
        self.len_entry.pack(side="left", padx=15, ipady=6)
        
        # 生成按钮
        self.gen_btn = tk.Button(self.root, text="⚡ 生成口令", font=("Microsoft YaHei UI", 12, "bold"),
                                bg="#238636", fg="white", activebackground="#2ea043",
                                relief="flat", width=18, height=2, cursor="hand2",
                                command=self.generate)
        self.gen_btn.pack(pady=18)
        self.gen_btn.bind("<Enter>", lambda e: self.gen_btn.config(bg="#2ea043"))
        self.gen_btn.bind("<Leave>", lambda e: self.gen_btn.config(bg="#238636"))
        
        # 结果区域
        card3 = tk.Frame(self.root, bg="#161b22", padx=20, pady=15)
        card3.pack(padx=30, pady=10, fill="x")
        
        tk.Label(card3, text="◆ 生成结果", font=("Microsoft YaHei UI", 11, "bold"),
                bg="#161b22", fg="#58a6ff").pack(anchor="w", pady=(0, 10))
        
        res_row = tk.Frame(card3, bg="#161b22")
        res_row.pack(fill="x")
        
        self.result_entry = tk.Entry(res_row, font=("Consolas", 15), width=24, justify="center",
                                    bg="#21262d", fg="#7ee787", relief="flat",
                                    highlightthickness=0)
        self.result_entry.pack(side="left", ipady=10, fill="x", expand=True)
        
        self.copy_btn = tk.Button(res_row, text="📋 复制", font=("Microsoft YaHei UI", 11, "bold"),
                                 bg="#1f6feb", fg="white", activebackground="#388bfd",
                                 relief="flat", width=10, height=2, cursor="hand2",
                                 command=self.copy)
        self.copy_btn.pack(side="left", padx=(15, 0))
        self.copy_btn.bind("<Enter>", lambda e: self.copy_btn.config(bg="#388bfd"))
        self.copy_btn.bind("<Leave>", lambda e: self.copy_btn.config(bg="#1f6feb"))
        
        # 状态提示
        self.status = tk.Label(self.root, text="", font=("Microsoft YaHei UI", 10),
                              bg="#0d1117", fg="#3fb950")
        self.status.pack(pady=8)
        
        self.root.mainloop()
    
    def generate(self):
        chars = ""
        req = []
        
        if self.v1.get():
            chars += string.ascii_uppercase
            req.append(random.choice(string.ascii_uppercase))
        if self.v2.get():
            chars += string.ascii_lowercase
            req.append(random.choice(string.ascii_lowercase))
        if self.v3.get():
            chars += string.digits
            req.append(random.choice(string.digits))
        if self.v4.get():
            sp = "!@#$%^&*()_+-="
            chars += sp
            req.append(random.choice(sp))
        
        if not chars:
            messagebox.showwarning("提示", "请至少选择一种字符类型")
            return
        
        try:
            n = int(self.len_entry.get())
            if n < 8 or n > 32:
                messagebox.showwarning("提示", "长度需在8-32之间")
                return
        except:
            messagebox.showwarning("提示", "请输入有效数字")
            return
        
        for _ in range(500):
            p = req.copy()
            p.extend(random.choice(chars) for _ in range(n - len(req)))
            random.shuffle(p)
            pwd = "".join(p)
            if pwd not in self.history:
                self.history.add(pwd)
                break
        
        self.result_entry.delete(0, "end")
        self.result_entry.insert(0, pwd)
        self.status.config(text="")
    
    def copy(self):
        pwd = self.result_entry.get()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            self.status.config(text="✓ 已复制到剪贴板")
            self.root.after(3000, lambda: self.status.config(text=""))
        else:
            messagebox.showinfo("提示", "请先生成口令")

if __name__ == "__main__":
    App()
