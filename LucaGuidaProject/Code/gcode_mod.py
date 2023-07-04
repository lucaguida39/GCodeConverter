def conversion():
    import os
    import tempfile
    from replacement import rep_dict_function #
    from deletion import del_list_function #
#    from toolchange import tool_change
#    from toolchange import head_activation
    from toolchange import toolchange_function
    from layerchange import layerchange_function #
    layerchange_dict=layerchange_function()
    del_list=del_list_function()
    rep_dict=rep_dict_function()
    [tool_change, head_activation, pos]=toolchange_function()


#=====================================================================================
#Find the temporary file folder in which settings are stored
#=====================================================================================
    temp=tempfile.gettempdir()
    filename = temp + "/datagcodeconverter.txt"


#=====================================================================================
#Recover stored settings
#=====================================================================================
    file=open(filename)
    lines = file.readlines()
    folder_path = (lines[0].strip())
    LedActive = bool(int(lines[1].strip()))
    if lines[2].strip()=="":
        LedTime=0
    if lines[2].strip()!="":
        LedTime = float(lines[2].strip())
    ExtraRun = bool(int(lines[3].strip()))
    ExtraRunDir = str(lines[4].strip())
    if lines[5].strip()=="":
        ExtraRunLen = 0
    if lines[5].strip()!="":
        ExtraRunLen = str(lines[5].strip())


#=====================================================================================
# Generating a new "file" object
#=====================================================================================
    class new_gcode():
        def __init__(self, file_name):
            self.file_name = file_name
            self.txt_file_name = self.file_name[:-6] + ".txt"
            self.file_path = os.path.join(folder_path ,self.file_name)
            with open(os.path.join(folder_path, file_name), 'r') as gcode_text :    self.gcode_text = gcode_text.readlines()
            self.gcode = [x.strip("\n") for x in self.gcode_text] #removing the new-lines \n notation
            self.replaced_list = []
            self.final_gcode = []
            self.to_export_gcode = []


#=====================================================================================
# Function that automatically generates new folders
#=====================================================================================
    def mkdir(filename):
        global folder_destination
        folder_destination = os.path.join(folder_path ,filename)
        if not os.path.exists(os.path.join(folder_path , filename)):
            os.makedirs(os.path.join(folder_path , filename))
        return folder_destination


#=====================================================================================
# Function that parses through files contained in folder_path and extracts those with ".gcode extension"
#=====================================================================================
    def check_gcode():
        filenames_list = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".gcode"):
                filenames_list.append(filename)
            else:
                continue
        return filenames_list


#=====================================================================================
#Identifying existing GCodes and creating a new folder for converted ones
#=====================================================================================
    filenames_list = check_gcode()
    NumberOfFiles=len(filenames_list)
    if NumberOfFiles == 0:
        return NumberOfFiles
    results_destination = mkdir('Converted')
    object_list = []
    #print("_______________________________________________\nGcode coverter for Chimera MK2 \nDeveloped at +Lab, Politecnico di Milano \n\n")
    for i in filenames_list:
       object_list.append(new_gcode(i))
       #print("Gcode file found:  {}".format(i))
    #print("\n \nConverting...")


#=====================================================================================
#Conversion of single Gcode starts
#=====================================================================================
    for x in object_list:
       #We are in a single g-code:

       #Variables which keep trace of the current head, layer and printing state
       new_head=0
       layer=0
       print_started=0


#=====================================================================================
#The current GCode is analysed line-by-line
#=====================================================================================
       for y in x.gcode:
          change_head=False


#=====================================================================================
#Keeping trace of tool in use, previous tool used and tool change in progress
#=====================================================================================
          if y == "T0 ; change extruder" \
          or y == "T1 ; change extruder" \
          or y == "T2 ; change extruder" \
          or y == "T3 ; change extruder" \
          or y == "T4 ; change extruder" \
          or y == "T5 ; change extruder" \
          or y == "T6 ; change extruder" \
          or y == "T7 ; change extruder":
              previous_head=new_head
              new_head = int(y[1:2])
              change_head=True
              retracted=1


#=====================================================================================
#Toolchange
#=====================================================================================
          if change_head==True and print_started==1:
                  lines=tool_change[previous_head][new_head]
                  del(y)
                  y=[]
                  y=lines

          if change_head==True and print_started==0:
                  lines=head_activation[new_head]
                  del(y)
                  y=[]
                  y=lines
                  print_started=1


