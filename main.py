from tkinter import *
from tkinter import messagebox
import json  # Import JSON module for saving and loading data

#### Persistent Storage ####
# File to store events
EVENTS_FILE = "events.json"

# A placeholder list to store events
events = []
admin = "1235"

# Load events from the JSON file
def load_events():
    global events
    try:
        with open(EVENTS_FILE, "r") as file:
            events = json.load(file)
    except FileNotFoundError:
        events = []  # If the file doesn't exist, initialize an empty list
    except json.JSONDecodeError:
        events = []  # If the file is corrupted, initialize an empty list

# Save events to the JSON file
def save_events():
    with open(EVENTS_FILE, "w") as file:
        json.dump(events, file, indent=4)

colorbg = 'white'
colorfg = 'black'
#### Functions ####
def settings():
    def apply_changes():
        
        global colorbg, colorfg
        colorbg = entrybg.get()
        colorfg = entryfg.get()

        if colorbg == colorfg:
            messagebox.showerror("Error", "Background and Font colors cannot be the same!")
            return
        settingsTk.config(bg=colorbg)
        for widget in settingsTk.winfo_children():
            widget.config(bg=colorbg, fg=colorfg)
        
        
        apply_to_all_windows()

        settingsTk.destroy()

    settingsTk = Tk()
    settingsTk.title("Settings")
    settingsTk.geometry("250x200+500+100")
    settingsTk.config(bg=colorbg)

    Label(settingsTk, text="Background color", bg=colorbg, fg=colorfg).pack(pady=5)
    entrybg = Entry(settingsTk)
    entrybg.insert(0, colorbg)  # Default background color value
    entrybg.pack(pady=10)

    Label(settingsTk, text="Font color", bg=colorbg, fg=colorfg).pack(pady=5)
    entryfg = Entry(settingsTk)
    entryfg.insert(0, colorfg)  # Default foreground color value
    entryfg.pack(pady=10)


    if colorbg == colorfg:
        print("color the same")
        # messagebox.showerror("Error", "Color Cant be the Same!")
        # entryfg.insert(0, colorfg)
        # entrybg.insert(0, colorbg)
    else:
        Button(settingsTk, text="Apply", command=apply_changes, bg=colorbg, fg=colorfg).pack(pady=10)

    settingsTk.mainloop()

def apply_to_all_windows():
    # Apply color changes to each window, but check if they exist first
    if 'root' in globals() and root.winfo_exists():
        root.config(bg=colorbg)
        for widget in root.winfo_children():
            widget.config(bg=colorbg, fg=colorfg)

    if 'adminTk' in globals() and adminTk.winfo_exists():
        adminTk.config(bg=colorbg)
        for widget in adminTk.winfo_children():
            widget.config(bg=colorbg, fg=colorfg)

    if 'createTk' in globals() and createTk.winfo_exists():
        createTk.config(bg=colorbg)
        for widget in createTk.winfo_children():
            widget.config(bg=colorbg, fg=colorfg)

    if 'deleteTk' in globals() and deleteTk.winfo_exists():
        deleteTk.config(bg=colorbg)
        for widget in deleteTk.winfo_children():
            widget.config(bg=colorbg, fg=colorfg)

    if 'editTk' in globals() and editTk.winfo_exists():
        editTk.config(bg=colorbg)
        for widget in editTk.winfo_children():
            widget.config(bg=colorbg, fg=colorfg)

    if 'viewTk' in globals() and viewTk.winfo_exists():
        viewTk.config(bg=colorbg)
        for widget in viewTk.winfo_children():
            widget.config(bg=colorbg, fg=colorfg)

def execute_input(dropVar):  # what happens when you press execute
    user_input = dropVar.get()
    if user_input == "Create Event":
        create_event()
    elif user_input == "Delete Event":
        delete_event()
    elif user_input == "Edit Event":
        edit_event()
    elif user_input == "View Events":
        view_events()
    else:
        messagebox.showwarning("Warning", "Please select a valid action")

