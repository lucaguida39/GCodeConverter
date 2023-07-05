#=====================================================================================
from tkinter import *
import re
import os
from tkinter import filedialog
from gcode_mod import conversion
import tempfile
import time


#=====================================================================================
#If the script is running on a Mac, the library for optimized GUI is imported
#=====================================================================================
import platform
if platform.system()=='Darwin':
    from tkmacosx import *


NumberOfFiles=0
InProgressOpen=False
ErrorOpen=False


#=====================================================================================
#Find the temporary file folder in which store settings
#=====================================================================================
temp=tempfile.gettempdir()
filename = temp + "/datagcodeconverter.txt"


#=====================================================================================
#As the application is launched, previously stored settings, if any, are recovered
#This way, the user finds the settings used the previous time
#=====================================================================================
try:
    with open(filename) as file:
        lines = file.readlines()
        var1 = str(lines[0].strip()) if len(lines) > 0 else ""
        var2 = bool(int(lines[1].strip())) if len(lines) > 1 and lines[1].strip() in ["0", "1"] else ""
        var3 = float(lines[2].strip()) if len(lines) > 2 and lines[2].strip().replace(".", "", 1).isdigit() else ""
        var4 = bool(int(lines[3].strip())) if len(lines) > 3 and lines[3].strip() in ["0", "1"] else ""
        var5 = str(lines[4].strip()) if len(lines) > 4 and lines[4].strip() in ["Up", "Down", "Right", "Left"] else ""
        var6 = float(lines[5].strip()) if len(lines) > 5 and lines[5].strip().replace(".", "", 1).isdigit() else ""
except (FileNotFoundError, ValueError):
    var1, var2, var3, var4, var5, var6 = "", "", "", "", "", ""


#=====================================================================================
#Function to be executed when the "Convert" button is pressed
#=====================================================================================
def run_function():
    global InProgressOpen
    global ErrorOpen
    global InProgress
    global Error

#Close existing dialog windows, if any
    if InProgressOpen == True:
        if InProgress.winfo_exists()==1:
             InProgress.destroy()
    if ErrorOpen == True:
        if Error.winfo_exists()==1:
             Error.destroy()

#Export settings to an external file, in order to be available for
#next steps and to be saved after the app is closed
    File_Text=[]
    path_line = path_textbox.get()
    File_Text.append(path_line)
    UV_Check_line = LedChecked.get()
    if UV_Check_line==True:
        string=ledTime_textbox.get()
        if string !='' and string[-1]=='.':
            string=string[0:-1]
        if ((string!='' and float(string)==0) or string ==''):
                UV_Check_line=0
    File_Text.append(UV_Check_line)
    UV_time_line = ledTime_textbox.get()
    File_Text.append(UV_time_line)
    ExtraRun_Check_line=ExtraRunChecked.get()
    if ExtraRun_Check_line==True:
        string=extra_textbox.get()
        if string !='' and string[-1]=='.':
            string=string[0:-1]
        if ((string!='' and float(string)==0) or string ==''):
                ExtraRun_Check_line=0
    File_Text.append(ExtraRun_Check_line)
    Direction_Line=selected_direction.get()
    File_Text.append(Direction_Line)
    ExtraRun_Distance_Line=extra_textbox.get()
    File_Text.append(ExtraRun_Distance_Line)
    with open(filename, "w") as file:
        for item in File_Text:
            file.write("%s\n" % item)

#In case data is missing, an error message is shown
    if path_line=='' or (LedChecked.get()==True and (UV_time_line=='' or UV_time_line=='.')) or (ExtraRunChecked.get()==True and (ExtraRun_Distance_Line=='' or ExtraRun_Distance_Line=='.')):
        Error = Toplevel()
        Error.attributes('-topmost', 1)
        ErrorOpen=True
        Error.title("Error")
        WE = int(screen_width * 0.2)
        HE = int(screen_height * 0.15)
        XE=int(screen_width * 0.5-WE/2)
        YE=int(screen_height * 0.5-HE/2)
        Error.geometry('%dx%d+%d+%d' % (WE, HE, XE, YE))
        ErrorLabel = Label(Error)
        ErrorLabel['font'] = ('Helvetica Neue Medium', int(0.9*FontSize))
        ErrorLabel.place(relx = 0.5, rely = 0.3, anchor = CENTER)
        Ok = Button(Error)
        Ok['text']='Ok'
        Ok['font'] = ('Helvetica Neue Thin', FontSize)
        Ok['fg'] = '#002a8b'
        Ok['activeforeground']=run['fg']
        Ok['bg']='#a2b4eb'
        Ok['width'] = int(W/8.5)
        Ok['height'] = int(ButtonHeigth)
        Ok['command']=Error.destroy
        Ok.place(x=0.3*WE, y=0.65*HE)
        if ExtraRunChecked.get()==True and (ExtraRun_Distance_Line=='' or ExtraRun_Distance_Line=='.') :
            ErrorLabel['text']="Choose a valid extra run distance\nand try again."
        if LedChecked.get()==True and (UV_time_line=='' or UV_time_line=='.'):
            ErrorLabel['text']="Insert a valid UV curing time\nand try again."
        if path_line=='':
            ErrorLabel['text']="Choose a valid file path\nand try again."
        return

