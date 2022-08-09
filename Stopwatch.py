# Code explanation:
# - When a button is pressed, a function is run.
# - If the button was a digit (0-9 or . or :), it will add it to a list called displayed_expression
# - displayed_expression represents what appears on screen, and everytime it is updated config is called to change the displays
# - If it is an operation (-,+,*,/ and brackets count as well), then that is added to displayed_expression
# - The previous time is also appended to the calculate_expression, which hold all times in milliseconds, so operations can be performed.
# - When equals is pressed, the final time is added to calculate_expression, and then eval() is called on the expression
# - This evaluates the equation. If an error is raised at any point, is is caught by an try, except. This will raise a pop-up, and cancel the process.

# Other features:
# - If you type in a time like 157:00, then press equals this will convert it into h:m:s (e.g. 02:37:00)
# - Order of operations is adhered to and use of brackets is allowed
# - Can select different themes in the menu
# - Keystrokes work as well as the onscreen buttons

# Note: If using VS Code you can collapse all the functions using Ctrl+J, Ctrl+0 since there are so many functions
# Expand them all with Ctrl+J, Ctrl+K

from tkinter import Tk, Label, Button, PhotoImage, Menu, Toplevel, messagebox, Text, END, WORD
import stopwatchfuncs as f # Import external functions and tkinter

if __name__ == "__main__":
    calculator = Tk() # If running alone
else:
    calculator = Toplevel() # If running in another program

calculator.title("Time Calculator")
calculator.config(bg="white")       # Creating window
calculator.resizable(False,False)

icon = PhotoImage(file="assets/icon.png")
calculator.iconphoto(True, icon)    # Change icon

displayed_expression = ['']
calculate_expression = []
digitsbgcolour = "light green"
operationsbgcolour = "light blue"
entrybgcolour = "#ff7f7f"
colonbgcolour = "yellow"
digitsfgcolour = "black"
operationsfgcolour = "black"
entryfgcolour = "black"
colonfgcolour = "black"
displaybgcolour = "white"
displayfgcolour = "black"
numhistoryitems = 0        # Set initial variables and colour of widgets
continuefromequals = True  # If you want to continue from the result of the previous operation


# Functions for the calculator
def cls(): # Clear the calculator
    global displayed_expression
    global calculate_expression # Varaiables manipulated globally

    display.config(text="")
    smalldisplay.config(text="")
    displayed_expression = ['']
    calculate_expression = [] # Reset all the variables
def equals(): # Evaluate the expression
    # If at any point an error is thrown in here, it will be caught by the except in pressequals() 

    global displayed_expression
    global calculate_expression 
    global numhistoryitems

    calcstring = ' '.join(calculate_expression) # Make it into a string expression
    if round(eval(calcstring)) < 0: # If result is negative throw an error (can't have a negative time)
        messagebox.showerror(title="Error!", message="Does not compute - your result is negative.")
        cls()
        return
    result = f.MillisToHMSM(round(eval(calcstring))) # Result is just evaluating the string
    
    display.config(text=result) # Show the evaluation of the equation

    smalldisplay.config(text=f"{' '.join(displayed_expression)} = {result}") # Some formatting for the small display  
    historymenu.add_command(label=f"{' '.join(displayed_expression)} = {result}", command=lambda: viewhistory(f"{' '.join(displayed_expression)} = {result}")) # Add the result to the history menu

    if continuefromequals:
        displayed_expression = [result] # A new calculation begins with the result of the previous
    else:
        displayed_expression = [''] # A new calculation begins with an empty display

    calculate_expression = [] # Reset variables
    numhistoryitems += 1      # New history item has been added
    if numhistoryitems == 11:
        historymenu.delete(1)
        numhistoryitems -= 1  # Code to ensure if the amount of history items is larger than 10, it will delete the oldest items
