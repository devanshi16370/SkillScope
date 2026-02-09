import tkinter as tk
from tkinter import messagebox
import sqlite3
import signup_gui
import recruiter_dashboard
import userdashboard

def Login(usertype):
    def connect_db():
        return sqlite3.connect("SkillScope.db")

    def signup_page():
        login_window.destroy()
        signup_gui.open_signup_window(usertype)  # Make sure this function exists

    def login_user():
        username = username_var.get()
        password = password_var.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ? AND type = ?", 
                           (username, password, usertype))
            user = cursor.fetchone()
            if not user:
                messagebox.showerror("Error", "Invalid credentials!")
                return

            user_id = user[0]
            login_window.destroy()

            if usertype == "recruiter":
                cursor.execute("SELECT recruiter_id, company_name FROM recruiters_details WHERE user_id = ?", (user_id,))
                rec = cursor.fetchone()
                recruiter_dashboard.recruiter_dashboard(rec[0], rec[1])
            else:
                userdashboard.user_dashboard(user_id)

            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    # === Tkinter Window ===
    login_window = tk.Tk()
    login_window.title("Login - SkillScope")
    login_window.geometry("1000x1000")
    login_window.minsize(600, 400)
    login_window.configure(bg="#1e2a38")

    # === Background Frame ===
    wrapper = tk.Frame(login_window, bg="#1e2a38")
    wrapper.pack(fill="both", expand=True)

    # === Centered Form Frame ===
    form = tk.Frame(wrapper, bg="#2a3d53", padx=40, pady=30)
    form.place(relx=0.5, rely=0.5, anchor="center")

    # === Form Content ===
    tk.Label(form, text="Login", font=("Helvetica", 20, "bold"), bg="#2a3d53", fg="white").pack(pady=(0, 20))

    username_var = tk.StringVar()
    password_var = tk.StringVar()

    def input_field(label, var, show=""):
        tk.Label(form, text=label, bg="#2a3d53", fg="white", anchor="w").pack(fill="x")
        entry = tk.Entry(form, textvariable=var, show=show, font=("Helvetica", 11), bg="white")
        entry.pack(fill="x", pady=(0, 15))

    input_field("Username", username_var)
    input_field("Password", password_var, show="*")

    tk.Button(form, text="Login", command=login_user, bg="#10b981", fg="white",
              font=("Helvetica", 11, "bold")).pack(fill="x", pady=(0, 10))

    tk.Button(form, text="Don't have an account?", command=signup_page,
              bg="#6b7280", fg="white").pack(fill="x")

    # === Recenter form on resize ===
    def recenter(event):
        form.place(relx=0.5, rely=0.5, anchor="center")

    login_window.bind("<Configure>", recenter)
    login_window.mainloop()