def create_event():  # Function for creating events
    def save_event():
        # Collect data from the input fields
        name = entryname.get()
        due_date = entrydate.get()
        status = entryStatus.get()
        people = entryPeople.get()

        # Validate input
        if not name or not due_date or not status or not people:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Add the new event to the events list
        events.append({
            "Name": name,
            "Due Date": due_date,
            "Status": status,
            "People": people
        })

        # Save events to the file
        save_events()

        # Close the create event window
        createTk.destroy()
        messagebox.showinfo("Success", "Event created successfully!")

    createTk = Tk()  # Create a new window for event creation
    createTk.title("Create Event")
    createTk.geometry("300x500+1000+200")
    createTk.config(bg = colorbg)
    # Formatting for create window
    Label(createTk, text="Name of the Event:", bg = colorbg, fg = colorfg).pack(pady=5)
    entryname = Entry(createTk)
    entryname.pack(pady=10)

    Label(createTk, text="Due date of the Event:", bg = colorbg, fg = colorfg).pack(pady=5)
    entrydate = Entry(createTk)
    entrydate.pack(pady=10)

    Label(createTk, text="Current Project Status:", bg = colorbg, fg = colorfg).pack(pady=5)
    entryStatus = Entry(createTk)
    entryStatus.pack(pady=10)

    Label(createTk, text="People Involved:", bg = colorbg, fg = colorfg).pack(pady=5)
    entryPeople = Entry(createTk)
    entryPeople.pack(pady=10)

    # Save button
    save_button = Button(createTk, text="Save Event", command=save_event, bg = colorbg, fg = colorfg)
    save_button.pack(pady=10)

    createTk.mainloop()

def delete_event():  # Function to delete an event
    
    def delete_selected():
        try:
            selected_index = int(entryIndex.get()) - 1  # Convert input to zero-based index
            if 0 <= selected_index < len(events):
                del events[selected_index]
                save_events()  # Save events to the file after deletion
                deleteTk.destroy()
                messagebox.showinfo("Success", "Event deleted successfully!")
            else:
                messagebox.showerror("Error", "Invalid event number!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")

    deleteTk = Tk()
    deleteTk.title("Delete Event")
    deleteTk.geometry("300x300+1000+200")
    deleteTk.config(bg = colorbg)
    if events:
        for idx, event in enumerate(events, start=1):
            event_details = f"{idx}. Name: {event['Name']}"
            Label(deleteTk, text=event_details, wraplength=400, justify=LEFT, bg = colorbg, fg = colorfg).pack(pady=5)
    else:
        Label(deleteTk, text="No events to display.", font=("Arial", 12), bg = colorbg, fg = colorfg).pack(pady=10)
    

    Label(deleteTk, text="Enter the event number to delete:", bg = colorbg, fg = colorfg).pack(pady=5)
    entryIndex = Entry(deleteTk)
    entryIndex.pack(pady=10)

    delete_button = Button(deleteTk, text="Delete", command=delete_selected, bg = colorbg, fg = colorfg)
    delete_button.pack(pady=10)

    deleteTk.mainloop()

