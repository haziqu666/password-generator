import tkinter as tk
from tkinter import messagebox
import string
import random

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("晶环复杂口令生成器")
        self.root.geometry("520x480")
        self.root.resizable(False, False)
        
        # 深色科技风配色
        self.bg = "#1a1a2e"
        self.card_bg = "#16213e"
        self.accent = "#0f3460"
        self.highlight = "#00d9ff"
        self.text = "#ffffff"
        self.text_dim = "#a0a0a0"
        
        self.root.configure(bg=self.bg)
        
        # 历史密码记录
        self.history = set()
        
        # 主容器
        main = tk.Frame(self.root, bg=self.bg)
        main.pack(fill="both", expand=True, padx=30, pady=25)
        
        # 标题
        tk.Label(main, text="◈ 晶环复杂口令生成器 ◈", font=("Microsoft YaHei UI", 18, "bold"),
                bg=self.bg, fg=self.highlight).pack(pady=(0, 20))
        
        # 字符类型卡片
        card1 = tk.Frame(main, bg=self.card_bg, highlightbackground=self.accent,
                        highlightthickness=2)
        card1.pack(fill="x", pady=8)
        
        tk.Label(card1, text="▸ 字符类型", font=("Microsoft YaHei UI", 11, "bold"),
                bg=self.card_bg, fg=self.highlight).pack(anchor="w", padx=15, pady=(12, 8))
        
        cb_frame = tk.Frame(card1, bg=self.card_bg)
        cb_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        self.v1 = tk.IntVar(value=1)
        self.v2 = tk.IntVar(value=1)
        self.v3 = tk.IntVar(value=1)
        self.v4 = tk.IntVar(value=0)
        
        cb_style = {"font": ("Microsoft YaHei UI", 10), "bg": self.card_bg, 
                   "fg": self.text, "selectcolor": self.accent, "activebackground": self.card_bg,
                   "activeforeground": self.highlight}
        
        tk.Checkbutton(cb_frame, text="大写字母 (A-Z)", variable=self.v1, **cb_style).grid(row=0, column=0, sticky="w", padx=5, pady=3)
        tk.Checkbutton(cb_frame, text="小写字母 (a-z)", variable=self.v2, **cb_style).grid(row=0, column=1, sticky="w", padx=5, pady=3)
        tk.Checkbutton(cb_frame, text="数字 (0-9)", variable=self.v3, **cb_style).grid(row=1, column=0, sticky="w", padx=5, pady=3)
        tk.Checkbutton(cb_frame, text="特殊字符 (!@#$%^&*)", variable=self.v4, **cb_style).grid(row=1, column=1, sticky="w", padx=5, pady=3)
        
        # 密码长度卡片
        card2 = tk.Frame(main, bg=self.card_bg, highlightbackground=self.accent,
                        highlightthickness=2)
        card2.pack(fill="x", pady=8)
        
        tk.Label(card2, text="▸ 密码长度", font=("Microsoft YaHei UI", 11, "bold"),
                bg=self.card_bg, fg=self.highlight).pack(anchor="w", padx=15, pady=(12, 8))
        
        len_frame = tk.Frame(card2, bg=self.card_bg)
        len_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        tk.Label(len_frame, text="长度 (8-32):", font=("Microsoft YaHei UI", 10),
                bg=self.card_bg, fg=self.text).pack(side="left")
        
        self.length_entry = tk.Entry(len_frame, font=("Consolas", 12), width=8, justify="center",
                                    bg=self.accent, fg=self.text, insertbackground=self.highlight,
                                    relief="flat", highlightthickness=1, highlightbackground=self.highlight)
        self.length_entry.insert(0, "12")
        self.length_entry.pack(side="left", padx=15, ipady=5)
        
        # 生成按钮
        self.gen_btn = tk.Button(main, text="⚡ 生成口令", font=("Microsoft YaHei UI", 13, "bold"),
                                bg=self.highlight, fg="#000000", activebackground="#00b8d9",
                                activeforeground="#000000", relief="flat", cursor="hand2",
                                width=18, height=2, command=self.generate)
        self.gen_btn.pack(pady=18)
        
        # 结果卡片
        card3 = tk.Frame(main, bg=self.card_bg, highlightbackground=self.accent,
                        highlightthickness=2)
        card3.pack(fill="x", pady=8)
        
        tk.Label(card3, text="▸ 生成结果", font=("Microsoft YaHei UI", 11, "bold"),
                bg=self.card_bg, fg=self.highlight).pack(anchor="w", padx=15, pady=(12, 8))
        
        res_frame = tk.Frame(card3, bg=self.card_bg)
        res_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        self.result = tk.Entry(res_frame, font=("Consolas", 16), width=22, justify="center",
                              bg=self.accent, fg=self.highlight, readonlybackground=self.accent,
                              relief="flat", highlightthickness=1, highlightbackground=self.highlight,
                              state="readonly")
        self.result.pack(side="left", fill="x", expand=True, ipady=10)
        
        self.copy_btn = tk.Button(res_frame, text="📋 复制", font=("Microsoft YaHei UI", 11, "bold"),
                                 bg="#00c853", fg="#ffffff", activebackground="#00a844",
                                 relief="flat", cursor="hand2", width=10, height=2,
                                 command=self.copy)
        self.copy_btn.pack(side="left", padx=(15, 0))
        
        # 状态提示
        self.msg = tk.Label(card3, text="", font=("Microsoft YaHei UI", 10),
                           bg=self.card_bg, fg="#00c853")
        self.msg.pack(pady=(0, 8))
        
        self.root.mainloop()
    
    def generate(self):
        chars = ""
        required = []
        
        if self.v1.get():
            chars += string.ascii_uppercase
            required.append(random.choice(string.ascii_uppercase))
        if self.v2.get():
            chars += string.ascii_lowercase
            required.append(random.choice(string.ascii_lowercase))
        if self.v3.get():
            chars += string.digits
            required.append(random.choice(string.digits))
        if self.v4.get():
            special = "!@#$%^&*()_+-="
            chars += special
            required.append(random.choice(special))
        
        if not chars:
            messagebox.showwarning("提示", "请至少选择一种字符类型")
            return
        
        try:
            length = int(self.length_entry.get())
            if length < 8 or length > 32:
                messagebox.showwarning("提示", "长度需在 8-32 之间")
                return
        except:
            messagebox.showwarning("提示", "请输入有效数字")
            return
        
        # 生成不重复的密码
        for _ in range(1000):
            pwd_chars = required.copy()
            pwd_chars.extend(random.choice(chars) for _ in range(length - len(required)))
            random.shuffle(pwd_chars)
            pwd = "".join(pwd_chars)
            
            if pwd not in self.history:
                self.history.add(pwd)
                break
        else:
            messagebox.showinfo("提示", "已生成大量密码，建议更换字符组合")
        
        self.result.config(state="normal")
        self.result.delete(0, "end")
        self.result.insert(0, pwd)
        self.result.config(state="readonly")
        self.msg.config(text="")
    
    def copy(self):
        pwd = self.result.get()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            self.msg.config(text="✓ 已复制到剪贴板")
            self.root.after(3000, lambda: self.msg.config(text=""))
        else:
            messagebox.showinfo("提示", "请先生成口令")

if __name__ == "__main__":
    App()