def delete(): # Delete one character
    global displayed_expression
    global calculate_expression 

    if displayed_expression == [""]: # If there are no digits, can't delete anything
        return

    elif displayed_expression[-1] == '': # This means the previous entry was an operation
        del displayed_expression[-1]
        del displayed_expression[-2]

        del calculate_expression[-1]
        del calculate_expression[-2] # Delete the appropriate items

    elif displayed_expression[-1][-1] in "0123456789.:": # Previous is a digit
        displayed_expression[-1] = displayed_expression[-1][:-1] # Remove one character off the end

    if displayed_expression[-1] in "*/-+()": # If the last item is an operation, need to add a new item on the end
        displayed_expression.append('')

    display.config(text=displayed_expression[-1])
    smalldisplay.config(text=' '.join(displayed_expression)) # Update the labels

def pressdigit(entry): # 0,1,2,3,4,5,6,7,8,9,.,:
    global displayed_expression
    global calculate_expression 

    displayed_expression[-1] += entry  # Add the digit to the display list
    display.config(text=displayed_expression[-1])
    smalldisplay.config(text=' '.join(displayed_expression))  # Update the displays
def pressoperation(entry): # +,-,*,/,(,)
    global displayed_expression
    global calculate_expression 

    if displayed_expression[-1] == '' and displayed_expression != ['']:
        del displayed_expression[-1] # If there is a whitespace character as an element in the list, delete it so the operation can be appended.

    validTime, returnTime = f.analyseTime(displayed_expression[-1]) # Check if previous entry is a valid time

    if len(displayed_expression) > 3: # Allows division and multiplication by integer values
        if displayed_expression[-2] in "*/" and str.isdigit(displayed_expression[-1]): # If there is an integer next to a multiplication or division sign
            calculate_expression.append(displayed_expression[-1]) # Put it in the calculation list in millisecond form
            calculate_expression.append(entry)
            displayed_expression.append(entry) # Add the operation
            displayed_expression.append("") # Add a new item in the list
            display.config(text=entry)
            smalldisplay.config(text=' '.join(displayed_expression)) # Update the displays
            return
    if validTime: # If its a time
        displayed_expression[-1] = returnTime # Make the time into the proper format
        calculate_expression.append(str(f.convertToMillis(displayed_expression[-1]))) # Put it in the calculation list in millisecond form
        calculate_expression.append(entry)
        displayed_expression.append(entry) # Add the operation
        displayed_expression.append("") # Add a new item in the list
        display.config(text=entry)
        smalldisplay.config(text=' '.join(displayed_expression)) # Update the displays
        return
    if displayed_expression[-1] in "()":
        if displayed_expression[-1] not in "*/+-()": # Don't want to re-add an operation
            calculate_expression.append(displayed_expression[-1])
        calculate_expression.append(entry)
        displayed_expression.append(entry)
        displayed_expression.append('')
        display.config(text=entry)
        smalldisplay.config(text=' '.join(displayed_expression)) # Update the displays
        return
    if displayed_expression == ['']: # Can't add any operation at start other than (
        if entry == "(":
            calculate_expression.append(entry)
            displayed_expression.append(entry)
            displayed_expression.append("")
            display.config(text=entry)
            smalldisplay.config(text=' '.join(displayed_expression)) # Update the displays   
        return  