def edit_event():  # Function to edit an event
    def load_event():
        try:
            selected_index = int(entryIndex.get()) - 1  # Convert input to zero-based index
            if 0 <= selected_index < len(events):
                event = events[selected_index]

                # Pre-fill the fields with the selected event's data
                entryname.delete(0, END)
                entryname.insert(0, event["Name"])
                entrydate.delete(0, END)
                entrydate.insert(0, event["Due Date"])
                entryStatus.delete(0, END)
                entryStatus.insert(0, event["Status"])
                entryPeople.delete(0, END)
                entryPeople.insert(0, event["People"])
            else:
                messagebox.showerror("Error", "Invalid event number!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")

    def save_edited_event():
        try:
            selected_index = int(entryIndex.get()) - 1  # Convert input to zero-based index
            if 0 <= selected_index < len(events):
                # Update the event with new data
                events[selected_index] = {
                    "Name": entryname.get(),
                    "Due Date": entrydate.get(),
                    "Status": entryStatus.get(),
                    "People": entryPeople.get()
                }
                save_events()  # Save events to the file after editing
                editTk.destroy()
                messagebox.showinfo("Success", "Event updated successfully!")
            else:
                messagebox.showerror("Error", "Invalid event number!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")

    
    editTk = Tk()
    editTk.title("Edit Event")
    editTk.geometry("300x500+1000+200")
    editTk.config(bg = colorbg)
    if events:
        for idx, event in enumerate(events, start=1):
            event_details = f"{idx}. Name: {event['Name']}"
            Label(editTk, text=event_details, wraplength=400, justify=LEFT, bg = colorbg, fg = colorfg).pack(pady=5)
    else:
        Label(editTk, text="No events to display.", font=("Arial", 12), bg = colorbg, fg = colorfg).pack(pady=10)
    

    Label(editTk, text="Enter the event number to edit:", bg = colorbg, fg = colorfg).pack(pady=5)
    entryIndex = Entry(editTk)
    entryIndex.pack(pady=10)

    load_button = Button(editTk, text="Load Event", command=load_event, bg = colorbg, fg = colorfg)
    load_button.pack(pady=10)

    Label(editTk, text="Name of the Event:", bg = colorbg, fg = colorfg).pack(pady=5)
    entryname = Entry(editTk)
    entryname.pack(pady=10)

    Label(editTk, text="Due date of the Event:", bg = colorbg, fg = colorfg).pack(pady=5)
    entrydate = Entry(editTk)
    entrydate.pack(pady=10)

    Label(editTk, text="Current Project Status:", bg = colorbg, fg = colorfg).pack(pady=5)
    entryStatus = Entry(editTk)
    entryStatus.pack(pady=10)

    Label(editTk, text="People Involved:", bg = colorbg, fg = colorfg).pack(pady=5)
    entryPeople = Entry(editTk)
    entryPeople.pack(pady=10)

    save_button = Button(editTk, text="Save Changes", command=save_edited_event, bg = colorbg, fg = colorfg)
    save_button.pack(pady=10)

    
    editTk.mainloop()
    

def view_events():  # Function to display all events
    viewTk = Tk()
    viewTk.title("View Events")
    viewTk.geometry("300x300+1000+200")
    viewTk.config(bg = colorbg)
    # Display events in a list format
    if events:
        for idx, event in enumerate(events, start=1):
            event_details = f"{idx}. Name: {event['Name']}, Due Date: {event['Due Date']}, Status: {event['Status']}, People: {event['People']}"
            Label(viewTk, text=event_details, wraplength=400, justify=LEFT, bg = colorbg, fg = colorfg).pack(pady=5)
    else:
        Label(viewTk, text="No events to display.", font=("Arial", 12), bg = colorbg, fg = colorfg).pack(pady=10)

    viewTk.mainloop()

# Load events when the application starts
load_events()

def admin_Login(password):
    if(password == admin):
        adminTk.destroy()
        #### Root widgets ####
        root = Tk()
        root.title("Main Window")
        root.config(bg = colorbg,)

        label = Label(root, text="Welcome to [Working App Name], please choose which action you want to take:", font=("Arial", 12), bg = colorbg, fg = colorfg)
        label.pack(pady=10)

        dropVar = StringVar()
        dropVar.set("Choose Action")
        

        drop_menu = OptionMenu(root, dropVar, "Create Event", "Delete Event", "Edit Event", "View Events")
        drop_menu.config(bg=colorbg,fg = colorfg)
        drop_menu.pack(pady=10)

        execute_button = Button(root, text="Submit", command= lambda:execute_input(dropVar), bg = colorbg, fg = colorfg)
        execute_button.pack(pady=10)

        root.mainloop()
    else:
        messagebox.showerror("Error", "Invalid password!")
        
        
def destroy_admin():
    view_events()
    adminTk.destroy()
    
adminTk = Tk()
adminTk.title("Login")
adminTk.geometry("300x200+100+50")
adminTk.config(bg = colorbg)
label = Label(adminTk, text="Admin Login", font=("Arial", 12), bg = colorbg, fg = colorfg)
label.pack(pady=10)

entryLogin = Entry(adminTk)
entryLogin.pack(pady=10)

execute_button = Button(adminTk, text="Submit", command= lambda:admin_Login(entryLogin.get()), bg = colorbg, fg = colorfg)
execute_button.pack(pady=10)

execute_button = Button(adminTk, text="Continue as User", command= destroy_admin,  bg = colorbg, fg = colorfg)
execute_button.pack(pady=10)

execute_button = Button(adminTk, text = "Settings", command =settings,bg = colorbg, fg = colorfg)
execute_button.pack(pady=10)
adminTk.mainloop()