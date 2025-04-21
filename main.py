from tkinter import *
from tkinter import messagebox
import json
import os

EVENTS_FILE = "events.json"
SETTINGS_FILE = "settings.json"

events = []
admin_password = None
colorbg = 'white'
colorfg = 'black'
font_main = ("Arial", 11)
font_title = ("Arial", 13, "bold")

# ===== Load & Save =====
def load_events():
    global events
    try:
        with open(EVENTS_FILE, "r") as file:
            events = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        events = []

def save_events():
    with open(EVENTS_FILE, "w") as file:
        json.dump(events, file, indent=4)

def load_settings():
    global admin_password
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as file:
                data = json.load(file)
                admin_password = data.get("admin_password")
        except:
            admin_password = None

def save_settings(password):
    with open(SETTINGS_FILE, "w") as file:
        json.dump({"admin_password": password}, file)

# ===== GUI Theming =====
def apply_to_all_windows():
    for window_name in ['root', 'adminTk', 'createTk', 'deleteTk', 'editTk', 'viewTk']:
        if window_name in globals():
            window = globals()[window_name]
            if window.winfo_exists():
                window.config(bg=colorbg)
                for widget in window.winfo_children():
                    try:
                        widget.config(bg=colorbg, fg=colorfg)
                    except:
                        pass

# ===== Settings Window =====
def settings():
    def apply_changes():
        global colorbg, colorfg
        colorbg = entrybg.get()
        colorfg = entryfg.get()
        if colorbg == colorfg:
            messagebox.showerror("Error", "Background and Font colors cannot be the same!")
            return
        settingsTk.destroy()
        apply_to_all_windows()

    settingsTk = Tk()
    settingsTk.title("Settings")
    settingsTk.geometry("300x200+500+100")
    settingsTk.config(bg=colorbg)

    Label(settingsTk, text="Background Color:", bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    entrybg = Entry(settingsTk)
    entrybg.insert(0, colorbg)
    entrybg.pack(pady=5)

    Label(settingsTk, text="Font Color:", bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    entryfg = Entry(settingsTk)
    entryfg.insert(0, colorfg)
    entryfg.pack(pady=5)

    Button(settingsTk, text="Apply", command=apply_changes, bg=colorbg, fg=colorfg, font=font_main).pack(pady=15)
    settingsTk.mainloop()

# ===== Dispatcher =====
def execute_input(dropVar):
    action = dropVar.get()
    if action == "Create Event":
        create_event()
    elif action == "Delete Event":
        delete_event()
    elif action == "Edit Event":
        edit_event()
    elif action == "View Events":
        view_events()
    else:
        messagebox.showwarning("Warning", "Please select a valid action")

# ===== Event Actions (create/delete/edit/view) =====
# ... (Insert the same functions for create_event, delete_event, edit_event, view_events as previously provided) ...

# ===== Admin/Login Interface =====
def admin_Login(pwd):
    if pwd == admin_password:
        adminTk.destroy()
        launch_main_app()
    else:
        messagebox.showerror("Error", "Invalid password!")

def set_password(pwd1, pwd2):
    if not pwd1 or not pwd2:
        messagebox.showerror("Error", "Both fields are required!")
    elif pwd1 != pwd2:
        messagebox.showerror("Error", "Passwords do not match!")
    else:
        save_settings(pwd1)
        messagebox.showinfo("Success", "Password set! Please log in again.")
        setTk.destroy()
        main()

def launch_main_app():
    global root
    root = Tk()
    root.title("Event Manager")
    root.geometry("400x300+500+200")
    root.config(bg=colorbg)

    Label(root, text="Choose an action:", font=font_title, bg=colorbg, fg=colorfg).pack(pady=10)

    dropVar = StringVar(value="Choose Action")
    OptionMenu(root, dropVar, "Create Event", "Delete Event", "Edit Event", "View Events").pack(pady=10)

    Button(root, text="Submit", command=lambda: execute_input(dropVar), bg=colorbg, fg=colorfg, font=font_main).pack(pady=10)
    root.mainloop()

def destroy_admin():
    view_events()
    adminTk.destroy()

# ===== Main Entrypoint =====
def main():
    load_events()
    load_settings()

    if not admin_password:
        # First time setup
        global setTk
        setTk = Tk()
        setTk.title("Set Admin Password")
        setTk.geometry("300x200+500+200")
        setTk.config(bg=colorbg)

        Label(setTk, text="Set Admin Password", font=font_title, bg=colorbg, fg=colorfg).pack(pady=10)
        pwd1 = Entry(setTk, show="*")
        pwd1.pack(pady=5)
        pwd2 = Entry(setTk, show="*")
        pwd2.pack(pady=5)

        Button(setTk, text="Set Password", command=lambda: set_password(pwd1.get(), pwd2.get()), bg=colorbg, fg=colorfg, font=font_main).pack(pady=10)
        setTk.mainloop()
        return

    global adminTk
    adminTk = Tk()
    adminTk.title("Login")
    adminTk.geometry("300x250+100+50")
    adminTk.config(bg=colorbg)

    Label(adminTk, text="Admin Login", font=font_title, bg=colorbg, fg=colorfg).pack(pady=10)
    entryLogin = Entry(adminTk, show="*")
    entryLogin.pack(pady=10)

    Button(adminTk, text="Submit", command=lambda: admin_Login(entryLogin.get()), bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    Button(adminTk, text="Continue as User", command=destroy_admin, bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    Button(adminTk, text="Settings", command=settings, bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)

    adminTk.mainloop()

main()
