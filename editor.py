import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkFont
from core.scanner.scanner import Scanner
from core.scanner.tokens import *
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

try:
    from up import run
except ImportError:
    def run(fn, text):
        return None, None

class UpEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("UP Language Editor")
        self.root.geometry("1000x700")
        
        self.filename = None
        
        # Menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Run (Ctrl+R)", command=self.run_code)
        
        # Frame principal
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Editor
        editor_frame = tk.Frame(main_frame)
        editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(editor_frame, text="Editor", font=("Arial", 10, "bold")).pack(anchor="w")
        
        self.text_widget = tk.Text(editor_frame, wrap=tk.WORD, bg="#1e1e1e", 
                                   fg="#d4d4d4", font=("Courier", 11),
                                   insertbackground="white", padx=10, pady=10)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.text_widget.bind("<KeyRelease>", self.on_key_release)
        
        # Output
        output_frame = tk.Frame(main_frame)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(output_frame, text="Output", font=("Arial", 10, "bold")).pack(anchor="w")
        
        self.output_widget = tk.Text(output_frame, wrap=tk.WORD, bg="#1e1e1e",
                                     fg="#d4d4d4", font=("Courier", 11),
                                     state=tk.DISABLED, padx=10, pady=10)
        self.output_widget.pack(fill=tk.BOTH, expand=True)
        
        # Tags de coloracao
        self.text_widget.tag_config("keyword", foreground="#569cd6", font=("Courier", 11, "bold"))
        self.text_widget.tag_config("number", foreground="#b5cea8")
        self.text_widget.tag_config("string", foreground="#ce9178")
        self.text_widget.tag_config("function", foreground="#dcdcaa")
        self.text_widget.tag_config("comment", foreground="#6a9955")
        self.text_widget.tag_config("operator", foreground="#d4d4d4")
        
        # Bottom bar com botao Run
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(bottom_frame, text="Run (Ctrl+R)", command=self.run_code,
                 bg="#007acc", fg="white", font=("Arial", 10)).pack(side=tk.RIGHT)
        
        self.status_label = tk.Label(bottom_frame, text="Ready", fg="#d4d4d4", bg="#1e1e1e")
        self.status_label.pack(side=tk.LEFT)
        
        self.root.bind("<Control-r>", lambda e: self.run_code())
        
    def colorize_text(self):
        # Remove todas as tags
        for tag in ["keyword", "number", "string", "function", "comment", "operator"]:
            self.text_widget.tag_remove(tag, "1.0", tk.END)
        
        content = self.text_widget.get("1.0", tk.END)
        
        try:
            scanner = Scanner("editor", content)
            tokens, error = scanner.make_tokens()
            
            if error:
                return
            
            for token in tokens:
                if token.type == TT_KEYWORD and token.value in KEYWORDS:
                    self.highlight_token(token, "keyword")
                elif token.type == TT_KEYWORD and isinstance(token.value, (int, float)):
                    self.highlight_token(token, "number")
                elif token.type == TT_KEYWORD and isinstance(token.value, tuple) and token.value[0] == 'string_literal':
                    self.highlight_token(token, "string")
                elif token.type == TT_IDENTIFIER:
                    self.highlight_token(token, "function")
                    
        except Exception as e:
            pass
    
    def highlight_token(self, token, tag):
        start_line = token.pos_start.ln + 1
        start_col = token.pos_start.col
        end_line = token.pos_end.ln + 1
        end_col = token.pos_end.col
        
        start_idx = f"{start_line}.{start_col}"
        end_idx = f"{end_line}.{end_col}"
        
        self.text_widget.tag_add(tag, start_idx, end_idx)
    
    def on_key_release(self, event):
        self.colorize_text()
    
    def new_file(self):
        self.text_widget.delete("1.0", tk.END)
        self.filename = None
        self.root.title("UP Language Editor - Untitled")
        self.status_label.config(text="New file")
    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("UP files", "*.up"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert("1.0", content)
                self.filename = file_path
                self.root.title(f"UP Language Editor - {os.path.basename(file_path)}")
                self.status_label.config(text=f"Opened: {file_path}")
                self.colorize_text()
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
    
    def save_file(self):
        if self.filename:
            try:
                with open(self.filename, 'w', encoding='utf-8') as f:
                    f.write(self.text_widget.get("1.0", tk.END))
                self.status_label.config(text=f"Saved: {self.filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".up",
                                                filetypes=[("UP files", "*.up"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.text_widget.get("1.0", tk.END))
                self.filename = file_path
                self.root.title(f"UP Language Editor - {os.path.basename(file_path)}")
                self.status_label.config(text=f"Saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
    
    def run_code(self):
        code = self.text_widget.get("1.0", tk.END)
        
        self.output_widget.config(state=tk.NORMAL)
        self.output_widget.delete("1.0", tk.END)
        
        try:
            result, error = run("editor", code)
            
            if error:
                self.output_widget.insert(tk.END, error.as_string())
            else:
                if result is not None:
                    self.output_widget.insert(tk.END, str(result))
                self.status_label.config(text="Code executed successfully")
        except Exception as e:
            self.output_widget.insert(tk.END, f"Error: {str(e)}")
        
        self.output_widget.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    editor = UpEditor(root)
    root.mainloop()