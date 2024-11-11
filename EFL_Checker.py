import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def extract_unique_paths(file_path):
    try:
        # Read the file in binary mode
        with open(file_path, 'rb') as f:
            file_contents = f.read()
        decoded_contents = file_contents.decode('utf-8', errors='ignore')

        # Patterns to find paths starting with "chr" or "eft"
        pattern1 = r'\bchr[a-zA-Z0-9_/\\.-]*\b'
        pattern2 = r'\beft[a-zA-Z0-9_/\\.-]*\b'

        # Combine matches and remove duplicates
        matches = re.findall(pattern1, decoded_contents) + re.findall(pattern2, decoded_contents)
        unique_matches = set(matches)

        # Process matches based on specific conditions
        modified_matches = []
        for match in unique_matches:
            if r"\tex" in match:
                if match.endswith('_BM'):
                    modified_matches.append(match + '.tex')
                else:
                    modified_matches.append(match + '.ean')
            else:
                modified_matches.append(match + '.mod')
        
        result = sorted(modified_matches)
        output_text = f"{os.path.basename(file_path)}\nFile Paths Found:\n" + "\n".join(result)
        return output_text
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return ""

def browse_file():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=(("All Files", "*.*"),))
    if file_path:
        selected_file.set(file_path)

def process_file():
    file_path = selected_file.get()
    if file_path:
        output_text = extract_unique_paths(file_path)
        output_display.delete(1.0, tk.END)
        output_display.insert(tk.END, output_text)
    else:
        messagebox.showwarning("Warning", "Please select a file first.")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    if dark_mode:
        app.config(bg="#2E2E2E")
        file_frame.config(bg="#2E2E2E")
        label_file.config(bg="#2E2E2E", fg="white")
        entry_file.config(bg="#2E2E2E", fg="white", insertbackground="white")
        btn_browse.config(bg="#5D5D5D", fg="white")
        btn_process.config(bg="#5D5D5D", fg="white")
        btn_theme.config(bg="#5D5D5D", fg="white")
        output_display.config(bg="#3E3E3E", fg="white", insertbackground="white")
    else:
        app.config(bg="white")
        file_frame.config(bg="white")
        label_file.config(bg="white", fg="black")
        entry_file.config(bg="white", fg="black", insertbackground="black")
        btn_browse.config(bg="lightgray", fg="black")
        btn_process.config(bg="lightgray", fg="black")
        btn_theme.config(bg="lightgray", fg="black")
        output_display.config(bg="white", fg="black", insertbackground="black")

# Set up the main window
app = tk.Tk()
app.title("EFL Path Extractor")
app.geometry("600x450")

# Initialize theme
dark_mode = False

# File selection and processing controls
selected_file = tk.StringVar()
file_frame = tk.Frame(app)
file_frame.pack(pady=10)

label_file = tk.Label(file_frame, text="Selected File:")
label_file.grid(row=0, column=0, padx=5)

entry_file = tk.Entry(file_frame, textvariable=selected_file, width=50)
entry_file.grid(row=0, column=1, padx=5)

btn_browse = tk.Button(file_frame, text="Browse", command=browse_file)
btn_browse.grid(row=0, column=2, padx=5)

btn_process = tk.Button(app, text="Process File", command=process_file)
btn_process.pack(pady=10)

# Output display area
output_display = scrolledtext.ScrolledText(app, width=70, height=15)
output_display.pack(pady=10)

# Theme toggle button
btn_theme = tk.Button(app, text="Toggle Theme", command=toggle_theme)
btn_theme.pack(pady=5)

apply_theme()  # Apply the initial theme

app.mainloop()
