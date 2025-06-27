import customtkinter as ctk
import re
import random
import string
import pyperclip
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def check_strength(password):
    score = 0
    suggestions = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 12 characters.")

    if re.search(r"[A-Z]", password): score += 1
    else: suggestions.append("Add uppercase letters.")
    if re.search(r"[a-z]", password): score += 1
    else: suggestions.append("Add lowercase letters.")
    if re.search(r"\d", password): score += 1
    else: suggestions.append("Include numbers.")
    if re.search(r"[!@#$%^&*()_+{}\[\]:;,.<>?]", password): score += 1
    else: suggestions.append("Use special characters.")

    return score, suggestions


def update_strength(*args):
    pwd = password_entry.get()
    score, _ = check_strength(pwd)

    strength_bar.set(score / 7)

    if score >= 6:
        result_label.configure(text="🟢 Strong", text_color="lime")
    elif 4 <= score < 6:
        result_label.configure(text="🟡 Moderate", text_color="orange")
    else:
        result_label.configure(text="🔴 Weak", text_color="red")


def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(chars, k=14))
    password_entry.delete(0, "end")
    password_entry.insert(0, password)
    update_strength()
    toggle_clear_button()


def toggle_password():
    if show_toggle.get() == 1:
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*")


def copy_password():
    try:
        pyperclip.copy(password_entry.get())
        copied_label.configure(text="✅ Copied to clipboard", text_color="skyblue")
    except pyperclip.PyperclipException:
        copied_label.configure(text="❌ Install xclip (Linux)", text_color="red")


def toggle_theme():
    current = ctk.get_appearance_mode()
    new_theme = "light" if current == "Dark" else "dark"
    ctk.set_appearance_mode(new_theme)

    # Update button text colors based on theme
    text_color = "black" if new_theme == "light" else "white"
    generate_btn.configure(text_color=text_color)
    copy_btn.configure(text_color=text_color)
    check_btn.configure(text_color=text_color)
    theme_btn.configure(text_color=text_color)


def check_and_show():
    pwd = password_entry.get()
    score, tips = check_strength(pwd)

    update_strength()

    if score >= 6:
        msg = "✅ Strong password!"
    elif score >= 4:
        msg = "⚠️ Moderate password."
    else:
        msg = "❌ Weak password."

    if tips:
        msg += "\n\nSuggestions:\n" + "\n".join(f"• {tip}" for tip in tips)

    messagebox.showinfo("Strength Check", msg)


def clear_password():
    password_entry.delete(0, 'end')
    strength_bar.set(0)
    result_label.configure(text="")
    copied_label.configure(text="")
    clear_icon_btn.place_forget()


def toggle_clear_button(*args):
    if password_entry.get():
        x = password_entry.winfo_x() + password_entry.winfo_width() - 25
        y = password_entry.winfo_y() + 3
        clear_icon_btn.place(x=x, y=y)
    else:
        clear_icon_btn.place_forget()


app = ctk.CTk()
app.title("🔐 Password Validator ")
app.geometry("900x600")
app.minsize(700, 500)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

frame = ctk.CTkFrame(app, corner_radius=20)
frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)

frame.grid_columnconfigure(0, weight=1)

header = ctk.CTkLabel(master=frame, text="💾 Password Strength Checker", font=("Consolas", 22, "bold"))
header.grid(row=0, column=0, pady=(20, 10))

password_entry = ctk.CTkEntry(master=frame, width=500, height=40, font=("Consolas", 16), show="*", placeholder_text="Enter your password")
password_entry.grid(row=1, column=0, pady=10, padx=20)

def enable_shortcuts(event):
    widget = event.widget
    if event.state == 4:
        if event.keysym == "a":
            widget.select_range(0, 'end')
            return "break"
        elif event.keysym == "c":
            widget.event_generate("<<Copy>>")
            return "break"
        elif event.keysym == "v":
            widget.event_generate("<<Paste>>")
            return "break"
        elif event.keysym == "x":
            widget.event_generate("<<Cut>>")
            return "break"

password_entry.bind("<KeyRelease>", lambda e: (update_strength(), toggle_clear_button()))
password_entry.bind("<FocusIn>", lambda e: (password_entry.select_range(0, 'end'), toggle_clear_button()))
password_entry.bind("<Control-a>", lambda e: (password_entry.select_range(0, 'end'), "break"))
password_entry.bind("<KeyPress>", enable_shortcuts)

clear_icon_btn = ctk.CTkButton(
    master=frame,
    text="❌",
    width=30,
    height=30,
    fg_color="transparent",
    hover_color="#444",
    text_color="red",
    font=("Arial", 14),
    command=clear_password
)
clear_icon_btn.place_forget()

show_toggle = ctk.CTkCheckBox(master=frame, text="Show Password", command=toggle_password)
show_toggle.grid(row=2, column=0)

strength_bar = ctk.CTkProgressBar(master=frame, width=500)
strength_bar.grid(row=3, column=0, pady=15)
strength_bar.set(0)

result_label = ctk.CTkLabel(master=frame, text="", font=("Consolas", 16, "bold"))
result_label.grid(row=4, column=0)

button_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
button_frame.grid(row=5, column=0, pady=20)

generate_btn = ctk.CTkButton(master=button_frame, text="🔁 Generate Password", command=generate_password)
generate_btn.grid(row=0, column=0, padx=10)

copy_btn = ctk.CTkButton(master=button_frame, text="📋 Copy", command=copy_password)
copy_btn.grid(row=0, column=1, padx=10)

check_btn = ctk.CTkButton(master=button_frame, text="✔️ Check Strength", command=check_and_show)
check_btn.grid(row=0, column=2, padx=10)

theme_btn = ctk.CTkButton(master=frame, text="🌓 Toggle Theme", command=toggle_theme)
theme_btn.grid(row=6, column=0)

copied_label = ctk.CTkLabel(master=frame, text="", font=("Consolas", 12))
copied_label.grid(row=7, column=0, pady=10)

app.mainloop()