#A dialog window is opened to inform the user that the conversion is taking place
    InProgress = Toplevel()
    InProgressOpen=True
    InProgress.attributes('-topmost', 1)
    InProgress.title("Conversion")
    WP = int(screen_width * 0.2)
    HP = int(screen_height * 0.15)
    XP=int(screen_width * 0.5-WP/2)
    YP=int(screen_height * 0.5-HP/2)
    InProgress.geometry('%dx%d+%d+%d' % (WP, HP, XP, YP))
    InProgressLabel = Label(InProgress)
    InProgressLabel['font'] = ('Helvetica Neue Medium', int(0.9*FontSize))
    InProgressLabel.place(relx = 0.5, rely = 0.3, anchor = CENTER)
    InProgressLabel['text']="Conversion in progress.."
    InProgress.update()

#The function that converts GCodes is recalled
    NumberOfFiles=conversion()

#After the conversion, the dialog window informs the user about the output
    time.sleep(0.5)
    Close = Button(InProgress)
    Close['text']='Close'
    Close['font'] = ('Helvetica Neue Thin', FontSize)
    Close['fg'] = '#002a8b'
    Close['activeforeground']=run['fg']
    Close['bg']='#a2b4eb'
    Close['width'] = int(W/8.5)
    Close['height'] = int(ButtonHeigth)
    Close['command']=InProgress.destroy
    Close.place(x=0.3*WP, y=0.65*HP)
    if NumberOfFiles==0:
        InProgressLabel['text']="No G-Codes found!"
    if NumberOfFiles==1:
        InProgressLabel['text']="1 G-Code converted!"
    if NumberOfFiles>1:
        InProgressLabel['text']=str(NumberOfFiles)+" G-Codes converted!"
    InProgress.update()


#=====================================================================================
#Function to be launched when clicking on the "choose folder" Button
#It allows to choose and show the location of G-Codes to be converted
#=====================================================================================
def openfolder_function():
    global folder_path
    path = filedialog.askdirectory()
    if path!="":
        path_textbox.delete('0', END)
        folder_path=path
        path_textbox.insert(0, path)


#=====================================================================================
#Functions that activates entries when the correspondent checkbutton is selected
#=====================================================================================
def LedCheckbox_function():
    if (LedChecked.get() == True):
        ledTime_textbox['state']='normal'
    elif (LedChecked.get() == False):
        ledTime_textbox['state']='disabled'

def ExtraRunChecked_function():
    if (ExtraRunChecked.get() == True):
        drop['state']='normal'
        extra_textbox['state']='normal'
    elif (ExtraRunChecked.get() == False):
        drop['state']='disabled'
        extra_textbox['state']='disabled'


#=====================================================================================
#Set the GUI
#=====================================================================================
root = Tk()
root.title("ConvertMe")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size as a fraction of the screen size
W = int(screen_width * 0.7)
H = int(screen_height * 0.5)
X=int(screen_width * 0.5-W/2)
Y=int(screen_height * 0.5-H/2)
root.geometry('%dx%d+%d+%d' % (W, H, X, Y))

#Set position of objects
X1=int(0.033*W)
X2=int(0.24*W)
X3=int(0.43*W)
X4=int(0.52*W)
X5=int(0.615*W)
X6=int(0.82*W)
Y1=int(0.1*H)
Y2=int(0.2*H)
Y3=int(0.3*H)
Y4=int(0.37*H)
Y5=int(0.5*H)
YLast=int(0.85*H)
ButtonHeigth=int(0.07*H)
ButtonWidth=int(0.12*W)
SignatureX=int(0.01*W)
SignatureY=int(0.93*H)
FontSize=int(0.042*H)
label = Label(root)
string='G-Code converter - Developed at +Lab, Politecnico di Milano'
label['text']=string
label['font'] = ('Helvetica Neue Thin', FontSize)
label.place(x=SignatureX, y=SignatureY)


#=====================================================================================
#Button convert
#=====================================================================================
run = Button(root)
run['text']='Convert!'
run['font'] = ('Helvetica Neue Thin', FontSize)
run['fg'] = '#002a8b'
run['activeforeground']=run['fg']
run['bg']='#a2b4eb'
run['width'] = int(ButtonWidth)
run['height'] = int(ButtonHeigth)
run['command']=run_function
run.place(x=X6, y=YLast)