def pressequals(): # Equals button
    global displayed_expression
    global calculate_expression 
    global numhistoryitems 
    if len(displayed_expression) == 1: # If it only has one item then it should be simplified e.g. 135 -> 02:15:00.000
        validTime, returnTime = f.analyseTime(displayed_expression[0]) # Check if it's a valid time
        if validTime:
            display.config(text=returnTime)
            smalldisplay.config(text=f"{displayed_expression[0]} = {returnTime}") # Change displays
            historymenu.add_command(label=f"{displayed_expression[0]} = {returnTime}", command=lambda: viewhistory(f"{displayed_expression[0]} = {returnTime}"))
            # Add item to history menu
            if continuefromequals:
                displayed_expression = [returnTime] # A new calculation begin with the result of the previous
            else:
                displayed_expression = ['']
            calculate_expression = [] # Reset variables
            numhistoryitems += 1      # New history item has been added
            if numhistoryitems == 11:
                historymenu.delete(1)
                numhistoryitems -= 1
        return

    elif len(displayed_expression) < 3: # Has to have at least 3 elements to do a calculation
        return
    try:
            validTime2, returnTime2 = f.analyseTime(displayed_expression[-1]) # Check if valid time
    except IndexError:
        return # If there are no items to calculate, equals can't be pressed
    
    try:
        if displayed_expression[-1] == "": 
            del displayed_expression[-1] # Get rid of trailing whitespace
        if displayed_expression[-2] in "*/" and str.isdigit(displayed_expression[-1]): # If there is an int after multiplication/division
            calculate_expression.append(displayed_expression[-1]) # Put it in the calculation list in millisecond form
        elif validTime2:
            displayed_expression[-1] = returnTime2 # If last item is a time, convert to proper format
            calculate_expression.append(str(f.convertToMillis(displayed_expression[-1]))) # Add the time in milliseconds to calculate_expression

        equals() # Evaluate the expression

    except Exception as e: # If anything goes wrong with the calculation
        errorlog = messagebox.askyesno(title="Error!", message="Does not compute. Check your equation and try again, or refer to our help page. See error log?") # Pop up window
        if errorlog:
            messagebox.showerror(title="Error log", message=e) # Show error message
        cls()
        return


# Functions for menu options
def helpme(): # Help function
    helpwindow = Toplevel()
    helpwindow.title("Help")

    helptext = Text(helpwindow, wrap=WORD) # Creates a text widget
    helptext.grid(row=0, column=0, sticky = "NESW")

    helptext.tag_configure('title', font='Verdana 27 bold underline', background="yellow")
    helptext.tag_configure('subheading', font='Arial 18 bold')
    helptext.tag_configure('subsubheading', font='Arial 15 bold')
    helptext.tag_configure('body', font="Arial 15")
    helptext.tag_configure('eg', font="Arial 15 italic", foreground="grey") # Define tags

    # Have to put all of this in seperate inserts because there are different tags for each of them

    helptext.insert(END, "How to use the Time Calculator", 'title')
    helptext.insert(END, "\nPurposes:", 'subheading')
    helptext.insert(END, "\nFeel free to use this calculator for any purpose. It is intended for use with time data, but you can also multiply or divide by integer values.", 'body')
    helptext.insert(END, "\n\nTime input:", 'subheading')
    helptext.insert(END, '''\nTo use this calculator, there are several different types of times that can be inputted.
    - s / ss ''', 'body') 
    helptext.insert(END, '''(e.g. 1 or 12)''', 'eg')
    helptext.insert(END, '''\n    - m:ss / mm:ss ''', 'body')
    helptext.insert(END, '''(e.g. 1:30 or 12:20)''', 'eg')
    helptext.insert(END, '''\n    - h:mm:ss / hh:mm:ss ''', 'body') 
    helptext.insert(END, '''(e.g. 1:30:20 or 12:30:20)''', 'eg')
    helptext.insert(END, '\nImportant to note:', 'subsubheading')
    helptext.insert(END, '''\n    - All of these options can have milliseconds added on the end (.mmm)
    - In the small display at the top, all inputted times will be converted to:''', 'body')
    helptext.insert(END, '\n      ss.mmm, mm:ss.mmm or hh:mm:ss.mmm', 'eg')
    helptext.insert(END, '''\n    - If multiplying or dividing, make sure to do it in the form: time * int. If you input 1:30 * 2, the 2 will not be converted into a time, but if you do it the other way around, they will both be converted to times and your result will be incorrect.
    - Something else to note: when doing division of time / time, your result will come back in milliseconds. This is due to the way the times are calculated, but simply multiply your answer by 1000 and you will be good.''', 'body')
    helptext.insert(END, '\n\nBrackets:', 'subheading')
    helptext.insert(END, '''\nBrackets are incorporated for ease of use. You may opt to use them to make your equations clearer, or not to use them. Important to note: ''', 'body')
    helptext.insert(END, 'You cannot put a time by a bracket to represent multiplying it e.g. 12:30(2:20 + 1:30). This does not work. Please use 12:30 * (2:20 + 1:30), otherwise you will get an error.', 'eg')
    helptext.insert(END, '\n\nAdditionally, make sure to match all of your brackets, or you will get an error.', 'body')
    helptext.insert(END, '\n\nOrder of operations', 'subheading')
    helptext.insert(END, '\nOrder of operations is handled by the python eval() function. This evaluates brackets first, then multiplication/division, then addition/subtraction. If you want to circumvent this, you can use brackets to evaluate additions and subtractions before multiplications and divisions.', 'body')
    helptext.insert(END, '\n\nTroubleshooting', 'subheading')
    helptext.insert(END, '\nI\'m getting errors when I press equals!', 'subsubheading')
    helptext.insert(END, '\nTo get an idea for a possible reason for your error, you can open the error log.', 'body')
    helptext.insert(END, '''\n\nIf that doesn\'t work, other reasons are:
    - Your result is negative.
    - You have an unmatched bracket.
    - You put a number next to a bracket, remember to put operations between each value.
    - Dividing by 0.
    - Order of operations mistake.''', 'body')
    helptext.insert(END, '\n\nIf none of this works, that\'s a problem. We do not have a solution, or any customer support as this is just some student\'s project.', 'eg')
    helptext.insert(END, '\n\nTips and Tricks:', 'subheading')
    helptext.insert(END, '\nYou can use the keys to input, as well as the buttons on screen. The keys that work are: 0,1,2,3,4,5,6,7,8,9,.,:, backspace and esc to clear the screen. This can help you input times faster, and in my opinion is easier than using the buttons.', 'body')
    helptext.insert(END, '\n\nObviously, by navigating to this menu you have figured out the menus. If you use the settings menu you can customise the colour of all of the buttons, or select a theme. This is useful to create your own colour palettes.', 'body')
    helptext.insert(END, '\n\nIf you want to equate a time, like a movie run length, you can do this by inputting the time and then pressing equals.', 'body')
    helptext.insert(END, 'e.g. 147mins and 55seconds - input 147:55, press equals, and it equates to 2:27:55', 'eg')
    helpwindow.rowconfigure(0, weight=1)
    helpwindow.columnconfigure(0, weight=1)
