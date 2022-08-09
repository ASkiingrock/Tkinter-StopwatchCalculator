import tkinter as tk
from tkinter import messagebox as mb
import stopwatchfuncs as f
import json
import pyperclip
from functools import partial
from PIL import ImageTk, Image

offset = 0
ArrLaps = []
ArrLaps.append(["00:00:00.000", "00.000"]) 
started = 0
display = 1 # Initialise variables

# Started = 0
# Program has been reset

# Started = 1
# Program is running

# Started = 2
# Program has paused

window = tk.Tk()
window.geometry("646x316")
window.title("Pro Stopwatch v2.0 (Commercial Licence)")
window.resizable(width=True, height=True) # Initialise window

def quitall():
    window.destroy()

def start(): # When start/pause button pressed
    global started 
    global startTime
    global offset                          # Make variables able to be changes outside function's scope
    if started == 0:                       # Start button pressed after program reset
        started = 1                        # Therefore state should be changed to 1 (Program running) as the start button has been pressed
        startTime = f.GetTime()            # Start time of the program
        lap.config(text="Lap", bg="white") # Make the lap button look able to be pressed
        start.config(text="Pause", bg="red")
        save.config(fg="black", bg="grey")
    elif started == 1:                     # Start button pressed while program running
        offset = f.convertToMillis(displayedTime) # Get current stopwatch time in Milliseconds
                                                  # The "offset" is to make the stopwatch able to be paused and unpaused
                                                  # Basically, the stopwatch function takes the "offset" as well as the startTime and just adds the normal stopwatch time with the "offset" so that the stopwatch doesn't just start back at 0 again.
        lap.config(text="Reset", bg = "white") # Change lap button to say "reset"
        start.config(text="Start", bg="green")
        save.config(fg="black", bg="yellow")
        started = 2                        # Change state to paused
    elif started == 2:                     # State is paused
        startTime = f.GetTime()            # Get new time
        lap.config(text="Lap", bg="white") # Make lap look able to be pressed
        start.config(text="Pause", bg="red")
        save.config(fg="black", bg="grey")
        started = 1                        # Program state running

def lap(): # When lap/reset button is pressed
    global started
    global offset                                  # Make variables able to be changed in global scope
    global ArrLaps
    global displayedTime
    if started == 1:                               # If lap button is pressed while the timer is running
        if len(ArrLaps) == 1:
            global lapsContent 
            global lapsHead
            global scrollbar

            lapsHead = tk.Text(window, height=1, width=64, font=("Courier 16"), fg="white", bg="black", highlightthickness=0, borderwidth=2, relief="solid")
            lapsHead.insert(tk.END, '    Time:         Difference: \n')
            lapsHead.grid(row=6, column=0, columnspan=6, sticky="NSEW")
            lapsHead.tag_configure("center", justify='center')
            lapsHead.tag_add("center", 1.0, "end")

            lapsContent = tk.Text(window, height=7, width=64, font=("Courier 18 underline"), fg="white", bg="black", highlightthickness=0, borderwidth=2, relief="solid")
            lapsContent.insert(tk.END, str(f.printMultipleLaps(ArrLaps)))
            lapsContent.grid(row=7, column=0, columnspan=6, rowspan=3, sticky="NSEW")

            time.config(height=2, font=("Courier", 60), width=20)
            time.grid(row=0, column=0, columnspan=6, rowspan=6)
            
            #window.geometry('646x320')

            scrollbar = tk.Scrollbar(window, orient='vertical', command=lapsContent.yview, bg="black", )
            scrollbar.grid(row=7, column=5, sticky=tk.NS)
            lapsContent['yscrollcommand'] = scrollbar.set
        currentTime = f.newstopwatch(startTime, offset) # Current time in string form ("H:M:S.M")
        difference = f.MillisToHMSM(f.convertToMillis(currentTime)-f.convertToMillis(ArrLaps[-1][0])) # Difference from the previous time variables
        ArrLaps.append([currentTime, difference])  # Add the current time as well as the difference between it and the previous time in the lap array
        lapsContent.delete(1.0, tk.END)
        lapsContent.insert(tk.END, f.printMultipleLaps(ArrLaps))
        lapsContent.tag_configure("center", justify='center')
        lapsContent.tag_add("center", 1.0, "end")
        lapsContent.see("end")
    if started == 2:
        displayedTime = "00.000"
        started = 0
        offset = 0
        ArrLaps = []
        lapsContent.destroy()
        lapsHead.destroy()
        scrollbar.destroy()
        ArrLaps.append(["00:00:00.000", "00.000"]) # Reset all variables since the lap button now has the "reset" function once the timer is paused
        lap.config(text='Lap', bg="grey")          # Turn it into a "lap" button but it's greyed out since you can't use it while the timer is reset
        time.config(text="00.000", font=("Courier", 50), height=4, width=16)
        save.config(bg="grey")
        #window.geometry('646x316')

