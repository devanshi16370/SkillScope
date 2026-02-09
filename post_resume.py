import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import userdashboard

def postResume(userId):
    conn = sqlite3.connect('SkillScope.db')
    cursor = conn.cursor()

    def upload_resume():
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
           with open(file_path, "rb") as file:  # read in binary mode
            resume_content = file.read()


            cursor.execute("UPDATE user_details SET resume_content = ? WHERE user_id = ?", 
                        (resume_content, userId))
            conn.commit()
            messagebox.showinfo("✅ Success", "Resume uploaded successfully!")

    def go_back():
        resume_window.destroy()
        userdashboard.user_dashboard(userId)

    # --- Main Window ---
    resume_window = tk.Tk()
    resume_window.title("📄 Upload Resume - SkillScope")
    resume_window.geometry("450x350")
    resume_window.configure(bg="#2C3E50")  # Dark Theme Background

    # --- 🏷 Title Label ---
    title_label = tk.Label(resume_window, text="Upload Your Resume", font=("Arial", 16, "bold"),
                           fg="white", bg="#2C3E50")
    title_label.pack(pady=20)

    # ---  Upload Button ---
    def on_enter(e):
        btn_upload.config(bg="#2980B9")

    def on_leave(e):
        btn_upload.config(bg="#3498DB")

    btn_upload = tk.Button(resume_window, text="📂 Upload Resume", font=("Arial", 12, "bold"),
                           bg="#3498DB", fg="white", relief="flat", padx=20, pady=10, cursor="hand2",
                           command=upload_resume)
    btn_upload.pack(pady=10)
    btn_upload.bind("<Enter>", on_enter)
    btn_upload.bind("<Leave>", on_leave)

    # --- ⬅ Back Button ---
    btn_back = tk.Button(resume_window, text="⬅ Back", font=("Arial", 12, "bold"),
                         bg="#95A5A6", fg="white", relief="flat", width=15, cursor="hand2",
                         command=go_back)
    btn_back.pack(pady=20)

    resume_window.mainloop()
    conn.close()