def newwindow(): # Import the same file
    import main


# All of these functions just configure the colours of the widgets
# Start by creating colour variables, and then config the widgets
def lighttheme():
    digitsbgcolour = "light green"
    operationsbgcolour = "light blue"
    entrybgcolour = "#ff7f7f"
    colonbgcolour = "yellow"
    digitsfgcolour = "black"
    operationsfgcolour = "black"
    entryfgcolour = "black"
    colonfgcolour = "black"
    displaybgcolour = "white"
    displayfgcolour= "black"

    display.config(fg=displayfgcolour, bg=displaybgcolour)
    smalldisplay.config(fg=displayfgcolour, bg=displaybgcolour)
    multiply.config(bg=operationsbgcolour, fg=operationsfgcolour)
    divide.config(bg=operationsbgcolour, fg=operationsfgcolour)
    button1.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button2.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button3.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button4.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button5.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button6.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button7.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button8.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button9.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button0.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button_decimal.config(bg=colonbgcolour, fg=colonfgcolour)
    button_colon.config(bg=colonbgcolour, fg=colonfgcolour)
    add.config(bg=operationsbgcolour, fg=operationsfgcolour)
    subtract.config(bg=operationsbgcolour, fg=operationsfgcolour)
    clear.config(bg=entrybgcolour, fg=entryfgcolour)
    buttonequals.config(bg=entrybgcolour, fg=entryfgcolour)