def save(): # When save button pressed
    if started == 2:
        with open("saves.json", "r") as d:  # reading a file
            data = json.load(d)  # deserialization

        data["saves"].append([displayedTime, ''])

        with open("saves.json", "w") as d:
            json.dump(data, d)  # serializing back to the original file

def update(): # Updates time every frame
    global displayedTime
    if started == 1:
        displayedTime = f.newstopwatch(startTime, offset)
        time.config(text=displayedTime)
    window.after(1,update) # If the timer is running, every frame update the timer

# ^ Stopwatch functions

def delete(): # Deletes save
    compare = []

    with open("saves.json", "r") as d:  # reading a file
        data = json.load(d)  # deserialization

    delet = mb.askokcancel(title="Warning", message="This will delete all selected items, do you wish to continue?")

    if delet == True:
        for index,item in enumerate(data["saves"]):
            exec(f'if v{index}.get() == 1:\n compare.append(index)')
        
        for index in sorted(compare, reverse=True):
            del data["saves"][index]

        with open("saves.json", "w") as d:  # reading a file
            json.dump(data, d)
        
        savewindow.destroy()
        view()

def copy(): # Copies save to clipboard
    compare = []
    with open("saves.json", "r") as d:  # reading a file
        data = json.load(d)  # deserialization

    for index, item in enumerate(data["saves"]):
        exec(f'if v{index}.get() == 1:\n compare.append(item)')

    stroutput = ""
    if len(compare) == 1:
        pyperclip.copy(compare[0][0])
    if len(compare) > 1:
        for index, item in enumerate(compare):
            if index == 0:
                stroutput += item[0]
            else:
                stroutput += f', {item[0]}'
        pyperclip.copy(stroutput)

def savename(): # Have to define this in here to have access to variables
    compare = []

    with open("saves.json", "r") as d:  # reading a file
        data = json.load(d)  # deserialization

    for index, item in enumerate(data["saves"]):
        exec(f'if v{index}.get() == 1:\n compare.append(index)')
    
    for index in compare:
        exec(f'if name{index}.get() != "Name this time?":\n data["saves"][index] = [data["saves"][index][0], name{index}.get()]')

    with open("saves.json", "w") as d:  # reading a file
        json.dump(data, d)

def selectall(): # Selects all checkboxes
    global selecta
    # Select all 0, all 1
    # Select all 1, turn all to 0
    with open("saves.json", "r") as d:  # reading a file
        data = json.load(d)  # deserialization
    
    if selecta == 0:
        for index,item in enumerate(data["saves"]):
            exec(f'v{index}.set(1)')
        selecta = 1
    elif selecta == 1:
        for index,item in enumerate(data["saves"]):
            exec(f'v{index}.set(0)')
        selecta = 0

# ^ Save window functions

