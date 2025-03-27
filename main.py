from tkinter import *
from tkinter import messagebox
import json  # Import JSON module for saving and loading data

#### Persistent Storage ####
# File to store events
EVENTS_FILE = "events.json"

# A placeholder list to store events
events = []

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

#### Functions ####
def execute_input():  # what happens when you press execute
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

    # Formatting for create window
    Label(createTk, text="Name of the Event:").pack(pady=5)
    entryname = Entry(createTk)
    entryname.pack(pady=10)

    Label(createTk, text="Due date of the Event:").pack(pady=5)
    entrydate = Entry(createTk)
    entrydate.pack(pady=10)

    Label(createTk, text="Current Project Status:").pack(pady=5)
    entryStatus = Entry(createTk)
    entryStatus.pack(pady=10)

    Label(createTk, text="People Involved:").pack(pady=5)
    entryPeople = Entry(createTk)
    entryPeople.pack(pady=10)

    # Save button
    save_button = Button(createTk, text="Save Event", command=save_event)
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

    if events:
        for idx, event in enumerate(events, start=1):
            event_details = f"{idx}. Name: {event['Name']}"
            Label(deleteTk, text=event_details, wraplength=400, justify=LEFT).pack(pady=5)
    else:
        Label(deleteTk, text="No events to display.", font=("Arial", 12)).pack(pady=10)
    

    Label(deleteTk, text="Enter the event number to delete:").pack(pady=5)
    entryIndex = Entry(deleteTk)
    entryIndex.pack(pady=10)

    delete_button = Button(deleteTk, text="Delete", command=delete_selected)
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

    if events:
        for idx, event in enumerate(events, start=1):
            event_details = f"{idx}. Name: {event['Name']}"
            Label(editTk, text=event_details, wraplength=400, justify=LEFT).pack(pady=5)
    else:
        Label(editTk, text="No events to display.", font=("Arial", 12)).pack(pady=10)
    

    Label(editTk, text="Enter the event number to edit:").pack(pady=5)
    entryIndex = Entry(editTk)
    entryIndex.pack(pady=10)

    load_button = Button(editTk, text="Load Event", command=load_event)
    load_button.pack(pady=10)

    Label(editTk, text="Name of the Event:").pack(pady=5)
    entryname = Entry(editTk)
    entryname.pack(pady=10)

    Label(editTk, text="Due date of the Event:").pack(pady=5)
    entrydate = Entry(editTk)
    entrydate.pack(pady=10)

    Label(editTk, text="Current Project Status:").pack(pady=5)
    entryStatus = Entry(editTk)
    entryStatus.pack(pady=10)

    Label(editTk, text="People Involved:").pack(pady=5)
    entryPeople = Entry(editTk)
    entryPeople.pack(pady=10)

    save_button = Button(editTk, text="Save Changes", command=save_edited_event)
    save_button.pack(pady=10)

    
    editTk.mainloop()
    

def view_events():  # Function to display all events
    viewTk = Tk()
    viewTk.title("View Events")

    # Display events in a list format
    if events:
        for idx, event in enumerate(events, start=1):
            event_details = f"{idx}. Name: {event['Name']}, Due Date: {event['Due Date']}, Status: {event['Status']}, People: {event['People']}"
            Label(viewTk, text=event_details, wraplength=400, justify=LEFT).pack(pady=5)
    else:
        Label(viewTk, text="No events to display.", font=("Arial", 12)).pack(pady=10)

    viewTk.mainloop()

# Load events when the application starts
load_events()

#### Root widgets ####
root = Tk()
root.title("Main Window")

label = Label(root, text="Welcome to [Working App Name], please choose which action you want to take:", font=("Arial", 12))
label.pack(pady=10)

dropVar = StringVar()
dropVar.set("Choose Action")

drop_menu = OptionMenu(root, dropVar, "Create Event", "Delete Event", "Edit Event", "View Events")
drop_menu.pack(pady=10)

execute_button = Button(root, text="Submit", command=execute_input)
execute_button.pack(pady=10)

root.mainloop()