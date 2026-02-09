import tkinter as tk
from tkinter import scrolledtext

def start_chatbot(role):
    def respond():
        user_input = entry.get().strip().lower()
        chat_display.insert(tk.END, f"You: {user_input}\n")

        if role == "user":
            response = user_responses(user_input)
        elif role == "recruiter":
            response = recruiter_responses(user_input)
        else:
            response = "Unknown role."

        chat_display.insert(tk.END, f"Bot: {response}\n\n")
        entry.delete(0, tk.END)

    def user_responses(message):
        if any(x in message for x in ["hello", "hi", "hey"]):
            return "Hi there! How can I help with your job search today?"
        elif "apply" in message:
            return "To apply for a job, visit the Jobs section and click 'Apply' on a listing."
        elif "edit profile?" in message:
            return "You can edit your profile in the 'My Profile' section on the dashboard."
        elif " upload resume?" in message:
            return "You can upload or update your resume under the Profile > Resume tab."
        elif " interview" in message:
            return "Interview tips: Be confident, research the company, and dress professionally!"
        elif "status" in message:
            return "You can check your application status in the 'My Applications' tab."
        elif " recommend" in message:
            return "I recommend applying for jobs that match your skills and experience."
        elif "logout?" in message:
            return "To log out, click the logout icon in the top-right corner of the dashboard."
        else:
            return "I'm here to assist! Ask me about jobs, applications, profile, or interviews."

    def recruiter_responses(message):
        if any(x in message for x in ["hello", "hi", "hey"]):
            return "Hello! How can I assist you in managing your job postings?"
        elif " post job" in message:
            return "To post a job, go to 'Post Job' on the dashboard and fill in the job details."
        elif "view applications?" in message:
            return "You can view all applications under the 'Applications' tab for each job."
        elif "search candidate" in message:
            return "Use the 'Search Candidates' section to filter applicants by skills or experience."
        elif "schedule interview" in message:
            return "You can schedule interviews from the 'Applications' section by clicking 'Schedule'."
        elif "feedback" in message:
            return "Give candidate feedback after interviews in the same 'Applications' section."
        elif "edit  job?" in message:
            return "Go to 'My Jobs', select a job, and click 'Edit' to update its details."
        elif "logout" in message:
            return "To log out, click the logout icon in the top-right corner of the dashboard."
        else:
            return "Need help? Ask about posting jobs, managing candidates, or viewing applications."

    # Chatbot UI
    window = tk.Tk()
    window.title(f"{role.capitalize()} Chatbot")
    window.geometry("500x500")

    chat_display = scrolledtext.ScrolledText(window, wrap=tk.WORD)
    chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    entry = tk.Entry(window)
    entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
    entry.bind("<Return>", lambda event: respond())

    send_btn = tk.Button(window, text="Send", command=respond)
    send_btn.pack(side=tk.RIGHT, padx=10, pady=10)

    window.mainloop()

