import requests
import tkinter as tk
from tkinter import messagebox, ttk

URL = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"

history = []  # store all fetched facts


# ---------------- FACT FETCHING ---------------- #

def get_random_fact():
    fact_label.config(text="⏳ Fetching fact...")
    root.update_idletasks()  # refresh UI immediately

    try:
        response = requests.get(URL, timeout=5)

        if response.status_code == 200:
            fact = response.json()['text']
            display_text = f"💡 Did you know?\n\n{fact}"

            fact_label.config(text=display_text)
            history.append(fact)

        else:
            messagebox.showerror("Error", "Failed to fetch fact (Server Error).")

    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error", "Please check your internet connection.")


# ---------------- SAVE FACT ---------------- #

def save_fact():
    text = fact_label.cget("text")
    if text.strip() == "":
        messagebox.showinfo("Nothing to Save", "Get a fact first.")
        return

    with open("facts_log.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

    messagebox.showinfo("Saved", "Fact saved to facts_log.txt!")


# ---------------- COPY TO CLIPBOARD ---------------- #

def copy_fact():
    text = fact_label.cget("text")
    if text.strip() == "":
        messagebox.showinfo("Nothing to Copy", "Get a fact first.")
        return

    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Copied", "Fact copied to clipboard!")


# ---------------- FACT HISTORY WINDOW ---------------- #

def show_history():
    if not history:
        messagebox.showinfo("No History", "No facts fetched yet.")
        return

    hist_win = tk.Toplevel(root)
    hist_win.title("Fact History")
    hist_win.geometry("500x400")

    text_box = tk.Text(hist_win, wrap="word", font=("Arial", 11))
    text_box.pack(expand=True, fill="both")

    for fact in history:
        text_box.insert("end", f"• {fact}\n\n")

    text_box.config(state="disabled")


# ---------------- DARK MODE ---------------- #

def toggle_dark_mode():
    if dark_mode_var.get():
        root.configure(bg="#8F8F8FFF")
        fact_label.configure(bg="#1e1e1e", fg="white")
        title_label.configure(bg="#1e1e1e", fg="white")
    else:
        root.configure(bg="white")
        fact_label.configure(bg="white", fg="black")
        title_label.configure(bg="white", fg="black")


# ---------------- GUI SETUP ---------------- #

root = tk.Tk()
root.title("Random Fact Generator")
root.geometry("550x350")
root.configure(bg="white")

title_label = tk.Label(root, text="Random Fact Generator", font=("Arial", 18, "bold"), bg="white")
title_label.pack(pady=10)

fact_label = tk.Label(root, text="", wraplength=500, justify="center", font=("Arial", 12), bg="white")
fact_label.pack(pady=20)

btn_frame = tk.Frame(root, bg="white")
btn_frame.pack(pady=10)

get_btn = tk.Button(btn_frame, text="Get Fact", font=("Arial", 12), command=get_random_fact)
get_btn.grid(row=0, column=0, padx=10)

save_btn = tk.Button(btn_frame, text="Save Fact", font=("Arial", 12), command=save_fact)
save_btn.grid(row=0, column=1, padx=10)

copy_btn = tk.Button(btn_frame, text="Copy", font=("Arial", 12), command=copy_fact)
copy_btn.grid(row=0, column=2, padx=10)

history_btn = tk.Button(btn_frame, text="History", font=("Arial", 12), command=show_history)
history_btn.grid(row=0, column=3, padx=10)

# Dark mode toggle
dark_mode_var = tk.BooleanVar()
dark_mode_check = tk.Checkbutton(root, text="Dark Mode", variable=dark_mode_var,
                                 command=toggle_dark_mode, bg="white")
dark_mode_check.pack(pady=5)

quit_btn = tk.Button(root, text="Quit", font=("Arial", 12), command=root.quit)
quit_btn.pack(pady=10)

root.mainloop()