#=====================================================================================
#Layer change
#=====================================================================================
          if y == ";LAYER_CHANGE" and layer>0:
                  lines=layerchange_dict[new_head]
                  del(y)
                  y=[]
                  y=lines

          if y == ";Layer_Change" and layer>0:
                  lines=layerchange_dict[new_head]
                  del(y)
                  y=[]
                  y=lines

          if y == ";LAYER_CHANGE" or y == ";Layer_Change" :
              layer=layer+1


#=====================================================================================
#Retraction commands
#=====================================================================================
          if "F36000 ;" in y:
                  z="F36000 ;"
                  lines=rep_dict["F36000 ;"]
                  max=len(y)-len(z)+2
                  for c in range(max):
                      if y[c:c+len(z)]==z:
                          k=c
                          g=y[0:k]
                          lines[0]=g+lines[0]
                          del(y)
                          y=[]
                          y=lines


#=====================================================================================
#De-retraction commands
#=====================================================================================
          if "F72000 ;" in y:
                  z="F72000 ;"
                  lines=rep_dict["F72000 ;"]
                  max=len(y)-len(z)+2
                  for c in range(max):
                      if y[c:c+len(z)]==z:
                          k=c
                          g=y[0:k]
                          lines[0]=g+lines[0]
                          del(y)
                          y=[]
                          y=lines


#=====================================================================================
#Commands for extruder motor are deleted when using pneumatic extruders
#=====================================================================================
          #G1 is the commands to move the motor
          #G92 is the command to reset the extruder distance
          trigger_E=False
          if new_head == 0 or new_head == 1 or new_head == 2:
              if "G1" in y:
                  length=len(y)
                  for index in range(length):
                      if y[index:index+1]=="E":
                          y1=y[0:index]
                          trigger_E=True
                      if y[index:index+1]==";" and trigger_E==True:
                                y=y1+y[index:length+1]

          if new_head == 0 or new_head == 1 or new_head == 2:
              if "G92 E" in y:
                  y=";"

          if new_head == 0 or new_head == 1 or new_head == 2:
              if "G1 E" in y:
                  y=";"

          if new_head == 0 or new_head == 1 or new_head == 2:
              if isinstance(y,str)==0:
                  for i in range(len(y)):
                    if "G1 E" in y[i]:
                        y[i]=";"
              if isinstance(y,str)==1:
                  if "G1 E" in y:
                     y=";"

#=====================================================================================
#Commands for fans are deleted when using piston extruder
#=====================================================================================
          if new_head == 5:
              if "M106" in y:
                  y=";"
              if "M107" in y:
                  y=";"


#=====================================================================================
#Generating a new version of the Gcode, to be used for further modification
#=====================================================================================
          if isinstance(y,str)==0:
              for i in range(len(y)):
                x.replaced_list.append(y[i])
          if isinstance(y,str)==1:
              x.replaced_list.append(y)


#=====================================================================================
#Lines relative to skirt and change object are deleted
#=====================================================================================
       delim1 = True
       delim2 = True
       for i in x.replaced_list:
         if "point" in i and delim1 == False and layer>0:
           delim1 = True

         if "skirt point" in i and delim1 == True and layer>0:
           delim1 = False

         if "point" in i and delim2 == False:
            delim2 = True

         if "object" in i and delim2 == True:
            delim2 = False


#=====================================================================================
#Lines containing strings present in the "Deletion" file are deleted
#=====================================================================================
         for j in del_list:
            if j in i:
                i=";"


#=====================================================================================
#Final Gcode is created
#=====================================================================================
         if delim1 == True and delim2==True and i!=";":
             x.final_gcode.append(i)


#=====================================================================================
#Saving the transformed Gcode
#=====================================================================================
       for u in x.final_gcode:
          x.to_export_gcode = [f for f in x.final_gcode if f]

       with open(os.path.join(results_destination ,x.file_name[:-6] + "_conv.gcode"), 'w') as f: f.writelines(line + '\n' for line in x.final_gcode)


#=====================================================================================
#Returning the variable to the GUI script
#=====================================================================================
    #print("Completed!\n\n_______________________________________________\n\n")
    return NumberOfFiles
