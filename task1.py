import subprocess
import sys
import nltk
import tkinter as tk
from tkinter import scrolledtext, messagebox
from transformers import pipeline
import threading

# --- Install essential libraries if missing ---
def install_packages():
    packages = ["transformers", "torch", "nltk"]
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

install_packages()

# Ensure punkt tokenizer is available
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# Load summarizer model pipeline
summarizer = pipeline("summarization")

# --- Start GUI ---
app = tk.Tk()
app.title("🤖 TEXT SUMMARIZATION TOOL")
app.geometry("950x720")

# --- Define Theme Colors & Fonts ---
PRIMARY_COLOR = "#4B0082"     # Indigo
SECONDARY_COLOR = "#E6E6FA"   # Lavender
app.config(bg=SECONDARY_COLOR)

FONT_TITLE = ("Poppins", 20, "bold")
FONT_LABEL = ("Poppins", 12)
FONT_TEXT = ("Poppins", 11)

# --- GUI Layout ---

# Title
tk.Label(app, text="🧠 TEXT SUMMARIZATION TOOL", font=FONT_TITLE, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR).pack(pady=10)

# Token Counter
token_var = tk.StringVar()
token_var.set("Words: 0")
token_label = tk.Label(app, textvariable=token_var, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR, font=FONT_LABEL)
token_label.pack(anchor="e", padx=20)

# Input Label
tk.Label(app, text="Paste your long content/article here:", font=FONT_LABEL, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR).pack(anchor="w", padx=20)

# Input Text Area
input_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, height=15, font=FONT_TEXT)
input_area.pack(padx=20, pady=(5, 15), fill="both", expand=True)

# Summary Length Slider
tk.Label(app, text="Set maximum summary length (words):", font=FONT_LABEL, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR).pack(anchor="w", padx=20)
length_slider = tk.Scale(app, from_=50, to=300, orient=tk.HORIZONTAL, length=300)
length_slider.set(180)
length_slider.pack(pady=(0, 10))

# Output Label
tk.Label(app, text="Summary Output:", font=FONT_LABEL, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR).pack(anchor="w", padx=20)

# Output Text Area
output_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, height=10, font=FONT_TEXT, bg="white", fg="black")
output_area.pack(padx=20, pady=10, fill="both", expand=True)

# --- Functionalities ---

# Live Word Counter
def update_word_count(event=None):
    text = input_area.get("1.0", tk.END)
    word_count = len(text.strip().split())
    token_var.set(f"Words: {word_count}")

input_area.bind("<KeyRelease>", update_word_count)

# Summarize Logic
def summarize_text():
    text = input_area.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Missing Input", "Please enter some text.")
        return

    output_area.delete("1.0", tk.END)
    output_area.insert(tk.END, "🔄 Summarizing...")

    summarize_btn.config(state="disabled")

    def run_summary():
        try:
            max_len = length_slider.get()
            min_len = max(30, max_len // 2)
            summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
            output_area.delete("1.0", tk.END)
            output_area.insert(tk.END, summary[0]['summary_text'])
        except Exception as e:
            output_area.delete("1.0", tk.END)
            output_area.insert(tk.END, f"Error: {str(e)}")
        finally:
            summarize_btn.config(state="normal")

    threading.Thread(target=run_summary).start()

# Clear Text
def clear_text():
    input_area.delete("1.0", tk.END)
    output_area.delete("1.0", tk.END)
    token_var.set("Words: 0")

# Buttons
frame = tk.Frame(app, bg=SECONDARY_COLOR)
frame.pack(pady=10)

summarize_btn = tk.Button(frame, text="✨ Summarize", command=summarize_text,
                          font=FONT_LABEL, bg=PRIMARY_COLOR, fg="white", padx=15, pady=5)
summarize_btn.grid(row=0, column=0, padx=10)

clear_btn = tk.Button(frame, text="🧹 Clear All", command=clear_text,
                      font=FONT_LABEL, bg="#8B0000", fg="white", padx=15, pady=5)
clear_btn.grid(row=0, column=1, padx=10)

# --- Mainloop ---
app.mainloop()
