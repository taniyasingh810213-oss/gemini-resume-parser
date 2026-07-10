import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import fitz  # PyMuPDF
from google import genai

# --- Premium Palette ---
WINDOW_BG = "#EFEFFF"         # Modern soft cool-tint background
CARD_BG = "#FFFFFF"           # Crisp white card panels
TEXT_MAIN = "#50506E"         # Deep luxury dark navy
TEXT_MUTED = "#7579E7"        # Electric pastel purple for labels
ACCENT_BLUE = "#4D77FF"       # Soft accent blue
ACCENT_GREEN = "#20BF6B"      # Sleek mint green for success

def browse_file():
    file_path = filedialog.askopenfilename(
        title="Select a Resume or Document",
        filetypes=[("PDF Files", "*.pdf"), ("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if file_path:
        try:
            text_input.delete("1.0", tk.END)
            if file_path.lower().endswith('.pdf'):
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                text_input.insert(tk.END, text)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text_input.insert(tk.END, f.read())
                    
            status_label.config(text=f"📂 Loaded: {file_path.split('/')[-1]}", fg=ACCENT_BLUE)
        except Exception as e:
            messagebox.showerror("Error Reading File", f"Could not read file:\n{str(e)}")

def process_data():
    user_text = text_input.get("1.0", tk.END).strip()
    if not user_text:
        messagebox.showwarning("Warning", "Please enter text or choose a file first!")
        return
    
    try:
        # Paste your API key here inside the quotes
        import os
        client = genai.Client(api_key=os.environ.get("GEMINI API KEY"))
        
        status_label.config(text="🧠 Analyzing structure with Gemini...", fg=ACCENT_BLUE)
        root.update_idletasks()
        
        prompt = "Extract the name, email, skills, and work experience from this text."
        
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=[prompt, user_text],
        )
        
        output_display.config(state=tk.NORMAL)
        output_display.delete("1.0", tk.END)
        output_display.insert(tk.END, response.text)
        output_display.config(state=tk.DISABLED)
        
        status_label.config(text="✨ Data parsing complete!", fg=ACCENT_GREEN)
        
    except Exception as e:
        status_label.config(text="❌ Interface Error", fg="#FF4D4D")
        messagebox.showerror("Google API Error", str(e))

# Focus effects for custom graphics look
def on_focus_in(event):
    input_card.config(highlightbackground=ACCENT_BLUE, highlightthickness=2)

def on_focus_out(event):
    input_card.config(highlightbackground="#E5E9ED", highlightthickness=1)

# --- Main Engine ---
root = tk.Tk()
root.title("Gemini Intelligent Parser")
root.geometry("680x820")
root.configure(bg=WINDOW_BG)

# 1. Gradient-Style Top Header Banner
header_canvas = tk.Canvas(root, height=80, bg=TEXT_MAIN, highlightthickness=0)
header_canvas.pack(fill="x", pady=(0, 20))
header_canvas.create_text(40, 40, text="✨ AI RESUME PARSER", fill="#131111", font=("Segoe UI", 16, "bold"), anchor="w")
header_canvas.create_text(640, 40, text="V2.5 PRO", fill=TEXT_MUTED, font=("Segoe UI", 10, "bold"), anchor="e")

# Main Container for Card-styled Elements
container = tk.Frame(root, bg=WINDOW_BG)
container.pack(fill="both", expand=True, padx=35)

# 2. Input Box Section Header
lbl_frame = tk.Frame(container, bg=WINDOW_BG)
lbl_frame.pack(fill="x", pady=(5, 5))
tk.Label(lbl_frame, text="SOURCE DOCUMENT", font=("Segoe UI", 9, "bold"), bg=WINDOW_BG, fg=TEXT_MUTED).pack(side="left")

# Stylized Flat File Button
browse_btn = tk.Button(
    lbl_frame, text="📁 UPLOAD FILE", font=("Segoe UI", 8, "bold"),
    bg=ACCENT_BLUE, fg="white", activebackground="#E1E4ED", activeforeground="white",
    relief="flat", padx=15, pady=4, cursor="hand2"
)
browse_btn.config(command=browse_file)
browse_btn.pack(side="right")

# White Input Card (With Glow Framework)
input_card = tk.Frame(container, bg=CARD_BG, highlightbackground="#192B43", highlightthickness=1)
input_card.pack(fill="x", pady=(0, 15))

text_input = scrolledtext.ScrolledText(
    input_card, height=10, font=("Consolas", 10), 
    bg=CARD_BG, fg=TEXT_MAIN, relief="flat", bd=0, insertbackground=TEXT_MAIN
)
text_input.pack(fill="both", expand=True, padx=12, pady=12)
text_input.bind("<FocusIn>", on_focus_in)
text_input.bind("<FocusOut>", on_focus_out)

# 3. Large High-Graphics Action Button
run_btn = tk.Button(
    container, text="RUN INTELLIGENT EXTRACTION", font=("Segoe UI", 11, "bold"), 
    bg=ACCENT_GREEN, fg="white", activebackground="#959698", activeforeground="white",
    pady=12, command=process_data, relief="flat", cursor="hand2", bd=0
)
run_btn.pack(fill="x", pady=10)

# Status Engine Display
status_label = tk.Label(container, text="System Core Ready", font=("Segoe UI", 9, "italic"), bg=WINDOW_BG, fg=TEXT_MAIN)
status_label.pack(pady=5)

# 4. Output Results Card
tk.Label(container, text="PARSED STRUCTURAL DATA", font=("Segoe UI", 9, "bold"), bg=WINDOW_BG, fg=TEXT_MUTED).pack(anchor="w", pady=(15, 5))

output_card = tk.Frame(container, bg=CARD_BG, highlightbackground="#1A2C42", highlightthickness=1)
output_card.pack(fill="both", expand=True, pady=(0, 25))

output_display = scrolledtext.ScrolledText(
    output_card, font=("Segoe UI", 10), 
    bg=CARD_BG, fg=TEXT_MAIN, relief="flat", bd=0, state=tk.DISABLED
)
output_display.pack(fill="both", expand=True, padx=12, pady=12)

root.mainloop()
