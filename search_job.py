import tkinter as tk
from tkinter import ttk
import sqlite3
import userdashboard

def search_JOB(userId):
    conn = sqlite3.connect('SkillScope.db')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT location FROM jobs")
    locations = [row[0] for row in cursor.fetchall()]
    locations.insert(0, "All")

    def search_jobs():
        selected_location = location_var.get()
        skill_query = skill_entry.get().strip()

        query = "SELECT job_id, job_position, skills_required, salary, location FROM jobs WHERE 1=1"
        params = []

        if selected_location != "All":
            query += " AND location = ?"
            params.append(selected_location)

        if skill_query:
            query += " AND skills_required LIKE ?"
            params.append(f"%{skill_query}%")

        cursor.execute(query, params)
        filtered_jobs = cursor.fetchall()

        for row in job_tree.get_children():
            job_tree.delete(row)

        for job in filtered_jobs:
            job_tree.insert("", tk.END, values=job)

    def go_back():
        search_window.destroy()
        userdashboard.user_dashboard(userId)

    search_window = tk.Tk()
    search_window.title("🔍 Job Search - SkillScope")
    search_window.geometry("850x550")
    search_window.configure(bg="#2C3E50")  # Dark-themed background

    # ---  Title Label ---
    title_label = tk.Label(search_window, text="Find Your Dream Job", font=("Arial", 16, "bold"), fg="white", bg="#2C3E50")
    title_label.pack(pady=10)

    # --- Search Filters ---
    filter_frame = tk.Frame(search_window, bg="#34495E", padx=20, pady=10)
    filter_frame.pack(pady=10, fill="x")

    tk.Label(filter_frame, text="📍 Location:", font=("Arial", 10, "bold"), fg="white", bg="#34495E").grid(row=0, column=0, padx=10)
    location_var = tk.StringVar(value="All")
    location_dropdown = ttk.Combobox(filter_frame, textvariable=location_var, values=locations, state="readonly", font=("Arial", 10))
    location_dropdown.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(filter_frame, text="💼 Skill:", font=("Arial", 10, "bold"), fg="white", bg="#34495E").grid(row=0, column=2, padx=10)
    skill_entry = tk.Entry(filter_frame, font=("Arial", 10), width=20)
    skill_entry.grid(row=0, column=3, padx=10, pady=5)

    # --- 🔘 Search Button ---
    def on_enter(e):
        search_btn.config(bg="#2980B9")

    def on_leave(e):
        search_btn.config(bg="#3498DB")

    search_btn = tk.Button(filter_frame, text="🔍 Search", font=("Arial", 10, "bold"), 
                           bg="#3498DB", fg="white", relief="flat", padx=10, command=search_jobs)
    search_btn.grid(row=0, column=4, padx=10, pady=5)
    search_btn.bind("<Enter>", on_enter)
    search_btn.bind("<Leave>", on_leave)

    # ---Job Results Table ---
    columns = ("Job ID", "Job Title", "Skills Required", "Salary", "Location")
    job_tree = ttk.Treeview(search_window, columns=columns, show='headings', height=12)

    for col in columns:
        job_tree.heading(col, text=col, anchor="center")
        job_tree.column(col, anchor="center", width=150 if col != "Skills Required" else 250)

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 10))
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#34495E", foreground="black")

    job_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ---Back Button ---
    back_btn = tk.Button(search_window, text="⬅ Back", font=("Arial", 10, "bold"), 
                         bg="#95A5A6", fg="white", relief="flat", width=15, command=go_back)
    back_btn.pack(pady=10)

    search_window.mainloop()
    conn.close()
