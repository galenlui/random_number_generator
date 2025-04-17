# 开源程序，请勿贩卖，源码免费使用，欢迎大家完善修改，增加新的功能。
# (C)2025 Galen Studio(R)
# OICQ: 284121506

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class RandomNumberGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("随机数字、字母生成器(可随机模拟双色球和大乐透等选号)")
        self.root.geometry("420x600")  # 增加窗口高度以容纳新控件
        self.root.resizable(False, False)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("TRadiobutton", font=("Arial", 10))
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 生成类型选择
        ttk.Label(main_frame, text="生成类型:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.gen_type = tk.StringVar(value="number")
        ttk.Radiobutton(main_frame, text="数字", variable=self.gen_type, value="number").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(main_frame, text="字母", variable=self.gen_type, value="letter").grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(main_frame, text="字母和数字", variable=self.gen_type, value="alphanumeric").grid(row=1, column=2, sticky=tk.W)
        
        # 数字范围设置
        self.range_frame = ttk.LabelFrame(main_frame, text="数字范围设置", padding="10")
        self.range_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E, pady=10)
        
        ttk.Label(self.range_frame, text="最小值:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.min_value = tk.StringVar(value="1")
        ttk.Entry(self.range_frame, textvariable=self.min_value, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(self.range_frame, text="最大值:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.max_value = tk.StringVar(value="33")
        ttk.Entry(self.range_frame, textvariable=self.max_value, width=10).grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # 字母范围设置 - 添加这个新的框架
        self.letter_frame = ttk.LabelFrame(main_frame, text="字母范围设置", padding="10")
        self.letter_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W+tk.E, pady=10)
        
        # 添加字母大小写选择
        self.use_uppercase = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.letter_frame, text="包含大写字母", variable=self.use_uppercase).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # 修改为默认不选中小写字母
        self.use_lowercase = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.letter_frame, text="包含小写字母", variable=self.use_lowercase).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 添加字母范围选择
        ttk.Label(self.letter_frame, text="字母范围:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # 起始字母
        ttk.Label(self.letter_frame, text="从:").grid(row=1, column=1, sticky=tk.W, pady=5)
        self.start_letter = tk.StringVar(value="A")
        start_letter_combo = ttk.Combobox(self.letter_frame, textvariable=self.start_letter, width=5)
        start_letter_combo['values'] = tuple(string.ascii_uppercase)
        start_letter_combo.grid(row=1, column=2, sticky=tk.W, padx=5)
        
        # 结束字母
        ttk.Label(self.letter_frame, text="到:").grid(row=1, column=3, sticky=tk.W, pady=5)
        self.end_letter = tk.StringVar(value="Z")
        end_letter_combo = ttk.Combobox(self.letter_frame, textvariable=self.end_letter, width=5)
        end_letter_combo['values'] = tuple(string.ascii_uppercase)
        end_letter_combo.grid(row=1, column=4, sticky=tk.W, padx=5)
        
        # 生成数量设置
        ttk.Label(main_frame, text="生成数量:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.count = tk.StringVar(value="6")
        ttk.Entry(main_frame, textvariable=self.count, width=10).grid(row=4, column=1, sticky=tk.W, padx=5)
        
        # 是否允许重复 - 修改为默认不选中
        self.allow_duplicate = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="允许重复", variable=self.allow_duplicate).grid(row=5, column=0, sticky=tk.W, pady=5)
        
        # 生成按钮
        ttk.Button(main_frame, text="生成随机项", command=self.generate).grid(row=6, column=0, columnspan=3, pady=10)
        
        # 结果显示区域
        ttk.Label(main_frame, text="生成结果:", font=("Arial", 12, "bold")).grid(row=7, column=0, sticky=tk.W, pady=5)
        
        self.result_text = tk.Text(main_frame, height=8, width=50, wrap=tk.WORD)
        self.result_text.grid(row=8, column=0, columnspan=3, sticky=tk.W+tk.E)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=8, column=3, sticky=tk.NS)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # 复制按钮
        ttk.Button(main_frame, text="复制结果", command=self.copy_result).grid(row=9, column=0, columnspan=3, pady=10)
        
        # 绑定生成类型变更事件
        self.gen_type.trace_add("write", self.update_ui)
        
        # 初始化UI状态
        self.update_ui()
        
    def update_ui(self, *args):
        # 根据生成类型更新UI
        gen_type = self.gen_type.get()
        
        if gen_type == "number":
            # 数字模式：启用数字范围，禁用字母范围
            for child in self.range_frame.winfo_children():
                child.configure(state="normal")
            for child in self.letter_frame.winfo_children():
                child.configure(state="disabled")
        elif gen_type == "letter":
            # 字母模式：禁用数字范围，启用字母范围
            for child in self.range_frame.winfo_children():
                child.configure(state="disabled")
            for child in self.letter_frame.winfo_children():
                child.configure(state="normal")
        else:  # alphanumeric模式
            # 字母和数字模式：同时启用数字范围和字母范围
            for child in self.range_frame.winfo_children():
                child.configure(state="normal")
            for child in self.letter_frame.winfo_children():
                child.configure(state="normal")
    
    def generate(self):
        try:
            # 获取生成数量
            count = int(self.count.get())
            if count <= 0:
                messagebox.showerror("错误", "生成数量必须大于0")
                return
                
            gen_type = self.gen_type.get()
            result = []
            
            if gen_type == "number":
                # 生成数字
                min_val = int(self.min_value.get())
                max_val = int(self.max_value.get())
                
                if min_val > max_val:
                    messagebox.showerror("错误", "最小值不能大于最大值")
                    return
                
                # 检查是否有足够的不重复数字可供选择
                if not self.allow_duplicate.get() and count > (max_val - min_val + 1):
                    messagebox.showerror("错误", f"在范围 {min_val} 到 {max_val} 内没有足够的不重复数字可供选择")
                    return
                
                if self.allow_duplicate.get():
                    result = [random.randint(min_val, max_val) for _ in range(count)]
                else:
                    result = random.sample(range(min_val, max_val + 1), count)
                    
            elif gen_type == "letter":
                # 生成字母
                letters = ""
                
                # 获取字母范围
                start_upper = self.start_letter.get().upper()
                end_upper = self.end_letter.get().upper()
                
                # 验证输入的字母范围
                if not (start_upper in string.ascii_uppercase and end_upper in string.ascii_uppercase):
                    messagebox.showerror("错误", "请输入有效的字母范围（A-Z）")
                    return
                
                # 确保起始字母不大于结束字母
                if start_upper > end_upper:
                    messagebox.showerror("错误", "起始字母不能大于结束字母")
                    return
                
                # 根据选择的大小写和范围生成字母集
                if self.use_uppercase.get():
                    start_idx = string.ascii_uppercase.index(start_upper)
                    end_idx = string.ascii_uppercase.index(end_upper)
                    letters += string.ascii_uppercase[start_idx:end_idx+1]
                
                if self.use_lowercase.get():
                    start_idx = string.ascii_uppercase.index(start_upper)
                    end_idx = string.ascii_uppercase.index(end_upper)
                    letters += string.ascii_lowercase[start_idx:end_idx+1]
                
                # 检查是否至少选择了一种字母类型
                if not letters:
                    messagebox.showerror("错误", "请至少选择一种字母类型（大写或小写）")
                    return
                
                if self.allow_duplicate.get():
                    result = [random.choice(letters) for _ in range(count)]
                else:
                    if count > len(letters):
                        messagebox.showerror("错误", f"没有足够的不重复字母可供选择（当前可用字母数：{len(letters)}）")
                        return
                    result = random.sample(letters, count)
                    
            elif gen_type == "alphanumeric":
                # 生成字母和数字
                chars_list = []  # 使用列表而不是字符串，以便更好地控制唯一性
                
                # 获取字母范围
                start_upper = self.start_letter.get().upper()
                end_upper = self.end_letter.get().upper()
                
                # 验证输入的字母范围
                if not (start_upper in string.ascii_uppercase and end_upper in string.ascii_uppercase):
                    messagebox.showerror("错误", "请输入有效的字母范围（A-Z）")
                    return
                
                # 确保起始字母不大于结束字母
                if start_upper > end_upper:
                    messagebox.showerror("错误", "起始字母不能大于结束字母")
                    return
                
                # 根据选择的大小写和范围生成字母集
                if self.use_uppercase.get():
                    start_idx = string.ascii_uppercase.index(start_upper)
                    end_idx = string.ascii_uppercase.index(end_upper)
                    for char in string.ascii_uppercase[start_idx:end_idx+1]:
                        chars_list.append(char)
                
                if self.use_lowercase.get():
                    start_idx = string.ascii_lowercase.index(start_upper.lower())
                    end_idx = string.ascii_lowercase.index(end_upper.lower())
                    for char in string.ascii_lowercase[start_idx:end_idx+1]:
                        chars_list.append(char)
                
                # 获取数字范围
                try:
                    min_val = int(self.min_value.get())
                    max_val = int(self.max_value.get())
                    
                    if min_val > max_val:
                        messagebox.showerror("错误", "最小值不能大于最大值")
                        return
                        
                    # 添加数字到字符列表中
                    for i in range(min_val, max_val + 1):
                        chars_list.append(str(i))
                except ValueError:
                    messagebox.showerror("错误", "请输入有效的数字范围")
                    return
                
                # 检查是否至少选择了一种字母类型
                if not (self.use_uppercase.get() or self.use_lowercase.get()):
                    messagebox.showerror("错误", "请至少选择一种字母类型（大写或小写）")
                    return
                
                # 生成结果
                if self.allow_duplicate.get():
                    result = [random.choice(chars_list) for _ in range(count)]
                else:
                    if count > len(chars_list):
                        messagebox.showerror("错误", f"没有足够的不重复字符可供选择（当前可用字符数：{len(chars_list)}）")
                        return
                    result = random.sample(chars_list, count)
            
            # 显示结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, ", ".join(map(str, result)))
            
        except ValueError as e:
            messagebox.showerror("输入错误", "请确保所有输入都是有效的数字")
    
    def copy_result(self):
        result = self.result_text.get(1.0, tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("成功", "结果已复制到剪贴板")
        else:
            messagebox.showinfo("提示", "没有可复制的结果")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomNumberGenerator(root)
    root.mainloop()