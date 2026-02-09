import tkinter as tk
from tkinter import messagebox
import sqlite3
import userdashboard

def edit_Profile(userID):
    conn = sqlite3.connect('SkillScope.db')
    cursor = conn.cursor()

    def update_profile():
        try:
            cursor.execute("UPDATE users SET username=?, email=?, phone_no=? WHERE user_id=?", 
                           (username_entry.get(), email_entry.get(), phone_entry.get(), userID))
            cursor.execute("UPDATE user_details SET top_skill=? WHERE user_id=?", 
                           (skills_entry.get(), userID))
            conn.commit()
            messagebox.showinfo("Success", "Profile updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile: {e}")

    def go_back():
        edit_window.destroy()
        userdashboard.user_dashboard(userID)

    edit_window = tk.Tk()
    edit_window.title("Edit Profile")
    edit_window.geometry("500x450")
    edit_window.configure(bg="#2C3E50")  # Dark background

    # Card Frame
    frame = tk.Frame(edit_window, bg="#34495E", padx=20, pady=20)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    tk.Label(frame, text="Edit Profile", font=("Arial", 16, "bold"), fg="white", bg="#34495E").pack(pady=10)

    def create_entry(label_text):
        tk.Label(frame, text=label_text, font=("Arial", 10, "bold"), fg="white", bg="#34495E").pack(anchor="w", pady=3)
        entry = tk.Entry(frame, font=("Arial", 12), bg="#ECF0F1", relief="flat", width=30)
        entry.pack(pady=5)
        return entry

    username_entry = create_entry("Username")
    email_entry = create_entry("Email")
    phone_entry = create_entry("Phone Number")
    skills_entry = create_entry("Top Skills (comma-separated)")

    # Styled Button with Hover Effect
    def on_enter(e):
        e.widget.config(bg="#2980B9")

    def on_leave(e):
        e.widget.config(bg="#3498DB")

    btn_update = tk.Button(frame, text="Update Profile", font=("Arial", 12, "bold"),
                           bg="#3498DB", fg="white", relief="flat", width=20, command=update_profile)
    btn_update.pack(pady=10)
    btn_update.bind("<Enter>", on_enter)
    btn_update.bind("<Leave>", on_leave)

    btn_back = tk.Button(frame, text="Back", font=("Arial", 10, "bold"),
                         bg="#95A5A6", fg="white", relief="flat", width=20, command=go_back)
    btn_back.pack(pady=5)

    edit_window.mainloop()
    conn.close()
