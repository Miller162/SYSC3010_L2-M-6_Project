"""
This code provides the GUI interface for the main program
"""
from tkinter import *
import sqlite3
from PIL import ImageTk, Image
import pandas as pd

global user_input
#in case no input is entered, use the default value
user_input = 85

global email_input
#in case no email is entered, use default email
email_input = "hemas.assistant@gmail.com"

try:
    dbconnect = sqlite3.connect("database.db")
    dbconnect.row_factory = sqlite3.Row
    cursor = dbconnect.cursor()
except:
    print("failure to connect to database file")


#create functions
def get_input():
    global user_input
    return user_input

def get_email_input():
    global email_input
    return email_input

def retrieve_input():
    global user_input
    global email_input

    light_input_str = light_input.get()
    user_input = int(light_input_str)
    #print(light_input_str)
    
    email_input_str = email_input.get()
    #print(email_input_str)    
    
    show_value = Toplevel(app)
    show_value.title("Saved value")
    view_frame = Frame(show_value)
    saved_text = Text(view_frame)
    
    saved_text.insert(END, "Light threshold value saved: %s" %light_input_str)
    saved_text.insert(END, "\nEmail address saved: %s" %email_input_str)
    
    saved_text.pack()
    view_frame.pack()

def radio_select_value():
    if radio_select.get() == 1:
        return False
    else:        
        return True

def radio_preference_value_blind():
    if radio_preference_blind.get() == 2:
        return 0
    else:
        return 1

def radio_preference_value_light():
    if radio_preference_light.get() == 2:
        return 0
    else:
        return 1

def show_data(RPI_log):
    data_view = Toplevel(app)
    data_view.resizable(False, False)
    data_view.title(RPI_log)
    data_frame = Frame(data_view)
    text_box = Text(data_frame)
    text_box.insert(END, pd.read_sql_query("SELECT * FROM %s" %RPI_log, dbconnect))
    
    scroll_bar = Scrollbar(data_frame)
    scroll_bar.pack(side=RIGHT, fill=Y)
    text_box.pack(side=LEFT, fill=Y)
    scroll_bar.config(command=text_box.yview)
    text_box.config(yscrollcommand=scroll_bar.set)    
    
    #text_box.pack()
    data_frame.pack()

    
#create the GUI window (app)
app = Tk()
app.title("H.E.M.A.S.")
#create a label for the GUI window
label = Label(text="H.E.M.A.S. Centre", foreground="white", background="#33B8FF")
#create a canvas to place the group logo on
canvas = Canvas(app, width = 300, height = 300)
#import the logo image
img = ImageTk.PhotoImage(Image.open("mage.png"))
#place the logo image on the canvas
canvas.create_image(20, 20, anchor=NW, image=img)

#capture the user input
light_input = StringVar()
radio_select = IntVar()
radio_select.set(1)
radio_preference_blind = IntVar()
radio_preference_light = IntVar()
radio_preference_blind.set(1)
radio_preference_light.set(1)

#email functionality
email_input = StringVar()

#create the options frame
option_frame = Frame(app)

#create the description label
select_description = Label(option_frame, text="Select if the system should use automatic or manual threshold value")
select_description.pack(side=TOP)

#create the radio buttons
automatic_select = Radiobutton(option_frame, text="Automatic", padx = 20, variable=radio_select, value=1, command=lambda:radio_select_value())
manual_select = Radiobutton(option_frame, text="Manual", padx = 20, variable=radio_select, value=2)
automatic_select.pack(anchor=W)
manual_select.pack(anchor=W)

#create the description label for manual options
preference_description = Label(option_frame, text="Select the desired state for the blinds and lights (used if manual selected above)")
preference_description.pack(side=TOP)

#create the manual selection radio buttons
manual_blind_preference_on = Radiobutton(option_frame, text="blinds: On", padx = 20, variable=radio_preference_blind, value=1, command=lambda:radio_preference_value_blind())
manual_blind_preference_off = Radiobutton(option_frame, text="blinds: Off", padx = 20, variable=radio_preference_blind, value=2, command=lambda:radio_preference_value_blind())
manual_light_preference_on = Radiobutton(option_frame, text="lights: On", padx = 20, variable=radio_preference_light, value=1, command=lambda:radio_preference_value_light())
manual_light_preference_off = Radiobutton(option_frame, text="lights: Off", padx = 20, variable=radio_preference_light, value=2, command=lambda:radio_preference_value_light())

manual_blind_preference_on.pack(anchor=W)
manual_blind_preference_off.pack(anchor=W)
manual_light_preference_on.pack(anchor=W)
manual_light_preference_off.pack(anchor=W)

#create a label for a the light level text entry box
light_label = Label(option_frame, text="Light Level Threshold")
light_label.pack(side=LEFT)

#create the text entry field for the light level
light_level_entry_box = Entry(option_frame, textvariable=light_input)
light_level_entry_box.pack(side=LEFT)

#create a button to save the specified light threshold
light_commit_button = Button(option_frame, text="Save value", command=lambda:retrieve_input())
light_commit_button.pack(side=LEFT)

#create a frame for the email field
email_frame = Frame(app)

#create the label for the email notifications
email_description = Label(email_frame, text="Enter your email for notifications")
email_description.pack(side=LEFT)

#create the text entry field for the email
email_entry_box = Entry(email_frame, textvariable=email_input)
email_entry_box.pack(side=LEFT)

#create the button to save the email
email_commit_button = Button(email_frame, text="Save email", command=lambda:retrieve_input())
email_commit_button.pack(side=LEFT)


#create button frame (have buttons to open different views)
selector_frame = Frame(app)
#note: the lambda function is required so that the new windows aren't created before the button is pressed
RPI1_button = Button(selector_frame, text="RPI1_log", command=lambda:show_data("RPI1_log"))
RPI2_button = Button(selector_frame, text="RPI2_log", command=lambda:show_data("RPI2_log"))
RPI3_button = Button(selector_frame, text="RPI3_log", command=lambda:show_data("RPI3_log"))
RPI4_button = Button(selector_frame, text="RPI4_log", command=lambda:show_data("RPI4_log"))
#pack the buttons into the frame
RPI1_button.pack(side=LEFT)
RPI2_button.pack(side=LEFT)
RPI3_button.pack(side=LEFT)
RPI4_button.pack(side=LEFT)

#pack the GUI elements
label.pack(fill=X)
canvas.pack()
option_frame.pack()
email_frame.pack()
selector_frame.pack()
app.mainloop()