def darktheme():
    displayfgcolour = "white"
    digitsfgcolour = "light green"
    operationsfgcolour = "light blue"
    entryfgcolour = "#ff7f7f"
    colonfgcolour = "yellow"
    digitsbgcolour = "black"
    operationsbgcolour = "black"
    entrybgcolour = "black"
    colonbgcolour = "black"
    displaybgcolour= "black"

    display.config(fg=displayfgcolour, bg=displaybgcolour)
    smalldisplay.config(fg=displayfgcolour, bg=displaybgcolour)
    multiply.config(bg=operationsbgcolour, fg=operationsfgcolour)
    divide.config(bg=operationsbgcolour, fg=operationsfgcolour)
    button1.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button2.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button3.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button4.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button5.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button6.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button7.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button8.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button9.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button0.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button_decimal.config(bg=colonbgcolour, fg=colonfgcolour)
    button_colon.config(bg=colonbgcolour, fg=colonfgcolour)
    add.config(bg=operationsbgcolour, fg=operationsfgcolour)
    subtract.config(bg=operationsbgcolour, fg=operationsfgcolour)
    clear.config(bg=entrybgcolour, fg=entryfgcolour)
    buttonequals.config(bg=entrybgcolour, fg=entryfgcolour)
def lightdisplay():
    display.config(fg="black", bg="white")
    smalldisplay.config(fg="black", bg="white")
def darkdisplay():
    display.config(fg="white", bg="black")
    smalldisplay.config(fg="white", bg="black")
def lightbackground():
    calculator.config(bg="white")
def darkbackground():
    calculator.config(bg="black")
def lightnumbuttons():
    digitsbgcolour = "light green"
    digitsfgcolour = "black"

    button1.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button2.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button3.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button4.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button5.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button6.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button7.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button8.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button9.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button0.config(bg=digitsbgcolour, fg=digitsfgcolour)
def darknumbuttons():
    digitsbgcolour = "black"
    digitsfgcolour = "light green"

    button1.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button2.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button3.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button4.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button5.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button6.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button7.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button8.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button9.config(bg=digitsbgcolour, fg=digitsfgcolour)
    button0.config(bg=digitsbgcolour, fg=digitsfgcolour)
def lightoperations():
    operationsbgcolour = "light blue"
    operationsfgcolour = "black"

    multiply.config(bg=operationsbgcolour, fg=operationsfgcolour)
    divide.config(bg=operationsbgcolour, fg=operationsfgcolour)
    add.config(bg=operationsbgcolour, fg=operationsfgcolour)
    subtract.config(bg=operationsbgcolour, fg=operationsfgcolour)
def darkoperations():
    operationsbgcolour = "black"
    operationsfgcolour = "light blue"

    multiply.config(bg=operationsbgcolour, fg=operationsfgcolour)
    divide.config(bg=operationsbgcolour, fg=operationsfgcolour)
    add.config(bg=operationsbgcolour, fg=operationsfgcolour)
    subtract.config(bg=operationsbgcolour, fg=operationsfgcolour)
def lightentry():
    entrybgcolour = "#ff7f7f"
    entryfgcolour = "black"

    clear.config(bg=entrybgcolour, fg=entryfgcolour)
    buttonequals.config(bg=entrybgcolour, fg=entryfgcolour)
def darkentry():
    entrybgcolour = "black"
    entryfgcolour = "#ff7f7f"

    clear.config(bg=entrybgcolour, fg=entryfgcolour)
    buttonequals.config(bg=entrybgcolour, fg=entryfgcolour)
def lightcolon():
    colonbgcolour = "yellow"
    colonfgcolour = "black"

    button_decimal.config(bg=colonbgcolour, fg=colonfgcolour)
    button_colon.config(bg=colonbgcolour, fg=colonfgcolour)
def darkcolon():
    colonbgcolour = "black"
    colonfgcolour = "yellow"

    button_decimal.config(bg=colonbgcolour, fg=colonfgcolour)
    button_colon.config(bg=colonbgcolour, fg=colonfgcolour)


# Functions for history
def viewhistory(historyitem): # When a history item is pressed
    global displayed_expression
    global calculate_expression

    display.config(text=historyitem.split(" = ")[1])
    smalldisplay.config(text=historyitem)
    displayed_expression = [historyitem.split(" = ")[1]]
    calculate_expression = []
    pass # Views history item by just changing the lists and configuring displays
def clearhistory(): # Clear all history items
    global numhistoryitems
    for i in range(numhistoryitems, 0, -1):
        historymenu.delete(i)
    numhistoryitems = 0 # Clear items in reverse because it's easier that way since the indexes don't get mixed up

