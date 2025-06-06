from tkinter import *
from tkinter import messagebox
import json

# ===== Persistent Storage =====
EVENTS_FILE = "events.json"
events = []

PASSWORD_FILE = "password.json"
admin = "username"

def setPass():
    def confirmPass(ogPass, newPass1, NewPass2):
        global admin
        load_password()
        if (ogPass != admin):
            messagebox.showwarning("Warning", "Incorrect Previous Password")
        elif (newPass1 != NewPass2):
            messagebox.showwarning("Warning", "New Passwords don't Match")
        elif (ogPass == newPass1):
            messagebox.showwarning("Warning", "New Password must be Different from Old")
        else:
            admin = newPass1
            with open(PASSWORD_FILE, "w") as f:
                json.dump({"admin": admin}, f)
            messagebox.showinfo("Success", "Password Successfully Updated!")
            setPASSTK.destroy()

    setPASSTK = Tk()
    setPASSTK.title("Set New Password")
    setPASSTK.geometry("300x300+100+50")
    setPASSTK.config(bg=colorbg)

    Label(setPASSTK, text="Previous Password:", bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    entryOriginalPass = Entry(setPASSTK)
    entryOriginalPass.pack(pady=5)

    Label(setPASSTK, text="New Password:", bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    entryNewPass1 = Entry(setPASSTK)
    entryNewPass1.pack(pady=5)

    Label(setPASSTK, text="Confirm New Password:", bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    entryNewPass2 = Entry(setPASSTK)
    entryNewPass2.pack(pady=5)

    Button(setPASSTK, text="Submit Password", command=lambda: confirmPass(entryOriginalPass.get(), entryNewPass1.get(), entryNewPass2.get()), bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    setPASSTK.mainloop()

def load_events():
    global events
    try:
        with open(EVENTS_FILE, "r") as file:
            events = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        events = []

def load_password():
    global admin
    try:
        with open(PASSWORD_FILE, "r") as f:
            data = json.load(f)
            admin = data.get("admin", "username")
    except (FileNotFoundError, json.JSONDecodeError):
        admin = "username"

def save_events():
    with open(EVENTS_FILE, "w") as file:
        json.dump(events, file, indent=4)

colorbg = 'white'
colorfg = 'black'
font_main = ("Arial", 11)
font_title = ("Arial", 13, "bold")

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

def create_event():
    def save_event():
        name, due, status, people = entryname.get(), entrydate.get(), entryStatus.get(), entryPeople.get()
        if not all([name, due, status, people]):
            messagebox.showerror("Error", "All fields are required!")
            return
        events.append({"Name": name, "Due Date": due, "Status": status, "People": people})
        save_events()
        createTk.destroy()
        messagebox.showinfo("Success", "Event created successfully!")

    global createTk
    createTk = Tk()
    createTk.title("Create Event")
    createTk.geometry("350x400+1000+200")
    createTk.config(bg=colorbg)

    Label(createTk, text="Name of Event:", bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    entryname = Entry(createTk)
    entryname.pack(pady=5)

    Label(createTk, text="Due Date:", bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    entrydate = Entry(createTk)
    entrydate.pack(pady=5)

    Label(createTk, text="Status:", bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    entryStatus = Entry(createTk)
    entryStatus.pack(pady=5)

    Label(createTk, text="People Involved:", bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    entryPeople = Entry(createTk)
    entryPeople.pack(pady=5)

    Button(createTk, text="Save Event", command=save_event, bg=colorbg, fg=colorfg, font=font_main).pack(pady=20)
    createTk.mainloop()

def delete_event():
    def delete_selected():
        try:
            idx = int(entryIndex.get()) - 1
            if 0 <= idx < len(events):
                del events[idx]
                save_events()
                deleteTk.destroy()
                messagebox.showinfo("Success", "Event deleted.")
            else:
                messagebox.showerror("Error", "Invalid number.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")

    global deleteTk
    deleteTk = Tk()
    deleteTk.title("Delete Event")
    deleteTk.geometry("350x400+1000+200")
    deleteTk.config(bg=colorbg)

    if events:
        for i, event in enumerate(events, 1):
            Label(deleteTk, text=f"{i}. {event['Name']}", bg=colorbg, fg=colorfg, font=font_main).pack()
    else:
        Label(deleteTk, text="No events available.", bg=colorbg, fg=colorfg, font=font_main).pack()

    Label(deleteTk, text="Enter number to delete:", bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    entryIndex = Entry(deleteTk)
    entryIndex.pack(pady=5)

    Button(deleteTk, text="Delete", command=delete_selected, bg=colorbg, fg=colorfg, font=font_main).pack(pady=10)
    deleteTk.mainloop()

def edit_event():
    def load_event():
        try:
            idx = int(entryIndex.get()) - 1
            if 0 <= idx < len(events):
                e = events[idx]
                entryname.delete(0, END)
                entryname.insert(0, e["Name"])
                entrydate.delete(0, END)
                entrydate.insert(0, e["Due Date"])
                entryStatus.delete(0, END)
                entryStatus.insert(0, e["Status"])
                entryPeople.delete(0, END)
                entryPeople.insert(0, e["People"])
            else:
                messagebox.showerror("Error", "Invalid number.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")

    def save_changes():
        try:
            idx = int(entryIndex.get()) - 1
            if 0 <= idx < len(events):
                events[idx] = {
                    "Name": entryname.get(),
                    "Due Date": entrydate.get(),
                    "Status": entryStatus.get(),
                    "People": entryPeople.get()
                }
                save_events()
                editTk.destroy()
                messagebox.showinfo("Success", "Event updated.")
            else:
                messagebox.showerror("Error", "Invalid number.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")

    global editTk
    editTk = Tk()
    editTk.title("Edit Event")
    editTk.geometry("350x500+1000+200")
    editTk.config(bg=colorbg)

    if events:
        for i, event in enumerate(events, 1):
            Label(editTk, text=f"{i}. {event['Name']}", bg=colorbg, fg=colorfg, font=font_main).pack()
    else:
        Label(editTk, text="No events to edit.", bg=colorbg, fg=colorfg, font=font_main).pack()

    Label(editTk, text="Event number to edit:", bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)
    entryIndex = Entry(editTk)
    entryIndex.pack(pady=5)

    Button(editTk, text="Load", command=load_event, bg=colorbg, fg=colorfg, font=font_main).pack(pady=5)

    entryname, entrydate, entryStatus, entryPeople = Entry(editTk), Entry(editTk), Entry(editTk), Entry(editTk)
    for label, entry in [("Name:", entryname), ("Due Date:", entrydate),
                         ("Status:", entryStatus), ("People:", entryPeople)]:
        Label(editTk, text=label, bg=colorbg, fg=colorfg, font=font_main).pack()
        entry.pack(pady=3)

    Button(editTk, text="Save Changes", command=save_changes, bg=colorbg, fg=colorfg, font=font_main).pack(pady=10)
    editTk.mainloop()

def view_events():
    global viewTk
    viewTk = Tk()
    viewTk.title("All Events")
    viewTk.geometry("450x500+1000+200")
    viewTk.config(bg=colorbg)

    frame = Frame(viewTk, bg=colorbg)
    frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    canvas = Canvas(frame, bg=colorbg, highlightthickness=0)
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=colorbg)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    if events:
        for i, e in enumerate(events, 1):
            Label(scrollable_frame, text=f"Event {i}", font=font_title, bg=colorbg, fg=colorfg).pack(anchor=W, pady=(10, 0))
            Label(scrollable_frame, text=f"Name: {e['Name']}", bg=colorbg, fg=colorfg, font=font_main).pack(anchor=W)
            Label(scrollable_frame, text=f"Due Date: {e['Due Date']}", bg=colorbg, fg=colorfg, font=font_main).pack(anchor=W)
            Label(scrollable_frame, text=f"Status: {e['Status']}", bg=colorbg, fg=colorfg, font=font_main).pack(anchor=W)
            Label(scrollable_frame, text=f"People: {e['People']}", bg=colorbg, fg=colorfg, font=font_main).pack(anchor=W)
            Label(scrollable_frame, text="-"*60, bg=colorbg, fg=colorfg).pack(anchor=W, pady=(5,0))
    else:
        Label(scrollable_frame, text="No events found.", bg=colorbg, fg=colorfg, font=font_main).pack(pady=20)

    viewTk.mainloop()

# ===== New logout function =====
def logout(current_window):
    current_window.destroy()
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
    Button(adminTk, text = "Set Password", command = setPass, bg = colorbg, fg = colorfg, font = font_main).pack(pady=5)
    adminTk.mainloop()

def admin_Login(pwd):
    if pwd == admin:
        adminTk.destroy()
        global root
        root = Tk()
        root.title("Event Manager")
        root.geometry("400x300+500+200")
        root.config(bg=colorbg)

        Label(root, text="Choose an action:", font=font_title, bg=colorbg, fg=colorfg).pack(pady=10)

        dropVar = StringVar(value="Choose Action")
        OptionMenu(root, dropVar, "Create Event", "Delete Event", "Edit Event", "View Events").pack(pady=10)

        Button(root, text="Submit", command=lambda: execute_input(dropVar), bg=colorbg, fg=colorfg, font=font_main).pack(pady=10)
        Button(root, text="Logout", command=lambda: logout(root), bg=colorbg, fg=colorfg, font=font_main).pack(pady=10)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Invalid password!")

def destroy_admin():
    view_events()
    adminTk.destroy()

# ===== App Entry Point =====
load_events()
load_password()

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
Button(adminTk, text = "Set Password", command = setPass, bg = colorbg, fg = colorfg, font = font_main).pack(pady=5)

adminTk.mainloop()