def mean(array): # Calculates mean
    total = 0
    num = 0
    for item in array:
        total += f.convertToMillis(item[0])
        num += 1
    
    return f.MillisToHMSM(total // num)

def median(array): # Calculates median
    millis = []
    for item in array:
        millis.append(f.convertToMillis(item[0]))
    
    millis.sort()

    if len(millis)%2 == 1:
        return f.MillisToHMSM(millis[len(millis)//2])
    elif len(millis)%2 == 0:
        if len(millis) == 2:
            return f.MillisToHMSM((millis[0]+millis[1]) // 2)
        else:
            lb = millis[len(millis)//2]
            ub = millis[len(millis)//2 +1]
            return f.MillisToHMSM((lb + ub) // 2)

def comparetimes(): # Comparison window
    global comparewindow
    compare = []

    with open("saves.json", "r") as d:  # reading a file
        data = json.load(d)  # deserialization

    for index,item in enumerate(data["saves"]): # find selected times
        exec(f'if v{index}.get() == 1:\n compare.append(item)')
    
    if compare != []: # only if some times have been selected

        comparewindow = tk.Toplevel()
        comparewindow.title('Pro Stopwatch v2.0 (Commercial Licence) Time Comparison')
        comparewindow["background"] = "#FDF5DF"
        for index, item in enumerate(compare):
            text = str(item[1])
            exec(f'comparename{index} = tk.Entry(comparewindow)')
            exec(f'comparename{index}.grid(column=1, row={index}, padx=5)')
            if item[1] == "":
                exec(f'comparename{index}.insert(0, "Unnamed time")')
            else:
                exec(f'comparename{index}.insert(0, text)')
            exec(f'comparename{index}.config(state="readonly")')
            exec(f'comparetime{index} = tk.Label(comparewindow, text="{item[0]}", font=("Courier", 15), bg="#FDF5DF")')
            exec(f'comparetime{index}.grid(row={index}, column = 2)')

        def create_labels():

            mintitle = tk.Label(comparewindow, text="Min:", font=('Times New Roman', 30), bg="#FDF5DF")
            mintitle.grid(row=0, column=4, padx=50)

            minavg = sorted(compare)[0][0]
            minlabel = tk.Label(comparewindow, text=minavg, font=('Times New Roman', 25), bg="#FDF5DF")
            minlabel.grid(row=0, column=5)

            mincopy = tk.Button(comparewindow, text="Copy", bg="orange", fg="black", command=partial(pyperclip.copy, minavg))
            mincopy.grid(row=0, column=6, padx=15)

            maxtitle = tk.Label(comparewindow, text="Min:", font=('Times New Roman', 30), bg="#FDF5DF")
            maxtitle.grid(row=1, column=4, padx=50)

            maxavg = sorted(compare)[-1][0]
            maxlabel = tk.Label(comparewindow, text=maxavg, font=('Times New Roman', 25), bg="#FDF5DF")
            maxlabel.grid(row=1, column=5)

            maxcopy = tk.Button(comparewindow, text="Copy", bg="orange", fg="black", command=partial(pyperclip.copy, maxavg))
            maxcopy.grid(row=1, column=6, padx=15)

            meantitle = tk.Label(comparewindow, text="Mean:", font=('Times New Roman', 30), bg="#FDF5DF")
            meantitle.grid(row=2, column=4, padx=50)

            meanavg = mean(compare)
            meanlabel = tk.Label(comparewindow, text=meanavg, font=('Times New Roman', 25), bg="#FDF5DF")
            meanlabel.grid(row=2, column=5)

            meancopy = tk.Button(comparewindow, text="Copy", bg="orange", fg="black", command=partial(pyperclip.copy, meanavg))
            meancopy.grid(row=2, column=6, padx=15)

            mediantitle = tk.Label(comparewindow, text="Median:", font=('Times New Roman', 30), bg="#FDF5DF")
            mediantitle.grid(row=3, column=4, padx=50)

            medianavg = median(compare)
            medianlabel = tk.Label(comparewindow, text=medianavg, font=('Times New Roman', 25), bg="#FDF5DF")
            medianlabel.grid(row=3, column=5)

            mediancopy = tk.Button(comparewindow, text="Copy", bg="orange", fg="black", command=partial(pyperclip.copy, medianavg))
            mediancopy.grid(row=3, column=6, padx=15)

            if len(compare) < 5:
                row = 4
            else:
                row = len(compare)-1

            quit3 = tk.Button(comparewindow, text="Quit", fg="black", bg="red", command=quitall)
            quit3.grid(row=row, column=6, padx=25, pady=10, sticky="E")

        create_labels()

def view(): # Creates save window
    global selecta; selecta = 0
    global savewindow
    global data

    savewindow = tk.Toplevel()
    savewindow.title("Pro Stopwatch v2.0 (Commercial Licence) Saved Times")
    savewindow.resizable(width=True, height=True) # Initialise window
    savewindow["background"] = "#FDF5DF"

    with open("saves.json", "r") as d:  # reading a file
        data = json.load(d)

    def temp_text(e): # Makes text disappear
        for index, item in enumerate(data["saves"]):
            exec(f'if name{index}.get() == "":\n name{index}.insert(0, "Name this time?")\n name{index}.config(fg="grey")')
        if e.widget.get() == "Name this time?":
            e.widget.delete(0, "end")
        e.widget.config(fg="black")

    for index,item in enumerate(data["saves"]): # All dynamic variables for widgets
        text = str(item[1])
        exec(f'global name{index}; name{index} = tk.Entry(savewindow)')
        exec(f'name{index}.grid(column=1, row={index}, padx=5)')
        if item[1] == "":
            exec(f'name{index}.insert(0, "Name this time?")')
            exec(f'name{index}.config(fg="grey")')
        else:
            exec(f'name{index}.insert(0, text)')
            exec(f'name{index}.config(fg="black")')
        exec(f'name{index}.bind("<FocusIn>", temp_text)')
        exec(f'save{index} = tk.Label(savewindow, text="{item[0]}", fg="black", font=("Courier", 15), bg="#FDF5DF")')
        exec(f'save{index}.grid(column=2, row={index}, padx=5)')
        exec(f'global v{index}; v{index}=tk.IntVar()')
        exec(f'select{index} = tk.Checkbutton(savewindow, variable=v{index}, bg="#FDF5DF")')
        exec(f'select{index}.grid(column=5, row={index}, padx = 5)')
    
    def reloadpage(): # Reload view window
        savewindow.destroy()
        view()
    
    def create_labels():
        if data["saves"] != []:
            delet = tk.Button(savewindow, text="Delete", fg="black", bg="red", command=delete)
            delet.grid(row=0, column=6, padx=50, pady=5, sticky="W")

            savenames = tk.Button(savewindow, text="Save names", bg="orange", command=savename)
            savenames.grid(row=1, column=6, padx=50, pady=5, sticky="W")

            cop = tk.Button(savewindow, text="Copy", fg="white", bg="green", command=copy)
            cop.grid(row=2, column=6, padx=50, pady=5, sticky="W")

            compareitems = tk.Button(savewindow, text="Compare", bg="yellow", fg="black", command=comparetimes)
            compareitems.grid(row=3, column=6, padx=50, pady=5, sticky="W")

            selectal = tk.Button(savewindow, text="Select all", command=selectall)
            selectal.grid(row=4, column=6, padx=50, pady=5, sticky="W")

            if len(data["saves"]) < 6:
                row = 5
            else:
                row = len(data["saves"])

            reloadpag = tk.Button(savewindow, text="Reload page", fg="black", bg="#D3D3D3", command=reloadpage)
            reloadpag.grid(row=row, column=1, pady=5, padx=5, sticky="W")

            quit2 = tk.Button(savewindow, text="Quit", fg="black", bg="red", command=quitall)
            quit2.grid(row=row, column=6, padx=50, pady=5, sticky="W")

        else:
            savewindow.geometry('420x250')
            savewindow["background"] = "#FDF5DF"
            no = tk.Label(savewindow, text="No saved times recorded.", font=("Courier", 20), bg="#FDF5DF")
            no.grid(row=0, column=0, padx=12)
    create_labels()

# ^ Window functions

def calculator():
    import Stopwatch

def forwardcom():
    global display
    if display < 3:
        display += 1
    exec(f'panel.config(image=photo{display})')
    exec(f'head.config(text=head{display})')
    if display == 3:
        head.config(pady=54)
    else:
        head.config(pady=10)

def backwardcom():
    global display
    if display > 1:
        display -= 1
    exec(f'panel.config(image=photo{display})')
    exec(f'head.config(text=head{display})')
    if display == 3:
        head.config(pady=54)
    else:
        head.config(pady=10)

def helpcommand():
    global display; display = 1
    global panel
    global head

    helpwin = tk.Toplevel()
    helpwin["background"] = "#FEFFFD"
    helpwin.geometry('1000x700')

    global head1; head1 = "Time window"
    global head2; head2 = "Save window"
    global head3; head3 = "Compare window"

    head = tk.Label(helpwin, text=head1, font="Verdana 30", bg="#FEFFFD")
    head.grid(row=0, column=0, columnspan=5, pady=10)

    forw_btn = tk.PhotoImage(file="assets/forward2.png")
    forward = tk.Button(helpwin, image=forw_btn, command=backwardcom, highlightthickness=0, borderwidth=0)
    forward.grid(row=2, column=1, pady=18, sticky="E")

    back_btn = tk.PhotoImage(file="assets/backward.png")
    backward = tk.Button(helpwin, image=back_btn, command=forwardcom, highlightthickness=0, borderwidth=0)
    backward.grid(row=2, column=3, pady = 18, sticky="W")

    global photo1; photo1 = ImageTk.PhotoImage(Image.open("assets/timewindow3.png"))
    global photo2; photo2 = ImageTk.PhotoImage(Image.open("assets/savewindow2.png"))
    global photo3; photo3 = ImageTk.PhotoImage(Image.open("assets/comparewindow2.png"))

    panel = tk.Label(helpwin, image = photo1)
    panel.grid(row=1, column=0, columnspan=5)

    print(display)

    quit=tk.Button(helpwin, text="Quit", fg='white', bg="red",command=quitall)
    quit.grid(row=2, column=4, sticky="E", padx=30) # Pack quit button to right side   

    helpwin.mainloop()

# ^ Home screen funcs

time = tk.Label(window, text='00.000', fg="white", bg="black", font=("Courier", 80), height=4, width=16) 
time.grid(row=0, column=0, columnspan=6, rowspan=10, sticky="NSEW") # Pack timer text to fill screen, black monospaced text on black background

calc_btn = tk.PhotoImage(file="assets/calc_25x25.png")
calculator = tk.Button(window, image=calc_btn, command=calculator, bg="black", borderwidth=0)
calculator.grid(row=1, column=3, sticky="NE", pady=30)

help_btn= tk.PhotoImage(file='assets/help_25x25.png')
helpbutton = tk.Button(window, image=help_btn, command=helpcommand, bg="black", borderwidth=0)
helpbutton.grid(row=1, column=4, sticky="N", pady=30)

lap=tk.Button(window, text="Lap", fg='black', bg="grey", command=lap)
lap.grid(row=10, column=0, sticky="W") # Pack lap/reset button to left side

start=tk.Button(window, text="Start", fg='white', bg="green",command=start)
start.grid(row=10, column=1, sticky="W") # Pack start/pause button to left side

quit=tk.Button(window, text="Quit", fg='white', bg="red",command=quitall)
quit.grid(row=10, column=5, sticky="E") # Pack quit button to right side

viewsaves=tk.Button(window, text="View saves", fg='white', bg='green', command=view)
viewsaves.grid(row=10, column=4, sticky="E") # Pack view saves button to right side

save=tk.Button(window, text="Save", fg='black', bg="grey",command=save)
save.grid(row=10, column=3, sticky="E") # Pack Save button to right side

window.rowconfigure(1, weight=3)
window.rowconfigure(7, weight=1)
window.columnconfigure(1, weight=1)

# ^ Timer objects

window.after(1, update) # Call update on the first frame, then it gets called every frame due to it calling itself
window.mainloop() # Play the app