def continueequals(inp): # The continue from equals function
    global continuefromequals
    if inp == "Yes":
        continuefromequals = True 
    elif inp == "No":
        continuefromequals = False # Change the variables
    else:
        tempwin = Toplevel()
        tempwin.geometry("470x230")
        templabel = Label(tempwin, text='''Continue from equals is a feature designed to give you more control over your experience in the time calculator.\n\nAfter you've pressed equals, by default you will continue on pressing buttons after the result of the previous operation. e.g. 1:30 + 12:54 = 13:24.000, you will continue on typing with 13:24.000 already on your screen.\n\nThis is continue from equals ON. If you turn it off, it will display your result still, but you will start typing and the screen will be cleared.''', justify="left", font="Verdana 12", wraplength=450)
        templabel.grid() # Just create a small window to explain what the continuefromequals variable means

# Now to create the displays
display = Label(calculator, text="", fg=displayfgcolour, bg=displaybgcolour, font=("Verdana", 40), pady=10, width=14, anchor="e", borderwidth=0)
display.grid(row=0, column=0, columnspan=6, rowspan=2) # spans 5 columns and 2 rows
smalldisplay = Label(calculator, text="", fg=displayfgcolour, bg=displaybgcolour, font=("Courier", 10), anchor="e", width=40, borderwidth=0)
smalldisplay.grid(row=0, column=0, sticky="NW", columnspan=6) # small display for full equation

# Add menu options
menu = Menu(calculator)
calculator.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
settingsmenu = Menu(menu, tearoff=0)
historymenu = Menu(menu, tearoff=0)
menu.add_cascade(label="General",menu=filemenu) # Creating the general menu

theme_sub_menu = Menu(settingsmenu, tearoff=0)
customize_sub_menu = Menu(settingsmenu, tearoff=0)
display_sub_sub_menu = Menu(settingsmenu, tearoff=0)
background_sub_sub_menu = Menu(settingsmenu, tearoff=0)
numbuttons_sub_sub_menu = Menu(settingsmenu, tearoff=0)
operations_sub_sub_menu = Menu(settingsmenu, tearoff=0)
entry_sub_sub_menu = Menu(settingsmenu, tearoff=0)
colon_sub_sub_menu = Menu(settingsmenu, tearoff=0)
continuemenu = Menu(settingsmenu, tearoff=0)
continuesubmenu = Menu(filemenu, tearoff=0)             # Create all menus and submenus (and sub-submenus)

theme_sub_menu.add_command(label='Light', command=lighttheme)
theme_sub_menu.add_command(label='Dark', command=darktheme) # Create the theme sub menu options

customize_sub_menu.add_cascade(label='Display', menu=display_sub_sub_menu)
display_sub_sub_menu.add_command(label='Light', command=lightdisplay)
display_sub_sub_menu.add_command(label='Dark', command=darkdisplay) # Add to the sub menu another menu, with two options (light/dark)

customize_sub_menu.add_cascade(label='Background', menu=background_sub_sub_menu)
background_sub_sub_menu.add_command(label='Light', command=lightbackground)
background_sub_sub_menu.add_command(label='Dark', command=darkbackground)

customize_sub_menu.add_cascade(label="Number Buttons", menu=numbuttons_sub_sub_menu)
numbuttons_sub_sub_menu.add_command(label='Light', command=lightnumbuttons)
numbuttons_sub_sub_menu.add_command(label='Dark', command=darknumbuttons)

customize_sub_menu.add_cascade(label="Operations", menu=operations_sub_sub_menu)
operations_sub_sub_menu.add_command(label='Light', command=lightoperations)
operations_sub_sub_menu.add_command(label='Dark', command=darkoperations)

customize_sub_menu.add_cascade(label="Equals and clear", menu=operations_sub_sub_menu)
entry_sub_sub_menu.add_command(label='Light', command=lightentry)
entry_sub_sub_menu.add_command(label='Dark', command=darkentry)

customize_sub_menu.add_cascade(label="Point and colon", menu=operations_sub_sub_menu)
colon_sub_sub_menu.add_command(label='Light', command=lightcolon)
colon_sub_sub_menu.add_command(label='Dark', command=darkcolon)                         # Each one of these creates a new sub menu with 2 options

