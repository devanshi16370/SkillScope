import re
import sqlite3
import tkinter as tk
from tkinter import messagebox
from user_details import open_user_details
from recruiters_details import open_recruiter_details
from login import Login
import Setup_database

def Signup(usertype):
    def open_login_page():
        root.destroy()
        Login(usertype)

    def connect_db():
        conn = sqlite3.connect("SkillScope.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone_no TEXT NOT NULL UNIQUE,
                type TEXT NOT NULL
            )
        """)
        conn.commit()
        return conn

    def is_valid_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email)

    def is_valid_password(password):
        return len(password) >= 8 and not password.islower() and not password.isupper()

    def register_user():
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        email = entry_email.get().strip()
        phone_no = entry_phone.get().strip()

        if not username or not password or not email or not phone_no or not usertype:
            messagebox.showerror("Error", "All fields are required!")
            return

        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        if not is_valid_password(password):
            messagebox.showerror("Error", "Password must be at least 8 characters and contain both uppercase and lowercase letters.")
            return

        if not phone_no.isdigit() or len(phone_no) > 15:
            messagebox.showerror("Error", "Invalid phone number!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, email, phone_no, type) VALUES (?, ?, ?, ?, ?)",
                           (username, password, email, phone_no, usertype))
            conn.commit()

            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()[0]

            conn.close()
            messagebox.showinfo("Success", f"{usertype.capitalize()} registered successfully!")
            root.destroy()

            if usertype == 'user':
                open_user_details(user_id, username)
            else:
                open_recruiter_details(user_id, username)

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username, Email, or Phone number already exists!")

    # 🖥️ Root Window
    root = tk.Tk()
    root.title("Signup - SkillScope")
    root.geometry("1000x1000")
    root.minsize(600, 400)
    root.configure(bg="#1e2a38")

    # Outer Frame (fills full window)
    wrapper = tk.Frame(root, bg="#1e2a38")
    wrapper.pack(fill="both", expand=True)

    # Centered Form Frame
    form = tk.Frame(wrapper, bg="#2a3d53", padx=30, pady=30)
    form.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(form, text="Signup", font=("Arial", 20, "bold"), bg="#2a3d53", fg="white").pack(pady=(0, 20))

    def create_entry(label_text, show=""):
        tk.Label(form, text=label_text, font=("Arial", 11), fg="white", bg="#2a3d53").pack(anchor="w")
        entry = tk.Entry(form, font=("Arial", 11), width=30, bg="white", show=show)
        entry.pack(pady=(0, 10))
        return entry

    entry_username = create_entry("Username")
    entry_password = create_entry("Password", show="*")
    entry_email = create_entry("Email")
    entry_phone = create_entry("Phone Number")

    # Buttons
    def on_enter(e): e.widget.config(bg="#2980B9")
    def on_leave(e): e.widget.config(bg="#3498DB")

    register_btn = tk.Button(form, text=f"Register as {usertype}", command=register_user,
                             bg="#3498DB", fg="white", font=("Arial", 12, "bold"))
    register_btn.pack(fill="x", pady=(10, 5))
    register_btn.bind("<Enter>", on_enter)
    register_btn.bind("<Leave>", on_leave)

    login_btn = tk.Button(form, text="Already Have an Account?", command=open_login_page,
                          bg="#95A5A6", fg="white", font=("Arial", 10))
    login_btn.pack(fill="x", pady=(0, 10))

    # 📐 Centering logic on resize
    def recenter(event):
        form.place(relx=0.5, rely=0.5, anchor="center")

    root.bind("<Configure>", recenter)
    root.mainloop()