#=====================================================================================
#Choose folder path
#=====================================================================================
#Folder path textbox
path_textbox = Entry(root, width=55)
path_textbox['font'] = ('Helvetica Neue Thin', FontSize)
path_textbox.place(x=X2, y=Y1)
PathLabel = Label(root, text = "G-Codes path:")
PathLabel['font'] = ('Helvetica Neue Light', FontSize)
PathLabel.place(x=X1, y=Y1)

#Button choose path
explore = Button(root)
explore['text']='Choose folder'
explore['font'] = ('Helvetica Neue Thin', FontSize)
explore['fg'] = '#002a8b'
explore['activeforeground']=explore['fg']
explore['bg']='#a2b4eb'
explore['width'] = ButtonWidth
explore['height'] = ButtonHeigth
explore.place(x=X6, y=Y1)
explore['command']=openfolder_function


#=====================================================================================
#UV settings
#=====================================================================================
#functions that allows to insert only numbers
def validate_input(text):
    pattern = r'^\d*\.?\d*$'
    return re.match(pattern, text) is not None

def on_validate(P):
    if validate_input(P):
        return True
    else:
        root.bell()
        return False

#UV textbox
ledTime_textbox = Entry(root, width=8, validate="key", validatecommand=(root.register(on_validate), '%P'))
ledTime_textbox['state']='disabled'
ledTime_textbox['font'] = ('Helvetica Neue Thin', FontSize)
ledTime_textbox['disabledbackground']='#d4d4d4'
ledTime_textbox.place(x=X4, y=Y2)
ledTime_textbox['justify']='right'

#UV checkbox
LedChecked = IntVar()
LedCheck = Checkbutton(root, variable=LedChecked, onvalue=True, offvalue=False, command=LedCheckbox_function)
LedCheck.place(x=X2, y=Y2)

#Labels
LedCheckboxLabel = Label(root, text = "UV at Layer Change")
LedCheckboxLabel['font'] = ('Helvetica Neue Light', FontSize)
LedCheckboxLabel.place(x=X1, y=Y2)

UVTimeLabel = Label(root, text = "UV time:")
UVTimeLabel['font'] = ('Helvetica Neue Light', FontSize)
UVTimeLabel.place(x=X3, y=Y2)

SecondsLabel = Label(root, text = "s")
SecondsLabel['font'] = ('Helvetica Neue Thin', FontSize)
SecondsLabel.place(x=X5, y=Y2)


#=====================================================================================
#Extra run settings
#=====================================================================================
#Extra Run checkbox
ExtraRunChecked = IntVar()
ExtraRunCheckBox = Checkbutton(root, variable=ExtraRunChecked, onvalue=True, offvalue=False, command=ExtraRunChecked_function)
ExtraRunCheckBox.place(x=X2, y=Y3)

#Direction menu
options = ["Up", "Down", "Right", "Left"]
selected_direction = StringVar()
selected_direction.set( "Up" )
drop = OptionMenu(root , selected_direction , *options )
drop.place(x=X4, y=int(Y3))
drop['state']="disabled"

#Extra Run textbox
extra_textbox = Entry(root, width=8, validate="key")
extra_textbox['validatecommand'] = (root.register(validate_input), '%P')
extra_textbox['state']='disabled'
extra_textbox['font'] = ('Helvetica Neue Thin', FontSize)
extra_textbox['disabledbackground']='#d4d4d4'
extra_textbox.place(x=X4, y=Y4)
extra_textbox['justify']='right'

#Labels
ExtraRunCheckboxLabel = Label(root, text = "Extra run at Layer Change")
ExtraRunCheckboxLabel['font'] = ('Helvetica Neue Light', FontSize)
ExtraRunCheckboxLabel.place(x=X1, y=Y3)

DirectionLabel = Label(root, text = "Direction:")
DirectionLabel['font'] = ('Helvetica Neue Light', FontSize)
DirectionLabel.place(x=X3, y=Y3)

MmLabel = Label(root, text = "mm")
MmLabel['font'] = ('Helvetica Neue Thin', FontSize)
MmLabel.place(x=X5, y=Y4)


#=====================================================================================
#Insert previously stored settings in current window
#=====================================================================================
path_textbox.insert(0, var1)

if var2==True:
    LedCheck.select()
    ledTime_textbox['state']='normal'
    if var3!="":
        ledTime_textbox.insert(0,float(var3))

if var4==True:
    ExtraRunCheckBox.select()
    extra_textbox['state']='normal'
    drop['state']="normal"
    if var6!="":
        extra_textbox.insert(0,float(var6))

if var5 != "":
    selected_direction.set( var5 )

root.mainloop()


#=====================================================================================
#Line to transform it in an app on Mac (to be inserted in terminal)
#=====================================================================================
#pyinstaller --onefile --windowed --icon=icon.icns Main.py