continuemenu.add_command(label="Yes", command=lambda: continueequals("Yes"))
continuemenu.add_command(label="No", command=lambda: continueequals("No"))
continuemenu.add_command(label="?", command=lambda: continueequals("?"))

settingsmenu.add_cascade(label="Theme", menu=theme_sub_menu) # Prints new file in console
settingsmenu.add_cascade(label="Customize", menu=customize_sub_menu) # Add the menus
settingsmenu.add_cascade(label="Continue from equals", menu=continuemenu)

menu.add_cascade(label="Settings", menu=settingsmenu)

historymenu.add_command(label="Clear History", command=clearhistory)
menu.add_cascade(label="History", menu=historymenu)                 #  History menu is empty to start, items get added once equals is pressed

filemenu.add_command(label="New Window", command=newwindow)
filemenu.add_command(label="Help", command=helpme) # Prints new file in console
filemenu.add_separator()
filemenu.add_command(label="Quit", command=quit)


# Add buttons
multiply = Button(calculator, text="*", width=3, bg=operationsbgcolour, fg=operationsfgcolour, command=lambda: pressoperation("*"), font=("Verdana", 12))
multiply.grid(row=2, column=0, ipadx=25, ipady=5, pady=2, sticky="S")
divide = Button(calculator, text="/", width=3, bg=operationsbgcolour, fg=operationsfgcolour, command=lambda: pressoperation("/"), font=("Verdana", 12))
divide.grid(row=3, column=0, ipadx=25, ipady=5, pady=1)
del_img= PhotoImage(file='assets/deleteico2.png')
buttondel = Button(calculator, image=del_img, width=3, bg="red", command=delete, font=("Verdana", 12))
buttondel.grid(row=5, column=1, ipadx=40, ipady=3, pady=1)
button1 = Button(calculator, text="1", width=3, bg=digitsbgcolour, fg=digitsfgcolour, command=lambda: pressdigit("1"), font=("Verdana", 12))
button1.grid(row=2, column=1, ipadx=25, ipady=5, pady=2, sticky="S")
button2 = Button(calculator, text="2", width=3, bg=digitsbgcolour, fg=digitsfgcolour, command=lambda: pressdigit("2"), font=("Verdana", 12))
button2.grid(row=2, column=2, ipadx=25, ipady=5, pady=2, sticky="S")
button3 = Button(calculator, text="3", width=3, bg=digitsbgcolour, fg=digitsfgcolour, command=lambda: pressdigit("3"), font=("Verdana", 12))
button3.grid(row=2, column=3, ipadx=25, ipady=5, pady=2, sticky="S", columnspan=2)
button4 = Button(calculator, text="4", width=3, bg=digitsbgcolour, fg=digitsfgcolour, command=lambda: pressdigit("4"), font=("Verdana", 12))
button4.grid(row=3, column=1, ipadx=25, ipady=5, pady=1)
button5 = Button(calculator, text="5", width=3, bg=digitsbgcolour, fg=digitsfgcolour, command=lambda: pressdigit("5"), font=("Verdana", 12))
button5.grid(row=3, column=2, ipadx=25, ipady=5, pady=1)
button6 = Button(calculator, text="6", width=3, bg=digitsbgcolour, fg=digitsfgcolour, command=lambda: pressdigit("6"), font=("Verdana", 12))
button6.grid(row=3, column=3, ipadx=25, ipady=5, pady=1, columnspan=2)
button7 = Button(calculator, text="7", width=3, bg=digitsbgcolour, fg=digitsfgcolour, command=lambda: pressdigit("7"), font=("Verdana", 12))
button7.grid(row=4, column=1, ipadx=25, ipady=5, pady=1)
button8 = Button(calculator, text="8", width=3, bg=digitsbgcolour, fg=digitsfgcolour, command=lambda: pressdigit("8"), font=("Verdana", 12))
button8.grid(row=4, column=2, ipadx=25, ipady=5, pady=1)
button9 = Button(calculator, text="9", width=3, bg=digitsbgcolour, fg=digitsfgcolour, command=lambda: pressdigit("9"), font=("Verdana", 12))
button9.grid(row=4, column=3, ipadx=25, ipady=5, pady=1, columnspan=2)
button0 = Button(calculator, text="0", width=3, bg=digitsbgcolour, fg=digitsfgcolour, command=lambda: pressdigit("0"), font=("Verdana", 12))
button0.grid(row=5, column=2, ipadx=25, ipady=5, pady=1)
buttonlb = Button(calculator, text="(", width=2, bg=operationsbgcolour, fg=operationsfgcolour, command=lambda: pressoperation("("), font=("Verdana", 12))
buttonlb.grid(row=5, column=3, ipadx=7, ipady=5, pady=1, padx=1, sticky="W")
buttonrb = Button(calculator, text=")", width=2, bg=operationsbgcolour, fg=operationsfgcolour, command=lambda: pressoperation(")"), font=("Verdana", 12))
buttonrb.grid(row=5, column=4, ipadx=7, ipady=5, pady=1, sticky="W")
button_decimal = Button(calculator, text=".", width=3, bg=colonbgcolour, fg=colonfgcolour, command=lambda: pressdigit("."), font=("Verdana", 12))
button_decimal.grid(row=5, column=0, ipadx=25, ipady=5, pady=1)
button_colon = Button(calculator, text=":", width=3, bg=colonbgcolour, fg=colonfgcolour, command=lambda: pressdigit(":"), font=("Verdana", 12))
button_colon.grid(row=4, column=0, ipadx=25, ipady=5, pady=1)
add = Button(calculator, text="+", width=3, bg=operationsbgcolour, fg=operationsfgcolour, command=lambda: pressoperation("+"), font=("Verdana", 12))
add.grid(row=3, column=5, ipadx=25, ipady=5, pady=2, sticky="S")
subtract = Button(calculator, text="-", width=3, bg=operationsbgcolour, fg=operationsfgcolour, command=lambda: pressoperation("-"), font=("Verdana", 12))
subtract.grid(row=4, column=5, ipadx=25, ipady=5, pady=1)
clear = Button(calculator, text="AC", width=3, bg=entrybgcolour, fg=entryfgcolour,  command=cls, font=("Verdana", 12))
clear.grid(row=2, column=5, ipadx=25, ipady=5, pady=1)
buttonequals = Button(calculator, text="=", width=3, bg=entrybgcolour, fg=entryfgcolour,  command=lambda: pressequals(), font=("Verdana", 12))
buttonequals.grid(row=5, column=5, ipadx=25, ipady=5, pady=1)


