import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import requests
import threading
import re
import os
import json
from gtts import gTTS
import pygame

# --- เธ•เธฑเนเธเธเนเธฒเน€เธฃเธดเนเธกเธ•เนเธ ---
GEMINI_API_KEY = "AIzaSyCQlVpjn3RVdCucSktE23nTrRDTT3Yx3NE"
SELECTED_MODEL = "gemini-1.5-flash" # เธซเธฃเธทเธญเนเธเนเธฃเธฐเธเธ Auto-detect เธเธฒเธเนเธเนเธ”เธเนเธญเธเธซเธเนเธฒ
USER_NAME = "เธ•เนเธฐ"
SLOGAN = "เธญเธขเธนเนเธเธดเนเธเน เนเธกเนเน€เธเนเธเธ•เธฑเธง"

pygame.mixer.init()

class AICommander:
    def __init__(self, root):
        self.root = root
        self.root.title(f"AI Commander Pro - เธชเธงเธฑเธชเธ”เธตเธเธธเธ“ {USER_NAME}")
        self.root.geometry("900x800")
        self.root.configure(bg="#121212")
        
        self.setup_ui()
        self.safe_update_chat(f"เธฃเธฐเธเธ: เธชเธงเธฑเธชเธ”เธตเธเธฃเธฑเธเธเธธเธ“ {USER_NAME}! เธขเธดเธเธ”เธตเธ•เนเธญเธเธฃเธฑเธเธชเธนเนเธฃเธฐเธเธเธชเธฑเนเธเธเธฒเธฃเธญเธฑเธเธเธฃเธดเธขเธฐ\nเธชเนเธฅเนเธเธเธเธญเธเน€เธฃเธฒเธเธทเธญ: {SLOGAN}\n", "ai")

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # --- Tab 1: Chat & Voice ---
        self.tab_chat = tk.Frame(self.notebook, bg="#121212")
        self.notebook.add(self.tab_chat, text=" ๐’ฌ เธชเธเธ—เธเธฒ & เธชเธฑเนเธเธเธฒเธฃ ")

        # Toolbar
        toolbar = tk.Frame(self.tab_chat, bg="#1E1E1E")
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(toolbar, text="๐“ เธเธฑเธ”เธฅเธญเธเนเธเธ—", command=self.copy_chat, bg="#424242", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="๐“ฅ เธงเธฒเธเธเนเธญเธเธงเธฒเธก", command=self.paste_to_input, bg="#424242", fg="white").pack(side=tk.LEFT, padx=5)
        
        self.voice_var = tk.BooleanVar(value=True)
        tk.Checkbutton(toolbar, text="๐” เน€เธเธดเธ”เน€เธชเธตเธขเธ AI", variable=self.voice_var, bg="#1E1E1E", fg="white", selectcolor="#007ACC").pack(side=tk.RIGHT, padx=10)

        # Chat Area
        self.chat_box = scrolledtext.ScrolledText(self.tab_chat, bg="#1E1E1E", fg="white", font=("Tahoma", 11), state=tk.DISABLED)
        self.chat_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.chat_box.tag_config("user", foreground="#4FC3F7")
        self.chat_box.tag_config("ai", foreground="#FFD700")

        # Input Area
        input_frame = tk.Frame(self.tab_chat, bg="#121212")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        self.entry_box = tk.Entry(input_frame, font=("Tahoma", 12), bg="#333", fg="white")
        self.entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry_box.bind("<Return>", lambda e: self.send_command())
        tk.Button(input_frame, text="เธชเนเธเธเธณเธชเธฑเนเธ", command=self.send_command, bg="#007ACC", fg="white", width=12).pack(side=tk.RIGHT, padx=5)

        # --- Tab 2: Code Editor ---
        self.tab_code = tk.Frame(self.notebook, bg="#121212")
        self.notebook.add(self.tab_code, text=" ๐’ป เธ•เธฑเธงเน€เธเธตเธขเธเนเธเนเธ” ")
        
        self.code_editor = scrolledtext.ScrolledText(self.tab_code, bg="#2D2D2D", fg="#D4D4D4", font=("Consolas", 12))
        self.code_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Button(self.tab_code, text="๐€ RUN CODE (Cloud)", command=self.run_code, bg="#4CAF50", fg="white", font=("Tahoma", 10, "bold")).pack(fill=tk.X, padx=10, pady=5)
        
        self.output_box = scrolledtext.ScrolledText(self.tab_code, height=8, bg="black", fg="#00FF00", font=("Consolas", 10))
        self.output_box.pack(fill=tk.BOTH, padx=10, pady=5)

    # --- Logic Functions ---
    def send_command(self):
        text = self.entry_box.get()
        if not text: return
        self.safe_update_chat(f"เธเธธเธ“ {USER_NAME}: {text}\n", "user")
        self.entry_box.delete(0, tk.END)
        threading.Thread(target=self.call_gemini, args=(text,), daemon=True).start()

    def call_gemini(self, text):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{SELECTED_MODEL}:generateContent?key={GEMINI_API_KEY}"
        # เน€เธเธดเนเธก Context เนเธซเน AI เธฃเธนเนเธเธฑเธเธเธทเนเธญเนเธฅเธฐเธชเนเธฅเนเธเธ
        context = f"User name: {USER_NAME}. Slogan: {SLOGAN}. Answer in Thai. If user asks for code, provide it in ```code``` blocks."
        data = {"contents": [{"parts": [{"text": f"{context}\nUser says: {text}"}]}]}
        
        try:
            res = requests.post(url, json=data, timeout=30)
            reply = res.json()['candidates'][0]['content']['parts'][0]['text']
            self.safe_update_chat(f"AI: {reply}\n\n", "ai")
            
            # เน€เธฅเนเธเน€เธชเธตเธขเธ
            if self.voice_var.get():
                self.play_voice(reply)
            
            # เธ•เธฃเธงเธเธเธฑเธเนเธเนเธ”
            code_match = re.search(r"```(?:\w+)?\n(.*?)```", reply, re.DOTALL)
            if code_match:
                code = code_match.group(1)
                self.root.after(0, lambda: self.update_editor(code))
        except Exception as e:
            self.safe_update_chat(f"โ ๏ธ เธเธดเธ”เธเธฅเธฒเธ”: {e}\n", "error")

    def play_voice(self, text):
        def _speak():
            try:
                clean_text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
                tts = gTTS(text=clean_text, lang='th')
                tts.save("temp_voice.mp3")
                pygame.mixer.music.load("temp_voice.mp3")
                pygame.mixer.music.play()
            except: pass
        threading.Thread(target=_speak, daemon=True).start()

    def update_editor(self, code):
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert(tk.END, code)
        self.notebook.select(1) # เธชเธฅเธฑเธเธซเธเนเธฒเนเธเธ—เธตเนเนเธ—เนเธเนเธเนเธ”

    def run_code(self):
        code = self.code_editor.get("1.0", tk.END)
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, "เธเธณเธฅเธฑเธเธฃเธฑเธเนเธเนเธ”...\n")
        
        def _execute():
            try:
                res = requests.post('https://emkc.org/api/v2/piston/execute', json={
                    "language": "python", "version": "3.10.0", "files": [{"content": code}]
                })
                out = res.json().get('run', {}).get('output', 'No output')
                self.root.after(0, lambda: self.output_box.insert(tk.END, out))
            except Exception as e:
                self.root.after(0, lambda: self.output_box.insert(tk.END, f"Error: {e}"))
        
        threading.Thread(target=_execute, daemon=True).start()

    def copy_chat(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.chat_box.get("1.0", tk.END))

    def paste_to_input(self):
        self.entry_box.insert(tk.INSERT, self.root.clipboard_get())

    def safe_update_chat(self, text, tag):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, text, tag)
        self.chat_box.see(tk.END)
        self.chat_box.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = AICommander(root)
    root.mainloop()
