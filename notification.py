import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ✅ Add a new notification (role: 'user' or 'recruiter')
def add_notification(user_id, message, role="user"):
    conn = sqlite3.connect("SkillScope.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notifications (user_id, message, role, is_read, created_at)
        VALUES (?, ?, ?, 0, ?)
    """, (user_id, message, role, datetime.now()))
    conn.commit()
    conn.close()

# ✅ Get all notifications for a user/recruiter by role
def get_notifications(user_id, role="user"):
    conn = sqlite3.connect("SkillScope.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT notification_id, message, is_read, created_at 
        FROM notifications 
        WHERE user_id = ? AND role = ?
        ORDER BY created_at DESC
    """, (user_id, role))
    data = cursor.fetchall()
    conn.close()
    return data

# ✅ Show notifications in a popup window
def show_notifications(user_id, role="user"):
    notifications = get_notifications(user_id, role)

    notif_window = tk.Toplevel()
    notif_window.title("Your Notifications")
    notif_window.geometry("400x400")
    notif_window.configure(bg="white")

    if not notifications:
        tk.Label(notif_window, text="No notifications available.", bg="white", fg="gray").pack(pady=20)
        return

    for notif in notifications:
        notif_id, message, is_read, created_at = notif
        color = "black" if is_read else "blue"
        tk.Label(
            notif_window,
            text=f"{message}\n🕒 {created_at}",
            fg=color,
            bg="white",
            wraplength=360,
            justify="left",
            anchor="w"
        ).pack(pady=10, anchor="w", padx=10)

    mark_all_as_read(user_id, role)

# ✅ Mark all notifications as read
def mark_all_as_read(user_id, role="user"):
    conn = sqlite3.connect("SkillScope.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ? AND role = ?", (user_id, role))
    conn.commit()
    conn.close()

# ✅ Get unread notification count
def get_unread_count(user_id, role="user"):
    conn = sqlite3.connect("SkillScope.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM notifications 
        WHERE user_id = ? AND role = ? AND is_read = 0
    """, (user_id, role))
    count = cursor.fetchone()[0]
    conn.close()
    return count