# Bind keystrokes to work
calculator.bind("(", lambda event: pressoperation("("))
calculator.bind(")", lambda event: pressoperation(")"))
calculator.bind("0", lambda event: pressdigit("0"))
calculator.bind("1", lambda event: pressdigit("1"))
calculator.bind("2", lambda event: pressdigit("2"))
calculator.bind("3", lambda event: pressdigit("3"))
calculator.bind("4", lambda event: pressdigit("4"))
calculator.bind("5", lambda event: pressdigit("5"))
calculator.bind("6", lambda event: pressdigit("6"))
calculator.bind("7", lambda event: pressdigit("7"))
calculator.bind("8", lambda event: pressdigit("8"))
calculator.bind("9", lambda event: pressdigit("9"))
calculator.bind(".", lambda event: pressdigit("."))
calculator.bind(":", lambda event: pressdigit(":"))
calculator.bind("+", lambda event: pressoperation("+"))
calculator.bind("-", lambda event: pressoperation("-"))
calculator.bind("*", lambda event: pressoperation("*"))
calculator.bind("x", lambda event: pressoperation("*"))
calculator.bind("/", lambda event: pressoperation("/"))
calculator.bind("=", lambda event: pressequals())
calculator.bind("<Return>", lambda event: pressequals())
calculator.bind("<BackSpace>", lambda event: delete())
calculator.bind("<Escape>", lambda event: cls())

if __name__ == "__main__":
    calculator.mainloop() # If running alone