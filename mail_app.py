import tkinter as tk
from tkinter import messagebox, scrolledtext
from database import setup_db, cursor, conn
from auth import register, login
from mailer import send_email

setup_db()
current_user = None

root = tk.Tk()
root.title("Mail Application - CodeClause")
root.geometry("500x650")
root.resizable(False, False)

# ------------------ Main Container ------------------
container = tk.Frame(root)
container.pack(fill="both", expand=True)

def clear_container():
    for widget in container.winfo_children():
        widget.destroy()

# ------------------ Login Screen ------------------
def login_screen():
    clear_container()
    frame = tk.Frame(container)
    frame.pack(expand=True)

    tk.Label(frame, text="Login", font=("Arial", 20)).pack(pady=20)

    tk.Label(frame, text="Username").pack(pady=5)
    user_entry = tk.Entry(frame, width=30)
    user_entry.pack(pady=5)

    tk.Label(frame, text="Password").pack(pady=5)
    pwd_entry = tk.Entry(frame, show="*", width=30)
    pwd_entry.pack(pady=5)

    def do_login():
        global current_user
        uid = login(user_entry.get(), pwd_entry.get())
        if uid:
            current_user = uid
            dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def go_register():
        register_screen()

    tk.Button(frame, text="Login", width=15, command=do_login).pack(pady=10)
    tk.Button(frame, text="Go to Register", width=15, command=go_register).pack(pady=5)

# ------------------ Register Screen ------------------
def register_screen():
    clear_container()
    frame = tk.Frame(container)
    frame.pack(expand=True)

    tk.Label(frame, text="Register", font=("Arial", 20)).pack(pady=20)

    tk.Label(frame, text="Username").pack(pady=5)
    user_entry = tk.Entry(frame, width=30)
    user_entry.pack(pady=5)

    tk.Label(frame, text="Password").pack(pady=5)
    pwd_entry = tk.Entry(frame, show="*", width=30)
    pwd_entry.pack(pady=5)

    def do_register():
        if register(user_entry.get(), pwd_entry.get()):
            messagebox.showinfo("Success", "Registered successfully! Please login.")
            login_screen()
        else:
            messagebox.showerror("Error", "User already exists")

    tk.Button(frame, text="Register", width=15, command=do_register).pack(pady=10)
    tk.Button(frame, text="Back to Login", width=15, command=login_screen).pack(pady=5)

# ------------------ Dashboard ------------------
def dashboard():
    clear_container()
    frame = tk.Frame(container)
    frame.pack(expand=True)

    tk.Label(frame, text="Dashboard", font=("Arial", 20)).pack(pady=20)

    tk.Button(frame, text="Configure SMTP", width=20, command=smtp_config).pack(pady=10)
    tk.Button(frame, text="Send Mail", width=20, command=send_mail_ui).pack(pady=10)
    tk.Button(frame, text="View Sent Emails", width=20, command=view_sent_emails).pack(pady=10)
    tk.Button(frame, text="View SMTP Settings", width=20, command=view_smtp_settings).pack(pady=10)
    tk.Button(frame, text="Logout", width=20, command=login_screen).pack(pady=10)

# ------------------ SMTP Config ------------------
def smtp_config():
    clear_container()
    frame = tk.Frame(container)
    frame.pack(expand=True)

    tk.Label(frame, text="SMTP Settings", font=("Arial", 20)).pack(pady=20)

    tk.Label(frame, text="Email").pack(pady=5)
    email_entry = tk.Entry(frame, width=30)
    email_entry.pack(pady=5)

    tk.Label(frame, text="SMTP Server").pack(pady=5)
    server_entry = tk.Entry(frame, width=30)
    server_entry.pack(pady=5)

    tk.Label(frame, text="Port").pack(pady=5)
    port_entry = tk.Entry(frame, width=30)
    port_entry.pack(pady=5)

    tk.Label(frame, text="App Password").pack(pady=5)
    pwd_entry = tk.Entry(frame, show="*", width=30)
    pwd_entry.pack(pady=5)

    def save():
        cursor.execute("DELETE FROM smtp_settings WHERE user_id=?", (current_user,))
        cursor.execute(
            "INSERT INTO smtp_settings VALUES (NULL,?,?,?,?,?)",
            (current_user, email_entry.get(), server_entry.get(), int(port_entry.get()), pwd_entry.get())
        )
        conn.commit()
        messagebox.showinfo("Saved", "SMTP Configuration Saved")
        dashboard()

    tk.Button(frame, text="Save SMTP Settings", width=20, command=save).pack(pady=10)
    tk.Button(frame, text="Back to Dashboard", width=20, command=dashboard).pack(pady=5)

# ------------------ Send Mail ------------------
def send_mail_ui():
    clear_container()
    frame = tk.Frame(container)
    frame.pack(expand=True)

    tk.Label(frame, text="Send Mail", font=("Arial", 20)).pack(pady=20)

    tk.Label(frame, text="To").pack(pady=5)
    to_entry = tk.Entry(frame, width=40)
    to_entry.pack(pady=5)

    tk.Label(frame, text="Subject").pack(pady=5)
    subject_entry = tk.Entry(frame, width=40)
    subject_entry.pack(pady=5)

    tk.Label(frame, text="Message").pack(pady=5)
    body_text = tk.Text(frame, height=10, width=45)
    body_text.pack(pady=5)

    def send():
        success, msg = send_email(
            current_user,
            to_entry.get(),
            subject_entry.get(),
            body_text.get("1.0", tk.END)
        )
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    tk.Button(frame, text="Send Mail", width=20, command=send).pack(pady=10)
    tk.Button(frame, text="Back to Dashboard", width=20, command=dashboard).pack(pady=5)

# ------------------ View Sent Emails ------------------
def view_sent_emails():
    clear_container()
    frame = tk.Frame(container)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Sent Emails", font=("Arial", 20)).pack(pady=10)

    text_area = scrolledtext.ScrolledText(frame, width=60, height=25)
    text_area.pack(pady=5)

    cursor.execute("SELECT receiver, subject, message, timestamp, status FROM sent_mails WHERE user_id=?", (current_user,))
    records = cursor.fetchall()
    if not records:
        text_area.insert(tk.END, "No emails sent yet.")
    else:
        for r in records:
            text_area.insert(tk.END, f"To: {r[0]}\nSubject: {r[1]}\nMessage: {r[2]}\nTime: {r[3]}\nStatus: {r[4]}\n{'-'*50}\n")

    text_area.config(state="disabled")
    tk.Button(frame, text="Back to Dashboard", width=20, command=dashboard).pack(pady=10)

# ------------------ View SMTP Settings ------------------
def view_smtp_settings():
    clear_container()
    frame = tk.Frame(container)
    frame.pack(expand=True)

    tk.Label(frame, text="SMTP Settings", font=("Arial", 20)).pack(pady=10)

    cursor.execute("SELECT email, server, port, app_password FROM smtp_settings WHERE user_id=?", (current_user,))
    record = cursor.fetchone()
    if not record:
        tk.Label(frame, text="No SMTP settings configured yet.", fg="red").pack(pady=20)
    else:
        email, server, port, pwd = record
        tk.Label(frame, text=f"Email: {email}").pack(pady=5)
        tk.Label(frame, text=f"SMTP Server: {server}").pack(pady=5)
        tk.Label(frame, text=f"Port: {port}").pack(pady=5)
        tk.Label(frame, text=f"App Password: {'*'*len(pwd)}").pack(pady=5)

    tk.Button(frame, text="Back to Dashboard", width=20, command=dashboard).pack(pady=10)

# ------------------ Start App ------------------
login_screen()
root.mainloop()
