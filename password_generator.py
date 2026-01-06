import tkinter as tk
from tkinter import messagebox
import string
import random

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("晶环复杂口令生成器")
        self.root.geometry("460x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        
        self.history = set()
        
        # 标题
        tk.Label(self.root, text="晶环复杂口令生成器", font=("Arial", 16, "bold"),
                bg="#1e1e2e", fg="#00d4ff").pack(pady=15)
        
        # 字符类型
        f1 = tk.LabelFrame(self.root, text=" 字符类型 ", font=("Arial", 10, "bold"),
                          bg="#1e1e2e", fg="#00d4ff")
        f1.pack(padx=25, pady=8, fill="x")
        
        self.v1 = tk.IntVar(value=1)
        self.v2 = tk.IntVar(value=1)
        self.v3 = tk.IntVar(value=1)
        self.v4 = tk.IntVar(value=0)
        
        tk.Checkbutton(f1, text="大写字母 A-Z", variable=self.v1, bg="#1e1e2e", fg="white",
                      selectcolor="#333", activebackground="#1e1e2e").grid(row=0, column=0, sticky="w", padx=10, pady=2)
        tk.Checkbutton(f1, text="小写字母 a-z", variable=self.v2, bg="#1e1e2e", fg="white",
                      selectcolor="#333", activebackground="#1e1e2e").grid(row=0, column=1, sticky="w", padx=10, pady=2)
        tk.Checkbutton(f1, text="数字 0-9", variable=self.v3, bg="#1e1e2e", fg="white",
                      selectcolor="#333", activebackground="#1e1e2e").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        tk.Checkbutton(f1, text="特殊字符 !@#$%", variable=self.v4, bg="#1e1e2e", fg="white",
                      selectcolor="#333", activebackground="#1e1e2e").grid(row=1, column=1, sticky="w", padx=10, pady=2)
        
        # 密码长度
        f2 = tk.LabelFrame(self.root, text=" 密码长度 (8-32) ", font=("Arial", 10, "bold"),
                          bg="#1e1e2e", fg="#00d4ff")
        f2.pack(padx=25, pady=8, fill="x")
        
        self.len_entry = tk.Entry(f2, font=("Arial", 12), width=10, justify="center")
        self.len_entry.insert(0, "12")
        self.len_entry.pack(pady=8)
        
        # 生成按钮
        tk.Button(self.root, text="生成口令", font=("Arial", 12, "bold"),
                 bg="#00d4ff", fg="black", width=20, height=2,
                 command=self.generate).pack(pady=15)
        
        # 结果框和复制按钮
        f3 = tk.Frame(self.root, bg="#1e1e2e")
        f3.pack(padx=25, pady=5, fill="x")
        
        self.result_entry = tk.Entry(f3, font=("Consolas", 14), width=28, justify="center")
        self.result_entry.pack(side="left", ipady=8)
        
        tk.Button(f3, text="复制", font=("Arial", 11, "bold"),
                 bg="#00c853", fg="white", width=8, height=2,
                 command=self.copy).pack(side="left", padx=10)
        
        # 状态
        self.status = tk.Label(self.root, text="", font=("Arial", 10), bg="#1e1e2e", fg="#00c853")
        self.status.pack(pady=5)
        
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
            self.status.config(text="已复制!")
        else:
            messagebox.showinfo("提示", "请先生成口令")

if __name__ == "__main__":
    App()
