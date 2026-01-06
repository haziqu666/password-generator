import tkinter as tk
from tkinter import messagebox
import string
import random

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("密码生成器")
        self.root.geometry("400x350")
        self.root.configure(bg="#f0f0f0")
        
        # 标题
        tk.Label(self.root, text="密码生成器", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # 字符类型
        frame1 = tk.LabelFrame(self.root, text="字符类型", font=("Arial", 10), bg="#f0f0f0")
        frame1.pack(padx=20, pady=5, fill="x")
        
        self.v1 = tk.IntVar(value=1)
        self.v2 = tk.IntVar(value=1)
        self.v3 = tk.IntVar(value=1)
        self.v4 = tk.IntVar(value=0)
        
        tk.Checkbutton(frame1, text="大写字母 A-Z", variable=self.v1, bg="#f0f0f0").pack(anchor="w", padx=10)
        tk.Checkbutton(frame1, text="小写字母 a-z", variable=self.v2, bg="#f0f0f0").pack(anchor="w", padx=10)
        tk.Checkbutton(frame1, text="数字 0-9", variable=self.v3, bg="#f0f0f0").pack(anchor="w", padx=10)
        tk.Checkbutton(frame1, text="特殊字符 !@#$%", variable=self.v4, bg="#f0f0f0").pack(anchor="w", padx=10)
        
        # 密码长度
        frame2 = tk.LabelFrame(self.root, text="密码长度 (8-32)", font=("Arial", 10), bg="#f0f0f0")
        frame2.pack(padx=20, pady=5, fill="x")
        
        self.length_entry = tk.Entry(frame2, font=("Arial", 12), width=10)
        self.length_entry.insert(0, "12")
        self.length_entry.pack(padx=10, pady=5)
        
        # 生成按钮
        tk.Button(self.root, text="生成密码", font=("Arial", 12, "bold"), bg="#4A90D9", fg="white",
                  width=15, height=1, command=self.generate).pack(pady=10)
        
        # 结果
        frame3 = tk.LabelFrame(self.root, text="生成结果", font=("Arial", 10), bg="#f0f0f0")
        frame3.pack(padx=20, pady=5, fill="x")
        
        self.result = tk.Entry(frame3, font=("Consolas", 14), width=25, state="readonly")
        self.result.pack(side="left", padx=10, pady=10)
        
        tk.Button(frame3, text="复制", bg="#5CB85C", fg="white", command=self.copy).pack(side="left", padx=5)
        
        self.msg = tk.Label(self.root, text="", fg="green", bg="#f0f0f0")
        self.msg.pack()
        
        self.root.mainloop()
    
    def generate(self):
        chars = ""
        if self.v1.get(): chars += string.ascii_uppercase
        if self.v2.get(): chars += string.ascii_lowercase
        if self.v3.get(): chars += string.digits
        if self.v4.get(): chars += "!@#$%^&*()_+-="
        
        if not chars:
            messagebox.showwarning("提示", "请至少选择一种字符类型")
            return
        
        try:
            length = int(self.length_entry.get())
            if length < 8 or length > 32:
                messagebox.showwarning("提示", "长度需在8-32之间")
                return
        except:
            messagebox.showwarning("提示", "请输入有效数字")
            return
        
        pwd = "".join(random.choice(chars) for _ in range(length))
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
            self.msg.config(text="已复制!")

if __name__ == "__main__":
    App()
